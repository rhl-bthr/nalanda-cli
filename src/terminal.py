#! /usr/bin/python
# Pro-Panda
# Termi-Nalanda

from __future__ import print_function
from bs4 import BeautifulSoup
import os, io, requests

import slides, notices

INSTALLATION_FOLDER = os.path.join(os.path.expanduser('~'), '.termi-nalanda')
def bold(text):
    return '\033[1m' + text + '\033[0m'

def login():
    session = requests.session()
    try:
        config = io.open(os.path.join(INSTALLATION_FOLDER, 'config.txt'), 'r')
    except IOError:
        quit("Unable to read from file. Please reinstall termi-Nalanda")
    config = (config.read()).split('\n')
    session.post('http://nalanda.bits-pilani.ac.in/login/index.php', data={
        'username': config[0],
        'password': config[1],
    })
    return config[2], session

# Updating Subject List and making folders
def subject_list_folders(slides_path):
    try:
        name_file = io.open(
        os.path.join(
            INSTALLATION_FOLDER,
            'Subjects','name.txt'),
        'r')
        url_file = io.open(os.path.join(INSTALLATION_FOLDER, 'Subjects','url.txt'), 'r')
    except IOError:
        quit("Unable to read from file. Please reinstall termi-Nalanda")
    url_list = (url_file.read()).split('\n')
    subject_list = (name_file.read()).split('\n')
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
    res_urls, news_urls, notice_urls = ([[] for x in range(len(subject_links))] for y in range(3))
    for x in range(len(subject_links)):
        for y in range(len(subject_links[x])):
            url = (subject_links[x][y]).get('href')
            if('resource/view.php?id' in url or 'folder/view.php?id=' in url):
                res_urls[x].append(url)
            elif('page/view.php?id' in url):
                notice_urls[x].append(
                    [url, subject_links[x][y].contents[1].contents[0]])
            elif('forum/view.php?id' in url):
                news_urls[x].append(url)
            #Needs to be worked upon and added at a later stage.
            # elif('/mod/' in url and 'id' in url and 'index' not in url):
            #     notice_urls[x].append([url, subject_links[x][y].contents])
    return notice_urls, news_urls, res_urls

def terminal_display(update_list=None,update_type=None,
        sub_names=[], message=None):
    print (bold(update_type+':'))
    check_for_no_update = sum([len(x) for x in update_list])
    if(check_for_no_update == 0):
        print ("\tNo new " + update_type)
        return 0
    if (message is None):
        for x in range(len(sub_names)):
            for y in range(len(update_list[x])):
                if(y == 0):
                    print (bold('\n'+sub_names[x] + '-'))
                print ('\t' + bold(str(y + 1))+'. ' + update_list[x][y][1])
                print ("\t\t" + update_list[x][y][0])
    else:
        for x in range(len(sub_names)):
            if(len(update_list[x]) != 0):
                print (bold(sub_names[x]) + message)
    print ('-' * 60 + '\n')
    
def main():
    """Displaying notices, news and other announcements, updating slides"""
    print ("\t\t" + bold("**Nalanda**"))
    slides_path, session = login()
    subject_names, subject_urls = subject_list_folders(slides_path)
    subject_links = get_all_links(subject_urls, session)
    notice_urls, news_urls, res_urls = sorting_links(subject_links)
    notices.main(session, subject_names, notice_urls, news_urls)
    slides.main(session, subject_names, res_urls, slides_path)

if(__name__ == '__main__'):
    main()