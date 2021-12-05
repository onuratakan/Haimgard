import requests
from rich.console import Console
from rich.table import Table
import random
from bs4 import BeautifulSoup
import urllib.request as hyperlink
import os
import time
import re

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "wordpress/themesdedection"
        self.description = "WordPress themes detection."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True
        self.options = {
            "target": {"value": None, "required": True},
            "ssl": {"value": None, "required": False},
            "sslverify": {"value": None, "required": False},
            "port": {"value": 443, "required": False},
            "path": {"value": None, "required": False},
            "requestdelay": {"value": 0.1, "required": False},
            "themenumber": {"value": 100, "required": False},
            "aggressive": {"value": False, "required": False},
            "update": {"value": False, "required": False}
        }

    def info(self):
        console = Console()
        table = Table()
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Author")
        table.add_row(self.name, self.description, self.author)
        console.print(table)


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
        requestdelay = float(self.options["requestdelay"]["value"])
        themenumber = int(self.options["themenumber"]["value"])
        aggressive = True if self.options["aggressive"]["value"] == "1" else False
        update = True if self.options["update"]["value"] ==  "1" else False
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

        this_dir, this_filename = os.path.split(__file__)
        themestxt = os.path.join(this_dir, "themes.txt")

        if update:
            link = hyperlink.urlopen('http://themes.svn.wordpress.org/')
            wordPressSoup = BeautifulSoup(link,'lxml')
            with open(themestxt, 'wt', encoding='utf8') as file:
                    file.write(wordPressSoup.text)

        console = Console()
        table = Table()
        table.add_column("NAME")
        table.add_column("PATH")
        table.add_column("VERSION")





        theme_found = False


        regex = re.compile('wp-content/themes/(.*?)/.*?[css|js].*?ver=([0-9\.]*)')
        match = regex.findall(requests.get(url, headers={"User-Agent":random.choice(user_agents)}, verify = sslverify).text)
        themes = []
        for m in match:
            theme_name = m[0]
            theme_name = theme_name.replace('-master','')
            theme_name = theme_name.replace('.min','')
            theme_version = m[1]
            if theme_name not in themes:
                theme_found = True
                themes.append(theme_name)
                theme_url = url + f"/wp-content/themes/{theme_name}"
                theme_url_results = theme_url if requests.get(theme_url, headers={"User-Agent":random.choice(user_agents)}, verify = sslverify).status_code == 200 else "X"
                table.add_row(str(theme_name), theme_url_results, theme_version)

        if aggressive:
            with open(themestxt, 'r', encoding='utf-8') as f:
                lines = f.readlines()        
            for line in lines[:themenumber]:
                url2 = url + f"/wp-content/themes/{line}"
                if requests.get(url2, headers={"User-Agent":random.choice(user_agents)}, verify = sslverify).status_code == 200:
                    theme_found = True
                    table.add_row(str(line), str(url2), str("?"))
                time.sleep(requestdelay)
        
        
        if theme_found:
            print(f"\033[32m[+]\033[0m WordPress themes is detected on {url}")
            console.print(table)
        else:
            print(f"[-] WordPress themes is not detected on {url}")
