#Rahul Bothra
#Pro-Panda
#Termi-Nal-anda

import requests
import folders, subject_update, slides, notices, news
from bs4 import BeautifulSoup

print '\033[1m' + "\t\t**Termi-Nalanda**" + '\033[0m'
session = requests.session()
subject_a_all, link_list = [], []
flaggy = 1
credentials = open('res/credentials.txt','r').readlines()
folders.make(['News','Notices','Downloaded'])  #Making folders for storing data
session.post('http://nalanda.bits-pilani.ac.in/login/index.php', data = {
    'username':credentials[0].strip(),
    'password':credentials[1].strip(),
}) #Logging in
path = credentials[2].strip()
if(path[-1]!='/'):
    path=path+'/'

sub_list,sub_names = subject_update.update(session) #Updating user's subject list and urls
folders.subject_make(sub_names,path) #Making folders for lecture slides

for subj in sub_list: #getting all links in each subject page
    result = session.get(subj)
    soup = BeautifulSoup(result.text,"html.parser")
    subject_a_all.append(soup.find_all('a',{'onclick':""}))
notice_urls, news_urls, resource_urls = [],[],[]

for x in range(len(subject_a_all)): #Filtering each url into the 3 categories
    subject_notices_urls, subject_news_urls, subject_resource_urls = [], [], []
    for y in range(len(subject_a_all[x])):
        url = (subject_a_all[x][y]).get('href')
        if('resource/view.php?id' in url or 'folder/view.php?id=' in url):
            subject_resource_urls.append(url)
        elif('page/view.php?id' in url):
            subject_notices_urls.append([url,subject_a_all[x][y].contents[1].contents[0]])
        elif('forum/view.php?id' in url):
            subject_news_urls.append(url)
    notice_urls.append(subject_notices_urls)
    news_urls.append(subject_news_urls)
    resource_urls.append(subject_resource_urls)

notices.display(session, sub_names, notice_urls)#Displaying Notices
news.display(session,sub_names, news_urls)#Displaying News
slides.update(session,sub_names,resource_urls,path)#Updating Slides
