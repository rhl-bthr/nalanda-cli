from terminal import terminal_display
import io, os

INSTALLATION_FOLDER = os.path.join(os.path.expanduser('~'), '.termi-nalanda')
def download(session, sub_names, resource_urls, path):
    subject_updates = [0 for x in resource_urls]
    for x in range(len(sub_names)):
        done_slides_file = io.open(os.path.join(INSTALLATION_FOLDER,"Lectures",sub_names[x]+'.txt'),'a+')
        done_slides_file.seek(0)
        done_slides = done_slides_file.read().split('\n')
        for y in range(len(resource_urls[x])):
            if (resource_urls[x][y] not in done_slides):
                if ('folder/view' in resource_urls[x][y]):
                    id_param = resource_urls[x][y].split('php')[1]
                    try:
                        result = session.get(
                        'http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php' + id_param)
                    except session.exceptions.ConnectionError:
                        quit("No Internet Connection. Please retry")
                else:
                    result = session.get(resource_urls[x][y])
                file_name = result.headers['content-disposition'].split('e="')[
                    1].split('"')[0]
                with io.open(os.path.join(path, sub_names[x], file_name), 'wb') as f:
                    f.write(result.content)
                done_slides_file.write(resource_urls[x][y]+'\n')
                subject_updates[x]+=1
    return subject_updates

def main(session, sub_names, resource_urls, path):
    subject_updates = download(session, sub_names, resource_urls, path)
    terminal_display(None, 'Lectures', sub_names, " has new updates", subject_updates)