from rich.console import Console
from rich.table import Table
import random
import json
import nmap
import xml.etree.ElementTree

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "info"
        self.description = "Get information of an Instagram user."
        self.author = "Onur Atakan ULUSOY"
        self.runauto = True             
        self.options = {
            "insname": {"value": None, "required": True},
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


        name = self.options["insname"]["value"]


        console = Console()
        table = Table()
        table.add_column("NAME/EMAIL/USERNAME")
        table.add_column("SCRIPT : RESULT")

        table.add_row(str(port))


        if open_service:
            print(f"\033[32m[+]\033[0m Founded some information on {name}")
            console.print(table)
        else:
            print(f"[-] Any information founded on {name}")