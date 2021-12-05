import requests
from rich.console import Console
from rich.table import Table
import random
from scapy.all import srp, Ether, ARP
from mac_vendor_lookup import MacLookup

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "scan/network"
        self.description = "Scan network"
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

        console = Console()
        table = Table()
        table.add_column("IP")
        table.add_column("MAC")
        table.add_column("VENDOR")
        found = False

        packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=f"{target}/24")
        result = srp(packet, timeout=timeout, verbose=0)[0]
        for sent, received in result:
            found = True
            table.add_row(received.psrc, received.hwsrc, MacLookup().lookup(received.hwsrc))


        if found:
            print(f"\033[32m[+]\033[0m Found some device on {target}") 
            console.print(table)
        else:
            print(f"[-] Any device founded on {target}")
