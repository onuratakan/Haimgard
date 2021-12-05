import requests
from rich.console import Console
from rich.table import Table
import random
import json
import re


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "wordpress/userdedection"
        self.description = "Get wordpress users."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True             
        self.options = {
            "target": {"value": None, "required": True},
            "ssl": {"value": None, "required": False},
            "sslverify": {"value": None, "required": False},
            "port": {"value": 443, "required": False},
            "path": {"value": None, "required": False}
        }

    def info(self):
        console = Console()
        table = Table()
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Author")
        table.add_row(self.name, self.description, self.author)
        console.print(table)
        
    def xmlrpc_check_admin(self, url, username, verify):
        post = "<methodCall><methodName>wp.getUsersBlogs</methodName><params><param><value><string>" + username + "</string></value></param><param><value><string>" + "123" + "</string></value></param></params></methodCall>"
        req = requests.post(f"{url}/xmlrpc.php", data=post, verify = verify)
        regex = re.compile("isAdmin.*boolean.(\d)")
        match = regex.findall(req.text)
        if len(match) != 0:
            if int(match[0]):
                return True
            else:
                return False

    def run(self):
        for key in self.options:
            if (
                self.options[key]["value"] is None
                and self.options[key]["required"] is True
            ):
                self.logger.error(f"Required key {str(key)} is not set for {self.name}")
                return


        target = self.options["target"]["value"]
        ssl = True if self.options["ssl"]["value"] == "1" else False
        sslverify = True if self.options["sslverify"]["value"] == "1" else False
        port = int(self.options["port"]["value"])
        path = self.options["path"]["value"]

        url = f"https://{target}:{port}{path}" if ssl else f"http://{target}:{port}{path}"

        user_agents = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2."
        ]


        url2 = f"{url}/wp-json/wp/v2/users"
        r = requests.get(url2, headers={"User-Agent":random.choice(user_agents)}, verify = sslverify)
        if r.status_code == 200:
            if "id" in r.text:

                user_list = json.loads(r.text)
                console = Console()
                table = Table()
                table.add_column("ID")
                table.add_column("NAME")
                table.add_column("URL")
                table.add_column("DESCRIPTION")
                table.add_column("LINK")
                table.add_column("SLUG")
                table.add_column("ADMIN")
                [table.add_row(str(user["id"]), str(user["name"]), str(user["url"]), str(user["description"][:40] + "..."), str(user["link"]), str(user["slug"]), str("+") if self.xmlrpc_check_admin(url, user["name"], sslverify) else str("-")) for user in user_list]
                print(f"\033[32m[+]\033[0m WordPress user is detected on {url2}")
                console.print(table)
            else:
                print(f"[-] WordPress user is not detected on {url2}")
        else:
            print(f"[-] WordPress user is not detected on {url2}")
