#!/bin/bash

# Manual deployment script for Rifa1122
# This script replicates the CI workflow deployment logic for local/manual use

set -euo pipefail

# Argument parsing
DRY_RUN=false
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--dry-run]"
      exit 1
      ;;
  esac
done

# Configuration - Update these variables as needed
IMAGE="${IMAGE:-ghcr.io/your-org/rifa1122:latest}"
REMOTE_HOST="${REMOTE_HOST:-your-staging-host.com}"
REMOTE_USER="${REMOTE_USER:-your-user}"
REMOTE_DIR="${REMOTE_DIR:-~/deploy/rifa1122}"
SSH_KEY_PATH="${SSH_KEY_PATH:-~/.ssh/id_rsa}"
GHCR_USERNAME="${GHCR_USERNAME:-}"
GHCR_PAT="${GHCR_PAT:-}"

# Validate required variables
if [[ -z "$REMOTE_HOST" || -z "$REMOTE_USER" ]]; then
    echo "Error: REMOTE_HOST and REMOTE_USER must be set"
    exit 1
fi

if [[ "$DRY_RUN" == "true" ]]; then
    echo "DRY RUN MODE: Simulating deployment without executing commands"
fi

echo "Deploying image: $IMAGE to $REMOTE_USER@$REMOTE_HOST ($REMOTE_DIR)"

# SSH options for security
SSH_OPTS="-o StrictHostKeyChecking=yes -o BatchMode=yes -o ConnectTimeout=10 -i $SSH_KEY_PATH"

# Function to run commands on remote host
remote_exec() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "DRY RUN: ssh $SSH_OPTS $REMOTE_USER@$REMOTE_HOST $@"
    else
        ssh $SSH_OPTS $REMOTE_USER@$REMOTE_HOST "$@"
    fi
}

# Function to sync files to remote host
sync_files() {
    local files="../backend/docker-compose.prod.yml ../backend/nginx.conf ../backend/.env.prod.example"
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "DRY RUN: rsync -avz --delete -e \"ssh $SSH_OPTS\" $files $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"
    else
        rsync -avz --delete -e "ssh $SSH_OPTS" $files $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/
    fi
}

# Check SSH connection
echo "Testing SSH connection..."
remote_exec "echo 'SSH connection successful'"

# Sync necessary files to remote host
echo "Syncing configuration files to remote host..."
sync_files

# Remote deployment commands
remote_exec <<EOF
set -euo pipefail
cd "$REMOTE_DIR"

echo "Remote: docker version"
docker --version || true

# Optional GHCR login for private images
if [[ -n "$GHCR_USERNAME" && -n "$GHCR_PAT" ]]; then
    echo "Logging into GHCR"
    echo "$GHCR_PAT" | docker login ghcr.io -u "$GHCR_USERNAME" --password-stdin
fi

echo "Ensure docker compose/plugin available"
if command -v docker >/dev/null && (docker compose version >/dev/null 2>&1 || command -v docker-compose >/dev/null); then
    echo "Using docker compose flow"

    # Check if compose file exists
    if [[ -f docker-compose.prod.yml ]]; then
        echo "Validating compose configuration"
        IMAGE="$IMAGE" docker compose -f docker-compose.prod.yml config

        echo "Pulling via docker compose"
        IMAGE="$IMAGE" docker compose -f docker-compose.prod.yml pull --ignore-pull-failures || true

        echo "Bringing services up (compose)"
        IMAGE="$IMAGE" docker compose -f docker-compose.prod.yml up -d

        echo "Recording deployment info"
        DEPLOY_LOG="deploy.log"
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Deployed $IMAGE manually" >> "$DEPLOY_LOG"
        docker image inspect --format 'Digest: {{index .RepoDigests 0}}' "$IMAGE" >> "$DEPLOY_LOG" 2>/dev/null || echo "Digest: unknown" >> "$DEPLOY_LOG"
        echo "---" >> "$DEPLOY_LOG"
    else
        echo "No docker-compose.prod.yml found; cannot proceed"
        exit 1
    fi
else
    echo "docker compose not available; cannot proceed without compose"
    exit 1
fi

echo "Finished deploy of $IMAGE"
echo "Services status:"
docker compose -f docker-compose.prod.yml ps

# Setup logrotate for deploy.log
sudo tee /etc/logrotate.d/deploy <<LOGROTATE_EOF
$REMOTE_DIR/deploy.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
LOGROTATE_EOF

# Verification steps
echo "Verifying deployment..."
if docker compose -f docker-compose.prod.yml ps | grep -q "Up"; then
    echo "Services are running successfully"
    # Check health endpoint if available
    if command -v curl >/dev/null; then
        echo "Checking health endpoint..."
        # Assuming the service exposes a health check on /health or similar
        # Adjust the URL based on your compose configuration
        HEALTH_URL="http://localhost:8000/health"
        if curl -f --max-time 10 "$HEALTH_URL" >/dev/null 2>&1; then
            echo "Health check passed"
        else
            echo "Warning: Health check failed or not available"
        fi
    fi
else
    echo "Error: Services are not running properly"
    exit 1
fi
EOF

if [[ "$DRY_RUN" == "false" ]]; then
    echo "Deployment completed successfully!"
else
    echo "DRY RUN: Deployment simulation completed."
fi