from bs4 import BeautifulSoup
def display(session,sub_names,news_urls):
    print ('-'*60)+ '\n\033[1m\nNews and Announcements-\n\033[0m'
    s_no=0
    for x in range(len(sub_names)):
        news_flag=1
        subj_file_news = open('res/News/'+sub_names[x],'a+r')
        read_news = subj_file_news.readlines()
        subject_news=[]
        subject_news_url = []
        for y in range(len(news_urls[x])):
            result = session.get(news_urls[x][y])
            soup = BeautifulSoup(result.text,"html.parser")
            discussion_list=soup.find_all('tr','discussion')
            for url in discussion_list:
                if url.find('td','topic starter pinned'):
                    subject_news.append(url.contents[0].contents[1].contents[0])
                    subject_news_url.append(url.contents[0].contents[1].get('href'))
                else:
                    subject_news.append(url.contents[0].contents[0].contents[0])
                    subject_news_url.append(url.contents[0].contents[0].get('href'))

        diff = len(subject_news)-len(read_news)
        if(diff):
            for y in range(len(subject_news)):
                if (subject_news[y]+'\n' not in read_news):
                    if news_flag==1:
                        s_no+=1
                        print '\n'+'\033[1m' + str(s_no) + '. ' + sub_names[x] + '\033[0m'
                    print '\t'+str(news_flag) + '. '+ subject_news[y] + '\n\t\t' + subject_news_url[y]
                    news_flag+=1
                    subj_file_news.write(subject_news[y]+'\n')
            if(news_flag!=1):
                print ""
    if(s_no)==0:
        print "\t*No New news*"