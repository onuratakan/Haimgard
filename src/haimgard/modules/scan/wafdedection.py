import requests
from rich.console import Console
from rich.table import Table
import random
import json
import re


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/wafdedection"
        self.description = "WAF dedection."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True             
        self.options = {
            "target": {"value": None, "required": True},
            "ssl": {"value": None, "required": False},
            "sslverify": {"value": None, "required": False},
            "port": {"value": None, "required": False},
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


        console = Console()
        table = Table()
        table.add_column("NAME")
        table.add_column("PATH")


        r = requests.get(url, headers={"User-Agent":random.choice(user_agents)}, verify = sslverify)

        not_plugin_wafs = [
            "cloudflare",
            "__cfduid"
        ]

        waf_found = False
        for waf in not_plugin_wafs:
            if re.search(waf,str(r.headers),re.I):
                waf_found = True
                table.add_row(waf, "X")


        if waf_found:
            print(f"\033[32m[+]\033[0m WAF is detected on {url}")
            console.print(table)
        else:
            print(f"[-] WAF is not detected on {url}")
