#!/usr/bin/env python3
"""
Simple startup script for the AutoGen Discussion Backend
"""

import os
import sys
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        import dotenv
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has API_KEY"""
    env_path = Path("../../.env")  # Look in project root
    if not env_path.exists():
        env_path = Path(".env")  # Look in current directory
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("Please create a .env file with your API_KEY:")
        print("API_KEY=your_azure_openai_api_key")
        return False
    
    # Load and check for API_KEY
    from dotenv import load_dotenv
    load_dotenv(env_path)
    
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("❌ API_KEY not found in .env file")
        print("Please add your Azure OpenAI API key to the .env file:")
        print("API_KEY=your_azure_openai_api_key")
        return False
    
    print("✅ API_KEY found in .env file")
    return True

def main():
    print("🚀 Starting AutoGen Discussion Backend...")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_env_file():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🌐 Starting Flask server on http://localhost:5000")
    print("📝 Open index.html in your browser to use the interface")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the backend
    try:
        from backend import app
        app.run(debug=True, port=5000, host='0.0.0.0')
    except KeyboardInterrupt:
        print("\n👋 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
