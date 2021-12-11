from rich.console import Console
from rich.table import Table
import random
import json
import nmap
import xml.etree.ElementTree

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/scriptvuln"
        self.description = "Script vuln dedection."
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
        table.add_column("SERVICE/PROTOCOL/PORT")
        table.add_column("SCRIPT : RESULT")

        nm = nmap.PortScanner()
        nm.scan(target, arguments='--script=vuln')

        open_service = False
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = list(nm[host][proto].keys())
                lport.sort()
                for port in lport:
                        if nm[host][proto][port].get("script") is not None:
                            vuln = ""
                            for key, value in nm[host][proto][port]["script"].items():
                                vuln += f"{key} : {value}\n"
                            open_service = True
                            table.add_row(str(nm[host][proto][port]["name"]) + "/" + str(proto) + "/" + str(port), vuln)

        if open_service:
            print(f"\033[32m[+]\033[0m Founded some script vuln on {target}")
            console.print(table)
        else:
            print(f"[-] Any script vuln founded on {target}")