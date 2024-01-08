from rich import print
from helpers.helper import Helper
from helpers.validations import Validations
from repositories.clients_repository import clients_menu
from repositories.employee_repository import employees_menu
from repositories.users_repository import users_menu
from repositories.analysis_repository import analysis_menu
from repositories.analysis_request_repository import analysis_request_menu
from repositories.analysis_type_repository import analysis_type_menu
from repositories.analysis_reports_repository import analysis_report_menu

def load():
    __start()
    
def __start():
    __main_menu()
    
def __analysis():
    Helper.splash("Gestão de Análises")
    Helper.new_line()
    print("1. Análises")
    print("2. Tipo de Análises")
    print("3. Pedidos de Análises")
    print("4. Resultados de Análises")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        __analysis()
        return
    
    match choice:
        case "1":
            analysis_menu()
        case "2":
            analysis_type_menu()
        case "3":
            analysis_request_menu()
        case "4":
           analysis_report_menu()
        case "0":
            print("Voltar!")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            __analysis()
    
def __main_menu():
    while True:
        Helper.splash()
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
                users_menu()
            case "3":
                employees_menu()
            case "4":
                __analysis()
            case "0":
                print("Até breve!")
                break
            case _:
                print("[red]Opção inválida![/red]")
                Helper.system_pause()
                __start()
    
if __name__ == "__main__":
    load()