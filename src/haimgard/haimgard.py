#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cmd
import importlib
import importlib.util
import readline
import sys
import time
import os
import re
import cowsay
import colorama
from colorama import Fore, Style
from loguru import logger
from rich.console import Console
from rich.table import Table

this_dir, this_filename = os.path.split(__file__)


version_path = os.path.join(this_dir, "VERSION.txt")
with open(version_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    version = lines[0]

print(cowsay.get_output_string('daemon', f"Haimgard Version: {version}"))


#Modules
dir = os.path.join(this_dir, "modules")
for root,dirs,files in os.walk(dir):
    for each_dirs in dirs:
        if not each_dirs == "__pycache__":
            count = 0
            for root,dirs,files in os.walk(os.path.join(dir, each_dirs)):
                for each in files:
                    if each.endswith(".py"):
                        count += 1
            print(f"\033[34mNumber of {each_dirs}:\033[0m",count)


class PhoenixShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.module = None
        self.prompt = "{}haimgard{} > ".format(Fore.YELLOW, Style.RESET_ALL)

        self.options = {
            "target": {"value": None, "required": True},
            "ssl": {"value": True, "required": False},
            "port": {"value": 443, "required": False},
            "path": {"value": "/", "required": False}
        }        

    def do_list(self, arg):
        "list dos"
        if arg == "":
            logger.error("Please give a category")
            return          
        dir = os.path.join(this_dir, "modules", arg)
        found = False
        for root,dirs,files in os.walk(dir):
            for each in files:
                if each.endswith(".py"):
                    found = True
                    print(f"- {os.path.splitext(each)[0]}") 

        if not found:
            logger.error("No module found")
            return          

    def do_use(self, arg):
        "use exploit/solr/cve-2019-0193"
        args = arg.split()
        if self.module is None:
            try:
                module_path = os.path.join(this_dir, "modules", f"{args[0]}.py")
            except:
                logger.error("No module specified")
                return
            if not os.path.isfile(module_path):
                logger.error("the specified module does not exist")
                return
            spec = importlib.util.spec_from_file_location("module.name", str(module_path))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.module = module.Module(logger)

            logger.success("Successfully loaded {}".format(args[0]))
            self.prompt = "{}haimgard{} ({}{}{}) > ".format(
                Fore.YELLOW, Style.RESET_ALL, Fore.RED, args[0], Style.RESET_ALL
            )
            for option in self.options:
                if option in self.module.options:
                    self.module.options[option]["value"] = self.options[option]["value"]
        else:
            logger.error("Module already selected")

    def do_show(self, arg):
        if self.module is None:
            logger.warning("Please select a module first")
            return
        table = Table()
        table.add_column("Key")
        table.add_column("Value")
        table.add_column("Required")

        for key in self.module.options:
            table.add_row(
                key,
                str(self.module.options[key]["value"]),
                str(self.module.options[key]["required"]),
            )
        Console().print(table)

    def do_set(self, arg):
        "set an option for the selected module"
        if self.module is None:
            logger.warning("Please select a module first")
            return
        key = arg.split()[0]
        value = arg.split()[1]
        if key not in self.module.options:
            logger.error("Option does not exist")
            return
        self.module.options[key]["value"] = value
        try:
            self.options[key]["value"] = value
        except:
            pass


    def do_run(self,arg):
        try:
            self.module.run()
        except BaseException:
            logger.exception("An exception was thrown!")
        

    def do_exploit(self,arg):
        self.module.run()

    def do_info(self, arg):
        if self.module is None:
            logger.warning("Please select a module first")
            return
        self.module.info()

    def do_clear(self, arg):
        try:
            os.system("clear")
        except:
            os.system("cls")

    def do_version(self,arg):
        "version info"
        version_path = os.path.join(this_dir, "VERSION.txt")
        with open(version_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            version = lines[0]
            print(version)

    def do_exit(self, arg):
        "exit the Haimgard shell"
        os.system("find . -name '*.pyc' -delete")
        sys.exit(1)
    def do_quit(self, arg):
        "exit the module"
        self.module = None
        self.prompt = "{}haimgard{} > ".format(Fore.YELLOW, Style.RESET_ALL)
    def do_EOF(self, arg):
        os.system("find . -name '*.pyc' -delete")
        sys.exit(1)

    def do_search(self,arg):
        search_path = os.path.join(this_dir, "modules")
        for root,dirs,files in os.walk(search_path):
            for name in files:
                name_list = []
                name_list.append(root)
                name_list.append(name)
                str ='/'
                string_list = str.join(name_list)
                #print(string_list)
                
                if arg in string_list:
                    print("\033[32m[STATUS] Already Found\033[0m")
                    pass

                    
                    

        
def main():
    colorama.init()
    logger.remove(0)
    logger.add(sys.stderr, colorize=True, format="<level>{level}: {message}</level>")
    while True:
        try:
            PhoenixShell().cmdloop()
        except KeyboardInterrupt:
            print()
            logger.warning("Please use EOF or the exit/quit commands to exit")
        except Exception:
            raise
if __name__ == "__main__":
    main()
