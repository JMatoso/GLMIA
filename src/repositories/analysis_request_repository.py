from entities.analysis_request import AnalysisRequest
from entities.analysis_type import AnalysisType
from entities.client import Client
from entities.client_type import ClientType
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

ANALYSIS = []
ANALYSIS_TYPE = []
CLIENTS = []
CLIENT_TYPES = []

def __load_data(text = "Gestão de Pedidos de Análise"):
    Helper.splash(text)
    global ANALYSIS
    global ANALYSIS_TYPE
    global CLIENTS
    global CLIENT_TYPES
    if ANALYSIS == [] or ANALYSIS_TYPE == [] or CLIENTS == [] or CLIENT_TYPES == []:
        ANALYSIS = [AnalysisRequest.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_REQUEST_PATH)]
        ANALYSIS_TYPE = [AnalysisType.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_TYPE_PATH)]
        CLIENTS = [Client.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_PATH)]
        CLIENT_TYPES = [ClientType.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_TYPES_PATH)]
    print(f"\n[bold]{len(ANALYSIS)} pedidos de análises(s) registrada(s) no sistema.[/bold]\n")

def analysis_request_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        analysis_request_menu()
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
            analysis_request_menu()
            
def __insert_analysis():
    while True:        
        __generate_analysis_type_table()
        type_analysis_id = input("Id do Tipo de Análise: ")
        if(Validations.isnumber(type_analysis_id) == False):
            continue
        
        analysis_type = DataContext.get_by_id(int(type_analysis_id), ANALYSIS_TYPE)
        if analysis_type == None:
            print("[red]O tipo de análise que pretende associar não existe![/red]\n")
            Helper.system_pause()
            continue
        
        __generate_client_table()
        client_id = input("Id do Cliente: ")
        if(Validations.isnumber(client_id) == False):
            continue
        
        client = DataContext.get_by_id(int(client_id), CLIENTS)
        if client == None:
            print("[red]O cliente que pretende associar não existe![/red]\n")
            Helper.system_pause()
            continue
        
        __generate_client_type_table()
        client_type_id = input("Id do Tipo de Cliente: ")
        if(Validations.isnumber(client_type_id) == False):
            continue
        client_type = DataContext.get_by_id(int(client_type_id), CLIENT_TYPES)
        if client_type == None:
            print("[red]O tipo de cliente que pretende associar não existe![/red]\n")
            Helper.system_pause()
            continue
        
        return AnalysisRequest(0, type_analysis_id, client_id, client_type_id)
   
def __insert():
    Helper.splash("Criar Pedido de Análise", "Gestão de Pedidos de Análise")
    Helper.new_line()
    ANALYSIS.append(__insert_analysis())
    DataContext.save_json(Constants.ANALYSIS_REQUEST_PATH, ANALYSIS)
    Helper.system_pause()
    analysis_request_menu()

def __delete():
    Helper.splash("Eliminar Pedido de Análise", "Gestão de Análise")
    Helper.new_line()
    id = input("Id do pedido a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    analysis = DataContext.get_by_id(int(id), ANALYSIS)
    if analysis == None:
        print("[red]O pedido de análise que pretende eliminar não existe![/red]")
        Helper.system_pause()
        analysis_request_menu()
        return
    
    ANALYSIS.remove(analysis)
    if DataContext.save_json(Constants.ANALYSIS_REQUEST_PATH, ANALYSIS) == True:
        print("[green]Pedido de análise eliminado com sucesso![/green]")
    Helper.system_pause()
    analysis_request_menu()

def __update():
    Helper.splash("Alterar Pedido de Análise", "Gestão de Pedidos de Análises")
    Helper.new_line()
    id = input("Id da análise a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_analysis = DataContext.get_by_id(int(id), ANALYSIS)
    if old_analysis == None:
        print("[red]O pedido que pretende alterar não existe![/red]")
        Helper.system_pause()
        analysis_request_menu()
        return
    
    Helper.new_line()
    new_analysis = __insert_analysis()
    new_analysis.id = old_analysis.get_id()
    new_analysis.created = old_analysis.get_created()
    
    ANALYSIS.remove(old_analysis)
    ANALYSIS.append(new_analysis)
    
    if DataContext.save_json(Constants.ANALYSIS_REQUEST_PATH, ANALYSIS) == True:
        print("[green]Pedido alterado com sucesso![/green]")
    Helper.system_pause()
    analysis_request_menu()

def __search():
    Helper.splash("Encontrar Pedidos de Análise", "Gestão de Pedidos de Análises")
    Helper.new_line()
    keyword = input("Nome, preço, tipo de análise, data (ou em branco para listar todos) > ")    
    __generate_employee_table(DataContext.filter_analysis_request(keyword, ANALYSIS), ANALYSIS_TYPE, CLIENTS, CLIENT_TYPES)
    Helper.pause()
    analysis_request_menu()    

def __generate_analysis_type_table():
    print("\n[bold]Tipos de Análises[/bold]\n")
    for x in sorted(ANALYSIS_TYPE, key=lambda x: x.get_name()):
        print(f"[bold]{x.get_id()}[/bold] - {x.get_name()}")
    print("\n[yellow][bold]Selecione o tipo de análise, informando o seu Id.[/yellow][/bold]\n")
    
def __generate_client_table():
    print("\n[bold]Clientes[/bold]\n")
    for x in sorted(CLIENTS, key=lambda x: x.get_name()):
        print(f"[bold]{x.get_id()}[/bold] - {x.get_name()}")
    print("\n[yellow][bold]Selecione o cliente, informando o seu Id.[/yellow][/bold]\n")
    
def __generate_client_type_table():
    print("\n[bold]Tipos de Cliente[/bold]\n")
    for x in sorted(CLIENT_TYPES, key=lambda x: x.get_name()):
        print(f"[bold]{x.get_id()}[/bold] - {x.get_name()}")
    print("\n[yellow][bold]Selecione o tipo de cliente, informando o seu Id.[/yellow][/bold]\n")
    
def __generate_employee_table(values, analises, clients, client_types):
    Helper.new_line()

    table = Table(title=f"Pedidos de Análise Encontrados ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Tipo de Análise", justify="right", style="white")
    table.add_column("Tipo de Cliente", justify="right", style="white")
    table.add_column("Cliente", justify="right", style="white")
    table.add_column("Data", justify="center", style="white", no_wrap=True)
    
    for x in sorted(values, key=lambda x: x.get_created(), reverse=True):
        analysis_type = DataContext.get_by_id(int(x.get_type_analysis_id()), analises)
        if analysis_type == None:
            analysis_type = AnalysisType(0, "Não Encontrado", "Não Encontrado")
            
        client_type = DataContext.get_by_id(int(x.get_client_type_id()), client_types)
        if client_type == None:
            client_type = ClientType(0, "Não Encontrado")
            
        client = DataContext.get_by_id(int(x.get_client_id()), clients)
        if client == None:
            client = Client(0, "Não Encontrado")
            
        table.add_row(str(x.get_id()), 
                      "{} ({})".format(analysis_type.get_name(), analysis_type.get_id()),
                      "{} ({})".format(client_type.get_name(), client_type.get_id()),
                      "{} ({})".format(client.get_name(), client.get_id()),
                      Helper.to_date(x.get_created()))
    
    print(table)

if __name__ == "__main__":
    analysis_request_menu()