import uvicorn
import sys
import os

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("==========================================================")
    print("NEBULA: Intelligent Astronomical Data Platform (Backend)")
    print("Starting server at http://127.0.0.1:8000")
    print("Interactive API Docs: http://127.0.0.1:8000/docs")
    print("==========================================================")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
