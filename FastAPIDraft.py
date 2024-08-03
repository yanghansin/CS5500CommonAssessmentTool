from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import json
import numpy as np
import pickle

#request would include whatever the front end gives us
#we would clean the data, does not include all of teh interventions
#then we would prepare the data by duplicating it and each would have a different variation of interventions
#because of the way batching works, we don't have to do the prediction on each row, we can treat it as one 
#unit of data, then we're doing inference on 128 generated rown, then we look at the ones with highest 3 scores
#return as a JSON (talk with wayne), return interventions. success rate would 
#the user is going to have to run it
# the user will get 2 results. first is prediction with no interventions and following x will be with best results
# before friday, try to break things down 
# when make fxn to clean data, don't overcomplicate it
# when generating 127 rows that are all combinations, just say "here;s the list and return list of lists and do all that are permutations"
#have fxn that returns all combos
#API cleans it, generations of new rows, runs prediction and produces JSON and top results
#why pickle - takes memory as it is in python and takes a binary snapshot and saves it to a file  joblib
# to do: run mean test on model, write fxn to check all inputs are filled in, sanitize data

model = pickle.load(open("model.pkl","rb"))

#website address that takes input from a form, processes it and returns result
# first, we process inputs by cleaning them on and sanitizing them, 
# augment input by creating 127 copies, with a variation on the interventions

app = FastAPI()


# input data
class PredictionInput(BaseModel):
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
    income_source: int
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str
    interventions: List[str]

def interpret_and_calculate(data):
    # Separate demographics and interventions
    demographics = {
        'work_experience': data['work_experience'],
        'canada_workex': data['canada_workex'],
        'dep_num': data['dep_num'],
        'canada_born': data['canada_born'],
        'citizen_status': data['citizen_status'],
        'level_of_schooling': data['level_of_schooling'],
        'fluent_english': data['fluent_english'],
        'reading_english_scale': data['reading_english_scale'],
        'speaking_english_scale': data['speaking_english_scale'],
        'writing_english_scale': data['writing_english_scale'],
        'numeracy_scale': data['numeracy_scale'],
        'computer_scale': data['computer_scale'],
        'transportation_bool': data['transportation_bool'],
        'caregiver_bool': data['caregiver_bool'],
        'housing': data['housing'],
        'income_source': data['income_source'],
        'felony_bool': data['felony_bool'],
        'attending_school': data['attending_school'],
        'currently_employed': data['currently_employed'],
        'substance_use': data['substance_use'],
        'time_unemployed': data['time_unemployed'],
        'need_mental_health_support_bool': data['need_mental_health_support_bool']
    }
    interventions = data['interventions']
    
    # Convert categorical variables to integers (same as before)
    categorical_cols_integers = {
        'dep_num': {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '10': 10
        },
        'canada_born': {
            "No": 0,
            "Yes": 1
        },
        'citizen_status': {
            "No": 0,
            "Yes": 1
        },
        'fluent_english': {
            "No": 0,
            "Yes": 1
        },
        'numeracy_bool': {
            "No": 0,
            "Yes": 1
        },
        'computer_bool': {
            "No": 0,
            "Yes": 1
        },
        'transportation_bool': {
            "No": 0,
            "Yes": 1
        },
        'caregiver_bool': {
            "No": 0,
            "Yes": 1
        },
        'income_source': {

        },
        'level_of_schooling': {
            'Grade 0-8': 1,
            'Grade 9': 2,
            'Grade 10': 3,
            'Grade 11': 4,
            'Grade 12 or equivalent (GED)': 5,
            'OAC or Grade 13': 6,
            'Some college': 7,
            'Some university': 8,
            'Some apprenticeship': 9,
            'Certificate of Apprenticeship': 10,
            'Journeyperson': 11,
            'Certificate/Diploma': 12,
            'Bachelor’s degree': 13,
            'Post graduate': 14
        },
        'housing_situation': {
            'Renting-private': 1,
            'Renting-subsidized': 2,
            'Boarding or lodging': 3,
            'Homeowner': 4,
            'Living with family/friend': 5,
            'Institution': 6,
            'Temporary second residence': 7,
            'Band-owned home': 8,
            'Homeless or transient': 9,
            'Emergency hostel': 10
        }
    }

    # Convert demographics  to integers
    demographics_integers = {col: categorical_cols_integers.get(col, {}).get(val, val) for col, val in demographics.items()}
    X_pred_baseline = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_baseline, fill_value=0)
    X_pred_success = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_success, fill_value=0)

    # Predict baseline return to work and success increase
    baseline_return_to_work = rf_model_baseline.predict(X_pred_baseline)[0]
    success_increase_results = {}
    for intervention in interventions:
        X_pred_success[intervention] = 1
        success_increase_results[intervention] = rf_model_success_increase.predict(X_pred_success)[0]
        X_pred_success[intervention] = 0
    
    total_increase = baseline_return_to_work + sum(success_increase_results.values())

    result = {
        "baseline_return_to_work": baseline_return_to_work,
        "success_increase_for_each_intervention": success_increase_results,
        "total_increase": total_increase
    }
    
    return result

@app.post("/predict")
async def predict(data: PredictionInput):
    result = interpret_and_calculate(data.dict())
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)