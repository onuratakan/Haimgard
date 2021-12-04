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
            "port": {"value": 443, "required": False},
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

        nm = nmap.PortScanner()
        nm_scan_arguments = f"-p {port} "
        nm_scan_arguments += "-O"
        nm_scan = nm.scan(target, arguments=nm_scan_arguments)
        for hosts in nm_scan["scan"]:
            if nm[hosts].has_key('osclass'):
                for osclass in nm[hosts]['osclass']:
                    print('OsClass.type : {0}'.format(osclass['type']))
                    print('OsClass.vendor : {0}'.format(osclass['vendor']))
                    print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                    print('OsClass.osgen : {0}'.format(osclass['osgen']))
                    print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                    print('')
                    print(f"\033[32m[+]\033[0m OS is detected on {hosts}")

            elif nm[hosts].has_key('osmatch'):
                for osmatch in nm[hosts]['osmatch']:
                    print('osmatch.name : {0}'.format(osmatch['name']))
                    print('osmatch.accuracy : {0}'.format(osmatch['accuracy']))
                    print('osmatch.line : {0}'.format(osmatch['line']))
                    print('')
                    print(f"\033[32m[+]\033[0m OS is detected on {hosts}")

            elif nm[hosts].has_key('fingerprint'):
                print('Fingerprint : {0}'.format(nm[target]['fingerprint']))
                print(f"\033[32m[+]\033[0m OS is detected on {hosts}")
            else:
                print(f"[-] OS is not detected on {url}")     
