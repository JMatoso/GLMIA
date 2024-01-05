from rich import print
from helpers.helper import Helper
from helpers.validations import Validations
from repositories.clients_repository import clients_menu
from repositories.employee_repository import employees_menu

def load():
    __start()
    
def __start():
    Helper.splash()
    __main_menu()
    
def __main_menu():
    Helper.new_line()
    print("1. Gestão de [bold]Clientes[/bold]")
    print("2. Gestão de [bold]Utilizadores[/bold]")
    print("3. Gestão de [bold]Funcionários[/bold]")
    print("4. Gestão de [bold]Análises[/bold]")
    print("0. [red]Sair[/red]")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        __start()
        return
    
    match choice:
        case "1":
            clients_menu()
        case "2":
            print("Utilizadores")
        case "3":
            employees_menu()
        case "4":
            print("Análises")
        case "0":
            print("Até breve!")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            __start()
    
if __name__ == "__main__":
    load()