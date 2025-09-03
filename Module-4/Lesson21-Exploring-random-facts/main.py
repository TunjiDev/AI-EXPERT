import requests

URL = "https://uselessfacts.jsph.pl/random.json?language=en"

def get_random_fact():
    try:
        resp = requests.get(URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        print(f"Did you know? {data.get('text', '').strip()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch fact: {e}")

def main():
    while True:
        cmd = input("Press Enter for a random fact, or type 'q' to quit: ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        get_random_fact()

if __name__ == "__main__":
    main()
