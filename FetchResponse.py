import requests
import json

def send_api_request(url, data):
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Parse the JSON response
        prediction = response.json()
        
        # Create the result message based on the prediction
        result = 'Cardiovascular Disease detected' if prediction['result'] == 1 else 'No Cardiovascular Disease detected'
        
        # Create a JSON response
        json_response = {
            "prediction": prediction['result'],
        }
        
        return json_response
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    api_url = "http://127.0.0.1:5000/predict"
    
    json_data = {
        'Age' : 50,
        'Gender' : 1,
        'Height' : 168,
        'Weight' : 62.0,
        'Cholesterol' : 0,
        'BMI' : 21.967120,
        'BloodPressureCategory' : "bp_Hypertension Stage 1",
        'Systolic' : 110,
        'Diastolic' : 80,
        'Smoke' : 0,
        'Alcohol' : 0,
        'Active' : 1,
        'Glucose' : 0
    }
    
    response = send_api_request(api_url, json_data)
    
    if response is not None:
        print("Response received: " + response['prediction'])     # Pretty print the JSON response
    else:
        print("Failed to get response")
