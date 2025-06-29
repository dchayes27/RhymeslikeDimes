#!/usr/bin/env python3
"""
Railway deployment entry point for RhymeslikeDimes
"""
import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

try:
    # Import the FastAPI app from backend
    from app.main import app
    
    if __name__ == "__main__":
        import uvicorn
        
        # Get port from environment (Railway sets this)
        port = int(os.environ.get("PORT", 8001))
        host = "0.0.0.0"
        
        print(f"🚀 Starting RhymeslikeDimes API on {host}:{port}")
        
        # Start the server
        uvicorn.run(
            app, 
            host=host, 
            port=port,
            log_level="info"
        )
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📁 Current working directory:", os.getcwd())
    print("🐍 Python path:", sys.path)
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup error: {e}")
    sys.exit(1)