import os
import requests
from bs4 import BeautifulSoup
import io
from terminal import login

INSTALLATION_FOLDER = os.path.join(os.path.expanduser('~'), '.termi-nalanda')

FOLDER_LIST = ['News', 'Notices', 'Lectures', 'Subjects']

try:
   input = raw_input
except NameError:
   pass

def take_config():
    email = input("\nEnter your BITS ID [Eg: f2016015]\n") + '@pilani.bits-pilani.ac.in'
    pwd = input("Enter your Nalanda Password\n")
    path = input("Enter the path to store the lecture slides [Refer to readme]\n")
    config_path = os.path.join(INSTALLATION_FOLDER, 'config.txt')
    path = os.path.join(os.path.expanduser('~'), path)
    f = io.open(config_path, 'w')
    config = (email + '\n' + pwd + '\n' + path)
    f.write(unicode(config))
    f.close()


def make_folders():
    for folder_name in FOLDER_LIST:
        os.makedirs(os.path.join(INSTALLATION_FOLDER, folder_name))


def get_subject_list(session):
    url_file_name = os.path.join(INSTALLATION_FOLDER, 'Subjects', 'url.txt')
    name_file_name = os.path.join(INSTALLATION_FOLDER, 'Subjects', 'name.txt')
    url_file = io.open(url_file_name, 'w')
    name_file = io.open(name_file_name, 'w')
    result = session.get('http://nalanda.bits-pilani.ac.in/my')
    soup = BeautifulSoup(result.text, "html.parser")
    subject_url = []
    subject_name = []
    for x in soup.find_all('div', 'column c1'):
        subject_url.append(x.contents[0].get('href'))
        subject_name.append(((x.contents[0].contents[1]).split('/')[0]).split('\\')[0])
    url_file.write('\n'.join(subject_url))
    name_file.write('\n'.join(subject_name))


def main():
    take_config()
    dump, session = login()
    make_folders()
    get_subject_list(session)


if(__name__ == '__main__'):
    main()
