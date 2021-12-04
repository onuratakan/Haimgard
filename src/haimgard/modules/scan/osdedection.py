from rich.console import Console
from rich.table import Table
import random
import json
import nmap


class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/osdedection"
        self.description = "OS dedection."
        self.author = "Onur Atakan ULUSOY"             
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

        try:
            for k, v in nm_scan.get('scan').items():
                if v.get('osmatch'):
                    for i in v.get('osmatch'):
                        print(f"\033[32m[+]\033[0m {i.get('name')} OS is detected on {hosts}")
                else:
                    break
        except (xml.etree.ElementTree.ParseError, nmap.nmap.PortScannerError):
            pass
        except Exception as e:
            print(f"[-] OS is not detected on {url}")  
