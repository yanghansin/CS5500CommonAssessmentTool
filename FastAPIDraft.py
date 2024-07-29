from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

app = FastAPI()


X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline, X_success_increase, y_success_increase, rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success = prepare_models()

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

    # Convert demographics to integers
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