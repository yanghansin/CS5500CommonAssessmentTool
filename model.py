import pandas as pd
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def prepare_models():
    # Load dataset and define the features and labels
    classCode = pd.read_csv('training_data.csv')
    
    # Define categorical columns and interventions
    categorical_cols = ['dep_num', 
                        'canada_born',
                        'citizen_status',
                        'level_of_schooling',
                        'fluent_english',
                        'numeracy_bool',
                        'computer_bool',
                        'transportation_bool',
                        'caregiver_bool',
                        'housing',
                        'income_source',
                        'felony_bool',
                        'attending_school',
                        'currently_employed',
                        'time_unemployed',
                        'canada_workex']
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
    X_categorical_baseline = classCode[categorical_cols]
    y_baseline = classCode['baseline_return_to_work']
    X_train_baseline, _, y_train_baseline, _ = train_test_split(
        X_categorical_baseline, y_baseline, test_size=0.2, random_state=42)
    
    X_success_increase = classCode[categorical_cols + interventions]
    y_success_increase = classCode['success_increase']
    
    # Initialize and train the random forest models
    rf_model_baseline = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_baseline.fit(X_train_baseline, y_train_baseline)

    rf_model_success_increase = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_success_increase.fit(X_success_increase, y_success_increase)
    
    # Define feature names used during training
    feature_names_baseline = X_categorical_baseline.columns.tolist()
    feature_names_success = X_success_increase.columns.tolist()
    
    return rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success


# 
#  
]
def interpret_and_calculate(data):
    # Separate demographics and interventions
    demographics = {
        'dep_num': data[0],
        'canada_born': data[1],
        'citizen_status': data[2],
        'level_of_schooling': data[3],
        'fluent_english': data[4],
        'numeracy_bool': data[5],
        'computer_bool': data[6],
        'transportation_bool': data[7],
        'caregiver_bool': data[8],
        'housing': data[9],
        'income_source': data[10],
        'felony_bool': data[11],
        'attending_school': data[12],
        'currently_employed': data[13],
        'time_unemployed': data[14],
        'canada_workex': data[15],
    }
    interventions = data[16:]
    
    # Convert categorical variables to integers (same as before)
    categorical_cols_integers = {
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
        },
        'have_disability': {
            "No": 0,
            "Yes": 1
        }

# 'dep_num', 
#                         'canada_born',
#                         'citizen_status',
#                         'level_of_schooling',
#                         'fluent_english',
#                         'numeracy_bool',
#                         'computer_bool',
#                         'transportation_bool',
#                         'caregiver_bool',
#                         'housing',
#                         'income_source',
#                         'felony_bool',
#                         'attending_school',
#                         'currently_employed',
#                         'time_unemployed',
#                         'canada_workex'
    }

    # Prepare models and feature names (same as before)
    rf_model_baseline, rf_model_success_increase, feature_names_baseline, feature_names_success = prepare_models()

    # Prepare input data (same as before)
    demographics_integers = {col: categorical_cols_integers[col][val] for col, val in demographics.items()}
    X_pred_baseline = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_baseline, fill_value=0)
    X_pred_success = pd.DataFrame([demographics_integers]).reindex(columns=feature_names_success, fill_value=0)

    # Predict baseline return to work and success increase (same as before)
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
