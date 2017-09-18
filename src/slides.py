def update(session,sub_names,resource_urls,path):
    print ('-'*60)+'\n\033[1m\nUpdating Slides-\n\033[0m'
    s_no=0
    for x in range(len(sub_names)):
        downloaded_subject_file = open('res/Downloaded/'+sub_names[x],'a+r')
        downloaded = downloaded_subject_file.readlines()
        diff = len(resource_urls[x])-len(downloaded)
        for y in range(1,diff+1):
            if (y==1):
                s_no=s_no+1
                print "\t" + str(s_no) + '. ' + sub_names[x] + " has new updates."
            if ('folder/view' in resource_urls[x][-y]):
                id_param = resource_urls[x][-y].split('php')[1]
                result = session.get('http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php'+id_param)
            else:
                result = session.get(resource_urls[x][-y])
            file_name= result.headers['content-disposition'].split('e="')[1].split('"')[0]
            with open(path+'Lectures/'+sub_names[x]+'/'+file_name, 'wb') as f:
                f.write(result.content)
            downloaded_subject_file.write("a\n")
    if s_no==0:
        print "\t*No new slides*"
    else:
        print "\t*All subjects updated!*"
