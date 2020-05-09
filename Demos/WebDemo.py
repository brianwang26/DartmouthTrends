from bs4 import BeautifulSoup
import requests

url = "https://tylergarrett.com/"
request = requests.get(url)
soup = BeautifulSoup(request.content, 'html.parser')

print(soup.prettify())

a = []
for text in soup.find_all('p'):
    b = text.get_text()
    a.append(b)
print(a)