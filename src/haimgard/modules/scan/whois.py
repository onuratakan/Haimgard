import requests
from rich.console import Console
from rich.table import Table
import random
import json
import re
import whois

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/whois"
        self.description = "Scan whois."
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

        result = whois.whois(target)

        
        if result["domain_name"] is not None:
            print(f"\033[32m[+]\033[0m Whois founded on {target}")
            print(result)
        else:
            print(f"[-] Whois not founded on {target}")
