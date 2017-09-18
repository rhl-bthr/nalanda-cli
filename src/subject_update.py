from bs4 import BeautifulSoup

def update(session):
    subj_file = open('res/subjects','a+r')
    subj_list = subj_file.readlines()
    subj_name_file = open('res/subjectName','a+r')
    subj_name_list = subj_name_file.readlines()
    if subj_list==[]:
        result = session.get('http://nalanda.bits-pilani.ac.in/my')
        soup = BeautifulSoup(result.text,"html.parser")
        for x in soup.find_all('div','column c1'):
            subject_url = x.contents[0].get('href')
            subject_name = (x.contents[0].contents[1]).split('/')[0]
            subj_list.append(subject_url)
            subj_name_list.append(subject_name)
            subj_file.write(subject_url+'\n')
            subj_name_file.write(subject_name+'\n')
        subj_name_list = [(x.split('\\')[0]).split('\n')[0] for x in subj_name_list]
        return subj_list,subj_name_list
    else:
        subj_name_list = [x.split('\n')[0] for x in subj_name_list]
        return subj_list, subj_name_list