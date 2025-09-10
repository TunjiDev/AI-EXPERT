import requests
from config import HF_API_KEY, API_URL  # Keep keys safe in config.py

# ============================================
# 🚀 Sentiment Analysis Tool with Hugging Face
# ============================================

# Hugging Face API URL (sentiment model)
api_url = f"{API_URL}"

# Authorization headers
headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

# 🎬 Try out different sentences here!
sample_texts = [
    "I love this movie! It was fantastic.",
    "This product is the worst thing I’ve ever bought.",
    "Hmm… I’m not sure how I feel about this."
]

# Function to analyze sentiment
def analyze_sentiment(text: str):
    """Send text to Hugging Face API and return sentiment predictions."""
    response = requests.post(api_url, headers=headers, json={"inputs": text})

    if response.status_code == 200:
        result = response.json()
        print(f"\n🔎 Analyzing: \"{text}\"")
        print("📊 Results:")
        for item in result[0]:
            label = item["label"]
            score = item["score"]
            print(f"  - {label}: {score:.4f}")
    else:
        print(f"\n⚠️ Error {response.status_code}: {response.text}")


# Run sentiment analysis on all sample texts
if __name__ == "__main__":
    print("=== Sentiment Analysis Tool ===")
    for text in sample_texts:
        analyze_sentiment(text)
    print("\n✅ Analysis complete! Try adding your own sentences.")
