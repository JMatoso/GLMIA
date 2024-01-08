from entities.analysis import Analysis
from entities.analysis_type import AnalysisType
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print
from rich.columns import Columns

ANALYSIS = []
ANALYSIS_TYPE = []

def __load_data(text = "Gestão de Análises"):
    Helper.splash(text)
    global ANALYSIS
    global ANALYSIS_TYPE
    if ANALYSIS == [] or ANALYSIS_TYPE == []:
        ANALYSIS = [Analysis.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_PATH)]
        ANALYSIS_TYPE = [AnalysisType.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_TYPE_PATH)]
    print(f"\n[bold]{len(ANALYSIS)} análises(s) registrada(s) no sistema.[/bold]\n")

def analysis_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        analysis_menu()
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
            analysis_menu()
            
def __insert_analysis():
    while True:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        price = input("Price: ")
        if(Validations.notempty(price) == False):
            continue
        
        description = input("Description: ")
        if(Validations.notempty(description) == False):
            continue
        
        __generate_analysis_type_table()
        
        analysis_type_id = input("Id do Tipo de Análise: ")
        if(Validations.isnumber(analysis_type_id) == False):
            continue
        
        analysis_type = DataContext.get_by_id(int(analysis_type_id), ANALYSIS_TYPE)
        if analysis_type == None:
            print("[red]O tipo de análise que pretende associar não existe![/red]\n")
            Helper.system_pause()
            continue
        
        return Analysis(0, name, description, price, analysis_type_id)
   
def __insert():
    Helper.splash("Inserir Análise", "Gestão de Análise")
    Helper.new_line()
    ANALYSIS.append(__insert_analysis())
    DataContext.save_json(Constants.ANALYSIS_PATH, ANALYSIS)
    Helper.system_pause()
    analysis_menu()

def __delete():
    Helper.splash("Eliminar Análise", "Gestão de Análise")
    Helper.new_line()
    id = input("Id da análise a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    Analysis = DataContext.get_by_id(int(id), ANALYSIS)
    if Analysis == None:
        print("[red]A análise que pretende eliminar não existe![/red]")
        Helper.system_pause()
        analysis_menu()
        return
    
    ANALYSIS.remove(Analysis)
    if DataContext.save_json(Constants.ANALYSIS_PATH, ANALYSIS) == True:
        print("[green]Análise eliminado com sucesso![/green]")
    Helper.system_pause()
    analysis_menu()

def __update():
    Helper.splash("Alterar Análise", "Gestão de Análises")
    Helper.new_line()
    id = input("Id da análise a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_analysis = DataContext.get_by_id(int(id), ANALYSIS)
    if old_analysis == None:
        print("[red]A análise que pretende alterar não existe![/red]")
        Helper.system_pause()
        analysis_menu()
        return
    
    Helper.new_line()
    new_analysis = __insert_analysis()
    new_analysis.id = old_analysis.get_id()
    
    ANALYSIS.remove(old_analysis)
    ANALYSIS.append(new_analysis)
    
    if DataContext.save_json(Constants.ANALYSIS_PATH, ANALYSIS) == True:
        print("[green]Análise alterada com sucesso![/green]")
    Helper.system_pause()
    analysis_menu()

def __search():
    Helper.splash("Encontrar Análise", "Gestão de Análises")
    Helper.new_line()
    keyword = input("Nome, preço, id do tipo de análise (ou em branco para listar todos) > ")    
    __generate_employee_table(DataContext.filter_by_name_price_or_id(keyword, ANALYSIS), ANALYSIS_TYPE)
    Helper.pause()
    analysis_menu()    

def __generate_analysis_type_table():
    print("\n[bold]Tipos de Análises[/bold]\n")
    for x in sorted(ANALYSIS_TYPE, key=lambda x: x.get_name()):
        print(f"[bold]{x.get_id()}[/bold] - {x.get_name()}")
    print("\n[yellow][bold]Selecione o tipo de análise, informando o seu Id.[/yellow][/bold]\n")
    
def __generate_employee_table(values, analises):
    Helper.new_line()

    table = Table(title=f"Análises Encontrados ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Tipo de Análise", justify="right", style="white")
    table.add_column("Preço", justify="right", style="white", no_wrap=True)
    table.add_column("Descrição", justify="right", style="white")
    
    for x in sorted(values, key=lambda x: x.get_name()):
        analysis_type = DataContext.get_by_id(int(x.get_type_analysis_id()), analises)
        if analysis_type == None:
            analysis_type = AnalysisType(0, "Não Encontrado", "Não Encontrado")
            
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      "{} ({})".format(analysis_type.get_name(), analysis_type.get_id()),
                      Helper.to_currency(x.get_price()),
                      x.get_description())
    
    print(table)

if __name__ == "__main__":
    analysis_menu()