import requests
import re

def get_csrf_token():
    response = requests.get('https://pastebin.com/')
    csrf_token = re.search(r'<meta name="csrf-token" content="([^"]+)"', response.text)
    
    if csrf_token:
        return csrf_token.group(1)
    return None

if __name__ == "__main__":
    token = get_csrf_token()
    print(f"CSRF Token: {token}")