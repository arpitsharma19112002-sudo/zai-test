# Configuration Reference

Complete reference for all configuration options.

---

## Configuration Files

| File | Purpose |
|------|---------|
| `package.json` | Project metadata and dependencies |
| `tsconfig.json` | TypeScript configuration |
| `.eslintrc.js` | ESLint configuration |
| `.prettierrc` | Prettier configuration |

---

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Key Options

| Option | Description |
|--------|-------------|
| `target` | JavaScript version to compile to |
| `module` | Module system to use |
| `strict` | Enable all strict type-checking options |
| `outDir` | Output directory for compiled files |
| `rootDir` | Root directory of source files |

---

## ESLint Configuration

```javascript
module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    // Custom rules
  }
};
```

---

## Prettier Configuration

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

---

## Project Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `dev` | `node src/index.js` | Start development server |
| `build` | `tsc` | Build for production |
| `start` | `node dist/index.js` | Start production server |
| `test` | `jest` | Run tests |
| `lint` | `eslint src/` | Lint code |
| `format` | `prettier --write .` | Format code |

---

*This is a template. Update with your actual configuration.*
