# GymIntel Web Documentation

Welcome to the GymIntel Web documentation! This directory contains all the technical documentation for the project.

## 📚 Documentation Index

### Development Guides
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Comprehensive development setup and guidelines
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines and container-first development policy
- **[TESTING.md](TESTING.md)** - Testing framework, strategies, and best practices

### Project Context
- **[CLAUDE.md](CLAUDE.md)** - AI assistant context, architecture details, and development phases

## 🔗 Quick Links

### Getting Started
1. Read the [main README](../README.md) for project overview
2. Follow [DEVELOPMENT.md](DEVELOPMENT.md) for setup instructions
3. Review [CONTRIBUTING.md](CONTRIBUTING.md) before making changes
4. Consult [TESTING.md](TESTING.md) for testing requirements

### Key Commands
```bash
# Start development environment
./dev-start.sh

# Run all tests
./scripts/test.sh

# View logs
docker compose logs -f

# Access services
# Frontend: http://localhost:3000
# GraphQL: http://localhost:8000/graphql
# API Docs: http://localhost:8000/docs
```

### Development Philosophy
- **Container-First**: All development in Docker containers
- **Type-Safe**: TypeScript frontend, Python type hints
- **Test-Driven**: 80% minimum code coverage
- **GraphQL-First**: Schema-driven development

## 🗺️ Documentation Structure

```
docs/
├── README.md         # This file
├── DEVELOPMENT.md    # Development setup guide
├── CONTRIBUTING.md   # Contribution guidelines
├── TESTING.md        # Testing documentation
└── CLAUDE.md         # AI context & architecture
```

## 📝 Documentation Standards

When updating documentation:
1. Keep language clear and concise
2. Include code examples where helpful
3. Update the table of contents if adding sections
4. Ensure all links are relative and working
5. Follow Markdown best practices

## 🤝 Need Help?

- Check existing [GitHub Issues](https://github.com/a-deal/gymintel-web/issues)
- Review the troubleshooting sections in each guide
- Create a detailed issue if you encounter problems

---

**Remember**: This project follows a container-first development policy. No local development tools should be installed!