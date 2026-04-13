# API Reference

Complete reference for all API endpoints and schemas.

---

## Overview

This document provides detailed API specifications for all available endpoints.

---

## Authentication

| Type | Description |
|------|-------------|
| Bearer Token | JWT token in Authorization header |
| API Key | X-API-Key header |

---

## Endpoints

### Users

#### GET /api/users

List all users.

**Parameters:**

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| page | query | integer | No | Page number (default: 1) |
| limit | query | integer | No | Items per page (default: 20) |
| sort | query | string | No | Sort field (default: createdAt) |

**Response:**

```json
{
  "users": [
    {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "ISO 8601 date"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

---

#### GET /api/users/:id

Get a user by ID.

**Parameters:**

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| id | path | string | Yes | User ID |

**Response:**

```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "createdAt": "ISO 8601 date"
}
```

**Errors:**

| Code | Description |
|------|-------------|
| 404 | User not found |
| 401 | Unauthorized |

---

#### POST /api/users

Create a new user.

**Body:**

```json
{
  "email": "string (required)",
  "name": "string (required)",
  "password": "string (required, min 8 chars)"
}
```

**Response:**

```json
{
  "id": "string",
  "email": "string",
  "name": "string",
  "createdAt": "ISO 8601 date"
}
```

**Errors:**

| Code | Description |
|------|-------------|
| 400 | Invalid input |
| 409 | Email already exists |

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

## Rate Limiting

| Tier | Limit | Window |
|------|-------|--------|
| Anonymous | 60 requests | 1 minute |
| Authenticated | 1000 requests | 1 minute |

---

*This is a template. Update with your actual API endpoints.*
