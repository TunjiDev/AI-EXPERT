# ============================ PART 1 ============================
from config import HF_API_KEY
import requests, base64, os, re, time
from PIL import Image
from colorama import init, Fore, Style

init(autoreset=True)

ROUTER_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

VISION_MODELS = [
    "moonshotai/Kimi-K2.6:novita",                              
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct:sambanova",
    "meta-llama/Llama-3.2-11B-Vision-Instruct:sambanova",
]
TEXT_MODELS = [
    "Qwen/Qwen2.5-7B-Instruct:together",
    "Qwen/Qwen2.5-14B-Instruct:together",
    "Qwen/Qwen2.5-32B-Instruct:together",
    "mistralai/Mistral-7B-Instruct-v0.3:together",
    "mistralai/Mixtral-8x7B-Instruct-v0.1:together",
    "meta-llama/Llama-3-8B-Instruct",
    "MiniMaxAI/MiniMax-M1-80k",
]

def _data_url(path: str) -> str:
    with open(path, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode("utf-8")

def query_hf_api(payload: dict):
    try:
        r = requests.post(ROUTER_URL, headers=HEADERS, json=payload, timeout=120)
    except requests.RequestException as e:
        return None, f"Request failed: {e}"
    if r.status_code != 200:
        try:
            j = r.json()
            msg = j.get("error", {}).get("message") or str(j)
        except Exception:
            msg = (r.text or "").strip() or r.reason or "Request failed."
        return None, f"Status {r.status_code}: {msg}"
    try:
        return r.json(), None
    except Exception:
        return None, "Non-JSON response received from the API."

def _extract_text(data) -> str:
    msg = (data or {}).get("choices", [{}])[0].get("message", {}) or {}
    return (msg.get("content") or "").strip()

def _run_models(models, messages, max_tokens=160, temperature=0.3):
    last_err = None
    for model in models:
        data, err = query_hf_api({"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature})
        if err:
            last_err = err
            continue
        out = _extract_text(data)
        if out:
            return out, None
        last_err = "Empty response from model."
    return None, last_err or "All models failed."

def _words(text: str):
    return re.findall(r"\S+", (text or "").strip())

def _exact_n_words(text: str, n: int) -> str:
    return " ".join(_words(text)[:n])

def _ensure_sentence_end(text: str) -> str:
    t = (text or "").strip()
    if t and t[-1] not in ".!?":
        t += "."
    return t

# ============================ PART 2 (PASTE INTO PART 1) ============================
# Paste this block by REPLACING the two stub functions in Part 1:
# - generate_text(...)
# - generate_exact_sentence(...)


def generate_text(prompt: str, max_new_tokens: int = 220) -> str:
    raise Exception("Part 2 code not added")

def generate_exact_sentence(prompt: str, n_words: int, max_new_tokens: int, tries: int = 6) -> str:
    raise Exception("Part 2 code not added")


# ============================ PART 2 (PASTE INTO PART 1) ============================

def get_basic_caption(image_path: str) -> str:
    print(f"{Fore.YELLOW}🖼️ Generating basic caption ...")
    msgs = [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Write one complete sentence describing this image."},
            {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
        ],
    }]
    cap, err = _run_models(VISION_MODELS, msgs, max_tokens=90, temperature=0.2)
    return cap if cap else f"[Error] {err}"

def print_menu():
    print(f"""{Style.BRIGHT}{Fore.GREEN}
================ Image-to-Text Conversion =================
Select output type:
1. Caption (5 words)
2. Description (30 words)
3. Summary (50 words)
4. Exit
=============================================================
""")

def main():
    image_path = input(f"{Fore.BLUE}Enter the path of the image (e.g., test.jpg): {Style.RESET_ALL}")
    if not os.path.exists(image_path):
        print(f"{Fore.RED}❌ The file '{image_path}' does not exist.")
        return
    try:
        Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to open image: {e}")
        return

    basic_caption = get_basic_caption(image_path)
    print(f"{Fore.YELLOW}📝 Basic caption: {Style.BRIGHT}{basic_caption}\n")

    while True:
        print_menu()
        choice = input(f"{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}").strip()

        if basic_caption.startswith("[Error]") and choice in {"1", "2", "3"}:
            basic_caption = get_basic_caption(image_path)
            print(f"{Fore.YELLOW}📝 Basic caption: {Style.BRIGHT}{basic_caption}\n")

        if choice == "1":
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Caption (5 words): {Style.BRIGHT}{basic_caption}\n")
            else:
                out = _ensure_sentence_end(_exact_n_words(basic_caption, 5))
                print(f"{Fore.GREEN}✅ Caption (5 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")

        elif choice == "2":
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate description: {basic_caption}")
                continue
            prompt = ("Rewrite as EXACTLY 30 words. Single paragraph. One complete sentence. "
                      "End with a period. No title/bullets.\n\nText: " + basic_caption)
            try:
                out = generate_exact_sentence(prompt, 30, max_new_tokens=220, tries=6)
                print(f"{Fore.GREEN}✅ Description (30 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to generate description: {e}")

        elif choice == "3":
            if basic_caption.startswith("[Error]"):
                print(f"{Fore.RED}❌ Failed to generate summary: {basic_caption}")
                continue
            prompt = ("Write EXACTLY 50 words. Single paragraph. One complete sentence. "
                      "End with a period. No title/bullets/extra text.\n\nImage seed: " + basic_caption)
            try:
                out = generate_exact_sentence(prompt, 50, max_new_tokens=280, tries=7)
                print(f"{Fore.GREEN}✅ Summary (50 words): {Fore.YELLOW}{Style.BRIGHT}{out}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Failed to generate summary: {e}")

        elif choice == "4":
            print(f"{Fore.GREEN}👋 Goodbye!")
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()



# import base64, requests
# from config import HF_API_KEY

# API_URL = "https://router.huggingface.co/v1/chat/completions"
# HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}
# MODELS = [
#     "zai-org/GLM-4.5V",
#     "Qwen/Qwen2.5-VL-72B-Instruct",
#     "Qwen/Qwen2.5-VL-32B-Instruct",
#     "google/gemma-3-27b-it",
# ]

# def data_url(b: bytes) -> str:
#     return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")

# def extract_err(r: requests.Response) -> str:
#     try:
#         j = r.json()
#         return j.get("error", {}).get("message") or str(j)
#     except Exception:
#         return (r.text or "").strip() or r.reason or "Request failed."

# def box(title: str, lines: list[str], icon: str):
#     w = max(30, len(title) + 4, *(len(x) for x in lines))
#     print("\n" + "┏" + "━" * (w + 2) + "┓")
#     print(f"┃ {icon} {title.ljust(w - 2)} ┃")
#     print("┣" + "━" * (w + 2) + "┫")
#     for x in lines:
#         print(f"┃ {x.ljust(w)} ┃")
#     print("┗" + "━" * (w + 2) + "┛\n")

# def caption_single_image():
#     image_source = input("🖼️ Enter image filename (default: test.jpg): ").strip() or "test.jpg"
#     try:
#         with open(image_source, "rb") as f:
#             img = f.read()
#     except Exception as e:
#         box("File Error", [f"Could not load: {image_source}", f"Reason: {e}"], "❌")
#         return

#     base = {
#         "messages": [{
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Give a short caption for this image."},
#                 {"type": "image_url", "image_url": {"url": data_url(img)}},
#             ],
#         }],
#         "max_tokens": 60,
#         "temperature": 0.2,
#     }

#     last = None
#     for model in MODELS:
#         payload = dict(base, model=model)
#         try:
#             r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
#         except requests.RequestException as e:
#             last = f"Request failed: {e}"
#             continue

#         if r.status_code != 200:
#             last = extract_err(r)
#             continue

#         try:
#             d = r.json()
#         except Exception:
#             last = "Non-JSON response received from the API."
#             continue

#         cap = (d.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
#         if cap:
#             box("Image Caption Generated", [
#                 f"🖼️ Image  : {image_source}",
#                 "📝 Caption:",
#                 f"   {cap}",
#             ], "🎉")
#             return
#         last = "No caption found."

#     box("Caption Failed", [f"🖼️ Image  : {image_source}", f"❌ Error : {last or 'Unknown error'}"], "⚠️")

# def main():
#     caption_single_image()

# if __name__ == "__main__":
#     main()


# from config import HF_API_KEY
# import requests
# from PIL import Image
# import io
# import os
# from colorama import init, Fore, Style
# import json

# # Initialize Colorama for colorful output
# init(autoreset=True)

# # -------------------------------------------------------------------------------
# # Utility function to send API requests
# # -------------------------------------------------------------------------------
# def query_hf_api(api_url, payload=None, files=None, method="post"):
#     headers = {"Authorization": f"Bearer {HF_API_KEY}"}
#     try:
#         if method.lower() == "post":
#             # When files provided, send them along with the payload.
#             response = requests.post(api_url, headers=headers, json=payload, files=files)
#         else:
#             response = requests.get(api_url, headers=headers, params=payload)
#         if response.status_code != 200:
#             raise Exception(f"Status {response.status_code}: {response.text}")
#         return response.content
#     except Exception as e:
#         print(f"{Fore.RED}❌ Error while calling API: {e}")
#         raise

# # -------------------------------------------------------------------------------
# # Task: Get a basic caption from an image using an image captioning model.
# # -------------------------------------------------------------------------------
# def get_basic_caption(image, model="nlpconnect/vit-gpt2-image-captioning"):
#     print(f"{Fore.YELLOW}???? Generating basic caption using vit-gpt2-image-captioning ...")
#     api_url = f"https://api-inference.huggingface.co/models/{model}"
#     buffered = io.BytesIO()
#     # Save as JPEG (this model works well with JPEG images)
#     image.save(buffered, format="JPEG")
#     buffered.seek(0)
#     headers = {"Authorization": f"Bearer {HF_API_KEY}"}
#     response = requests.post(api_url, headers=headers, data=buffered.read())
#     result = response.json()
#     if isinstance(result, dict) and "error" in result:
#         return f"[Error] {result['error']}"
#     # Expecting result to be a list of dicts with 'generated_text'
#     caption = result[0].get("generated_text", "No caption generated.")
#     return caption

# # -------------------------------------------------------------------------------
# # Task: Generate text using a text generation model (e.g. GPT-2)
# # -------------------------------------------------------------------------------
# def generate_text(prompt, model="gpt2", max_new_tokens=60):
#     print(f"{Fore.CYAN}???? Generating text with prompt: {prompt}")
#     api_url = f"https://api-inference.huggingface.co/models/{model}"
#     payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_new_tokens}}
#     text_bytes = query_hf_api(api_url, payload=payload)
#     try:
#         result = json.loads(text_bytes.decode("utf-8"))
#     except Exception as e:
#         raise Exception("Failed to decode text generation response.")
#     if isinstance(result, dict) and "error" in result:
#         raise Exception(result["error"])
#     generated = result[0].get("generated_text", "")
#     return generated

# # -------------------------------------------------------------------------------
# # Helper: Truncate text to a specific word count.
# # -------------------------------------------------------------------------------
# def truncate_text(text, word_limit):
#     words = text.strip().split()
#     return " ".join(words[:word_limit])

# # -------------------------------------------------------------------------------
# # Interactive menu for image-to-text output
# # -------------------------------------------------------------------------------
# def print_menu():
#     print(f"""{Style.BRIGHT}
# {Fore.GREEN}================ Image-to-Text Conversion =================
# Select output type:
# 1. Caption (5 words)
# 2. Description (30 words)
# 3. Summary (50 words)
# 4. Exit
# ===========================================================
# """)

# def main():
#     image_path = input(f"{Fore.BLUE}Enter the path of the image for text generation (e.g., test.jpg): {Style.RESET_ALL}")
#     if not os.path.exists(image_path):
#         print(f"{Fore.RED}❌ The file '{image_path}' does not exist.")
#         return
    
#     try:
#         image = Image.open(image_path)
#     except Exception as e:
#         print(f"{Fore.RED}❌ Failed to open image: {e}")
#         return
    
#     # Get a basic caption from the image
#     basic_caption = get_basic_caption(image)
#     print(f"{Fore.YELLOW}???? Basic caption: {Style.BRIGHT}{basic_caption}\n")
    
#     while True:
#         print_menu()
#         choice = input(f"{Fore.CYAN}Enter your choice (1-4): {Style.RESET_ALL}")
#         if choice == "1":
#             # Caption: take first 5 words from basic caption
#             caption = truncate_text(basic_caption, 5)
#             print(f"{Fore.GREEN}✅ Caption (5 words): {Style.BRIGHT}{caption}\n")
#         elif choice == "2":
#             # Description: expand basic caption to a 30-word description using GPT-2.
#             prompt_text = f"Expand the following caption into a detailed description in exactly 30 words: {basic_caption}"
#             try:
#                 generated = generate_text(prompt_text, max_new_tokens=40)
#                 description = truncate_text(generated, 30)
#                 print(f"{Fore.GREEN}✅ Description (30 words): {Style.BRIGHT}{description}\n")
#             except Exception as e:
#                 print(f"{Fore.RED}❌ Failed to generate description: {e}")
#         elif choice == "3":
#             # Summary: expand basic caption to a summary in 50 words.
#             prompt_text = f"Summarize the content of the image described by this caption into a summary of exactly 50 words: {basic_caption}"
#             try:
#                 generated = generate_text(prompt_text, max_new_tokens=60)
#                 summary = truncate_text(generated, 50)
#                 print(f"{Fore.GREEN}✅ Summary (50 words): {Style.BRIGHT}{summary}\n")
#             except Exception as e:
#                 print(f"{Fore.RED}❌ Failed to generate summary: {e}")
#         elif choice == "4":
#             print(f"{Fore.GREEN}???? Goodbye!")
#             break
#         else:
#             print(f"{Fore.RED}❌ Invalid choice. Please enter a number between 1 and 4.")

# if __name__ == "__main__":
#     main()