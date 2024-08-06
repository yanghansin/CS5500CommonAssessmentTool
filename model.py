import pandas as pd
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

#can something complex, like flask or fastAPI
# we are doing a generalized version of the data, if the training data is individuals we would generalize
###make it modular, whatever data we get from user goes back into model
#models are not good at updating on individual lines very often
#every time we get a query, we would save data to new CSV, to intermediate storage, the data we are training from
#training data that has been verified, what we are doing is prediction
# we take predictions and put them aside to verify, and then in future social worker will compare outcome to prediction
#we would get individualized data after 2 weeks we anonymize it and feed it back to model
#

def prepare_models():
    # Load dataset and define the features and labels
    backendCode = pd.read_csv('data_commontool.csv')
    
    # Define categorical columns and interventions
    #how to validate input data
    #pandas
    #make a fxn whose only job is to take in one row of data that would throw an error as appropiate
    #if coming from website, put it in model
    #assume current data is currently cleaned up
    #refactor and remove baseline
    categorical_cols = ['age',
                        'gender', #bool
                        'work_experience', #years of work experience
                        'canada_workex',#years of work experience in canada
                        'dep_num', #number of dependents
                        'canada_born', #born in canada
                        'citizen_status', #citizen status
                        'level_of_schooling', #highest level achieved (1-14)
                        'fluent_english', #english level fluency, scale (1-10)
                        'reading_english_scale', #reading scale (1-10)
                        'speaking_english_scale', #speaking level comfort (1-10)
                        'writing_english_scale', #writing scale (1-10) 
                        'numeracy_scale', #numeracy scale (1-10)
                        'computer_scale', #computer use scale (1-10)
                        'transportation_bool', #need transportation support (bool)
                        'caregiver_bool', #is a primary care giver bool
                        'housing', #housing situation 1-10
                        'income_source', #source of income 1-10
                        'felony_bool', #has a felony bool
                        'attending_school', #currently a student bool
                        'currently_employed', #currently employed bool
                        'substance_use', #disorder, bool
                        'time_unemployed', #number of years unemployed
                        'need_mental_health_support_bool'] #need support
    interventions = [
        'employment_assistance',
        'life_stabilization',
        'retention_services',
        'specialized_services',
        'employment_related_financial_supports',
        'employer_financial_supports',
        'enhanced_referrals'
    ]
    
    # Prepare training data
    X_categorical_baseline = backendCode[categorical_cols]
    y_baseline = backendCode['success_rate']
    X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline = train_test_split(
        X_categorical_baseline, y_baseline, test_size=0.2, random_state=42)

    
    # Example: Train a RandomForestRegressor model for baseline data
    rf_model_baseline = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_baseline.fit(X_train_baseline, y_train_baseline)

    # Example: Predicting on the test set
    baseline_predictions = rf_model_baseline.predict(X_test_baseline)
    #todo = calculate error rate by comparing baseline to test y values and report on the accuracy. MSE or otherwise

    # Define feature names used during training
    feature_names_baseline = X_categorical_baseline.columns.tolist()
    
    return rf_model_baseline
#     return X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline, X_success_increase, y_success_increase, rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success

# X_train_baseline, X_test_baseline, y_train_baseline, y_test_baseline, X_success_increase, y_success_increase, rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success = prepare_models()

# # Print the variables
# print(X_train_baseline)
# print(X_test_baseline)
# print(y_train_baseline)
# print(y_test_baseline)
# print(X_success_increase)
# print(y_success_increase)
# print(rf_model_baseline)
# print(rf_model_success_increase)
# print(feature_names_baseline)
# print(feature_names_success)

#do calculation for error rate
#there's the preparation of the model and there's the saving of the file and that's a snapshot of our model after 
#training, the easiest way is to use pickle.

model = prepare_models()
import pickle
pickle.dump(model,open("model.pkl", "wb")) #saves model to the file name input, write binary
#when we write API, 
model = pickle.load(open("model.pkl", "rb")) #read binary

# def interpret_and_calculate(data):

# #                         'work_experience', #years of work experience
# #                         'canada_workex',#years of work experience
# #                         'dep_num', #number of dependents
# #                         'canada_born', #born in canada
# #                         'citizen_status', #citizen status
# #                         'level_of_schooling', #highest level achieved (1-14)
# #                         'fluent_english', #english level fluency, scale (1-1-)
# #                         'reading_english_scale', #reading scale (1-10)
# #                         'speaking_english_scale', #speaking level comfort (1-10)
# #                         'writing_english_scale', #writing scale (1-10)
# #                         'numeracy_scale', #numeracy scale (1-10)
# #                         'computer_scale', #computer use scale  (1-10)
# #                         'transportation_bool', #need transportation support (bool)
# #                         'caregiver_bool', #is a primary care giver bool
# #                         'housing', #housing situation 1-10
# #                         'income_source', #source of income 1-10
# #                         'felony_bool', #has a felony bool
# #                         'attending_school', #currently a student bool
# #                         'currently_employed', #currently employed bool
# #                         'substance_use', #disorder, bool
# #                         'time_unemployed', #number of years unemployed
# #                         'need_mental_health_support_bool'] #need support]
#     # Separate demographics and interventions
#     demographics = {
#         'work_ex':
#         'dep_num': data[0],
#         'canada_born': data[1],
#         'citizen_status': data[2],
#         'level_of_schooling': data[3],
#         'fluent_english': data[4],
#         'numeracy_bool': data[5],
#         'computer_bool': data[6],
#         'transportation_bool': data[7],
#         'caregiver_bool': data[8],
#         'housing': data[9],
#         'income_source': data[10],
#         'felony_bool': data[11],
#         'attending_school': data[12],
#         'currently_employed': data[13],
#         'time_unemployed': data[14],
#         'canada_workex': data[15],
#     }
#     interventions = data[16:]
    
#     # Convert categorical variables to integers (same as before)
#     categorical_cols_integers = {
#         'dep_num': {
#             '0': 0,
#             '1': 1,
#             '2': 2,
#             '3': 3,
#             '4': 4,
#             '5': 5,
#             '6': 6,
#             '7': 7,
#             '8': 8,
#             '10': 10
#         },
#         'canada_born': {
#             "No": 0,
#             "Yes": 1
#         },
#         'citizen_status': {
#             "No": 0,
#             "Yes": 1
#         },
#         'fluent_english': {
#             "No": 0,
#             "Yes": 1
#         },
#         'numeracy_bool': {
#             "No": 0,
#             "Yes": 1
#         },
#         'computer_bool': {
#             "No": 0,
#             "Yes": 1
#         },
#         'transportation_bool': {
#             "No": 0,
#             "Yes": 1
#         },
#         'caregiver_bool': {
#             "No": 0,
#             "Yes": 1
#         },
#         'income_source': {

#         },
#         'level_of_schooling': {
#             'Grade 0-8': 1,
#             'Grade 9': 2,
#             'Grade 10': 3,
#             'Grade 11': 4,
#             'Grade 12 or equivalent (GED)': 5,
#             'OAC or Grade 13': 6,
#             'Some college': 7,
#             'Some university': 8,
#             'Some apprenticeship': 9,
#             'Certificate of Apprenticeship': 10,
#             'Journeyperson': 11,
#             'Certificate/Diploma': 12,
#             'Bachelor’s degree': 13,
#             'Post graduate': 14
#         },
#         'housing_situation': {
#             'Renting-private': 1,
#             'Renting-subsidized': 2,
#             'Boarding or lodging': 3,
#             'Homeowner': 4,
#             'Living with family/friend': 5,
#             'Institution': 6,
#             'Temporary second residence': 7,
#             'Band-owned home': 8,
#             'Homeless or transient': 9,
#             'Emergency hostel': 10
#         }

#     }

#     # Prepare models and feature names (same as before)
#     rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success = prepare_models()

#     # Prepare input data (same as before)
#     demographics_integers = {col: categorical_cols_integers[col][val] for col, val in demographics.items()}
#     X_pred_baseline = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_baseline, fill_value=0)
#     X_pred_success = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_success, fill_value=0)

#     # Predict baseline return to work and success increase (same as before)
#     baseline_return_to_work = rf_model_baseline.predict(X_pred_baseline)[0]
#     success_increase_results = {}
#     for intervention in interventions:
#         X_pred_success[intervention] = 1
#         success_increase_results[intervention] = rf_model_success_increase.predict(X_pred_success)[0]
#         X_pred_success[intervention] = 0
    
#     total_increase = baseline_return_to_work + sum(success_increase_results.values())

#     result = {
#         "baseline_return_to_work": baseline_return_to_work,
#         "success_increase_for_each_intervention": success_increase_results,
#         "total_increase": total_increase
#     }
    
#     return result