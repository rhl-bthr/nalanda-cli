from __future__ import print_function
import os
import io
import requests
from bs4 import BeautifulSoup

join = os.path.join
INSTALL_PATH = join(os.path.expanduser('~'), '.termi-nalanda')


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


def find_new(session, sub_names, urls_title, update_type):
    new_urls_title = [[]for x in range(len(sub_names))]
    for x in range(len(sub_names)):
        subject_file = io.open(
            os.path.join(
                INSTALL_PATH,
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
                subject_file.write("\n" + urls_title[x][y][1])
    return new_urls_title


def term_display(update_list=None, update_type=None,
                 sub_names=[], path=None):
    print (bold(update_type + ':'))
    no_update = sum([len(x) for x in update_list])
    if(no_update == 0):
        print ("\tNo new " + update_type)
        return 0
    if (update_type=="Lectures"):
        [print (bold(sub_names[x]) + " has new updates") for x in range(len(sub_names))
         if len(update_list[x]) != 0]
        print ("file://"+path)
    else:
        for x in range(len(sub_names)):
            for y in range(len(update_list[x])):
                if(y == 0):
                    print (bold('\n' + sub_names[x] + '-'))
                print ('\t' + bold(str(y + 1)) + '. ' + update_list[x][y][1])
                print ("\t\t" + update_list[x][y][0])
    print ('-' * 60 + '\n')


def download(session, sub_names, res_urls, path):
    sub_updates = [[] for x in sub_names]
    for x in range(len(sub_names)):
        done_slides_file = io.open(
            join(
                INSTALL_PATH,
                "Lectures",
                sub_names[x] +
                '.txt'),
            'a+')
        done_slides_file.seek(0)
        done_slides = done_slides_file.read().split('\n')
        for y in range(len(res_urls[x])):
            if (res_urls[x][y] not in done_slides):
                if ('folder/view' in res_urls[x][y]):
                    id_param = res_urls[x][y].split('php')[1]
                    result = session.get(
                        'http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php' + id_param)
                else:
                    result = session.get(res_urls[x][y])
                file_name = result.headers['content-disposition'].split('e="')[
                    1].split('"')[0]
                with io.open(join(path, sub_names[x], file_name), 'wb') as f:
                    f.write(result.content)
                done_slides_file.write(res_urls[x][y] + '\n')
                sub_updates[x].append([])
    return sub_updates


def main(session, sub_names, sorted_urls, path):
    notice_urls, news_urls, res_urls = sorted_urls
    print ("\t\t" + bold("**Nalanda**"))
    unread_update = find_new(
        session, sub_names, notice_urls, 'Notices')
    term_display(unread_update, 'Notices', sub_names)
    subject_news_url = get_news(session, sub_names, news_urls)
    unread_update = find_new(
        session, sub_names, subject_news_url, 'News')
    term_display(unread_update, 'News', sub_names)
    update_list = download(session, sub_names, res_urls, path)
    term_display(update_list, 'Lectures', sub_names, path)