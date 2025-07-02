#!/usr/bin/env python
"""Test script to verify imports work correctly."""
import os
import sys

print(f"Python version: {sys.version}")
print(f"Python path: {sys.path}")

try:
    import uvicorn

    print(f"✓ uvicorn imported successfully: {uvicorn.__version__}")
except ImportError as e:
    print(f"✗ Failed to import uvicorn: {e}")

try:
    import fastapi

    print(f"✓ fastapi imported successfully: {fastapi.__version__}")
except ImportError as e:
    print(f"✗ Failed to import fastapi: {e}")

try:
    import strawberry  # noqa: F401

    # Strawberry doesn't have __version__ attribute
    print("✓ strawberry imported successfully")
except ImportError as e:
    print(f"✗ Failed to import strawberry: {e}")

print("\nChecking if requirements.txt exists:")

if os.path.exists("requirements.txt"):
    print("✓ requirements.txt found")
    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "uvicorn" in line.lower():
                print(f"  Found uvicorn in requirements: {line.strip()}")
else:
    print("✗ requirements.txt not found")
