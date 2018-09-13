import os
from getpass import getpass

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    quit("Required Libraries aren't installed. Please restart installation.")

join = os.path.join
INSTALL_PATH = join(os.path.expanduser("~"), ".nalanda-cli")
session = requests.session()

FOLDER_LIST = ["News", "Notices", "Lectures", "Subjects"]


if __name__ == "__main__":
    try:
        for folder_name in FOLDER_LIST:
        os.makedirs(join(INSTALL_PATH, folder_name))

        while True:
            email = input("\nEnter BITS ID [Eg: f2016015]\n")
            email += "@pilani.bits-pilani.ac.in"

            password = getpass(prompt = "Enter nalanda password:")

            with open(join(INSTALL_PATH, "config.txt"), "w") as f:
                config = email + "\n" + password
                f.write(config)

            result = session.post(
                "http://nalanda.bits-pilani.ac.in/login/index.php",
                data={
                    "username": email,
                    "password": password,
                })
            result = BeautifulSoup(result.text, "html.parser")

            if not result.find_all("a", {"id": "loginerrormessage"}):
                break
            print("Username or Password Incorrect. Please retry")

        with open(join(INSTALL_PATH, "sub-url.txt"), "w") as url_file:
            with open(join(INSTALL_PATH, "sub-name.txt"), "w") as name_file:

                result = session.get("http://nalanda.bits-pilani.ac.in/my")
                soup = BeautifulSoup(result.text, "html.parser")

                sub_url, sub_name = [], []

                for x in soup.find_all("div", "column c1"):
                    sub_url.append(x.contents[0].get("href"))
                    sub_name.append(((x.contents[0].contents[1]).split("/")[0]).split("\\")[0])

                url_file.write("\n".join(sub_url))
                name_file.write("\n".join(sub_name))

    except KeyboardInterrupt:
        quit("Installation cancelled by user. Please retry.")
    except requests.exceptions.ConnectionError:
        quit("No Internet Connection. Please retry.")
    except IOError:
        quit("Unable to read from file. Please reinstall nalanda-cli.")
