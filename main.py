import tls_client 
import random
import time
import re
import toml
import ctypes
import threading

import os

from Solver.Challenge import CloudflareSolver
from concurrent.futures import ThreadPoolExecutor, as_completed

from functools import wraps
from logmagix import Logger, Home

with open('input/config.toml') as f:
    config = toml.load(f)

DEBUG = config['dev'].get('Debug', False)
log = Logger()

def debug(func_or_message, *args, **kwargs) -> callable:
    if callable(func_or_message):
        @wraps(func_or_message)
        def wrapper(*args, **kwargs):
            result = func_or_message(*args, **kwargs)
            if DEBUG:
                log.debug(f"{func_or_message.__name__} returned: {result}")
            return result
        return wrapper
    else:
        if DEBUG:
            log.debug(f"Debug: {func_or_message}")

def debug_response(response) -> None:
    debug(response.headers)
    debug(response.text)
    debug(response.status_code)

class Miscellaneous:
    @debug
    def get_proxies(self) -> dict:
        try:
            if config['dev'].get('Proxyless', False):
                return None
                
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    log.warning("No proxies available. Running in proxyless mode.")
                    return None
                
                proxy_choice = random.choice(proxies)
        
                proxy_dict = {
                    "http": f"http://{proxy_choice}",
                    "https": f"http://{proxy_choice}"
                }
                    
                debug(f"Using proxy: {proxy_choice}")
                return proxy_dict
        except FileNotFoundError:
            log.failure("Proxy file not found. Running in proxyless mode.")
            return None
    
    @debug 
    def randomize_user_agent(self) -> str:
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Linux i686",
            "X11; Ubuntu; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
            ("Firefox", f"{random.randint(80, 115)}.0"),
            ("Safari", f"{random.randint(13, 16)}.{random.randint(0, 3)}"),
            ("Edge", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
        ]
        
        webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 99)}"
        platform = random.choice(platforms)
        browser_name, browser_version = random.choice(browsers)
        
        if browser_name == "Safari":
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"Version/{browser_version} Safari/{webkit_version}"
            )
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({platform}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        else:
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"{browser_name}/{browser_version} Safari/{webkit_version}"
            )
        
        return user_agent

    @debug
    def solve_challenge(self, url: str, user_agent: str, proxies: dict = None) -> tuple[str, str]:
        debug("Solving Captcha Challenge")
        
        playwright_proxy = None
        if proxies and not config['dev'].get('Proxyless', False):
            proxy_str = proxies.get('http') or proxies.get('https')
            if proxy_str:
                # Convert http://user:pass@host:port format to Playwright format
                proxy_parts = re.match(r'http://(?:(.+):(.+)@)?(.+):(\d+)', proxy_str)
                if proxy_parts:
                    username, password, host, port = proxy_parts.groups()
                    playwright_proxy = {
                        "server": f"http://{host}:{port}",
                    }
                    if username and password:
                        playwright_proxy.update({
                            "username": username,
                            "password": password
                        })
                    debug(f"Using proxy for Playwright: {host}:{port}")
        
        with CloudflareSolver(
            user_agent=user_agent,
            timeout=30,
            http2=True,
            http3=True,
            headless=True,
            proxy=playwright_proxy
        ) as solver:
            solver.page.goto(url)
            clearance_cookie = solver.extract_clearance_cookie(solver.cookies)
            
            if clearance_cookie is None:
                solver.solve_challenge()
                clearance_cookie = solver.extract_clearance_cookie(solver.cookies)
                
            if clearance_cookie:
                return clearance_cookie["value"].replace("cf_clearance=", "")
            return None
    
    class Title:
        def __init__(self) -> None:
            self.running = False

        def start_title_updates(self, total, start_time) -> None:
            self.running = True
            def updater():
                while self.running:
                    self.update_title(total, start_time)
                    time.sleep(0.5)
            threading.Thread(target=updater, daemon=True).start()

        def stop_title_updates(self) -> None:
            self.running = False

        def update_title(self, total, start_time) -> None:
            try:
                elapsed_time = round(time.time() - start_time, 2)
                title = f'discord.cyberious.xyz | Total: {total} | Time Elapsed: {elapsed_time}s'

                sanitized_title = ''.join(c if c.isprintable() else '?' for c in title)
                ctypes.windll.kernel32.SetConsoleTitleW(sanitized_title)
            except Exception as e:
                log.debug(f"Failed to update console title: {e}")

class AccountCreator:
    def __init__(self, proxies: dict = None) -> None:
        self.session = tls_client.Session("chrome_131", random_tls_extension_order=True)
        
        self.session.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'connection': 'keep-alive',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryum79Hhy32iHTcq62',
            'host': 'pastebin.com',
            'origin': 'https://pastebin.com',
            'referer': 'https://pastebin.com/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': Miscellaneous().randomize_user_agent(),
        }
        self.session.proxies = proxies
        
    def get_csrf_token(self) -> str | None:
        debug("Getting csfr token")
        debug(f"Using headers: {self.session.headers}")

        response = self.session.get('https://pastebin.com/')
        
        debug_response(response)

        csrf_token = re.search(r'<meta name="csrf-token" content="([^"]+)"', response.text)
        
        if response.status_code == 200:
            if csrf_token:
                return csrf_token.group(1)
            return None
        elif response.status_code == 403:
            log.warning("Cloudflare challenge detected, solving captcha and retrying...")
            
            start = time.time()
            clearance = Miscellaneous().solve_challenge('https://pastebin.com/', self.session.headers['user-agent'], self.session.proxies)
            log.message('Cloudflare', f"Successfully solved captcha: {clearance[:40]}...", start, time.time())
            
            if clearance:
                self.session.cookies.update({'cf_clearance': clearance})
                return self.get_csrf_token()
            else:
                log.failure("Failed to solve Cloudflare challenge")
                return None
        else:
            log.failure(f"Failed to get CSRF token. Status code: {response.status_code}")

    def post(self, csfr_token: str, content: str, title: str) -> str | None:
        debug("Posting content")
        debug(f"Using headers: {self.session.headers}")

        data = f'------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="_csrf-frontend"\n\n{csfr_token}\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[text]"\n\n{content}\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[category_id]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[tag]"\n\n\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[format]"\n\n1\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[expiration]"\n\nN\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[status]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[is_password_enabled]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[is_burn]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[name]"\n\n{title}\n------WebKitFormBoundaryum79Hhy32iHTcq62--\n'

        response = self.session.post('https://pastebin.com/', data=data)
        
        debug_response(response)
        
        if response.status_code == 302:
            return response.headers['Location']
        else:
            if "You have reached your guest paste limit of 10 pastes per 24 hours" in response.text:
                log.warning("Guest paste limit exceeded (10 pastes/24h). Try using a different proxy.")
            else:
                log.failure(f"Failed to post content. If you are not using proxies these are rate limits (200). Status code: {response.status_code}")
            
@debug
def load_file_content(filepath: str) -> list:
    try:
        with open(filepath, encoding='utf-8') as f:
            content = [line.strip() for line in f if line.strip()]
        return content
    
    except UnicodeDecodeError:
        log.failure(f"Failed to decode {filepath}. Please ensure it's UTF-8 encoded.")
    except PermissionError:
        log.failure(f"Permission denied when accessing {filepath}")
    except Exception as e:
        log.failure(f"Error reading {filepath}: {str(e)}")
    return []

class Content:
    def __init__(self) -> None:
        self.content_list = []  # Will now store tuples of (content, title)
        self.content_lock = threading.Lock()
        self._load_content()
    
    @debug
    def _load_content(self) -> None:
        content_file = 'input/content.txt'
        if os.path.exists(content_file):
            with open(content_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    # For content.txt, store content with empty title
                    for block in content.split('\n\n'):
                        if block.strip():
                            self.content_list.append((block.strip(), ""))
                if self.content_list:
                    log.info(f"Loaded {len(self.content_list)} entries from content.txt")
                    return

        content_dir = 'input/Content'
        if os.path.exists(content_dir):
            try:
                files = [f for f in os.listdir(content_dir) 
                        if os.path.isfile(os.path.join(content_dir, f))]
                
                for file in files:
                    filepath = os.path.join(content_dir, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read().strip()
                            if content:
                                title = os.path.splitext(file)[0]  # Get filename without extension
                                self.content_list.append((content, title))
                                debug(f"Loaded content from {file}")
                    except Exception as e:
                        log.failure(f"Failed to load {file}: {str(e)}")
                
                if self.content_list:
                    log.info(f"Loaded content from {len(files)} files in Content directory")
                    return
            except Exception as e:
                log.failure(f"Error accessing Content directory: {str(e)}")
        
        log.warning("No content found in content.txt or Content directory!")

    @debug
    def get_random_content(self) -> tuple[str, str] | None:
        with self.content_lock:
            try:
                if self.content_list:
                    return random.choice(self.content_list)
                log.failure("No content available to post")
                return None
            except Exception as e:
                log.failure(f"Error getting random content: {str(e)}")
                return None

def post_content(content_manager: Content) -> bool:
    while True:
        try:
            start = time.time()
            
            content_tuple = content_manager.get_random_content()
            if not content_tuple:
                return
            
            content, title = content_tuple
            proxies = Miscellaneous().get_proxies()
            account_creator = AccountCreator(proxies)
            csrf_token = account_creator.get_csrf_token()
            
            if not csrf_token:
                log.failure("Failed to obtain CSRF token")
                return
                
            response = account_creator.post(csrf_token, content, title)
            
            if response:
                log.message(f"Pastebin", f"Posted content. URL: {response}", start, time.time())
                
                with open("output/links.txt", "a") as f:
                    f.write(f"{response}\n")
            
        except Exception as e:
            log.failure(f"Error in post_content: {str(e)}")

def main() -> None:
    try:
        start_time = time.time()
        
        # Initialize basic classes
        Misc = Miscellaneous()
        Banner = Home("Pastebin Poster", align="center", credits="discord.cyberious.xyz")
        content_manager = Content()
        
        # Display Banner
        Banner.display()

        if not content_manager.content_list:
            log.failure("No content available to post. Exiting...")
            return

        total = 0
        thread_count = config['dev'].get('Threads', 1)

        # Start updating the title
        title_updater = Misc.Title()
        title_updater.start_title_updates(total, start_time)
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
                try:
                    futures = [
                        executor.submit(post_content, content_manager)
                        for _ in range(thread_count)
                    ]

                    for future in as_completed(futures):
                        try:
                            if future.result():
                                total += 1
                        except Exception as e:
                            log.failure(f"Thread execution error: {str(e)}")
                except Exception as e:
                    log.failure(f"Thread pool error: {str(e)}")

    except KeyboardInterrupt:
        log.info("Process interrupted by user. Exiting...")
        title_updater.stop_title_updates()
    except Exception as e:
        log.failure(f"Critical error: {str(e)}")
    finally:
        title_updater.stop_title_updates()

if __name__ == "__main__":
    main()