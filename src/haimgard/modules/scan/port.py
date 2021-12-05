import requests
from rich.console import Console
from rich.table import Table
import random
import socket

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/port"
        self.description = "Scan port"
        self.author = "Onur Atakan ULUSOY"
        self.runauto = False
        self.options = {
            "target": {"value": None, "required": True},
            "timeout": {"value": None, "required": True},
            "start": {"value": None, "required": True},
            "end": {"value": None, "required": True},
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
        start = int(self.options["start"]["value"])
        end = int(self.options["end"]["value"])

        port_range = range(int(start), (int(end) + 1))

        console = Console()
        table = Table()
        table.add_column("PORT")
        open_port = False
        for port in port_range:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                open_port = True
                table.add_row(str(port))
            s.close()

        if open_port:
            print(f"\033[32m[+]\033[0m Finded some open port on {target}") 
            console.print(table)
        else:
            print(f"[-] Any open port finded on {target}")
