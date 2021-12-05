from rich.console import Console
from rich.table import Table
import random
import json
import nmap
import xml.etree.ElementTree

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/osdedection"
        self.description = "OS dedection."
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

        nm = nmap.PortScanner()
        nm_scan_arguments = "-O"
        nm_scan = nm.scan(target, arguments=nm_scan_arguments)

        console = Console()
        table = Table()
        table.add_column("OS")
        table.add_column("HOST")
        found = False
        try:
            for k, v in nm_scan.get('scan').items():
                if v.get('osmatch'):
                    found = True
                    for i in v.get('osmatch'):
                        table.add_row(i.get('name'), k)
        except (xml.etree.ElementTree.ParseError, nmap.nmap.PortScannerError):
            pass
        except Exception as e:
            logger.exception(e)
            print(f"[-] OS is not detected on {target}")  

        if found:
            print(f"\033[32m[+]\033[0m OS is detected on {target}")
            console.print(table)
        else:
            print(f"[-] OS is not detected on {target}")
