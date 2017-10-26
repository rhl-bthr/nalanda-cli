#! /usr/bin/python
# Pro-Panda
# Termi-Nalanda

from __future__ import print_function
import os, io
import requests
import slides
import notices
from bs4 import BeautifulSoup

INSTALLATION_FOLDER = os.path.join(os.path.expanduser('~'), '.termi-nalanda')

def login():
    session = requests.session()
    config = io.open(os.path.join(INSTALLATION_FOLDER, 'config.txt'), 'r')
    config = (config.read()).split('\n')
    session.post('http://nalanda.bits-pilani.ac.in/login/index.php', data={
        'username': config[0],
        'password': config[1],
    })
    return config[2], session

# Updating Subject List and making folders


def subject_list_folders(slides_path):
    name_file = io.open(
        os.path.join(
            INSTALLATION_FOLDER,
            'Subjects/name.txt'),
        'r')
    subject_list = (name_file.read()).split('\n')
    url_file = io.open(os.path.join(INSTALLATION_FOLDER, 'Subjects/url.txt'), 'r')
    url_list = (url_file.read()).split('\n')
    for subject in subject_list:
        subject_path = os.path.join(slides_path, subject)
        if not os.path.exists(subject_path):
            os.makedirs(subject_path)
    return subject_list, url_list

# Getting all relevant links in each subject page
def get_all_links(subject_urls, session):
    subject_links = []
    for subj in subject_urls:
        result = session.get(subj)
        soup = BeautifulSoup(result.text, "html.parser")
        subject_links.append(soup.find_all('a', {'onclick': ""}))
    return subject_links

# Sorting Urls
def sorting_links(subject_links):
    resource_urls = [[] for x in range(len(subject_links))]
    news_urls = [[] for x in range(len(subject_links))]
    notice_urls = [[] for x in range(len(subject_links))]
    for x in range(len(subject_links)):
        for y in range(len(subject_links[x])):
            url = (subject_links[x][y]).get('href')
            if('resource/view.php?id' in url or 'folder/view.php?id=' in url):
                resource_urls[x].append(url)
            elif('page/view.php?id' in url):
                notice_urls[x].append(
                    [url, subject_links[x][y].contents[1].contents[0]])
            elif('forum/view.php?id' in url):
                news_urls[x].append(url)
            # elif('/mod/' in url and 'id' in url and 'index' not in url):
            #     notice_urls[x].append([url, subject_links[x][y].contents])
    return notice_urls, news_urls, resource_urls


def main():
    """Displaying notices, news and other announcements, updating slides"""
    print ("\t\t" + notices.bold("**Nalanda**"))
    slides_path, session = login()
    subject_names, subject_urls = subject_list_folders(slides_path)
    subject_links = get_all_links(subject_urls, session)
    notice_urls, news_urls, resource_urls = sorting_links(subject_links)
    notices.main(session, subject_names, notice_urls, news_urls)
    slides.main(session, subject_names, resource_urls, slides_path)

if(__name__ == '__main__'):
    main()