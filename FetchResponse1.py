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
        result = "Diabetes" if prediction['result'] == 1 else "No Diabetes"
        
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
    api_url = "http://192.168.11.248:5000/predictDiabetes"
    
    json_data = {
        'BloodPressure' : 'Yes',
        'HeartAttack' : 'No',
        'Age' : 168.0,
        'Gender' : 'Female',
        'HighCholesterol' : 'Yes',
        'Stroke' : 'past history',
        'CholesterolCheck' : "Within 1 year",
        'BMI' : 110,
        'Veggies' : 'No',
        'Fruits' : 'Yes',
        'Alcohol' : 'Alcoholic',
        'Active' : 'Active',
        'Smoke' : 'Non Smoker'
    }
    
    response = send_api_request(api_url, json_data)
    
    if response is not None:
        print("Response received: " + response['prediction'])     # Pretty print the JSON response
    else:
        print("Failed to get response")
