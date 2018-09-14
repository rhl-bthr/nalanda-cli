import os
from getpass import getpass
import json

try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    quit("Required Libraries aren't installed. Please restart installation.")

join = os.path.join
INSTALL_PATH = join(os.path.expanduser("~"), ".nalanda-cli")
session = requests.session()


try:
    config = {}
    name_url_pair = {}

    while True:
        config["username"] = input("\nEnter BITS ID [Eg: f2016015]\n") +
                          "@pilani.bits-pilani.ac.in"

        config["password"] = getpass(prompt = "Enter nalanda password:")

        result = session.post(
            "http://nalanda.bits-pilani.ac.in/login/index.php",
            data = config)
        result = BeautifulSoup(result.text, "html.parser")

        if not result.find_all("a", {"id": "loginerrormessage"}):
            break
        print("Username or Password Incorrect. Please retry")

    with open(join(INSTALL_PATH, "config.json"), "w") as f:
        json.dumps(config, f)

    with open(join(INSTALL_PATH, "subjects.json"), "w") as sub_file:
        result = session.get("http://nalanda.bits-pilani.ac.in/my")
        soup = BeautifulSoup(result.text, "html.parser")

        for x in soup.find_all("div", "column c1"):
            name_url_pair[x.contents[0].get("href")] = ((x.contents[0].contents[1]).split("/")[0]).split("\\")[0]
        json.dumps(name_url_pair, sub_file)


except KeyboardInterrupt:
    quit("Installation cancelled by user. Please retry.")
except requests.exceptions.ConnectionError:
    quit("No Internet Connection. Please retry.")
except IOError:
    quit("Unable to read from file. Please reinstall nalanda-cli.")
