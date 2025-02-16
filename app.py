from flask import Flask, request, jsonify
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from huggingface_hub import InferenceClient

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'

@app.route('/predictCardiovascular', methods=['POST'])
def cardiovascularPredict():
    if request.is_json:
        if request.is_json:
            data = request.get_json()
            input_dictionary = {key: value for key, value in data.items()}
        else:
            return jsonify({"error": "Request must be JSON"}), 400
    
    age_years = int(input_dictionary['Age'])
    if (input_dictionary['Gender'].lower() == 'female'):
        gender = 0
    else:
        gender = 1
    height = float(input_dictionary['Height'])
    weight = float(input_dictionary['Weight'])
    if(input_dictionary['Cholesterol'].lower == 'normal'):
        cholesterol = 0
    elif(input_dictionary['Cholesterol'].lower == 'above normal'):
        cholesterol = 1
    else:
        cholesterol = 2
    bmi = float(weight / (height * height))
    # bmi = float(input_dictionary['BMI'])
    bp_category = input_dictionary['BloodPressureCategory']
    ap_hi = int(input_dictionary['Systolic'])
    ap_lo = int(input_dictionary['Diastolic'])
    if(input_dictionary['Smoke'].lower == 'smoker'):
        smoke = 1
    else:
        smoke = 0
    if(input_dictionary['Alcohol'].lower == 'alcoholic'):
        alco = 1
    else:
        alco = 0
    if(input_dictionary['Active'].lower == 'active'):
        active = 1
    else:
        active = 0
    if(input_dictionary['Glucose'].lower == 'normal'):
        gluc = 0
    elif(input_dictionary['Glucose'].lower == 'above normal'):
        gluc = 1
    else:
        gluc = 2

    with open('model1.pkl', 'rb') as f:  # 'rb' = read binary mode
        loaded_model = pickle.load(f)

    with open('scaler1.pkl', 'rb') as f:  # 'rb' = read binary mode
        loaded_scaler = pickle.load(f)
    
    new_patient = transform_input_data(gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, age_years, bmi, bp_category)
    patient_data_scaled = loaded_scaler.transform([new_patient])
    prediction = loaded_model.predict(patient_data_scaled)
    result = 'Cardiovascular Disease detected' if prediction[0] == 1 else 'No Cardiovascular Disease detected'
    return jsonify({"result": result})

@app.route('/predictDiabetes', methods=['POST'])
def diabetesPredict():
    if request.is_json:
        if request.is_json:
            data = request.get_json()
            input_dictionary = {key: value for key, value in data.items()}
        else:
            return jsonify({"error": "Request must be JSON"}), 400
    
    if(input_dictionary['BloodPressure'].lower == 'yes'):
        highbp = 1
    else:
        highbp = 0
    if(input_dictionary['HeartAttack'].lower == 'yes'):
        heartattack = 1
    else:
        heartattack = 0 
    age = input_dictionary['Age']
    if (input_dictionary['Gender'].lower == 'female'):
        sex = 0
    else:
        sex = 1
    if(input_dictionary['HighCholesterol'].lower == 'yes'):
        highchol = 1
    else:
        highchol = 0
    if(input_dictionary['Stroke'].lower == 'past history'):
        stroke = 1
    else: 
        stroke = 0
    if(input_dictionary['CholesterolCheck'].lower == 'within 1 year'):
        cholesterol = 0
    else:
        cholesterol = 1
    bmi = float(input_dictionary['BMI'])
    # bmi = float(input_dictionary['BMI'])
    if(input_dictionary['Smoke'].lower == 'smoker'):
        smoke = 1
    else:
        smoke = 0
    if(input_dictionary['Veggies'].lower == 'yes'):
        veggies = 1
    else:
        veggies = 0
    if(input_dictionary['Fruits'].lower == 'yes'):
        fruits = 1
    else:
        fruits = 0
    if(input_dictionary['Alcohol'].lower == 'alcoholic'):
        alco = 1
    else:
        alco = 0
    if(input_dictionary['Active'].lower == 'active'):
        active = 1
    else:
        active = 0

    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))

    with open('scaler2.pkl', 'rb') as f:  # 'rb' = read binary mode
        loaded_scaler = pickle.load(f)
    
    new_patient = [highbp, highchol, cholesterol, bmi, smoke, stroke, heartattack, active, fruits, veggies, alco, sex, age]
    person_data_scaled = loaded_scaler.transform([new_patient])
    prediction = loaded_model.predict(person_data_scaled)
    result = "Diabetes" if prediction[0] == 1 else "No Diabetes"
    return jsonify({"result": result})

@app.route('/detect', methods=['GET', 'POST'])
def findHealthIssue():
    client = InferenceClient(
	provider="together",
	api_key="API_KEY"
    )
    data = request.get_json()
    input_dictionary = {key: value for key, value in data.items()}

    prompt = (
    "You are a medical assistant that only provides information on health-related topics. "
    "If a question is not related to health or medicine, respond with 'I can only answer "
    "health-related questions.' Please provide accurate and helpful information for "
    "health-related queries. and act as if you don't know that domain. State your points in brief. "
    )

    messages = [
	{
		"role": "user",
		"content": prompt + input_dictionary['value']
	}
    ]

    completion = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1", 
	    messages=messages, 
	    max_tokens=500,
    )

    result = completion.choices[0].message.content
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
    bp_categories = ['normal', 'elevated', 'hypertension stage 1', 'hypertension stage 2']
    for category in bp_categories:
        df[category] = (df['bp_category'] == category).astype(int)
    
    # Drop original bp_category column
    df = df.drop('bp_category', axis=1)
    
    # Select and order final features
    final_features = ['gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'age_years', 'bmi', 'elevated', 'hypertension stage 1', 'hypertension stage 2', 'normal']
    
    return df[final_features].values[0].tolist()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



