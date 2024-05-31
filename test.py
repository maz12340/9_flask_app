import requests

# URL веб-сервера
url = 'https://localhost:5000'

# Путь к нашему самоподписанному SSL-сертификату
ssl_cert = 'ssl_cert/cert.pem'

# Отключаем проверку SSL-сертификата (только для тестирования!)
requests.packages.urllib3.disable_warnings()

# Отправка GET-запроса на главную страницу
response = requests.get(url, verify=ssl_cert)
print(response.text)
