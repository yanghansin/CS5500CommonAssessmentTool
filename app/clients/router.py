from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.clients.service.logic import interpret_and_calculate

app = FastAPI()

@app.post("/predict")
async def predict(data: PredictionInput):
    print("Running from UI")
    result = interpret_and_calculate(data.model_dump()) #testing through API with server, write a fxn that calls iac, give it a default dict
    return result

@app.get("/test")
async def testform():
    with open("testform.html") as file:
        data = file.read()
        return HTMLResponse(content=data,status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)