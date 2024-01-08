import os
import platform

from time import sleep
from datetime import datetime

from rich import print
from rich.text import Text
from rich.align import Align
from rich.panel import Panel

class Helper:
    @staticmethod
    def splash(text = "Gestão do Laboratório de Monitorização e Investigação Ambiental", title = "AED"):
        Helper.clear()
        print(Panel(Align.center(Text("\n{}\n".format(text))), title=title, style="bold white"))
    
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
        
    @staticmethod
    def to_currency(value):
        currency = format(float(value), ',.2f')
        return currency + "€"
    
    @staticmethod
    def to_date(value):
        formats = ['%d/%m/%Y', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f']
        for fmt in formats:
            try:
                date = datetime.strptime(str(value), fmt)
                return date.strftime('%b %d, %Y - %H:%M')
            except:
                pass
        return str(value)
    
    @staticmethod
    def get_ticks_string():
        time = datetime.now()
        return str(int(time.timestamp() * 1e7) + 621355968000000000)

    