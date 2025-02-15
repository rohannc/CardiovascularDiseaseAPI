from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/predict', methods=['POST'])
def cardiovascularPredict():
    if request.is_json:
        if request.is_json:
            data = request.get_json()
            input_dictionary = {key: value for key, value in data.items()}
        else:
            return jsonify({"error": "Request must be JSON"}), 400
    
    age_years = input_dictionary['Age']
    gender = input_dictionary['Gender']
    height = input_dictionary['Height']
    weight = input_dictionary['Weight']
    cholesterol = input_dictionary['Cholesterol']
    bmi = input_dictionary['BMI']
    bp_category = input_dictionary['BloodPressureCategory']
    ap_hi = input_dictionary['Systolic']
    ap_lo = input_dictionary['Diastolic']
    smoke = input_dictionary['Smoke']
    alco = input_dictionary['Alcohol']
    active = input_dictionary['Active']
    gluc = input_dictionary['Glucose']

    with open('model1.pkl', 'rb') as f:  # 'rb' = read binary mode
        loaded_model = pickle.load(f)

    with open('scaler1.pkl', 'rb') as f:  # 'rb' = read binary mode
        loaded_scaler = pickle.load(f)
    
    new_patient = transform_input_data(gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, age_years, bmi, bp_category)
    patient_data_scaled = loaded_scaler.transform([new_patient])
    prediction = loaded_model.predict(patient_data_scaled)
    result = 'Cardiovascular Disease detected' if prediction[0] == 1 else 'No Cardiovascular Disease detected'
    return jsonify({"result": result})

def transform_input_data(gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, 
                         smoke, alco, active, age_years, bmi, bp_category):
    
    # Create a dictionary with input data
    data = {
        'gender': [gender],
        'height': [height],
        'weight': [weight],
        'ap_hi': [ap_hi],
        'ap_lo': [ap_lo],
        'cholesterol': [cholesterol],
        'gluc': [gluc],
        'smoke': [smoke],
        'alco': [alco],
        'active': [active],
        'age_years': [age_years],
        'bmi': [bmi],
        'bp_category': [bp_category]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Transform gender (decrease by 1)
    df['gender'] = df['gender'] - 1
    
    # Transform cholesterol and gluc (decrease by 1)
    df['cholesterol'] = df['cholesterol'] - 1
    df['gluc'] = df['gluc'] - 1
    
    # One-hot encode bp_category
    bp_categories = ['bp_Normal', 'bp_Elevated', 'bp_Hypertension Stage 1', 'bp_Hypertension Stage 2']
    for category in bp_categories:
        df[category] = (df['bp_category'] == category).astype(int)
    
    # Drop original bp_category column
    df = df.drop('bp_category', axis=1)
    
    # Select and order final features
    final_features = ['gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'age_years', 'bmi', 'bp_Elevated', 'bp_Hypertension Stage 1', 'bp_Hypertension Stage 2', 'bp_Normal']
    
    return df[final_features].values[0].tolist()

if __name__ == '__main__':
    app.run(debug=True)



