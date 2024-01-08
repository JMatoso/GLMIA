from entities.client_type import ClientType
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

CLIENT_TYPES = []

def __load_data(text = "Gestão de Tipo de Clientes"):
    Helper.splash(text)
    global CLIENT_TYPES
    if CLIENT_TYPES == []:
        CLIENT_TYPES = [ClientType.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_TYPES_PATH)]
    print(f"\n[bold]{len(CLIENT_TYPES)} tipo(s) de cliente(s) registrado(s) no sistema.[/bold]\n")

def clients_type_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        clients_type_menu()
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
        case "0":
            print("Voltando ao Menu Inicial...")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            clients_type_menu()
            
def __insert_client_type():
    while True:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        description = input("Descrição: ")
        if(Validations.notempty(description) == False):
            continue
        
        return ClientType(0, Validations.normalize(name), Validations.normalize(description, False))
   
def __insert():
    Helper.splash("Inserir Tipo de Cliente", "Tipo de Clientes")
    Helper.new_line()
    CLIENT_TYPES.append(__insert_client_type())
    DataContext.save_json(Constants.CLIENT_TYPES_PATH, CLIENT_TYPES)
    Helper.system_pause()
    clients_type_menu()

def __delete():
    Helper.splash("Eliminar Tipo de Cliente", "Tipo de Clientes")
    Helper.new_line()
    id = input("Id do tipo de cliente a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    client_type = DataContext.get_by_id(int(id), CLIENT_TYPES)
    if client_type == None:
        print("[red]O tipo de cliente que pretende eliminar não existe![/red]")
        Helper.system_pause()
        clients_type_menu()
        return
    
    CLIENT_TYPES.remove(client_type)
    if DataContext.save_json(Constants.CLIENT_TYPES_PATH, CLIENT_TYPES) == True:
        print("[green]Tipo cliente eliminado com sucesso![/green]")
    Helper.system_pause()
    clients_type_menu()

def __update():
    Helper.splash("Alterar Tipo Cliente", "Tipo de Clientes")
    Helper.new_line()
    id = input("Id do tipo de cliente a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_client_type = DataContext.get_by_id(int(id), CLIENT_TYPES)
    if old_client_type == None:
        print("[red]O tipo de cliente que pretende alterar não existe![/red]")
        Helper.system_pause()
        clients_type_menu()
        return
    
    Helper.new_line()
    new_client_type = __insert_client_type()
    new_client_type.id = old_client_type.get_id()
    
    CLIENT_TYPES.remove(old_client_type)
    CLIENT_TYPES.append(new_client_type)
    
    if DataContext.save_json(Constants.CLIENT_TYPES_PATH, CLIENT_TYPES) == True:
        print("[green]Tipo de cliente alterado com sucesso![/green]")
    Helper.system_pause()
    clients_type_menu()

def __search():
    Helper.splash("Encontrar Tipo de Clientes", "Tipo de Clientes")
    Helper.new_line()
    keyword = input("Nome (ou em branco para listar todos) > ")    
    __generate_client_table(DataContext.filter_type_by_name(keyword, CLIENT_TYPES))
    Helper.pause()
    clients_type_menu()    

def __generate_client_table(values):
    Helper.new_line()

    table = Table(title=f"Tipo de Clientes Encontrados ({len(values)})", show_lines=True, expand=True)

    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Descrição", justify="left", style="white")
    
    for x in sorted(values, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_description())
    print(table)

if __name__ == "__main__":
    clients_type_menu()