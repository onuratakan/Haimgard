import requests
from rich.console import Console
from rich.table import Table
import random
import socket
import nmap

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/servicededection"
        self.description = "Service dedection."
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


        console = Console()
        table = Table()
        table.add_column("SERVICE")
        table.add_column("VERSION")
        table.add_column("HOST")
        table.add_column("PROTOCOL")
        table.add_column("PORT")
        table.add_column("STATE")

        nm = nmap.PortScanner()
        nm_scan = nm.scan(target, arguments="-sV")

        open_service = False
        for host in nm.all_hosts():

            for proto in nm[host].all_protocols():
                lport = list(nm[host][proto].keys())
                lport.sort()
                for port in lport:   
                    if not str(nm[host][proto][port]["product"]) == "":
                        open_service = True
                        version = str(nm[host][proto][port]["product"]) + " "
                        version += str(nm[host][proto][port]["version"]) + " "
                        version += str(nm[host][proto][port]["extrainfo"]) + " "
                        table.add_row(str(nm[host][proto][port]["name"]), version, str(host), str(proto), str(port), str(nm[host][proto][port]['state']))


        if open_service:
            print(f"\033[32m[+]\033[0m Founded some service on {target}") 
            console.print(table)
        else:
            print(f"[-] Any service founded on {target}")
