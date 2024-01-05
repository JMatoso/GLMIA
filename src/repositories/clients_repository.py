from entities.client import Client
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

CLIENTS = []

def __load_data(text = "Gestão de Clientes"):
    Helper.splash(text)
    
    global CLIENTS
    if CLIENTS == []:
        CLIENTS = [Client.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_PATH)]
    print(f"\n[bold]{len(CLIENTS)} cliente(s) registrado(s) no sistema.[/bold]\n")
    
def clients_menu():
    __load_data()
    
    print("1. [cyan]Inserir[/cyan]")
    print("2. [red]Eliminar[/red]")
    print("3. [cyan]Alterar[/cyan]")
    print("4. [cyan]Filtrar[/cyan]")
    print("0. [red]Voltar[/red] ao Menu Inicial")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        clients_menu()
        return
    
    match choice:
        case "1":
            __insert()
        case "2":
            __delete()
        case "3":
            print("Alterar")
        case "4":
            __search()
        case "0":
            print("Sair")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            clients_menu()
    
def __delete():
    Helper.splash("Eliminar Cliente")
    
    id = input("Id do cliente a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    client = __get_client_by_id(int(id))
    if client == None:
        print("[red]O cliente que pretende eliminar não existe![/red]")
        Helper.system_pause()
        clients_menu()
        return
    
    CLIENTS.remove(client)
    if DataContext.save_json(Constants.CLIENT_PATH, CLIENTS) == True:
        print("[green]Cliente eliminado com sucesso![/green]")
    Helper.system_pause()
    clients_menu()
    
def __search():
    Helper.splash("Encontrar Clientes")
    
    keyword = input("Departamento, Nome (ou em branco para listar todos) > ")    
    __generate_client_table(__filter_client_by_name_or_departament(keyword))
    
    Helper.pause()
    clients_menu()

def __insert():
    Helper.new_line()
    Helper.splash("Inserir Cliente")
    success = False
    
    while success == False:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        email = input("Email: ")
        if(Validations.isvalidemail(email) == False):
            continue
        
        phone = input("Telefone: ")
        if(Validations.isnumber(phone) == False):
            continue
        
        genre = input("Género: ")
        
        birthdate = input("Data de Nascimento (dia/mês/ano): ")
        if(Validations.isvaliddate(birthdate) == False):
            continue
        
        address = input("Morada: ")
        if(Validations.notempty(address) == False):
            continue
        
        dept = input("Departamento: ")
        if(Validations.isvalidtext(dept, True) == False):
            continue
        
        CLIENTS.append(Client(0, Validations.normalize(name),
                              email.lower().strip(), 
                              phone, 
                              Validations.normalize(genre), 
                              birthdate, 
                              Validations.normalize(address), 
                              Validations.normalize(dept)))
        
        success = DataContext.save_json(Constants.CLIENT_PATH, CLIENTS)
        Helper.system_pause()
    
    clients_menu()

def __filter_client_by_name_or_departament(value):
    if Validations.isempty(value) == True:
        return CLIENTS
    
    return filter(lambda x: x.get_name() == value or x.get_dept() == value, CLIENTS)
    
def __get_client_by_id(id):    
    return next((x for x in CLIENTS if x.get_id() == id), None)

def __generate_client_table(values):
    Helper.new_line()
    
    result = list(values)

    table = Table(title=f"Clientes Encontrados ({len(result)})", show_lines=True)
    
    table.add_column("Id", justify="left", style="cyan", no_wrap=True)
    
    table.add_column("Nome", style="cyan")
    table.add_column("Genêro", justify="left", style="white")
    table.add_column("Nascimento", justify="left", style="white", no_wrap=True)
    
    table.add_column("Email", justify="right", style="white")
    table.add_column("Telefone", justify="right", style="white")
    table.add_column("Endereço", justify="right", style="white")
    
    table.add_column("Departamento", justify="right", style="white")
    
    for x in sorted(result, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_genre(), 
                      x.get_birthdate(), 
                      x.get_email(), 
                      x.get_phone(), 
                      x.get_address(),                      
                      x.get_dept())
    
    print(table)
    
if __name__ == "__main__":
    clients_menu()