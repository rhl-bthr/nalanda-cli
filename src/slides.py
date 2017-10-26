import io, os, requests

INSTALLATION_FOLDER = os.path.join(os.path.expanduser('~'), '.termi-nalanda')
def download(session, sub_names, res_urls, path):
    subject_updates = [[] for x in sub_names]
    for x in range(len(sub_names)):
        done_slides_file = io.open(os.path.join(INSTALLATION_FOLDER,"Lectures",sub_names[x]+'.txt'),'a+')
        done_slides_file.seek(0)
        done_slides = done_slides_file.read().split('\n')
        for y in range(len(res_urls[x])):
            if (res_urls[x][y] not in done_slides):
                if ('folder/view' in res_urls[x][y]):
                    id_param = res_urls[x][y].split('php')[1]
                    try:
                        result = session.get(
                        'http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php' + id_param)
                    except requests.exceptions.ConnectionError:
                        quit("No Internet Connection. Please retry")
                else:
                    result = session.get(res_urls[x][y])
                file_name = result.headers['content-disposition'].split('e="')[
                    1].split('"')[0]
                with io.open(os.path.join(path, sub_names[x], file_name), 'wb') as f:
                    f.write(result.content)
                done_slides_file.write(res_urls[x][y]+'\n')
                subject_updates[x].append([])
    return subject_updates

def main(session, sub_names, res_urls, path):
    from terminal import terminal_display
    update_list = download(session, sub_names, res_urls, path)
    terminal_display(update_list, 'Lectures', sub_names, " has new updates")