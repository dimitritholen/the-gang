# Coding Conventions

**Generated**: {DATE}
**Codebase Version**: {GIT_SHA}
**Analysis Confidence**: {OVERALL_CONFIDENCE}

---

## File Naming Conventions

### Components/Classes

**Pattern**: {PascalCase | kebab-case | snake_case}
**Conformance**: {X}% ({Y}/{Z} files)

**Examples**:

- ✅ `UserProfile.tsx`
- ✅ `AppointmentCard.tsx`
- ❌ `user-list.tsx` (deviation)

**Recommendation**: {Standardize on PascalCase | Accept mixed}

### Services/Utilities

**Pattern**: {camelCase | kebab-case | snake_case}
**Conformance**: {X}% ({Y}/{Z} files)

**Examples**:

- ✅ `authService.ts`
- ✅ `dateUtils.ts`

### Tests

**Pattern**: {_.test.ts | _.spec.ts | **tests**/}
**Conformance**: {X}% ({Y}/{Z} files)

**Examples**:

- ✅ `UserProfile.test.tsx`
- ✅ `authService.spec.ts`
- ⚠️ `__tests__/utils.ts` (alternative pattern)

**Recommendation**: {Choose one pattern}

---

## Directory Structure

**Organization Strategy**: {Feature-based | Type-based | Hybrid}

**Evidence**:

```
{ACTUAL_DIRECTORY_STRUCTURE}
```

**Interpretation**: {WHY_THIS_STRUCTURE}

**Confidence**: {High | Medium | Low}

---

## Code Naming Conventions

### Variables

**Pattern**: camelCase
**Conformance**: {X}%

**Special Cases**:

- Constants: `UPPER_SNAKE_CASE` ({X}% conformance)
- Private members: `_prefixedCamelCase` ({X}% conformance)
- Boolean flags: `is*`, `has*`, `should*` prefix

**Examples**:

```typescript
// ✅ Good
const userName = "John";
const MAX_RETRIES = 3;
const _privateData = {};
const isAuthenticated = true;

// ❌ Avoid
const user_name = "John"; // snake_case
const maxretries = 3; // no constant naming
const privateData = {}; // no underscore prefix
```

### Functions/Methods

**Pattern**: camelCase with descriptive verbs
**Conformance**: {X}%

**Conventions**:

- Async functions: Prefix with `fetch`, `load`, `get`, `save`
- Event handlers: Prefix with `handle` (e.g., `handleClick`)
- Boolean getters: Prefix with `is`, `has`, `should`
- Transforms: Use verbs like `format`, `parse`, `validate`

**Examples**:

```typescript
// ✅ Good
async function fetchUserData() {}
function handleSubmit() {}
function isValidEmail() {}
function formatDate() {}

// ❌ Avoid
async function userData() {} // Missing fetch/get
function submit() {} // Missing handle
function validEmail() {} // Missing is/has
```

---

## Code Style

### Linting/Formatting

**Linter**: {ESLint | Pylint | Rubocop | etc.}
**Formatter**: {Prettier | Black | etc.}
**Configuration**: {.eslintrc.js | etc.}

**Key Rules Enforced**:
{LIST_ENFORCED_RULES}

**Conformance**: {X}% (based on lint check)

### Line Length

**Maximum**: {80 | 100 | 120} characters
**Evidence**: {Config file or code analysis}
**Conformance**: {X}%

### Indentation

**Style**: {Spaces | Tabs}
**Size**: {2 | 4} {spaces | tabs}
**Evidence**: {.editorconfig | eslintrc}
**Conformance**: 100% (enforced by formatter)

### Quotes

**Style**: {Single | Double}
**Evidence**: {Prettier config | ESLint rule}
**Example**: `const name = 'John';` or `const name = "John";`

### Semicolons

**Usage**: {Always | Never | ASI}
**Evidence**: {Config file}
**Example**: `const x = 1;` or `const x = 1`

### Trailing Commas

**Usage**: {Always | ES5 | Never}
**Evidence**: {Prettier config}
**Example**:

```typescript
const obj = {
  name: "John",
  age: 30, // ← Trailing comma
};
```

---

## Error Handling Patterns

### Dominant Pattern

**Pattern**: {Toast notifications | Console logging | Throw to caller | Sentry/logging service}
**Confidence**: {X}% ({Y}/{Z} error handling blocks)

**Evidence** (analyzed {N} error handlers):

- Toast notifications: {X} instances ({Y}%)
- Console.error: {X} instances ({Y}%)
- Throw: {X} instances ({Y}%)
- Logging service: {X} instances ({Y}%)

### Standard Error Format

```typescript
// User-facing errors
catch (error) {
  toast.error(error.message);
  logger.error('Operation failed', { error, context });
}

// Internal errors (services)
catch (error) {
  throw new Error(`Operation failed: ${error.message}`);
}

// Logging only (background jobs)
catch (error) {
  console.error('Background task failed:', error);
}
```

**Recommendation**: {Standardize on pattern}

---

## API Design Patterns

### REST Endpoints

**URL Structure**: {PATTERN}
**Conformance**: {X}%

**Standard Format**:

```
{METHOD} /api/{version}/{resource}/{id?}/{action?}
```

**Examples**:

```
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
PATCH  /api/v1/users/:id
DELETE /api/v1/users/:id
POST   /api/v1/users/:id/activate
```

### HTTP Methods

**Usage** (RESTful compliance: {X}%):

- GET: Read operations ({X} endpoints)
- POST: Create operations ({X} endpoints)
- PUT: Full updates ({X} endpoints)
- PATCH: Partial updates ({X} endpoints)
- DELETE: Delete operations ({X} endpoints)

### Request/Response Format

**Request Body**:

```typescript
{
  // JSON payload
}
```

**Response Format** ({X}% conformance):

```typescript
{
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code: string;
    details?: any;
  };
}
```

### Status Codes

**Standard Usage**:

- 200: Success
- 201: Created
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

**Conformance**: {X}%

---

## Testing Conventions

### Test Structure

**Pattern**: {Describe-It | Given-When-Then | Arrange-Act-Assert}
**Conformance**: {X}%

**Standard Format**:

```typescript
describe("ComponentName", () => {
  describe("when condition", () => {
    it("should expected behavior", () => {
      // Arrange
      const input = setupInput();

      // Act
      const result = performAction(input);

      // Assert
      expect(result).toEqual(expected);
    });
  });
});
```

### Test File Organization

**Pattern**: {Co-located | **tests** directory | Separate test/ folder}
**Conformance**: {X}%

**Examples**:

- Co-located: `UserProfile.test.tsx` next to `UserProfile.tsx`
- Directory: `__tests__/UserProfile.test.tsx`
- Separate: `test/components/UserProfile.test.tsx`

### Mocking Strategy

**Libraries**: {Jest | Sinon | MSW | etc.}

**Patterns**:

- Database: {In-memory SQLite | Test containers | Mocked ORM}
- External APIs: {MSW | Nock | Manual mocks}
- Time/Date: {jest.useFakeTimers | Sinon fake timers}
- File system: {mock-fs | In-memory}

**Examples**:

```typescript
// Database mocking
jest.mock("./db", () => ({
  query: jest.fn(),
}));

// API mocking (MSW)
server.use(
  rest.get("/api/users", (req, res, ctx) => {
    return res(ctx.json({ users: [] }));
  }),
);
```

### Test Data

**Pattern**: {Factory functions | Fixtures | Inline}

**Example**:

```typescript
// Factory
function createTestUser(overrides = {}) {
  return {
    id: 1,
    name: "Test User",
    email: "test@example.com",
    ...overrides,
  };
}

// Usage
const user = createTestUser({ name: "John" });
```

---

## Comments & Documentation

### When to Comment

**Philosophy**: {Self-documenting code preferred | Liberal comments | JSDoc/Docstrings required}

**Required Comments**:

- Complex algorithms (explain why, not what)
- Public APIs (JSDoc/Docstrings)
- Workarounds (explain why workaround needed)
- TODOs (with issue tracker reference)

**Avoided Comments**:

- Obvious code (what is already clear from reading)
- Commented-out code (delete instead)
- Outdated comments (update or remove)

### Documentation Format

**JSDoc/TypeDoc** (for TypeScript/JavaScript):

```typescript
/**
 * Fetches user data from the API
 * @param userId - The unique identifier for the user
 * @returns Promise resolving to user object
 * @throws {NotFoundError} If user doesn't exist
 */
async function fetchUser(userId: string): Promise<User> {
  // Implementation
}
```

**Python Docstrings** (if applicable):

```python
def fetch_user(user_id: str) -> User:
    """
    Fetches user data from the API

    Args:
        user_id: The unique identifier for the user

    Returns:
        User object with all properties

    Raises:
        NotFoundError: If user doesn't exist
    """
    pass
```

---

## Import/Export Conventions

### Import Order

**Pattern**: {Grouped | Alphabetical | None}

**Standard Order**:

1. External libraries (React, lodash, etc.)
2. Internal absolute imports (@/components)
3. Relative imports (./utils)
4. CSS/assets

**Example**:

```typescript
// External
import React from "react";
import { useState } from "react";
import axios from "axios";

// Internal
import { Button } from "@/components/Button";
import { useAuth } from "@/hooks/useAuth";

// Relative
import { formatDate } from "./utils";
import "./styles.css";
```

### Export Style

**Pattern**: {Named exports | Default exports | Mixed}
**Preference**: {DETECTED_PREFERENCE}

**Examples**:

```typescript
// Named exports (preferred for utilities/components)
export function formatDate() {}
export function validateEmail() {}

// Default export (for single-purpose modules)
export default function UserProfile() {}
```

---

## State Management Patterns

### Local State

**Pattern**: {useState | this.state | etc.}

**Example**:

```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
```

### Global State

**Pattern**: {Redux | Context API | Zustand | MobX | etc.}

**Structure**: {Slice-based | Module-based | Atom-based}

**Example**:

```typescript
// Redux Toolkit slice
const authSlice = createSlice({
  name: "auth",
  initialState: { user: null, token: null },
  reducers: {
    setUser: (state, action) => {
      state.user = action.payload;
    },
  },
});
```

---

## Dependency Injection

**Pattern**: {Constructor injection | Parameter injection | Service locator | None}

**Example**:

```typescript
class UserService {
  constructor(
    private db: Database,
    private logger: Logger,
  ) {}

  async getUser(id: string) {
    this.logger.info(`Fetching user ${id}`);
    return this.db.query("SELECT * FROM users WHERE id = ?", [id]);
  }
}
```

**Conformance**: {X}% of services use DI

---

## Security Patterns

### Input Validation

**Library**: {Joi | Yup | Zod | class-validator | etc.}
**Coverage**: {X}% of endpoints

**Example**:

```typescript
const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
});
```

### Authentication

**Pattern**: {JWT | Session | OAuth | etc.}
**Token Storage**: {HttpOnly cookie | LocalStorage | etc.}

**Middleware**:

```typescript
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.replace("Bearer ", "");
  if (!token) return res.status(401).json({ error: "Unauthorized" });

  const user = verifyToken(token);
  req.user = user;
  next();
}
```

---

## Performance Patterns

### Caching

**Strategy**: {Redis | In-memory | HTTP cache | etc.}
**Locations**: {DETECTED_LOCATIONS}

**Example**:

```typescript
// Redis caching
const cached = await redis.get(`user:${id}`);
if (cached) return JSON.parse(cached);

const user = await fetchUserFromDB(id);
await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
return user;
```

### Database Optimization

**Indexes**: {DETECTED_INDEXES}
**Query Patterns**: {Eager loading | Lazy loading | Query builders}

**Example**:

```sql
-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_appointments_user_id ON appointments(user_id);
```

---

## Deviations & Inconsistencies

### Known Deviations

**File Naming**:

- {N} files use kebab-case instead of PascalCase
- Files: {LIST_FILES}
- Reason: {Legacy | Third-party | Unknown}

**Error Handling**:

- {N} instances use console.error instead of toast
- Locations: {LIST_LOCATIONS}
- Reason: {Background jobs | Server-side | Legacy}

### Recommendations

1. **Standardize file naming**: Rename {N} files to match convention
2. **Unify error handling**: Choose single pattern (recommend: toast for UI, logger for backend)
3. **Add missing tests**: {X}% of features lack tests
4. **Enforce linting**: Fix {N} linting violations

---

## References

- **Configuration Files**: {LIST_CONFIG_FILES}
- **Linting Rules**: {.eslintrc.js, .prettierrc, etc.}
- **Project README**: {README.md if exists}

---

**Usage Note**: Future code should follow these conventions. When uncertain, reference the dominant pattern (highest conformance %). For ambiguous cases, consult team or update this document.
