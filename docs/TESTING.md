# Testing Guide

## Overview

GymIntel Web has comprehensive testing coverage across frontend, backend, and integration layers using modern testing frameworks and container-first development principles.

## Testing Stack

### Frontend Testing
- **Framework**: Vitest (Vite-native, fast)
- **Component Testing**: React Testing Library  
- **DOM Environment**: jsdom
- **Mocking**: @apollo/client/testing for GraphQL
- **Coverage**: Built-in Vitest coverage

### Backend Testing
- **Framework**: pytest with async support
- **API Testing**: httpx AsyncClient
- **GraphQL Testing**: Direct schema testing
- **Database**: SQLite in-memory for tests
- **Coverage**: pytest-cov with HTML reports

### Integration Testing
- **Environment**: Docker Compose
- **Database**: PostgreSQL test instance
- **End-to-End**: Service-to-service communication
- **Health Checks**: API endpoint validation

## Running Tests

### Container-First (Recommended)

```bash
# Run all tests in containers
./scripts/test.sh

# Or manually with Docker Compose
docker compose -f docker-compose.test.yml up --build
```

### Local Development

```bash
# Frontend tests
cd frontend
npm test                    # Run once
npm run test:watch          # Watch mode
npm run test:coverage       # With coverage
npm run test:ui             # Visual UI

# Backend tests  
cd backend
pytest                      # Run all tests
pytest --cov=app           # With coverage
pytest -v tests/test_api.py # Specific file
pytest -k "test_health"     # Pattern matching
```

## Test Structure

### Frontend Tests

```
frontend/src/
├── test/
│   ├── setup.ts                    # Test configuration
│   └── App.test.tsx               # App component tests
├── components/
│   └── __tests__/
│       ├── GymCard.test.tsx       # Component tests
│       └── SearchFilters.test.tsx
└── pages/
    └── __tests__/
        ├── HomePage.test.tsx      # Page tests
        └── SearchPage.test.tsx
```

### Backend Tests

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration
│   ├── test_api.py                # API endpoint tests
│   ├── test_graphql.py            # GraphQL schema tests
│   └── test_models.py             # Database model tests
└── pytest.ini                    # Pytest settings
```

## Writing Tests

### Frontend Component Tests

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MockedProvider } from '@apollo/client/testing'
import GymCard from '../GymCard'

const mockGym = {
  id: '1',
  name: 'Test Gym',
  address: '123 Main St',
  confidence: 0.85
}

describe('GymCard', () => {
  it('renders gym information', () => {
    render(
      <MockedProvider mocks={[]}>
        <GymCard gym={mockGym} />
      </MockedProvider>
    )
    
    expect(screen.getByText('Test Gym')).toBeInTheDocument()
    expect(screen.getByText('85%')).toBeInTheDocument()
  })
})
```

### Backend API Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    """Test health check endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
```

### GraphQL Tests

```python
@pytest.mark.asyncio
async def test_list_metropolitan_areas(async_client: AsyncClient):
    """Test GraphQL query."""
    query = '''
    query {
      listMetropolitanAreas {
        name
        code
      }
    }
    '''
    
    response = await async_client.post(
        "/graphql",
        json={"query": query}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
```

## Coverage Requirements

### Minimum Coverage Targets
- **Frontend**: 80% line coverage
- **Backend**: 80% line coverage  
- **Integration**: All critical paths tested

### Coverage Reports

```bash
# Frontend coverage (HTML report)
cd frontend && npm run test:coverage
open coverage/index.html

# Backend coverage (HTML report)  
cd backend && pytest --cov=app --cov-report=html
open htmlcov/index.html
```

## Continuous Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
- Frontend linting (ESLint)
- Frontend type checking (TypeScript)  
- Frontend unit tests (Vitest)
- Backend linting (Black, isort, flake8)
- Backend unit tests (pytest)
- Docker build tests
- Integration tests
- Security scanning (Trivy)
```

### Test Commands in CI

```bash
# Frontend CI commands
npm run lint
npm run type-check  
npm run test:coverage

# Backend CI commands
black --check .
isort --check-only .
flake8 .
pytest --cov=app --cov-report=xml
```

## Testing Best Practices

### Frontend Testing
1. **Test behavior, not implementation**
2. **Use semantic queries** (getByRole, getByLabelText)
3. **Mock external dependencies** (Apollo Client, APIs)
4. **Test accessibility** with jest-dom matchers
5. **Avoid testing CSS** - focus on functionality

### Backend Testing  
1. **Use async/await** for all async operations
2. **Mock external APIs** (Yelp, Google Places)
3. **Test error conditions** alongside happy paths
4. **Use test database** - never test against production
5. **Test GraphQL schema** introspection and queries

### Integration Testing
1. **Test complete user workflows**
2. **Use realistic test data**
3. **Test service communication**
4. **Verify database state**
5. **Test error propagation**

## Debugging Tests

### Frontend Debugging
```bash
# Debug mode
npm run test:ui

# Specific test with debug output
npm test -- --reporter=verbose GymCard.test.tsx

# Watch mode for development
npm run test:watch
```

### Backend Debugging
```bash
# Verbose output
pytest -v -s

# Debug specific test
pytest -v -s tests/test_api.py::test_health_check

# Print coverage gaps
pytest --cov=app --cov-report=term-missing
```

### Docker Test Debugging
```bash
# View test logs
docker compose -f docker-compose.test.yml logs backend-tests

# Run tests interactively
docker compose -f docker-compose.test.yml run --rm backend-tests bash

# Debug test database
docker compose -f docker-compose.test.yml exec test-database psql -U test_user -d test_gymintel
```

## Performance Testing

### Load Testing (Future)
- **Tool**: Artillery.js for API load testing
- **Targets**: GraphQL queries, gym search endpoints
- **Metrics**: Response time, throughput, error rate

### Frontend Performance
- **Tool**: Lighthouse CI in GitHub Actions
- **Metrics**: Core Web Vitals, accessibility score
- **Targets**: Homepage, search page load times

## Test Data Management

### Fixtures
- **Frontend**: Mock GraphQL responses in `__mocks__/`
- **Backend**: Factory functions for model creation
- **Integration**: Seed scripts for realistic data

### Database Testing
- **Strategy**: Fresh database per test
- **Speed**: SQLite in-memory for unit tests
- **Integration**: PostgreSQL container for integration tests

## Troubleshooting

### Common Issues

**Frontend tests timeout**
```bash
# Increase timeout in vitest.config.ts
test: {
  testTimeout: 10000
}
```

**Backend database connection**
```bash
# Check test database URL
echo $DATABASE_URL

# Reset test database
docker compose -f docker-compose.test.yml down -v
```

**GraphQL schema errors**
```bash
# Regenerate GraphQL types
cd frontend && npm run codegen
```

## Security Testing

### Dependency Scanning
- **Tool**: Trivy in GitHub Actions
- **Frequency**: Every PR and nightly
- **Coverage**: npm packages, Python packages, Docker images

### OWASP Testing
- **Tool**: ZAP baseline scan (planned)
- **Target**: Production deployment
- **Coverage**: Common vulnerabilities

---

**Test Coverage Status**: ![CI](https://github.com/your-org/gymintel-web/workflows/CI/badge.svg)

For questions about testing setup, see `CONTRIBUTING.md` or create an issue.