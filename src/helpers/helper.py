import os
import platform

from time import sleep

from rich import print
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

class Helper:
    @staticmethod
    def Splash(text = "Gestão do Laboratório de Monitorização e Investigação Ambiental"):
        Helper.Clear()
        print(Panel(Align.center(Text("\n{}\n".format(text))), title="AED", style="bold white"))
    
    @staticmethod
    def Clear():
        if platform.system() == "Windows":
            os.system('cls')  
        else:
            os.system('clear')

    @staticmethod
    def Pause():
        input("\nPrima [ENTER] para continuar...")
        
    def SystemPause(seconds = 2):
        sleep(seconds)
        
    @staticmethod
    def NewLine():
        print("\n")