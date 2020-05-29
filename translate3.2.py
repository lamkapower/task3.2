import requests
import os

API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
URL_DETECT = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
AUTH_TOKEN = 'OAuth AgAAAAAMJHsPAADLWwiDAXCweUwDiCWuIShzcQo'
UPLOADFILE_URL = 'https://cloud-api.yandex.net/v1/disk/resources/upload'


def translate_file(infolder, outfolder, tolang='ru'):
    list_files = os.listdir(infolder)
    for file in list_files:
        with open(os.path.join(infolder, file), 'r', encoding='utf-8') as fi:
            data = fi.read()
            params = {
                'key': API_KEY,
                'text': data
            }
            response = requests.post(URL_DETECT, params=params)
            json_response = response.json()
            lang = json_response['lang']
            translate_params = {
                'key': API_KEY,
                'text': data,
                'lang': f'{lang}-{tolang}'
            }
            response = requests.post(URL, params=translate_params)
            json_ = response.json()
            string_text = ''.join(json_['text'])
        with open(os.path.join(outfolder, f'translated-{lang}-to-{tolang}-{file}') , 'w', encoding='utf-8') as fo:
            fo.write(string_text)


def upload_file(outfolder):
    upload_files_list = os.listdir(outfolder)
    for up_file in upload_files_list:
        payload = {}
        params = {
            'path': up_file,
            'overwrite': 'true'
        }
        headers = {
            'Authorization': AUTH_TOKEN
        }

        response = requests.get(UPLOADFILE_URL , params=params, headers=headers, data=payload)
        upload_link = response.json()['href']
        requests.put(upload_link, data=open(os.path.join(outfolder, up_file), 'rb'))


if __name__ == '__main__':
    translate_file('input' , 'output', 'pl')
    upload_file('output')