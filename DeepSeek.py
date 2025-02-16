import requests

def send_api_request(url, data):
    headers = {
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        
        # Parse the JSON response
        prediction = response.json()

        result = prediction['result']
        
        return result
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    api_url = "http://192.168.11.248:5000/detect"
    
    json_data = {
        'value' : 'I have a headache in my fore head. Can you tell me the cause?'
    }
    
    response = send_api_request(api_url, json_data)
    
    if response is not None:
        print("Response received:", response)  # Print the response directly
    else:
        print("Failed to get response")
