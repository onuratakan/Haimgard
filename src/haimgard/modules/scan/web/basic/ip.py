import requests
from rich.console import Console
from rich.table import Table
import socket

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "ip"
        self.description = "Find IP adress of an web application server."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True             
        self.options = {
            "target": {"value": None, "required": True},
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

        # get ip adress

        
        try:
            ip =  socket.gethostbyname(target)
            print(f"\033[32m[+]\033[0m {ip} is the ip adress of {target}")
        except:
            print(f"[-] IP adress not founded on {target}")
