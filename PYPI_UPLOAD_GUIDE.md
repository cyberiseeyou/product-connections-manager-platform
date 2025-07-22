# 📦 PyPI Upload Guide for Product Connections Manager

## Prerequisites Checklist

✅ **Twine Installed**: `pip install twine`  
✅ **Package Built**: Both `.whl` and `.tar.gz` files in `dist/`  
✅ **README Added**: Package description included  
✅ **License Set**: MIT License configured  

## Step-by-Step Upload Process

### Step 1: Create PyPI Account
1. Go to [pypi.org](https://pypi.org/account/register/)
2. Create your account
3. Verify your email address

### Step 2: Generate API Token (Recommended)
1. Go to [pypi.org/manage/account/#api-tokens](https://pypi.org/manage/account/#api-tokens)
2. Click "Add API token"
3. Give it a name like "product-connections-manager"
4. Set scope to "Entire account" (or specific project after first upload)
5. Copy the token (it starts with `pypi-`)

### Step 3: Test Upload (Optional but Recommended)

**Upload to TestPyPI first:**
```bash
python -m twine upload --repository testpypi dist/*
```

**Test the installation:**
```bash
pip install --index-url https://test.pypi.org/simple/ product-connections-manager
```

### Step 4: Upload to Production PyPI

**Method 1: Using API Token (Recommended)**
```bash
python -m twine upload dist/*
```
- Username: `__token__`
- Password: `pypi-AgEIcHl...` (your API token)

**Method 2: Using Username/Password**
```bash
python -m twine upload dist/*
```
- Username: `your_pypi_username`
- Password: `your_pypi_password`

## Commands Ready to Run

### Check Package Quality
```bash
cd "c:\Users\mathe\Python Projects\edr_printer_new"
python -m twine check dist/*
```

### Upload to TestPyPI
```bash
cd "c:\Users\mathe\Python Projects\edr_printer_new"
python -m twine upload --repository testpypi dist/*
```

### Upload to PyPI (Production)
```bash
cd "c:\Users\mathe\Python Projects\edr_printer_new"
python -m twine upload dist/*
```

## What Happens After Upload

1. **Package Available**: Your package will be available at `https://pypi.org/project/product-connections-manager/`
2. **Installation**: Users can install with `pip install product-connections-manager`
3. **Console Scripts**: The `edr-printer` and `edr-automated` commands will be available
4. **Documentation**: README will show on the PyPI page

## Security Best Practices

- ✅ Use API tokens instead of passwords
- ✅ Set token scope to specific project after first upload
- ✅ Store tokens securely (don't commit to git)
- ✅ Use TestPyPI for testing before production upload

## Troubleshooting

### Package Name Already Exists
- Choose a different name in `setup.py` and `pyproject.toml`
- Rebuild the package: `python -m build`

### Authentication Issues
- Double-check your API token
- Ensure username is `__token__` when using tokens
- Try username/password if token fails

### Upload Forbidden
- Package name might be reserved
- You might not have permission (check ownership)

## Your Package Details

- **Name**: `product-connections-manager`
- **Version**: `1.0.0`
- **Files Ready**: 
  - `product_connections_manager-1.0.0.tar.gz` (source)
  - `product_connections_manager-1.0.0-py3-none-any.whl` (wheel)

## Ready to Upload! 🚀

Your package is completely ready for PyPI upload. Just run the twine commands above!
