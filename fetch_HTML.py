from bs4 import BeautifulSoup
import requests

page = requests.get("https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage")
soup = BeautifulSoup(page.content, 'html.parser')

with open('HTML_content.txt', 'w') as f:
    f.write(soup.prettify())
