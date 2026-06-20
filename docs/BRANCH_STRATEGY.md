# DataNarrate - Branch Strategy

## Branching Model

We use a simplified Git Flow model for this project.

### Main Branches

- `main`: Production-ready code. Always stable.
- `develop`: Integration branch for features. Next version in development.

### Supporting Branches

- `feature/*`: New features. Branch off from `develop`, merge back into `develop`.
- `bugfix/*`: Bug fixes. Branch off from `develop`, merge back into `develop`.
- `hotfix/*`: Critical production fixes. Branch off from `main`, merge back into `main` and `develop`.

## Workflow Example

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-awesome-feature
   ```

2. Make changes and commit:
   ```bash
   git add .
   git commit -m "feat: add my awesome feature"
   ```

3. Push and create PR:
   ```bash
   git push origin feature/my-awesome-feature
   ```

4. After PR approval, merge into `develop`.
