#!/usr/bin/env python
"""
A simple script to check if the Google API key is properly loaded from the .env file.
"""
import os

# Try to explicitly load from .env file in case we're running outside Django
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded .env file")
except ImportError:
    print("❌ python-dotenv is not installed. Run: pip install python-dotenv")

api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    # Only show part of the key for security
    masked_key = f"{api_key[:5]}...{api_key[-4:]}" if len(api_key) > 10 else "***"
    print(f"✅ GOOGLE_API_KEY is set: {masked_key}")
else:
    print("❌ GOOGLE_API_KEY environment variable is not set")
    print("\nMake sure you have a .env file in the project root with the line:")
    print("GOOGLE_API_KEY=your_api_key_here")

# Print information to help debug
print("\nAdditional debugging information:")
print(f"Current working directory: {os.getcwd()}")
print("Environment variables:")
for key in os.environ:
    if "KEY" in key or "API" in key or "TOKEN" in key:
        value = os.environ[key]
        masked_value = f"{value[:3]}...{value[-3:]}" if len(value) > 8 else "***"
        print(f"  {key}: {masked_value}") 