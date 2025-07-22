# 🚀 GitHub Actions + PyPI Setup Guide

## Overview

Your repository now includes automated CI/CD with GitHub Actions that will:

1. **Test your code** on every push and pull request
2. **Automatically publish to PyPI** when you create a version tag

## 📋 Setup Steps

### Step 1: Push to GitHub

```bash
git push -u origin main
```

### Step 2: Set up PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/#api-tokens)
2. Click "Add API token"
3. Name: `product-connections-manager-github-actions`
4. Scope: `Entire account` (or specific project after first upload)
5. Copy the token (starts with `pypi-`)

### Step 3: Add GitHub Secret

1. Go to your GitHub repository: `https://github.com/cyberiseeyou/product-connections-manager-platform`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token (the entire `pypi-AgEI...` string)
6. Click **Add secret**

### Step 4: Create a Release

To publish to PyPI, create a version tag:

```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0
```

## 🔄 Workflows Explained

### Test Workflow (`.github/workflows/test.yml`)

**Triggers**: Every push to main/develop, every pull request
**Runs on**: Ubuntu, Windows, macOS
**Python versions**: 3.8, 3.9, 3.10, 3.11, 3.12

**What it does**:
- ✅ Installs dependencies
- ✅ Runs linting with flake8
- ✅ Runs tests with pytest
- ✅ Tests package import
- ✅ Tests console scripts
- ✅ Builds and tests package installation
- ✅ Uploads coverage to Codecov

### Publish Workflow (`.github/workflows/publish.yml`)

**Triggers**: When you push a version tag (e.g., `v1.0.0`)
**Runs on**: Ubuntu latest
**Python version**: 3.11

**What it does**:
- ✅ Runs full test suite first
- ✅ Builds source and wheel distributions
- ✅ Checks package quality
- ✅ Publishes to PyPI automatically

## 🏷️ Version Release Process

### 1. Update Version
Update version in these files:
- `product_connections_manager/__init__.py`
- `setup.py`
- `pyproject.toml`

### 2. Update Changelog
Add your changes to `CHANGELOG.md`

### 3. Commit Changes
```bash
git add .
git commit -m "Bump version to 1.0.1"
git push
```

### 4. Create Release Tag
```bash
git tag v1.0.1
git push origin v1.0.1
```

### 5. Watch the Magic! ✨
- GitHub Actions will automatically run tests
- If tests pass, it will build and publish to PyPI
- Your package will be available at `https://pypi.org/project/product-connections-manager/`

## 🔧 Advanced Options

### Publish to TestPyPI First
Uncomment the `repository-url` line in `publish.yml`:
```yaml
repository-url: https://test.pypi.org/legacy/
```

And add a `TEST_PYPI_API_TOKEN` secret.

### Manual Publishing
You can also trigger publishing manually:
1. Go to **Actions** tab in GitHub
2. Select **Publish to PyPI** workflow
3. Click **Run workflow**

## 🛡️ Security Features

- ✅ Uses PyPI API tokens instead of passwords
- ✅ Tokens stored as encrypted GitHub secrets
- ✅ Automatic package verification before publishing
- ✅ Multi-platform testing before release

## 📊 Monitoring

After setup, you can monitor:
- **GitHub Actions**: See all runs in the Actions tab
- **PyPI**: View package stats at `https://pypi.org/project/product-connections-manager/`
- **Downloads**: Track package adoption

## 🎯 Next Steps

1. **Push to GitHub**: `git push -u origin main`
2. **Add PyPI token** to GitHub secrets
3. **Create first release**: `git tag v1.0.0 && git push origin v1.0.0`
4. **Watch automated deployment** in GitHub Actions

Your Enhanced EDR Printer will be live on PyPI within minutes! 🎉
