#!/bin/bash

# PostgreSQL backup script for Rifa1122
# This script creates automated backups of the database

set -e

# Configuration
BACKUP_DIR="/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="rifa1122_backup_${TIMESTAMP}.sql"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Database connection details
DB_HOST="${POSTGRES_HOST:-postgres}"
DB_PORT="${POSTGRES_PORT:-5432}"
DB_NAME="${POSTGRES_DB:-rifa1122}"
DB_USER="${POSTGRES_USER:-rifa_user}"
DB_PASSWORD="${POSTGRES_PASSWORD}"

# Export password for pg_dump
export PGPASSWORD="$DB_PASSWORD"

echo "Starting database backup at $(date)"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Perform the backup
pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --no-password \
    --format=custom \
    --compress=9 \
    --verbose \
    --file="$BACKUP_PATH"

# Verify backup was created
if [ -f "$BACKUP_PATH" ]; then
    BACKUP_SIZE=$(stat -c%s "$BACKUP_PATH" 2>/dev/null || stat -f%z "$BACKUP_PATH" 2>/dev/null || echo "unknown")
    echo "Backup completed successfully: $BACKUP_NAME (Size: $BACKUP_SIZE bytes)"

    # Clean up old backups (keep last 7 days)
    echo "Cleaning up old backups..."
    find "$BACKUP_DIR" -name "rifa1122_backup_*.sql" -mtime +7 -delete

    echo "Backup process completed at $(date)"
else
    echo "ERROR: Backup file was not created"
    exit 1
fi

# Unset password
unset PGPASSWORD