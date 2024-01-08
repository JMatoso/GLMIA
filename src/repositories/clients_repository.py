from entities.client import Client
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext
from repositories.client_type_repository import clients_type_menu

from rich.table import Table
from rich import print

CLIENTS = []

def __load_data(text = "Gestão de Clientes", title = "AED"):
    Helper.splash(text, title)
    global CLIENTS
    if CLIENTS == []:
        CLIENTS = [Client.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_PATH)]
    print(f"\n[bold]{len(CLIENTS)} cliente(s) registrado(s) no sistema.[/bold]\n")
    
def clients_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("5. Tipo de Cliente")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        clients_menu()
        return
    
    match choice:
        case "1":
            __insert()
        case "2":
            __update()
        case "3":
            __search()
        case "4":
            __delete()
        case "5":
            clients_type_menu()
        case "0":
            print("Voltando ao Menu Inicial...")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            clients_menu()
    
def __delete():
    Helper.splash("Eliminar Cliente", "Clientes")
    Helper.new_line()
    id = input("Id do cliente a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    client = DataContext.get_by_id(int(id), CLIENTS)
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
    Helper.splash("Encontrar Clientes", "Clientes")
    Helper.new_line()
    keyword = input("Departamento, Nome (ou em branco para listar todos) > ")    
    __generate_client_table(DataContext.filter_by_name_or_departament(keyword, CLIENTS))
    Helper.pause()
    clients_menu()

def __insert_client():
    while True:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        email = input("Email: ")
        if(Validations.isvalidemail(email) == False):
            continue
        
        phone = input("Telefone: ")
        if(Validations.isvalidphone(phone) == False):
            continue
        
        genre = DataContext.get_genre()
        
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
    Helper.splash("Inserir Cliente", "Clientes")
    Helper.new_line()
    CLIENTS.append(__insert_client())
    DataContext.save_json(Constants.CLIENT_PATH, CLIENTS)
    Helper.system_pause()
    clients_menu()

def __update():
    Helper.splash("Alterar Cliente", "Clientes")
    Helper.new_line()
    id = input("Id do cliente a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_client = DataContext.get_by_id(int(id), CLIENTS)
    if old_client == None:
        print("[red]O cliente que pretende alterar não existe![/red]")
        Helper.system_pause()
        clients_menu()
        return
    
    Helper.new_line()
    new_client = __insert_client()
    new_client.id = old_client.get_id()
    
    CLIENTS.remove(old_client)
    CLIENTS.append(new_client)
    
    if DataContext.save_json(Constants.CLIENT_PATH, CLIENTS) == True:
        print("[green]Cliente alterado com sucesso![/green]")
    Helper.system_pause()
    clients_menu()
    
def __generate_client_table(values):
    Helper.new_line()

    table = Table(title=f"Clientes Encontrados ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Genêro", justify="left", style="white")
    table.add_column("Nascimento", justify="left", style="white", no_wrap=True)
    table.add_column("Telefone", justify="left", style="white")
    table.add_column("Email", justify="right", style="white")
    table.add_column("Endereço", justify="right", style="white")
    table.add_column("Departamento", justify="right", style="white")
    
    for x in sorted(values, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_genre(), 
                      Helper.to_date(x.get_birthdate()), 
                      x.get_phone(), 
                      x.get_email(), 
                      x.get_address(),                      
                      x.get_dept())
    print(table)
    
if __name__ == "__main__":
    clients_menu()