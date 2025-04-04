import uvicorn
import os
from pathlib import Path
import sys

# Add the project root directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Get host from environment variable or use default
    host = os.getenv("HOST", "0.0.0.0")
    
    # Get reload flag from environment variable or use default
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"Starting server on {host}:{port}")
    print("Press CTRL+C to stop")
    
    # Run the server
    uvicorn.run(
        "api.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    ) 