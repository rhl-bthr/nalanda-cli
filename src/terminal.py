#! /usr/bin/python
# Pro-Panda
# Termi-Nalanda

from __future__ import print_function
from bs4 import BeautifulSoup
import os
import io
import requests
import updates

join = os.path.join

INSTALL_PATH = join(os.path.expanduser("~"), ".termi-nalanda")


def login():
    session = requests.session()
    config = io.open(join(INSTALL_PATH, "config.txt"), "r")
    config = (config.read()).split("\n")
    session.post("http://nalanda.bits-pilani.ac.in/login/index.php", data={
        "username": config[0],
        "password": config[1],
    })
    return config[2], session


def sub_list_folders(slides_path):
    """Updating Subject List and making folders"""
    name_file = io.open(join(INSTALL_PATH, "Subjects", "name.txt"), "r")
    url_file = io.open(join(INSTALL_PATH, "Subjects", "url.txt"), "r")
    url_list = (url_file.read()).split("\n")
    sub_list = (name_file.read()).split("\n")
    for sub in sub_list:
        sub_path = join(slides_path, sub)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)
    return sub_list, url_list


def get_all_links(sub_urls, session):
    """Getting all relevant links in each subject page"""
    sub_links = [
        BeautifulSoup(session.get(sub).text, "html.parser")
        .find_all("a", {"onclick": ""})
        for sub in sub_urls
    ]
    return sub_links


def sorting_links(sub_links):
    res_urls, news_urls, notice_urls = (
        [[] for x in range(len(sub_links))] for y in range(3))
    for x in range(len(sub_links)):
        for y in range(len(sub_links[x])):
            url = (sub_links[x][y]).get("href")
            if("resource/view.php?id" in url or "folder/view.php?id=" in url):
                res_urls[x].append(url)
            elif("page/view.php?id" in url):
                try:
                    notice_urls[x].append(
                    [url, sub_links[x][y].contents[1].contents[0]])
                except:
                    continue
            elif("forum/view.php?id" in url):
                news_urls[x].append(url)
            # Needs to be worked upon and added at a later stage.
            # elif("/mod/" in url and "id" in url and "index" not in url):
            #     notice_urls[x].append([url, sub_links[x][y].contents])
    return (notice_urls, news_urls, res_urls)


def main():
    """Displaying notices, news and other announcements, updating slides"""
    try:
        slides_path, session = login()
        sub_names, sub_urls = sub_list_folders(slides_path)
        sub_links = get_all_links(sub_urls, session)
        sorted_links = sorting_links(sub_links)
        updates.main(session, sub_names, sorted_links, slides_path)
    except requests.exceptions.ConnectionError:
        quit("No Internet Connection. Please retry")
    except IOError:
        quit("Unable to read from file. Please reinstall termi-Nalanda")
    except KeyboardInterrupt:
        print("Stopped by user.")


if(__name__ == "__main__"):
    main()
