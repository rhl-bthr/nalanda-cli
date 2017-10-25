from __future__ import print_function
import os
from bs4 import BeautifulSoup
import io

import terminal


def bold(text):
    return '\033[1m' + text + '\033[0m'

def get_news(session, sub_names, news_urls):
    subject_news_url = [[] for x in range(len(sub_names))]
    for x in range(len(sub_names)):
        for y in range(len(news_urls[x])):
            result = session.get(news_urls[x][y])
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


def terminal_display(
        urls_title=None,
        update_type=None,
        sub_names=[],
        message=None,
        message_subject=[]):
    print bold(update_type+':')
    if (urls_title is not None):
        check_for_no_update = sum([len(x) for x in urls_title])
        if(check_for_no_update == 0):
            print "\tNo new " + update_type
        for x in range(len(sub_names)):
            for y in range(len(urls_title[x])):
                if(y == 0):
                    print bold('\n'+sub_names[x] + '-')
                print '\t' + bold(str(y + 1))+'. ' + str(urls_title[x][y][1])
                print "\t\t" + urls_title[x][y][0]
    else:
        if (sum(message_subject) == 0):
            print "\tNo new " + update_type
        for x in range(len(sub_names)):
            if(message_subject[x] != 0):
                print bold(sub_names[x]) + message
    print ('-' * 60 + '\n')


def find_new(session, sub_names, urls_title, update_type):
    new_urls_title = [[]for x in range(len(sub_names))]
    for x in range(len(sub_names)):
        subject_file = io.open(
            os.path.join(
                terminal.INSTALLATION_FOLDER,
                update_type,
                sub_names[x]),
            'a+')
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
    terminal_display(unread_notice_urls_title, 'Notices', sub_names)
    subject_news_url = get_news(session, sub_names, news_urls)
    unread_news_urls_title = find_new(
        session, sub_names, subject_news_url, 'News')
    terminal_display(unread_news_urls_title, 'News', sub_names)
