import uvicorn
from main import create_app

if __name__ == "__main__":
    app,db= create_app()
    print(" database app")
    uvicorn.run(app, host="0.0.0.0", port=8002)
