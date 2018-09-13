try:
    from bs4 import BeautifulSoup
    import os
    import io
    import requests
except ImportError:
    quit("Required Libraries aren't installed. Please restart installation.")

join = os.path.join
INSTALL_PATH = join(os.path.expanduser("~"), ".nalanda-cli")
FOLDER_LIST = ["News", "Notices", "Lectures", "Subjects"]

try:
    input = raw_input
except NameError:
    pass


def take_config():
    email = input("\nEnter BITS ID [Eg: f2016015]\n") + \
        "@pilani.bits-pilani.ac.in"
    pwd = input("Enter Nalanda Password\n")
    config_path = join(INSTALL_PATH, "config.txt")
    f = io.open(config_path, "w")
    config = (email + "\n" + pwd)
    try:
        f.write(config)
    except TypeError:
        f.write(unicode(config))
    f.close()


def make_folders():
    for folder_name in FOLDER_LIST:
        os.makedirs(join(INSTALL_PATH, folder_name))


def get_sub_list(session):
    url_file_name = join(INSTALL_PATH, "sub-url.txt")
    name_file_name = join(INSTALL_PATH, "sub-name.txt")
    url_file = io.open(url_file_name, "w")
    name_file = io.open(name_file_name, "w")
    result = session.get("http://nalanda.bits-pilani.ac.in/my")
    soup = BeautifulSoup(result.text, "html.parser")
    sub_url, sub_name = [], []
    for x in soup.find_all("div", "column c1"):
        sub_url.append(x.contents[0].get("href"))
        sub_name.append(
            ((x.contents[0].contents[1]).split("/")[0]).split("\\")[0])
    try:
        url_file.write("\n".join(sub_url))
        name_file.write("\n".join(sub_name))
    except TypeError:
        url_file.write(unicode("\n".join(sub_url)))
        name_file.write(unicode("\n".join(sub_name)))


def login():
    session = requests.session()
    config = io.open(join(INSTALL_PATH, "config.txt"), "r")
    config = (config.read()).split("\n")
    result = session.post(
        "http://nalanda.bits-pilani.ac.in/login/index.php",
        data={
            "username": config[0],
            "password": config[1],
        })
    result = BeautifulSoup(result.text, "html.parser")
    login_check = result.find_all("a", {"id": "loginerrormessage"})
    if(login_check):
        print("Username or Password Incorrect. Please retry")
        take_config()
        login()
    return config[2], session


def main():
    try:
        make_folders()
        take_config()
        dump, session = login()
        get_sub_list(session)
    except KeyboardInterrupt:
        print("Installation cancelled by user. Please retry.")
    except requests.exceptions.ConnectionError:
        quit("No Internet Connection. Please retry.")
    except IOError:
        quit("Unable to read from file. Please reinstall termi-Nalanda.")


if(__name__ == "__main__"):
    main()
