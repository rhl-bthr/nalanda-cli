def display(session,sub_names,notice_urls):
    print '\033[1mNotices-\n\033[0m'
    s_no=0
    for x in range(len(sub_names)):
        notice_flag=1
        subj_file_notice = open('res/Notices/'+sub_names[x],'a+r')
        read_notices = subj_file_notice.readlines()
        read_notices = [z.strip() for z in read_notices]
        for y in range(len(notice_urls[x])):
            notice_text = notice_urls[x][y][1]
            if (notice_text in read_notices):
                pass
            else:
                if(notice_flag==1):
                    s_no+=1
                    print '\033[1m' + str(s_no) + '. ' + sub_names[x] + '\033[0m'
                print '\t' + str(notice_flag) + '. ' + notice_text + '\n\t\t' + notice_urls[x][y][0]
                subj_file_notice.write(notice_text+'\n')
                notice_flag=notice_flag+1
        if(notice_flag!=1):
            print ""
    if(s_no)==0:
        print "\t*No New notices*"