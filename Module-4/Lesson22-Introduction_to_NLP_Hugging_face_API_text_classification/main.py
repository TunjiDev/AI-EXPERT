import requests
from config import HF_API_KEY, API_URL  # Import your key safely from config.py

# Hugging Face API URL for emotion detection model
api_url = f"{API_URL}"

# Use the imported API key
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# Sample input
text = "I love this movie! It was fantastic."

# Send POST request
response = requests.post(api_url, headers=headers, json={"inputs": text})

if response.status_code == 200:
    result = response.json()
    print("Detected emotions:")
    for emotion in result[0]:  # result is a list of dicts
        label = emotion["label"]
        score = emotion["score"]
        print(f"{label}: {score:.4f}")
else:
    print(f"Error: {response.status_code}\nMessage: {response.text}")
