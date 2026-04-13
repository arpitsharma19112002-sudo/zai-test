# Environment Variables Reference

Complete reference for all environment variables.

---

## Required Variables

| Variable | Type | Description | Example |
|----------|------|-------------|---------|
| `NODE_ENV` | string | Environment mode | `development`, `production`, `test` |
| `PORT` | number | Server port | `3000` |

---

## Optional Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `LOG_LEVEL` | string | `info` | Logging level |
| `API_TIMEOUT` | number | `30000` | API timeout in ms |

---

## Database Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `DATABASE_URL` | string | Yes | Database connection string |
| `DATABASE_POOL_SIZE` | number | No | Connection pool size |

### Example

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DATABASE_POOL_SIZE=10
```

---

## Authentication Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `JWT_SECRET` | string | Yes | Secret for JWT signing |
| `JWT_EXPIRY` | string | No | Token expiry time |
| `API_KEY` | string | No | API key for external services |

### Example

```bash
JWT_SECRET=your-super-secret-key-here
JWT_EXPIRY=7d
```

---

## Loading Environment Variables

Create a `.env` file in the project root:

```bash
# .env
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://localhost:5432/dev
JWT_SECRET=dev-secret
```

**Important:** Never commit `.env` files to version control!

---

## Validation

Validate environment variables on startup:

```typescript
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.string().transform(Number).default('3000'),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string().min(32),
});

const env = envSchema.parse(process.env);
```

---

*This is a template. Update with your actual environment variables.*
