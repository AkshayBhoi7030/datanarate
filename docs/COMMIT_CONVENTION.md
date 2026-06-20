# DataNarrate - Commit Convention

We follow Conventional Commits.

## Format

```
<type>(<scope>): <description>

<body>

<footer>
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Formatting, missing semi-colons, etc. (no code change)
- `refactor`: Neither fixes a bug nor adds a feature
- `perf`: Improves performance
- `test`: Adding or correcting tests
- `chore`: Build process or auxiliary tools

## Examples

```
feat(auth): add JWT token authentication
fix(query): resolve SQL injection vulnerability
docs(readme): update installation instructions
style: format code with black
refactor(db): restructure database models
perf(api): optimize query response time
test: add unit tests for user service
chore: update dependencies
```
