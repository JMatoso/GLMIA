import os
import platform

from time import sleep

from rich import print
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

class Helper:
    @staticmethod
    def splash(text = "Gestão do Laboratório de Monitorização e Investigação Ambiental"):
        Helper.clear()
        print(Panel(Align.center(Text("\n{}\n".format(text))), title="AED", style="bold white"))
    
    @staticmethod
    def clear():
        if platform.system() == "Windows":
            os.system('cls')  
        else:
            os.system('clear')

    @staticmethod
    def pause():
        input("\nPrima [ENTER] para continuar...")
        
    def system_pause(seconds = 2):
        sleep(seconds)
        
    @staticmethod
    def new_line():
        print("\n")