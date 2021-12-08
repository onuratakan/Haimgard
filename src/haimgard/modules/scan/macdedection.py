import requests
from rich.console import Console
from rich.table import Table
import random
import json
import re
from scapy.all import srp, ARP, Ether

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/macdedection"
        self.description = "MAC dedection."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = False             
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

        result = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=target), timeout=timeout, verbose=0)[0]
        result  = [print(f"\033[32m[+]\033[0m {received.hwsrc } MAC is detected on {target}") for sent, received in result]
        if len(result) == 0:
            print(f"[-] MAC is not detected on {target}")
        

