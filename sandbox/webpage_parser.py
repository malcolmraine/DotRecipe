import requests
from bs4 import BeautifulSoup

page = requests.get('https://tastesbetterfromscratch.com/pulled-pork/')  # Getting page HTML through request
soup = BeautifulSoup(page.content, 'html.parser')  # Parsing content using beautifulsoup

links = soup.select("table tbody tr td.titleColumn a")  # Selecting all of the anchors with titles
first10 = links[:10]  # Keep only the first 10 anchors
for anchor in first10:
    print(anchor.text)  # Display the innerText of each anchor