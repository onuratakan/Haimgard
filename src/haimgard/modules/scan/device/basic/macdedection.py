import requests
from rich.console import Console
from rich.table import Table
import socket


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "macdedection"
        self.description = "MAC dedection."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True             
        self.options = {
            "target": {"value": None, "required": True},
            "timeout": {"value": 5, "required": True},
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
        timeout = float(self.options["timeout"]["value"])

        try:
            from scapy.all import getmacbyip
            print(f"\033[32m[+]\033[0m {getmacbyip(socket.gethostbyname(target))} is the MAC adress of {target}")
        except Exception as e:
            self.logger.exception(e)
            print(f"[-] MAC is not detected on {target}")
        

