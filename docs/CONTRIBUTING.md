# Contributing to GymIntel Web

## 🐳 Container-First Development Policy

**All development for GymIntel Web must be done using Docker containers.** This ensures consistency across all development environments and keeps host systems clean.

### Why Container-First?

1. **Environment Consistency**: Same Node.js, Python, and database versions for everyone
2. **Clean Host System**: No local development dependencies required
3. **Easy Onboarding**: New contributors just need Docker
4. **Reproducible Builds**: Identical environments in development, testing, and production
5. **Dependency Isolation**: No conflicts with other projects or system installations

## 🚀 Getting Started

### Prerequisites
- **Docker Desktop** (latest stable version)
- **Git** for version control
- **Text Editor/IDE** of your choice (VS Code recommended)

### Development Environment Setup

```bash
# 1. Clone the repository
git clone https://github.com/a-deal/gymintel-web.git
cd gymintel-web

# 2. Start development environment
./dev-start.sh

# 3. That's it! All services are now running in containers
```

### Available Services

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React development server |
| Backend API | http://localhost:8000 | FastAPI + GraphQL server |
| GraphQL Playground | http://localhost:8000/graphql | Interactive GraphQL IDE |
| API Docs | http://localhost:8000/docs | Swagger/OpenAPI documentation |
| PostgreSQL | localhost:5432 | Database (internal to containers) |
| Redis | localhost:6379 | Cache & sessions (internal to containers) |

## 🛠️ Development Workflow

### Making Changes

#### Frontend Development
```bash
# All frontend changes are automatically hot-reloaded
# Edit files in ./frontend/src/ and see changes instantly

# Run frontend tests in container
docker compose exec frontend npm test

# Build production frontend
docker compose exec frontend npm run build
```

#### Backend Development
```bash
# All backend changes trigger automatic reload via uvicorn --reload
# Edit files in ./backend/app/ and see changes instantly

# Run backend tests in container
docker compose exec backend python -m pytest

# Access backend shell for debugging
docker compose exec backend bash
```

#### Database Operations
```bash
# Run database migrations
docker compose exec backend alembic upgrade head

# Create new migration
docker compose exec backend alembic revision --autogenerate -m "Description"

# Access PostgreSQL shell
docker compose exec database psql -U gymintel -d gymintel
```

### Container Management Commands

```bash
# View logs (all services)
docker compose logs -f

# View logs (specific service)
docker compose logs -f backend
docker compose logs -f frontend

# Restart a service
docker compose restart backend

# Rebuild and restart (after Dockerfile changes)
docker compose up --build backend

# Stop all services
docker compose down

# Clean restart (removes volumes)
docker compose down -v && docker compose up --build
```

### Installing New Dependencies

#### Frontend Dependencies
```bash
# Add new npm package
docker compose exec frontend npm install package-name

# Add dev dependency
docker compose exec frontend npm install --save-dev package-name

# The package.json will be updated automatically via volume mount
```

#### Backend Dependencies
```bash
# Add new Python package
docker compose exec backend pip install package-name

# Update requirements.txt
docker compose exec backend pip freeze > requirements.txt

# Rebuild container to persist changes
docker compose up --build backend
```

## 📝 Development Guidelines

### Code Style
- **Frontend**: ESLint + Prettier (configured in container)
- **Backend**: Black + isort + flake8 (configured in container)

```bash
# Format frontend code
docker compose exec frontend npm run lint

# Format backend code  
docker compose exec backend black .
docker compose exec backend isort .
```

### Testing
- All tests must run in containers
- Tests should pass before submitting pull requests
- Minimum 80% code coverage required

```bash
# Run all tests (recommended)
./scripts/test.sh

# Run tests manually
docker compose -f docker-compose.test.yml up --build

# Individual service tests
docker compose exec frontend npm run test:coverage
docker compose exec backend pytest --cov=app --cov-report=term-missing

# View coverage reports
open frontend/coverage/index.html
open backend/htmlcov/index.html
```

For detailed testing guidelines, see [TESTING.md](TESTING.md).

### Environment Variables
- Use `.env.example` as template
- Never commit actual API keys
- All environment variables are configured in `docker-compose.yml`

## 🚫 What NOT to Install Locally

**Do NOT install these on your host system:**
- ❌ Node.js / npm / yarn
- ❌ Python / pip / virtualenv
- ❌ PostgreSQL / Redis
- ❌ Any project-specific dependencies

**The only tools you need locally:**
- ✅ Docker Desktop
- ✅ Git
- ✅ Your preferred text editor/IDE

## 🔧 Troubleshooting

### Container Issues
```bash
# Clean restart everything
docker compose down -v
docker compose build --no-cache
docker compose up

# Check container status
docker compose ps

# View container resource usage
docker stats
```

### Port Conflicts
If you get port binding errors:
```bash
# Check what's using the ports
lsof -ti:3000,8000,5432,6379

# Kill processes using required ports
./cleanup.sh
```

### Database Issues
```bash
# Reset database completely
docker compose down -v
docker compose up database
docker compose exec backend alembic upgrade head
```

## 🤝 Contribution Process

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create** a feature branch: `git checkout -b feature/your-feature`
4. **Develop** using containers only (follow this guide)
5. **Test** your changes: `docker compose exec backend pytest && docker compose exec frontend npm test`
6. **Commit** your changes with clear messages
7. **Push** to your fork: `git push origin feature/your-feature`
8. **Create** a Pull Request

### Pull Request Requirements
- [ ] All tests pass in containers (`./scripts/test.sh`)
- [ ] Code coverage meets 80% minimum threshold
- [ ] No local development dependencies added
- [ ] Documentation updated if needed
- [ ] Docker configuration works correctly
- [ ] Code follows established style guidelines
- [ ] Security scan passes (Trivy)
- [ ] Frontend: ESLint and TypeScript checks pass
- [ ] Backend: Black, isort, and flake8 checks pass

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [GraphQL Documentation](https://graphql.org/)

## 🆘 Getting Help

If you encounter issues with the container-based development setup:

1. Check the [troubleshooting section](#-troubleshooting) above
2. Review existing [GitHub Issues](https://github.com/a-deal/gymintel-web/issues)
3. Create a new issue with:
   - Your Docker version: `docker --version`
   - Your Docker Compose version: `docker compose version`
   - Container logs: `docker compose logs`
   - Steps to reproduce the issue

---

**Remember: If you're installing development tools locally, you're doing it wrong!** 🐳

Everything should run in containers to maintain our clean, consistent development environment.