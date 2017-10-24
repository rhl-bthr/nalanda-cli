from notices import terminal_display
import os

def download(session, sub_names, resource_urls, path):
    for x in range(len(sub_names)):
        for y in range(len(resource_urls[x])):
            if ('folder/view' in resource_urls[x][y]):
                id_param = resource_urls[x][y].split('php')[1]
                result = session.get(
                    'http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php' + id_param)
            else:
                result = session.get(resource_urls[x][y])
            file_name = result.headers['content-disposition'].split('e="')[
                1].split('"')[0]
            with open(os.path.join(path, sub_names[x], file_name), 'wb') as f:
                f.write(result.content)
def main(session, sub_names, resource_urls, path):
    terminal_display(None,'Lecture-Slides',sub_names," has new Updates")
    download(session,sub_names,resource_urls,path)
    
