from entities.client import Client
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich import print

CLIENTS = []

def LoadData():
    global CLIENTS
    if CLIENTS == []:
        CLIENTS = [Client.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_PATH)]
    print(f"\n[bold]{len(CLIENTS)} cliente(s) registrado(s) no sistema.[/bold]\n")
    
def ClientsMenu():
    Helper.Splash("Gestão de Clientes")
    
    LoadData()
    
    print("[bold]1. [cyan]Inserir[/cyan][/bold]")
    print("[bold]2. [cyan]Eliminar[/cyan][/bold]")
    print("[bold]3. [cyan]Alterar[/cyan][/bold]")
    print("[bold]4. [cyan]Filtrar[/cyan][/bold]")
    print("[bold]0. [red]Voltar[/red] ao Menu Inicial[/bold]")
    
    choice = input("> ")
    if Validations.IsNumber(choice) == False:
        Helper.SystemPause()
        ClientsMenu()
        return
    
    match choice:
        case "1":
            InsertClient()
        case "2":
            print("Eliminar")
        case "3":
            print("Alterar")
        case "4":
            print("Filtrar")
        case "0":
            print("Sair")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.SystemPause()
            ClientsMenu()
    
def InsertClient():
    Helper.NewLine()
    Helper.Splash("Inserir Cliente")
    success = False
    
    while success == False:
        name = input("Nome: ")
        if(Validations.IsValidText(name) == False):
            continue
        
        email = input("Email: ")
        if(Validations.IsValidEmail(email) == False):
            continue
        
        phone = input("Telefone: ")
        if(Validations.IsNumber(phone) == False):
            continue
        
        genre = input("Género: ")
        
        birthdate = input("Data de Nascimento (dia/mês/ano): ")
        if(Validations.IsValidDate(birthdate) == False):
            continue
        
        address = input("Morada: ")
        if(Validations.IsNotEmpty(address) == False):
            continue
        
        dept = input("Departamento: ")
        if(Validations.IsValidText(dept, True) == False):
            continue
        
        CLIENTS.append(Client(Validations.Normalize(name),
                              email.lower().strip(), 
                              phone, 
                              Validations.Normalize(genre), 
                              birthdate, 
                              Validations.Normalize(address), 
                              Validations.Normalize(dept)))
        
        success = DataContext.save_json(Constants.CLIENT_PATH, CLIENTS)
        Helper.SystemPause()
    
    ClientsMenu()

if __name__ == "__main__":
    ClientsMenu()