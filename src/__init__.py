from rich import print
from helpers.helper import Helper
from helpers.validations import Validations
from controllers.clients_controller import ClientsMenu

def Load():
    Start()
    
def Start():
    Helper.Splash()
    MainMenu()
    
def MainMenu():
    print("\n[bold]1. Gestão de [cyan]Clientes[/cyan][/bold]")
    print("[bold]2. Gestão de [cyan]Utilizadores[/cyan][/bold]")
    print("[bold]3. Gestão de [cyan]Funcionários[/cyan][/bold]")
    print("[bold]4. Gestão de [cyan]Análises[/cyan][/bold]")
    print("[bold]0. [red]Sair[/red][/bold]")
    
    choice = input("> ")
    if Validations.IsNumber(choice) == False:
        Helper.SystemPause()
        Start()
        return
    
    match choice:
        case "1":
            ClientsMenu()
        case "2":
            print("Análises")
        case "3":
            print("Sair")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.SystemPause()
            Start()
    
if __name__ == "__main__":
    Load()