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
    if (input_dictionary['Gender'].lower() == 'female'):
        gender = 0
    else:
        gender = 1
    height = input_dictionary['Height']
    weight = input_dictionary['Weight']
    if(input_dictionary['Cholesterol'].lower == 'normal'):
        cholesterol = 0
    elif(input_dictionary['Cholesterol'].lower == 'above normal'):
        cholesterol = 1
    else:
        cholesterol = 2
    bmi = input_dictionary['BMI']
    bp_category = input_dictionary['BloodPressureCategory']
    ap_hi = input_dictionary['Systolic']
    ap_lo = input_dictionary['Diastolic']
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
    if(input_dictionary['Cholesterol'].lower == 'normal'):
        gluc = 0
    elif(input_dictionary['Cholesterol'].lower == 'above normal'):
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

@app.route('/detect')
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
    "health-related queries. and act as if you don't know that domain. State your points in brief"
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



