import requests

headers = {
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
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

data = '------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="_csrf-frontend"\n\n2htdll08ohkJfH4RRKyRF90o_C5rCpDAfJpjNVW7vB-fKWrEE0XQcmMySFd91t4gsmK5Tzte3fIZ8DdHHdnQcA==\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[text]"\n\nsex\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[category_id]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[tag]"\n\n\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[format]"\n\n1\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[expiration]"\n\nN\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[status]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[is_password_enabled]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[is_burn]"\n\n0\n------WebKitFormBoundaryum79Hhy32iHTcq62\nContent-Disposition: form-data; name="PostForm[name]"\n\n\n------WebKitFormBoundaryum79Hhy32iHTcq62--\n'

response = requests.post('https://pastebin.com/', headers=headers, data=data)

print(response.headers)
print(response.text)
print(response.status_code)
