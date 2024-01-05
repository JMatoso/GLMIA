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
    print("5. [cyan]Tipo de Cliente[/cyan]")
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
            __update()
        case "4":
            __search()
        case "5":
            print("Tipo de Cliente")
        case "0":
            print("Voltando ao Menu Inicial...")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            clients_menu()
    
def __delete():
    Helper.splash("Eliminar Cliente")
    Helper.new_line()
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
    Helper.new_line()
    keyword = input("Departamento, Nome (ou em branco para listar todos) > ")    
    __generate_client_table(__filter_client_by_name_or_departament(keyword))
    
    Helper.pause()
    clients_menu()

def __insert_client():
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
        
        return Client(0, Validations.normalize(name),
                              email.lower().strip(), 
                              phone, 
                              Validations.normalize(genre), 
                              birthdate, 
                              Validations.normalize(address), 
                              Validations.normalize(dept))
    
def __insert():
    Helper.splash("Inserir Cliente")
    Helper.new_line()
    CLIENTS.append(__insert_client())
    
    success = DataContext.save_json(Constants.CLIENT_PATH, CLIENTS)
    Helper.system_pause()
    
    clients_menu()

def __update():
    Helper.splash("Alterar Cliente")
    Helper.new_line()
    id = input("Id do cliente a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_client = __get_client_by_id(int(id))
    if old_client == None:
        print("[red]O cliente que pretende alterar não existe![/red]")
        Helper.system_pause()
        clients_menu()
        return
    
    new_client = __insert_client()
    new_client.id = old_client.get_id()
    new_client.created = old_client.get_created()
    
    CLIENTS.remove(old_client)
    CLIENTS.append(new_client)
    
    if DataContext.save_json(Constants.CLIENT_PATH, CLIENTS) == True:
        print("[green]Cliente alterado com sucesso![/green]")
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