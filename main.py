# Railway entry point
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)