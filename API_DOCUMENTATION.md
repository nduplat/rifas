# Rifa1122 API Documentation

## Overview

The Rifa1122 API is a comprehensive lottery and raffle management system built with FastAPI. It provides endpoints for managing raffles, tickets, users, and automated winner selection.

**Base URL:** `http://localhost:8000/api/v1` (development)
**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

## Authentication

The API uses JWT (JSON Web Token) based authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Authentication Endpoints

#### POST /auth/register

Register a new user account.

**Request Body:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "telefono": "+57 301 234 5678",
  "password": "securepassword123",
  "rol": "jugador"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "telefono": "+57 301 234 5678",
  "rol": "jugador",
  "creado_en": "2024-01-01T10:00:00Z"
}
```

#### POST /auth/login

Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "username": "juan.perez@email.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Raffles (Rifas) Endpoints

### GET /rifas/

List all raffles with optional pagination.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440003",
    "nombre": "Rifa Especial Navidad",
    "categoria_id": "550e8400-e29b-41d4-a716-446655440002",
    "loteria_id": "550e8400-e29b-41d4-a716-446655440001",
    "fecha_inicio": "2023-12-01T00:00:00Z",
    "fecha_fin": "2023-12-24T23:59:59Z",
    "numero_ganadores": 2,
    "estado": "activa",
    "total_boletas": 100
  }
]
```

### GET /rifas/{rifa_id}

Get detailed information about a specific raffle.

**Path Parameters:**
- `rifa_id` (string): UUID of the raffle

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440003",
  "nombre": "Rifa Especial Navidad",
  "categoria": {
    "id": "550e8400-e29b-41d4-a716-446655440002",
    "nombre": "Bronce",
    "color": "Marrón",
    "valor_boleta": 5000,
    "total_recaudo": 500000,
    "rake": 0.25,
    "fondo_premios": 375000,
    "premio_por_ganador": 187500,
    "comentario": "Premium"
  },
  "loteria": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "nombre": "Baloto",
    "descripcion": "Lotería nacional colombiana con sorteos diarios",
    "frecuencia": "diaria",
    "url_resultados": "https://www.baloto.com/resultados"
  },
  "fecha_inicio": "2023-12-01T00:00:00Z",
  "fecha_fin": "2023-12-24T23:59:59Z",
  "numero_ganadores": 2,
  "estado": "activa",
  "total_boletas": 100
}
```

### POST /rifas/

Create a new raffle. **Requires operator or admin role.**

**Request Body:**
```json
{
  "nombre": "Nueva Rifa Especial",
  "categoria_id": "550e8400-e29b-41d4-a716-446655440002",
  "loteria_id": "550e8400-e29b-41d4-a716-446655440001",
  "fecha_inicio": "2024-12-01T00:00:00Z",
  "fecha_fin": "2024-12-31T23:59:59Z",
  "numero_ganadores": 2
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440020",
  "nombre": "Nueva Rifa Especial",
  "categoria_id": "550e8400-e29b-41d4-a716-446655440002",
  "loteria_id": "550e8400-e29b-41d4-a716-446655440001",
  "fecha_inicio": "2024-12-01T00:00:00Z",
  "fecha_fin": "2024-12-31T23:59:59Z",
  "numero_ganadores": 2,
  "estado": "activa",
  "total_boletas": 0
}
```

### POST /rifas/{rifa_id}/close

Close a raffle and select winners. **Requires operator or admin role.**

**Path Parameters:**
- `rifa_id` (string): UUID of the raffle to close

**Response (200):**
```json
{
  "message": "Rifa cerrada exitosamente. Ganadores seleccionados.",
  "ganadores": [
    {
      "ticket_id": "550e8400-e29b-41d4-a716-446655440022",
      "numero_ganador": 7,
      "usuario_id": "550e8400-e29b-41d4-a716-446655440018",
      "monto_ganado": 187500
    }
  ]
}
```

## Tickets Endpoints

### GET /tickets/

Get user's purchased tickets.

**Query Parameters:**
- `skip` (int, optional): Number of records to skip (default: 0)
- `limit` (int, optional): Maximum number of records to return (default: 100)

**Response (200):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440020",
    "rifa_id": "550e8400-e29b-41d4-a716-446655440003",
    "usuario_id": "550e8400-e29b-41d4-a716-446655440018",
    "numero": 42,
    "comprado_en": "2023-12-01T14:30:00Z",
    "estado": "vendido",
    "rifa": {
      "id": "550e8400-e29b-41d4-a716-446655440003",
      "nombre": "Rifa Especial Navidad"
    }
  }
]
```

### POST /tickets/purchase

Purchase tickets for a raffle. **Rate limited to 10 purchases per minute.**

**Request Body:**
```json
{
  "rifa_id": "550e8400-e29b-41d4-a716-446655440003",
  "quantity": 3,
  "idempotency_key": "unique-purchase-id-12345"
}
```

**Response (201):**
```json
{
  "transaccion_id": "550e8400-e29b-41d4-a716-446655440030",
  "tickets": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440031",
      "numero": 15,
      "estado": "vendido"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440032",
      "numero": 27,
      "estado": "vendido"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440033",
      "numero": 89,
      "estado": "vendido"
    }
  ],
  "total_amount": 15000,
  "message": "Compra realizada exitosamente"
}
```

### POST /rifas/{rifa_id}/tickets

Alternative endpoint for purchasing tickets directly on a specific raffle.

**Path Parameters:**
- `rifa_id` (string): UUID of the raffle

**Request Body:** Same as `/tickets/purchase`

## Users Endpoints

### GET /users/me

Get current user profile information.

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440018",
  "nombre": "Juan Pérez",
  "email": "juan.perez@email.com",
  "telefono": "+57 301 234 5678",
  "rol": "jugador",
  "creado_en": "2024-01-01T10:00:00Z"
}
```

### PUT /users/me

Update current user profile.

**Request Body:**
```json
{
  "nombre": "Juan Pérez García",
  "telefono": "+57 301 234 5679"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440018",
  "nombre": "Juan Pérez García",
  "email": "juan.perez@email.com",
  "telefono": "+57 301 234 5679",
  "rol": "jugador",
  "creado_en": "2024-01-01T10:00:00Z"
}
```

## Webhooks

### POST /webhooks/stripe

Handle Stripe payment webhooks. This endpoint processes payment confirmations and failures.

**Headers:**
```
Content-Type: application/json
Stripe-Signature: t=1234567890,v1=signature...
```

**Request Body:** (Stripe webhook payload)
```json
{
  "id": "evt_1234567890",
  "object": "event",
  "api_version": "2020-08-27",
  "created": 1234567890,
  "data": {
    "object": {
      "id": "pi_1234567890",
      "object": "payment_intent",
      "amount": 15000,
      "currency": "cop",
      "status": "succeeded"
    }
  },
  "type": "payment_intent.succeeded"
}
```

**Response (200):**
```json
{
  "message": "Webhook processed successfully"
}
```

## Error Responses

### Common Error Format

```json
{
  "detail": "Error description message"
}
```

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors, insufficient funds, etc.)
- `401` - Unauthorized (invalid or missing JWT token)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `422` - Unprocessable Entity (validation errors)
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error

### Common Error Messages

- `"Email already registered"` - User registration with existing email
- `"Incorrect email or password"` - Invalid login credentials
- `"Rifa not found"` - Invalid raffle ID
- `"Cannot purchase for other users"` - Attempting to purchase tickets for another user
- `"Rifa ID mismatch"` - Rifa ID in URL doesn't match request body
- `"Insufficient funds"` - Not enough balance for purchase
- `"Rifa is not active"` - Attempting to purchase tickets for inactive raffle

## Rate Limiting

- Ticket purchases: 10 requests per minute per user
- General API endpoints: Configurable via environment variables

## Data Models

### User Roles

- `jugador` - Regular player
- `operador` - Raffle operator (can create/manage raffles)
- `admin` - System administrator

### Raffle States

- `activa` - Active (accepting ticket purchases)
- `cerrada` - Closed (no longer accepting purchases)
- `pendiente` - Pending (not yet started)

### Ticket States

- `disponible` - Available for purchase
- `vendido` - Sold
- `ganador` - Winning ticket
- `perdedor` - Losing ticket

## Pagination

Endpoints that return lists support pagination:

```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "size": 50,
  "pages": 3
}
```

Use `skip` and `limit` query parameters to control pagination.

## Idempotency

Purchase endpoints support idempotency keys to prevent duplicate transactions. Include an `idempotency_key` in purchase requests.

## Testing

Use the following test credentials for development:

**Admin User:**
- Email: `admin@rifa1122.com`
- Password: `admin123`

**Test User:**
- Email: `juan.perez@email.com`
- Password: `password123`