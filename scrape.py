import requests
from bs4 import BeautifulSoup
import re
import json

def get_links_from_page(topic, page):
    topic_url = f'https://4programmers.net/Forum/{topic}/?page={page}'
    resp = requests.get(topic_url)
    r = re.findall(r'https:\\/\\/4programmers.net\\/Forum\\/' + topic + r'\\/[^"?]*', resp.text)
    return list(set(map(lambda x: x.replace('\\', ''), r)))

def get_post(link):
    link = link.replace('\\', '')
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, 'html.parser')
    content = soup.find('div', class_='post-content')
    return content.get_text().replace(';', '').replace('\n', ' ')

def save_links():
    links = {
        'Kariera': [],
        'Edukacja': []
    }
    for topic in ['Kariera', 'Edukacja']:
        for page in range(25):
            links[topic] = links[topic] + get_links_from_page(topic, page)
    
    with open('links.json', 'w') as outfile:
        json.dump(links, outfile, indent=2)


def fetch_contents():
    with open('links.json', 'r') as infile:
        links = json.load(infile)
    
    for topic in ['Kariera', 'Edukacja']:
        for link in links[topic]:
            content = get_post(link)
            with open('posts.csv', 'a') as outfile:
                print(topic, content, sep=';', file=outfile)


if __name__ == '__main__':
    fetch_contents()
