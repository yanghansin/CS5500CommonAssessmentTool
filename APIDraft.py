from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from logic import interpret_and_calculate

app = FastAPI()

#entry point
#input data
#dictionary of key/value pairs
class PredictionInput(BaseModel):
    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str #is a string
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str

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