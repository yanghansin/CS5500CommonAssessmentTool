from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import json
import numpy as np
import pickle
from itertools import combinations_with_replacement

#request would include whatever the front end gives us
#we would clean the data, does not include all of the interventions
#then we would prepare the data by duplicating it and each would have a different variation of interventions
#because of the way batching works, we don't have to do the prediction on each row, we can treat it as one 
#unit of data, then we're doing inference on 128 generated rows, then we look at the ones with highest 3 scores
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
# fast API is separate from the model, no business logic, middle
# get data from website and turn into numbers 8.10

model = pickle.load(open("model.pkl","rb"))

#website address that takes input from a form, processes it and returns result
# first, we process inputs by cleaning them on and sanitizing them, 
# backend is in two parts, model is created once, that's where we would generalize or have specific data
# augment input by creating 127 copies, with a variation on the interventions
# we do a prediction using the model on the base data with no interventions-baseline score
# we predict again with 127 variations, which will each get their own score
# finally, we build a return that features the baseline & the top N combinations of interventions
# optionally, we save predictions for later examination --- 

#ensure data is in the same order.

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

def clean_input_data(data):
    #translate input into wahtever we trained the model on, numerical data in a specific order
    #if situation where interventions are set in stone, the command below is just cleaning up and organizing the input and making up baseline without any interventions
    #we are making list of interventions
    #any data has to be given by the form or we have to get rid of it
    #align column with order in columns-match up names, assume 
    # to do every column has to be in demographics
    columns = ["age","gender","work_experience","canada_workex","dep_num",	"canada_born",	
               "citizen_status",	"level_of_schooling",	"fluent_english",	"reading_english_scale",	
               "speaking_english_scale",	"writing_english_scale",	"numeracy_scale",	"computer_scale",	
               "transportation_bool",	"caregiver_bool",	"housing",	"income_source",	"felony_bool",	"attending_school",	
               "currently_employed",	"substance_use",	"time_unemployed",	"need_mental_health_support_bool"]
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
    output = []
    for column in columns:
        data = demographics[column]
        if type(data) == str :
            data = convert_text(data)
        output.append(data)
    return output
    #make list of column in correct order
    #to do, ask wayne to send numbers whenever possible
    # interventions = data['interventions']
    # to do - write a function to account for T/F Y/N input

def convert_text(data:str):
    #take string and do whatever we need to convert it into a number    
    # Convert categorical variables to integers (same as before)
    #turn into a list of dictionar
    categorical_cols_integers = [
        {
            "true": 1,
            "false": 0,
            "no": 0,
            "yes": 1
        },
        {
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
        {
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
    ]
    for category in categorical_cols_integers:
        if data in category:
            return category[data]
    return int(data)
    
    # Convert demographics  to integers

#first step is to repeat row of data 127 times, create 127 combinations, combine them
def create_matrix(row):
    data = [row.copy() for _ in range(127)] #127 because we have 7 interventions
    perms = intervention_permutations(7)
    data = np.array(data)
    perms = np.array(perms)
    matrix = np.concatenate((data,perms), axis = 1) #two 
    return matrix
#create matrix of permutations of 1 and 0 of num length
def intervention_permutations(num):
    perms = combinations_with_replacement([0,1],num)
    return perms

def get_baseline_row(row):
    base_interventions = np.array([0]*7) # no interventions
    row = np.array(row)
    line = np.concatenate((row,base_interventions), axis = 1)
    return line

def process_results(results):
    #placeholder, go through matrix and produce a list of intervention names for each row of the matrix, format, 
    #process, and return
    return results
#whatever wayne and I agree with is not necessarily this, might have to update
def interpret_and_calculate(data):
    # Separate demographics and interventions
    raw_data = clean_input_data(data)
    #expand into rows of data that include the interventions, then make predictions and format into output
    baseline_row = get_baseline_row(raw_data)
    intervention_rows = create_matrix(raw_data)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows)

    # need to tie interventions to percentages
    # concat predictions to intervention matrix
    result_matrix = np.concatenate((intervention_rows,intervention_predictions), axis = 1)
    
    # sort this matrix based on prediction
    result_matrix = np.sort(result_matrix, order = -1, axis = 0) #note, sorted by ascending
    # slice matrix to only top N results
    result_matrix = result_matrix[-3:,-8:] #-8 for interventions and prediction, want top 3
    # post process results if needed ie make list of names for each row
    results = process_results(result_matrix)
    # build output dict
    output = {
        "baseline": baseline_prediction,
        "interventions": results,
    }
    return output



    # Predict baseline return to work and success increase
    # baseline_return_to_work = rf_model_baseline.predict(X_pred_baseline)[0]
    # success_increase_results = {}
    # for intervention in interventions:
    #     X_pred_success[intervention] = 1
    #     success_increase_results[intervention] = rf_model_success_increase.predict(X_pred_success)[0]
    #     X_pred_success[intervention] = 0
    
    # total_increase = baseline_return_to_work + sum(success_increase_results.values())

    # result = {
    #     "baseline_return_to_work": baseline_return_to_work, #need to know the type
    #     "success_increase_for_each_intervention": success_increase_results, #what is this type, list, dict, etc.
    #     "total_increase": total_increase #define this type, will be dict
    # }
    
    # return result

#endpoints, a get and a post endpoint
#data has to follow format of prediction input

@app.post("/predict")
async def predict(data: PredictionInput):
    result = interpret_and_calculate(data.dict())
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# what is he expecting to get back re: interventions, a list of interventions by name and expected success?
# to do: run the code

#run it as a server, how to connect the two