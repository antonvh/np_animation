# Publishing to PyPI

This document provides instructions for building and publishing the np_animation package to PyPI.

## Prerequisites

Install build tools:

```bash
pip install --upgrade build twine
```

## Building the Package

1. Make sure the version number is updated in `pyproject.toml`

2. Build the distribution packages:

```bash
python -m build
```

This will create both source distribution (`.tar.gz`) and wheel (`.whl`) files in the `dist/` directory.

## Testing the Build

Before publishing, you can test the package locally:

```bash
pip install dist/np_animation-*.whl
```

## Uploading to PyPI

### Test PyPI (recommended for first time)

1. Register at <https://test.pypi.org/>

2. Upload to Test PyPI:

   ```bash
   python -m twine upload --repository testpypi dist/*
   ```

3. Test installation from Test PyPI:

   ```bash
   pip install --index-url https://test.pypi.org/simple/ np_animation
   ```

### Production PyPI

1. Register at <https://pypi.org/>

2. Upload to PyPI:

   ```bash
   python -m twine upload dist/*
   ```

## Version Management

Update the version number in:

- `pyproject.toml` (in the `[project]` section)
- `__init__.py` (the `__version__` variable)

Follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: incompatible API changes
- MINOR: backwards-compatible functionality additions
- PATCH: backwards-compatible bug fixes

## GitHub Release

After publishing to PyPI:

1. Create a git tag:

   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. Create a release on GitHub with the changelog
