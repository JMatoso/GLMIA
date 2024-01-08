from entities.analysis_request import AnalysisRequest
from entities.analysis_report import AnalysisReport
from entities.analysis_type import AnalysisType
from entities.client import Client
from entities.client_type import ClientType
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

from reportlab.pdfgen import canvas

ANALYSIS = []
ANALYSIS_TYPE = []
ANALYSIS_REPORTS = []
CLIENTS = []
CLIENT_TYPES = []

def __load_data(text = "Resultados das Análises"):
    Helper.splash(text)
    global ANALYSIS
    global ANALYSIS_TYPE
    global CLIENTS
    global CLIENT_TYPES
    global ANALYSIS_REPORTS
    if ANALYSIS == [] or ANALYSIS_TYPE == [] or CLIENTS == [] or CLIENT_TYPES == [] or ANALYSIS_REPORTS == []:
        ANALYSIS = [AnalysisRequest.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_REQUEST_PATH)]
        ANALYSIS_TYPE = [AnalysisType.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_TYPE_PATH)]
        CLIENTS = [Client.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_PATH)]
        CLIENT_TYPES = [ClientType.from_dict(item) for item in DataContext.load_json(Constants.CLIENT_TYPES_PATH)]
        ANALYSIS_REPORTS = [AnalysisReport.from_dict(item) for item in DataContext.load_json(Constants.ANALYSIS_REPORT_PATH)]
    print(f"\n[bold]{len(ANALYSIS_REPORTS)} resultado(s) registrada(s) no sistema.[/bold]\n")

def analysis_report_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("5. Exportar para PDF")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        analysis_report_menu()
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
            __exportToPdf()
        case "0":
            print("Voltando ao Menu Inicial...")
        case _:
            print("[red]Opção inválida![/red]")
            Helper.system_pause()
            analysis_report_menu()
            
def __insert_report():
    while True:        
        analysis_request_id = input("Id do pedido de análise > ")
        if(Validations.isnumber(analysis_request_id) == False):
            continue
        
        analysis_request = DataContext.get_by_id(int(analysis_request_id), ANALYSIS)
        if analysis_request == None:
            print("[red]O pedido de análise que pretende não existe![/red]")
            Helper.system_pause()
            analysis_report_menu()
            return
        
        description = input("Descrição > ")
        if(Validations.notempty(description) == False):
            continue
        
        positive = DataContext.get_positive_report()
        
        return AnalysisReport(0, analysis_request.get_type_analysis_id(), analysis_request.get_client_id(), analysis_request.get_client_type_id(), description, positive)
   
def __insert():
    Helper.splash("Criar Pedido de Análise", "Resultados das Análises")
    Helper.new_line()
    ANALYSIS_REPORTS.append(__insert_report())
    DataContext.save_json(Constants.ANALYSIS_REPORT_PATH, ANALYSIS_REPORTS)
    Helper.system_pause()
    analysis_report_menu()

def __delete():
    Helper.splash("Eliminar Resultado", "Resultados das Análises")
    Helper.new_line()
    id = input("Id do resultado a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    analysis = DataContext.get_by_id(int(id), ANALYSIS_REPORTS)
    if analysis == None:
        print("[red]O resultado que pretende eliminar não existe![/red]")
        Helper.system_pause()
        analysis_report_menu()
        return
    
    ANALYSIS_REPORTS.remove(analysis)
    if DataContext.save_json(Constants.ANALYSIS_REPORT_PATH, ANALYSIS_REPORTS) == True:
        print("[green]Resultado eliminado com sucesso![/green]")
    Helper.system_pause()
    analysis_report_menu()

def __update():
    Helper.splash("Alterar Pedido de Análise", "Resultados das Análises")
    Helper.new_line()
    id = input("Id do resultado a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_analysis = DataContext.get_by_id(int(id), ANALYSIS_REPORTS)
    if old_analysis == None:
        print("[red]O resultado que pretende alterar não existe![/red]")
        Helper.system_pause()
        analysis_report_menu()
        return
    
    
    Helper.new_line()
    new_analysis = __insert_report()
    new_analysis.id = old_analysis.get_id()
    new_analysis.created = old_analysis.get_created()
    
    ANALYSIS_REPORTS.remove(old_analysis)
    ANALYSIS_REPORTS.append(new_analysis)
    
    if DataContext.save_json(Constants.ANALYSIS_REPORT_PATH, ANALYSIS_REPORTS) == True:
        print("[green]Resultado alterado com sucesso![/green]")
    Helper.system_pause()
    analysis_report_menu()

def __search():
    Helper.splash("Encontrar Resultados", "Resultados das Análises")
    Helper.new_line()
    keyword = input("Tipo de análise, tipo de cliente, cliente, data (ou em branco para listar todos) > ")    
    __generate_employee_table(DataContext.filter_analysis_request(keyword, ANALYSIS_REPORTS), ANALYSIS_TYPE, CLIENTS, CLIENT_TYPES)
    Helper.pause()
    analysis_report_menu()    

def __exportToPdf():
    Helper.splash("Exportar Resultados", "Resultados das Análises")
    Helper.new_line()
    
    id = input("Id do resultado a exportar para PDF > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    analysis = DataContext.get_by_id(int(id), ANALYSIS_REPORTS)
    if analysis == None:
        print("[red]O resultado que pretende exportar não existe![/red]")
        Helper.system_pause()
        analysis_report_menu()
        return
    
    try:
        name = f"{analysis.get_id()}-{Helper.get_ticks_string()}.pdf"
        pdf = canvas.Canvas(name)
        x = 720
        
        pdf.setTitle(f'Nº {analysis.get_id()}')
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100,770, f'Relatório de Resultado de Análise ({analysis.get_id()})')
        pdf.setFont("Helvetica-Bold", 12)
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100,724, 'Cliente')
        client = __get_client(analysis.get_client_id())
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100,700, f'Nome: {client.get_name()}')
        pdf.drawString(100,680, f'Nascimento: {Helper.to_date(client.get_birthdate())}')
        pdf.drawString(100,660, f'Gênero: {client.get_genre()}')
        pdf.drawString(100,640, f'Telefone: {client.get_phone()}')
        pdf.drawString(100,620, f'Email: {client.get_email()}')
        pdf.drawString(100,600, f'Endereço: {client.get_address()}')
        pdf.drawString(100,580, f'Departamento: {client.get_dept()}')
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100,540, 'Tipo de Cliente')
        client_type = __get_client_type(analysis.get_client_type_id())
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100,520, f'Nome: {client_type.get_name()}')
        pdf.drawString(100,500, f'Descrição: {client_type.get_description()}')
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100,460, 'Tipo de Análise')
        analysis_type = __get_analysis_type(analysis.get_type_analysis_id())
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100,440, f'Tipo: {analysis_type.get_name()}')
        pdf.drawString(100,420, f'Descrição: {analysis_type.get_description()}')
        pdf.drawString(100,400, f'Preço: {Helper.to_currency(analysis_type.get_price())}')
        
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100,360, 'Resultado')
        
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100,340, f'Descrição: {analysis.get_description()}')
        pdf.drawString(100,320, f'Positivo: {"Sim" if analysis.get_positive() == True else "Não"}')
        
        pdf.drawString(100,280, f'Data: {Helper.to_date(analysis.get_created())}')
        
        pdf.save()
        
        print(f'[green]{name} criado com sucesso![/green]')
        Helper.pause()
    except Exception as e:
        print(e)
        print("[red]Ocorreu um erro ao exportar o resultado![/red]")
        Helper.pause()

def __generate_employee_table(values, analises, clients, client_types):
    Helper.new_line()

    table = Table(title=f"Resultados Encontrados ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Positivo", justify="center", style="white")
    table.add_column("Descrição", justify="left", style="white")
    table.add_column("Tipo de Análise", justify="right", style="white")
    table.add_column("Tipo de Cliente", justify="right", style="white")
    table.add_column("Cliente", justify="right", style="white")
    table.add_column("Data", justify="center", style="white", no_wrap=True)
    
    for x in sorted(values, key=lambda x: x.get_created(), reverse=True):
        analysis_type = __get_analysis_type(x.get_type_analysis_id())
        client_type = __get_client_type(x.get_client_type_id())
        client = __get_client(x.get_client_id())
            
        table.add_row(str(x.get_id()), 
                      "Sim" if x.get_positive() == True else "Não",
                       Validations.normalize(x.get_description(), False),
                      "{} ({})".format(analysis_type.get_name(), analysis_type.get_id()),
                      "{} ({})".format(client_type.get_name(), client_type.get_id()),
                      "{} ({})".format(client.get_name(), client.get_id()),
                      Helper.to_date(x.get_created()))
    
    print(table)

def __get_client(client_id):
    client = DataContext.get_by_id(int(client_id), CLIENTS)
    if client == None:
        return Client(0, "Não Encontrado", "", "", "", "", "", "")
    return client

def __get_client_type(client_type_id):
    client_type = DataContext.get_by_id(int(client_type_id), CLIENT_TYPES)
    if client_type == None:
        return ClientType(0, "Não Encontrado", "")
    return client_type

def __get_analysis_type(analysis_type_id):
    analysis_type = DataContext.get_by_id(int(analysis_type_id), ANALYSIS_TYPE)
    if analysis_type == None:
        return AnalysisType(0, "Não Encontrado", "Não Encontrado")
    return analysis_type

if __name__ == "__main__":
    analysis_report_menu()