from entities.analysis_type import AnalysisType
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

ANALYSIS_TYPE = []

def __load_data(text = "Gestão de Tipo de Análises"):
    Helper.splash(text)
    global ANALYSIS_TYPE
    if ANALYSIS_TYPE == []:
        ANALYSIS_TYPE = [AnalysisType.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_TYPE_PATH)]
    print(f"\n[bold]{len(ANALYSIS_TYPE)} tipo(s) de análise(s) registrada(s) no sistema.[/bold]\n")

def analysis_type_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        analysis_type_menu()
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
            analysis_type_menu()
            
def __insert_analysis_type():
    while True:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        description = input("Descrição: ")
        if(Validations.notempty(description) == False):
            continue
        
        price = input("Preço: ")
        if(Validations.notempty(price) == False):
            continue
        
        return AnalysisType(0, Validations.normalize(name), Validations.normalize(description, False), price)
   
def __insert():
    Helper.splash("Inserir Tipo de Análise", "Tipo de Análise")
    Helper.new_line()
    ANALYSIS_TYPE.append(__insert_analysis_type())
    DataContext.save_json(Constants.ANALYSIS_TYPE_PATH, ANALYSIS_TYPE)
    Helper.system_pause()
    analysis_type_menu()

def __delete():
    Helper.splash("Eliminar Tipo de Análise", "Tipo de Análise")
    Helper.new_line()
    id = input("Id do tipo de análise a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    client_type = DataContext.get_by_id(int(id), ANALYSIS_TYPE)
    if client_type == None:
        print("[red]O tipo de análise que pretende eliminar não existe![/red]")
        Helper.system_pause()
        analysis_type_menu()
        return
    
    ANALYSIS_TYPE.remove(client_type)
    if DataContext.save_json(Constants.ANALYSIS_TYPE_PATH, ANALYSIS_TYPE) == True:
        print("[green]Tipo de análise eliminado com sucesso![/green]")
    Helper.system_pause()
    analysis_type_menu()

def __update():
    Helper.splash("Alterar Tipo de Análise", "Tipo de Análise")
    Helper.new_line()
    id = input("Id do tipo de análise a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_analysis_type = DataContext.get_by_id(int(id), ANALYSIS_TYPE)
    if old_analysis_type == None:
        print("[red]O tipo de análise que pretende alterar não existe![/red]")
        Helper.system_pause()
        analysis_type_menu()
        return
    
    Helper.new_line()
    new_analysis_type = __insert_analysis_type()
    new_analysis_type.id = old_analysis_type.get_id()
    
    ANALYSIS_TYPE.remove(old_analysis_type)
    ANALYSIS_TYPE.append(new_analysis_type)
    
    if DataContext.save_json(Constants.ANALYSIS_TYPE_PATH, ANALYSIS_TYPE) == True:
        print("[green]Tipo de análise alterado com sucesso![/green]")
    Helper.system_pause()
    analysis_type_menu()

def __search():
    Helper.splash("Encontrar Tipo de Análise", "Tipo de Análise")
    Helper.new_line()
    keyword = input("Nome, preço (ou em branco para listar todos) > ")    
    __generate_client_table(DataContext.filter_by_name_or_price(keyword, ANALYSIS_TYPE))
    Helper.pause()
    analysis_type_menu()    

def __generate_client_table(values):
    Helper.new_line()

    table = Table(title=f"Tipo de Análises Encontradas ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Descrição", justify="right", style="white")
    table.add_column("Preço", justify="right", style="white", no_wrap=True)
    
    for x in sorted(values, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_description(),
                      Helper.to_currency(x.get_price()))
    print(table)

if __name__ == "__main__":
    analysis_type_menu()