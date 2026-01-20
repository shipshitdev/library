# API Test - API Testing Command

**Purpose:** Generate, run, and validate API tests for NestJS endpoints covering authentication, authorization, validation, error handling, and edge cases.

## When to Use

- Testing new API endpoints
- Validating API changes
- Creating integration tests
- Debugging API issues
- API documentation validation

## Project Context Discovery

**Before testing, discover the project's setup:**

1. **Identify API Framework:**
   - Check for NestJS structure
   - Review controller patterns
   - Check for DTOs and validation
   - Identify authentication system

2. **Discover Testing Setup:**
   - Check for Jest/Vitest configuration
   - Look for test files (`*.spec.ts`, `*.test.ts`)
   - Review testing utilities
   - Check for test database setup

3. **Identify API Patterns:**
   - Review existing tests for patterns
   - Check for test helpers/utilities
   - Review authentication test patterns
   - Check for database mocking

4. **Discover API Endpoints:**
   - Scan controllers for routes
   - Review OpenAPI/Swagger docs
   - Check `.http` files for examples
   - Review API documentation

## API Testing Workflow

### Phase 1: Generate Test Structure

**1.1 Identify Endpoint to Test**

```bash
/api-test /api/users
```

**Process:**

1. Read controller file
2. Identify route, method, DTOs
3. Check authentication requirements
4. Review validation rules
5. Identify dependencies

**1.2 Generate Test File**

**Location:** `[controller].spec.ts` (co-located with controller)

**Structure:**

```typescript
describe('UsersController', () => {
  let controller: UsersController;
  let service: UsersService;
  let app: INestApplication;

  beforeEach(async () => {
    // Test setup
  });

  describe('GET /api/users', () => {
    it('should return users', async () => {
      // Test implementation
    });
  });
});
```

### Phase 2: Test Implementation

**2.1 Authentication Tests**

```typescript
describe('Authentication', () => {
  it('should require authentication', async () => {
    const response = await request(app.getHttpServer())
      .get('/api/users')
      .expect(401);
    
    expect(response.body.message).toContain('Unauthorized');
  });

  it('should accept valid token', async () => {
    const token = await getAuthToken();
    const response = await request(app.getHttpServer())
      .get('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
  });
});
```

**2.2 Authorization Tests**

```typescript
describe('Authorization', () => {
  it('should filter by organization', async () => {
    const token = await getAuthToken('org1');
    const response = await request(app.getHttpServer())
      .get('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);
    
    // Verify all users belong to org1
    response.body.forEach(user => {
      expect(user.organization).toBe('org1');
    });
  });

  it('should prevent cross-organization access', async () => {
    const token = await getAuthToken('org1');
    const response = await request(app.getHttpServer())
      .get('/api/users/org2-user-id')
      .set('Authorization', `Bearer ${token}`)
      .expect(403);
  });
});
```

**2.3 Validation Tests**

```typescript
describe('Validation', () => {
  it('should reject invalid email', async () => {
    const token = await getAuthToken();
    const response = await request(app.getHttpServer())
      .post('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .send({ email: 'invalid-email', name: 'Test' })
      .expect(400);
    
    expect(response.body.message).toContain('email');
  });

  it('should require all required fields', async () => {
    const token = await getAuthToken();
    const response = await request(app.getHttpServer())
      .post('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .send({ email: 'test@example.com' })
      .expect(400);
  });
});
```

**2.4 Success Cases**

```typescript
describe('Success Cases', () => {
  it('should create user', async () => {
    const token = await getAuthToken();
    const createDto = {
      email: 'test@example.com',
      name: 'Test User',
      organization: 'org1'
    };

    const response = await request(app.getHttpServer())
      .post('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .send(createDto)
      .expect(201);

    expect(response.body).toMatchObject({
      email: createDto.email,
      name: createDto.name,
      organization: createDto.organization
    });
    expect(response.body._id).toBeDefined();
  });

  it('should return paginated results', async () => {
    const token = await getAuthToken();
    const response = await request(app.getHttpServer())
      .get('/api/users?page=1&limit=10')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(response.body.data).toHaveLength(10);
    expect(response.body.pagination).toMatchObject({
      page: 1,
      limit: 10,
      total: expect.any(Number)
    });
  });
});
```

**2.5 Error Handling Tests**

```typescript
describe('Error Handling', () => {
  it('should handle not found', async () => {
    const token = await getAuthToken();
    const response = await request(app.getHttpServer())
      .get('/api/users/non-existent-id')
      .set('Authorization', `Bearer ${token}`)
      .expect(404);

    expect(response.body.message).toContain('not found');
  });

  it('should handle duplicate email', async () => {
    const token = await getAuthToken();
    const createDto = { email: 'existing@example.com', name: 'Test' };

    // Create first user
    await request(app.getHttpServer())
      .post('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .send(createDto)
      .expect(201);

    // Try to create duplicate
    const response = await request(app.getHttpServer())
      .post('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .send(createDto)
      .expect(409);

    expect(response.body.message).toContain('already exists');
  });
});
```

**2.6 Edge Cases**

```typescript
describe('Edge Cases', () => {
  it('should handle empty results', async () => {
    const token = await getAuthToken('empty-org');
    const response = await request(app.getHttpServer())
      .get('/api/users')
      .set('Authorization', `Bearer ${token}`)
      .expect(200);

    expect(response.body).toEqual([]);
  });

  it('should handle large payloads', async () => {
    const token = await getAuthToken();
    const largeData = Array(1000).fill({ field: 'value' });
    
    const response = await request(app.getHttpServer())
      .post('/api/users/bulk')
      .set('Authorization', `Bearer ${token}`)
      .send({ users: largeData })
      .expect(201);
  });
});
```

### Phase 3: Test Execution

**3.1 Run Tests**

```bash
# Run all API tests
npm test

# Run specific test file
npm test users.controller.spec.ts

# Run with coverage
npm test -- --coverage

# Watch mode
npm test -- --watch
```

**3.2 Integration Tests**

```typescript
// e2e/users.e2e-spec.ts
describe('Users API (e2e)', () => {
  let app: INestApplication;
  let authToken: string;

  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
    
    authToken = await getAuthToken();
  });

  afterAll(async () => {
    await app.close();
  });

  it('/api/users (GET)', () => {
    return request(app.getHttpServer())
      .get('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200)
      .expect((res) => {
        expect(Array.isArray(res.body)).toBe(true);
      });
  });
});
```

### Phase 4: Test Validation

**4.1 Coverage Requirements**

- ✅ Line coverage > 80%
- ✅ Branch coverage > 75%
- ✅ Function coverage > 85%
- ✅ Critical paths 100% covered

**4.2 Test Quality**

- ✅ Tests are meaningful (not just for coverage)
- ✅ Tests are independent
- ✅ Tests are fast (< 100ms each)
- ✅ Tests are maintainable

## NestJS-Specific Patterns

### Test Module Setup

```typescript
beforeEach(async () => {
  const module: TestingModule = await Test.createTestingModule({
    controllers: [UsersController],
    providers: [
      UsersService,
      {
        provide: getModelToken(User.name),
        useValue: mockUserModel,
      },
    ],
  }).compile();

  controller = module.get<UsersController>(UsersController);
  service = module.get<UsersService>(UsersService);
});
```

### Mocking Dependencies

```typescript
const mockUsersService = {
  findAll: jest.fn(),
  findOne: jest.fn(),
  create: jest.fn(),
  update: jest.fn(),
  remove: jest.fn(),
};

beforeEach(async () => {
  const module = await Test.createTestingModule({
    controllers: [UsersController],
    providers: [
      {
        provide: UsersService,
        useValue: mockUsersService,
      },
    ],
  }).compile();

  controller = module.get<UsersController>(UsersController);
});
```

### Database Mocking

```typescript
const mockUserModel = {
  find: jest.fn(),
  findOne: jest.fn(),
  create: jest.fn(),
  findByIdAndUpdate: jest.fn(),
  findByIdAndDelete: jest.fn(),
};

// In test
mockUserModel.find.mockResolvedValue([
  { _id: '1', email: 'test@example.com', organization: 'org1' }
]);
```

## MongoDB Testing Patterns

### Test Database Setup

```typescript
beforeAll(async () => {
  // Connect to test database
  await mongoose.connect(process.env.TEST_DB_URI);
});

afterAll(async () => {
  await mongoose.connection.close();
});

beforeEach(async () => {
  // Clean database before each test
  await User.deleteMany({});
});
```

### Data Seeding

```typescript
async function seedTestData() {
  await User.create([
    { email: 'user1@test.com', organization: 'org1' },
    { email: 'user2@test.com', organization: 'org1' },
    { email: 'user3@test.com', organization: 'org2' },
  ]);
}
```

## Test Categories

### 1. Unit Tests

**Focus:** Individual methods/functions

```typescript
describe('UsersService', () => {
  it('should filter by organization', async () => {
    const result = await service.findAll('org1');
    expect(result.every(u => u.organization === 'org1')).toBe(true);
  });
});
```

### 2. Integration Tests

**Focus:** Controller + Service + Database

```typescript
describe('UsersController Integration', () => {
  it('should create and retrieve user', async () => {
    // Create
    const createResponse = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test' })
      .expect(201);

    // Retrieve
    const getResponse = await request(app)
      .get(`/api/users/${createResponse.body._id}`)
      .expect(200);

    expect(getResponse.body.email).toBe('test@example.com');
  });
});
```

### 3. E2E Tests

**Focus:** Full request/response cycle

```typescript
describe('Users API E2E', () => {
  it('should handle full user lifecycle', async () => {
    // Create → Read → Update → Delete
  });
});
```

## Common Test Patterns

### Authentication Helper

```typescript
async function getAuthToken(organizationId = 'org1'): Promise<string> {
  // Generate test token
  // Or use test user credentials
  const response = await request(app.getHttpServer())
    .post('/api/auth/login')
    .send({ email: 'test@example.com', password: 'test' });
  
  return response.body.accessToken;
}
```

### Request Helper

```typescript
function authenticatedRequest(method: string, url: string) {
  return async (token: string) => {
    return request(app.getHttpServer())
      [method](url)
      .set('Authorization', `Bearer ${token}`);
  };
}

// Usage
const getUsers = authenticatedRequest('get', '/api/users');
const response = await getUsers(token);
```

## Output Format

When generating tests:

```
🧪 API TEST GENERATION

Endpoint: GET /api/users
Controller: UsersController
File: users.controller.spec.ts

📋 TEST STRUCTURE GENERATED

✅ Authentication tests (2)
✅ Authorization tests (3)
✅ Validation tests (4)
✅ Success cases (5)
✅ Error handling (3)
✅ Edge cases (2)

📝 TEST FILE CREATED

Location: src/users/users.controller.spec.ts
Tests: 19
Estimated coverage: 85%

💡 NEXT STEPS

1. Review generated tests
2. Add project-specific test data
3. Run tests: npm test users.controller.spec.ts
4. Verify coverage meets requirements
```

---

**Created:** 2025-12-24
**Purpose:** Generate and run comprehensive API tests for NestJS endpoints
**Focus:** Authentication, authorization, validation, error handling, edge cases
