import requests
import time

API_URL = 'https://api.telegram.org/bot'
API_CATS_URL = 'https://api.thecatapi.com/v1/images/search'
API_DOGS_URL = 'https://random.dog/woof.json'
API_FOXES_URL = 'https://randomfox.ca/floof/'
BOT_TOKEN = 'token'
ERROR_TEXT = 'Здесь должна была быть картинка :('
err = 'Ты можешь выбрать между котом, лисой и собакой'

offset = -2
counter = 0
animal_response: requests.Response
animal_link: str
s = ''

while counter < 10000:
    print('attempt =', counter)
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if 'result' in updates and updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            s = result['message']['text']

            if s == '/dog' or s == 'dog':
                animal_response = requests.get(API_DOGS_URL)
                if animal_response.status_code == 200:
                    animal_link = animal_response.json()['url']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={animal_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

            elif s == '/fox' or s == 'fox':
                animal_response = requests.get(API_FOXES_URL)
                if animal_response.status_code == 200:
                    animal_link = animal_response.json()['image']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={animal_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

            elif s == '/cat' or s == 'cat':
                animal_response = requests.get(API_CATS_URL)
                if animal_response.status_code == 200:
                    animal_link = animal_response.json()[0]['url']
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={animal_link}')
                else:
                    requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')
                
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={err}')

    # time.sleep(1)
    counter += 1
