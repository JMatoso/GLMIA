from rich import print
from helpers.helper import Helper
from helpers.validations import Validations
from repositories.clients_repository import clients_menu

def load():
    start()
    
def start():
    Helper.splash()
    main_menu()
    
def main_menu():
    Helper.new_line()
    print("1. Gestão de [cyan]Clientes[/cyan]")
    print("2. Gestão de [cyan]Utilizadores[/cyan]")
    print("3. Gestão de [cyan]Funcionários[/cyan]")
    print("4. Gestão de [cyan]Análises[/cyan]")
    print("0. [red]Sair[/red]")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        start()
        return
    
    match choice:
        case "1":
            clients_menu()
        case "2":
            print("Utilizadores")
        case "3":
            print("Funcionários")
        case "4":
            print("Análises")
        case "0":
            print("Até breve!")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            start()
    
if __name__ == "__main__":
    load()