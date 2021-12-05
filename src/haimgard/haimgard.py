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
from types import FunctionType


this_dir, this_filename = os.path.split(__file__)

print(cowsay.get_output_string('daemon', "Haimgard"))


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


class HaimgardShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        self.file = None

        self.module = None
        self.prompt = "{}haimgard{} > ".format(Fore.YELLOW, Style.RESET_ALL)

        self.options = {
            "target": {"value": None, "required": True},
            "amount": {"value": 0, "required": False},
            "ssl": {"value": "1", "required": False},
            "sslverify": {"value": "1", "required": False},
            "port": {"value": 443, "required": False},
            "path": {"value": "", "required": False},
            "timeout": {"value": 1, "required": False},
            "start": {"value": 0, "required": False},
            "end": {"value": 0, "required": False},
            "requestdelay": {"value": 0.1, "required": False},
            "pluginnumber": {"value": 100, "required": False},
            "themenumber": {"value": 100, "required": False},
            "aggressive": {"value": "0", "required": False},
            "update": {"value": "0", "required": False}
        }        

    def do_mode(self, arg):
        "mode passive/normal"
        if arg == "":
            logger.error("Please give a value")
            return          

        if arg == "passive":
            self.options["amount"]["value"] = 0
            self.options["start"]["value"] = 0
            self.options["end"]["value"] = 0
        elif arg == "normal":
            self.options["amount"]["value"] = 100
            self.options["start"]["value"] = 1
            self.options["end"]["value"] = 100
        else:
            logger.error("No mode found") 

    def do_list(self, arg):
        "list wordpress"
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
        "use wordpress/adminpagededection"
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
                    if self.module.options[option]["value"] is None:
                        self.module.options[option]["value"] = self.options[option]["value"]
        else:
            logger.error("Module already selected")


    def do_runall(self, arg):
        "runall worpress"
        if arg == "":
            logger.error("Please give a category")
            return          
        dir = os.path.join(this_dir, "modules", arg)
        found = False
        for root,dirs,files in os.walk(dir):
            for each in files:
                if each.endswith(".py"):
                    found = True
                    module_path = os.path.join(this_dir, "modules", f"{arg}/{os.path.splitext(each)[0]}.py")
                    spec = importlib.util.spec_from_file_location("module.name", str(module_path))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module) 
                    the_module = module.Module(logger)
                    for option in self.options:
                        if option in the_module.options:
                            if the_module.options[option]["value"] is None:
                                the_module.options[option]["value"] = self.options[option]["value"]                     
                    try:
                        if the_module.runauto:
                            the_module.run()  
                    except BaseException:
                        logger.exception("An exception was thrown!")                

        if not found:
            logger.error("No module found")
            return          

    def do_runeverything(self, arg):
        "runeverything"
    
        dir = os.path.join(this_dir, "modules")
        for root,dirs,files in os.walk(dir):
            for each_dirs in dirs:
                if not each_dirs == "__pycache__":
                    found = False
                    for root,dirs,files in os.walk(os.path.join(this_dir, "modules", each_dirs)):
                        for each in files:
                            if each.endswith(".py"):
                                found = True
                                module_path = os.path.join(this_dir, "modules", f"{each_dirs}/{os.path.splitext(each)[0]}.py")
                                spec = importlib.util.spec_from_file_location("module.name", str(module_path))
                                module = importlib.util.module_from_spec(spec)
                                spec.loader.exec_module(module) 
                                the_module = module.Module(logger)
                                for option in self.options:
                                    if option in the_module.options:
                                        if the_module.options[option]["value"] is None:
                                            the_module.options[option]["value"] = self.options[option]["value"]                    
                                try:
                                    if the_module.runauto:
                                        the_module.run()
                                except BaseException:
                                    logger.exception("An exception was thrown!")                                                

        if not found:
            logger.error("No module found")
            return    

    def do_show(self, arg):
        "show"
        table = Table()
        table.add_column("Key")
        table.add_column("Value")
        table.add_column("Required")
        
        if self.module is None:
            for key in self.options:
                table.add_row(
                    key,
                    str(self.options[key]["value"]),
                    str(self.options[key]["required"]),
                )
            Console().print(table)
        else:
            for key in self.module.options:
                table.add_row(
                    key,
                    str(self.module.options[key]["value"]),
                    str(self.module.options[key]["required"]),
                )
            Console().print(table)

    def do_set(self, arg):
        "set target value"

        if arg == "" or len(arg.split()) != 2:
            logger.error("Please give a option and value")
            return

        key = arg.split()[0]
        value = arg.split()[1]
        finded_option = False
        try:
            self.module.options[key]["value"] = value
            finded_option = True
        except:
            pass
        try:
            self.options[key]["value"] = value
            finded_option = True
        except:
            pass

        if not finded_option:
            logger.error("No option found")


    def do_run(self,arg):
        "run"
        if self.module is not None:
            try:
                self.module.run()
            except BaseException:
                logger.exception("An exception was thrown!")
        else:
            logger.error("No module found")
            return         

    def do_info(self, arg):
        "info"
        if self.module is None:
            logger.warning("Please select a module first")
            return
        self.module.info()

    def do_clear(self, arg):
        "clear"
        try:
            os.system("clear")
        except:
            os.system("cls")

    def do_exit(self, arg):
        "exit the Haimgard shell"
        sys.exit(1)
    def do_quit(self, arg):
        "exit the module"
        self.module = None
        self.prompt = "{}haimgard{} > ".format(Fore.YELLOW, Style.RESET_ALL)
    def do_eof(self, arg):
        "eof"
        os.system("find . -name '*.pyc' -delete")
        sys.exit(1)

    def do_search(self,arg):
        "search for new modules"
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

    def do_record(self, arg):
        'record test'
        if arg == "":
            logger.error("Please give a filename")
            return
        self.file = open(arg+".haimgard", 'w')
    def do_stoprecord(self, arg):
        'stoprecord'
        if self.file is not None:
            self.file.close()
            self.file = None
        else:
            logger.error("No record found")       
    def do_playback(self, arg):
        'playback test'
        if arg == "":
            logger.error("Please give a filename")
            return             
        with open(arg+".haimgard") as f:
            for command in f.read().splitlines():
                self.onecmd(command)

    def precmd(self, line):
        line = line.lower()
        if self.file and 'playback' not in line and 'stoprecord' not in line:
            print(line, file=self.file)
        return line
                 
                    

        
def main():
    colorama.init()
    logger.remove(0)
    logger.add(sys.stderr, colorize=True, format="<level>{level}: {message}</level>")

    start = True
    while True:
        try:
            if len(sys.argv) > 1 and start:
                shell = HaimgardShell()
                arguments = ' '.join(sys.argv[1:])

                method_list = [x for x, y in HaimgardShell.__dict__.items() if type(y) == FunctionType]
                method_list.remove("__init__")
                methods = ""
                for method in method_list:
                    new_method = method.replace("do_", "")
                    methods += f"{new_method}|" if not method_list.index(method) == len(method_list) - 1 else f"{new_method}"


                command_list = re.split(r'.(?={methods})'.format(methods=methods), arguments)

                for command in command_list:
                    shell.onecmd(command)
                shell.cmdloop()
            else:
                HaimgardShell().cmdloop()
        except KeyboardInterrupt:
            print()
            logger.warning("Please use EOF or the exit/quit commands to exit")
        except Exception:
            raise

        start = False
if __name__ == "__main__":
    main()