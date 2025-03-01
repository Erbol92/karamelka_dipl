import shutil
import requests
import json
from diplom.settings import MEDIA_ROOT
authorization_key = 'OTdkYzJhNWQtZDViZS00ZjliLTk2M2YtYTJlNzZkYzkyZTExOjI4YzRiZGFjLTkxNjItNDNkYS05OTkzLWRkNWIyY2VjZDcyOA=='

def get_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"


    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '970dacf9-bf23-4ec7-86a6-471482011afe',
        'Authorization': f'Basic {authorization_key}'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify='russian_trusted_root_ca.cer')

    TOKEN = response.json()['access_token']
    return TOKEN

def push_and_get_photo(text):
    TOKEN = get_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "system",
                "content": "сделай точный рисунок по описанию"
            },
            {
                "role": "user",
                "content": f"{text}"
            }
        ],
        "function_call": "auto"
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {TOKEN}'
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, verify='russian_trusted_root_ca.cer')
    print()
    data = response.json()

    # Извлекаем содержимое
    content = data['choices'][0]['message']['content']

    # Находим строку с img src
    start_index = content.find('src="') + len('src="')
    end_index = content.find('"', start_index)

    # Извлекаем значение
    image_id = content[start_index:end_index]

    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{image_id}/content"

    headers = {
        'Accept': 'application/jpg',
        'Authorization': f'Bearer {TOKEN}'
    }

    response = requests.request(
        "GET", url, headers=headers, stream=True, verify='russian_trusted_root_ca.cer')

    with open(f'{MEDIA_ROOT}/fl.jpg', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
        return out_file
