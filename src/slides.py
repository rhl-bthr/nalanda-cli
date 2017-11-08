import io, os, requests

join = os.path.join
INSTALL_PATH = join(os.path.expanduser('~'), '.termi-nalanda')

def download(session, sub_names, res_urls, path):
    sub_updates = [[] for x in sub_names]
    for x in range(len(sub_names)):
        done_slides_file = io.open(join(INSTALL_PATH,"Lectures",sub_names[x]+'.txt'),'a+')
        done_slides_file.seek(0)
        done_slides = done_slides_file.read().split('\n')
        for y in range(len(res_urls[x])):
            if (res_urls[x][y] not in done_slides):
                if ('folder/view' in res_urls[x][y]):
                    id_param = res_urls[x][y].split('php')[1]
                    result = session.get(
                    'http://nalanda.bits-pilani.ac.in/mod/folder/download_folder.php' + id_param)
                else:
                    result = session.get(res_urls[x][y])
                file_name = result.headers['content-disposition'].split('e="')[
                    1].split('"')[0]
                with io.open(join(path, sub_names[x], file_name), 'wb') as f:
                    f.write(result.content)
                done_slides_file.write(res_urls[x][y]+'\n')
                sub_updates[x].append([])
    return sub_updates

def main(session, sub_names, res_urls, path):
    from updates import term_display
    update_list = download(session, sub_names, res_urls, path)
    term_display(update_list, 'Lectures', sub_names, " has new updates")