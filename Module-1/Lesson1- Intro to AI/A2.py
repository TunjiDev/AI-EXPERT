print("Hello! I'm your friendly chatbot.")
name = input("What's your name? ")
print(f"\nNice to meet you, {name}!\n")
feeling = input("How are you feeling today? ")
if "good" in feeling.lower() or "great" in feeling.lower():
    print("\nI'm glad to hear that!\n")
else:
    print("\nI hope your day gets better!\n")

hobby = input("What's your favorite hobby? ")
print(f"\nWow, {hobby} sounds fun!\n")