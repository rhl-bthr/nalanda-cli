from __future__ import print_function
import os, io
from bs4 import BeautifulSoup
import terminal

def get_news(session, sub_names, news_urls):
    subject_news_url = [[] for x in range(len(sub_names))]
    for x in range(len(sub_names)):
        for y in range(len(news_urls[x])):
            try:
                result = session.get(news_urls[x][y])
            except session.exceptions.ConnectionError:
                quit("No Internet Connection. Please retry")
            soup = BeautifulSoup(result.text, "html.parser")
            discussion_list = soup.find_all('tr', 'discussion')
            for url in discussion_list:
                if url.find('td', 'topic starter pinned'):
                    subject_news_url[x].append([url.contents[0].contents[1].get(
                        'href'), url.contents[0].contents[1].contents[0]])
                else:
                    subject_news_url[x].append([url.contents[0].contents[0].get(
                        'href'), url.contents[0].contents[0].contents[0]])
    return subject_news_url

def find_new(session, sub_names, urls_title, update_type):
    new_urls_title = [[]for x in range(len(sub_names))]
    for x in range(len(sub_names)):
        try:
            subject_file = io.open(
                os.path.join(
                    terminal.INSTALLATION_FOLDER,
                    update_type,
                    sub_names[x]),
                'a+')
        except IOError:
            quit("Unable to read from file. Please reinstall termi-Nalanda")
        subject_file.seek(0)
        subject_read = (subject_file.read()).split('\n')
        for y in range(len(urls_title[x])):
            if (urls_title[x][y][1] in subject_read):
                pass
            else:
                new_urls_title[x].append(urls_title[x][y])
                subject_file.write("\n"+urls_title[x][y][1])
    return new_urls_title

def main(session, sub_names, notice_urls, news_urls):
    unread_notice_urls_title = find_new(
        session, sub_names, notice_urls, 'Notices')
    terminal.terminal_display(unread_notice_urls_title, 'Notices', sub_names)
    subject_news_url = get_news(session, sub_names, news_urls)
    unread_news_urls_title = find_new(
        session, sub_names, subject_news_url, 'News')
    terminal.terminal_display(unread_news_urls_title, 'News', sub_names)