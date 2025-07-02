import os
import tldextract
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from typing import Dict, AnyStr, Any
from .constants import URL, VIRUS_TOTAL_BASE_URL


def is_safe_url(url: AnyStr) -> bool:
    """
    Function to check if url is safe using Virus Total API
    :param url: url to check
    :return: bool value if url is safe
    """
    headers = {'x-apikey': os.environ.get('VIRUS_TOTAL_API_KEY'),
               'accept': 'application/json',
               'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(f'{VIRUS_TOTAL_BASE_URL}/urls', data={URL: url}, headers=headers)
    if response.status_code != 200:
        return False
    data = response.json()
    analysis_id = data['data']['id']
    result = requests.get(f'{VIRUS_TOTAL_BASE_URL}/analyses/{analysis_id}', headers=headers)
    analysis = result.json()
    stats = analysis['data']['attributes']['stats']
    return stats['malicious'] == 0 and stats['suspicious'] == 0


def extract_url_information(url: AnyStr) -> Dict[AnyStr, Any]:
    """
    Function to parse information from url
    :param url: url to parse
    :return: dict that contain domain name, protocol, title, urls of all images and number of stylesheets
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string.strip() if soup.title else ''
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
    stylesheets = len(soup.find_all('link', rel='stylesheet'))

    parsed_url = urlparse(url)
    extracted = tldextract.extract(url)

    domain_name = f'{extracted.domain}.{extracted.suffix}'
    protocol = parsed_url.scheme

    return {
        'domain_name': domain_name,
        'protocol': protocol,
        'title': title,
        'images': images,
        'stylesheets': stylesheets,
    }
