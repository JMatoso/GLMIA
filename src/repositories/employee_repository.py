from entities.employee import Employee
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

EMPLOYEES = []

def __load_data(text = "Gestão de Funcionários"):
    Helper.splash(text)
    global EMPLOYEES
    if EMPLOYEES == []:
        EMPLOYEES = [Employee.from_dict(item) for item in DataContext.load_json(Constants.EMPLOYEE_PATH)]
    print(f"\n[bold]{len(EMPLOYEES)} tipo(s) de funcionários(s) registrado(s) no sistema.[/bold]\n")

def employees_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        employees_menu()
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
            employees_menu()
            
def __insert_employee():
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
        
        salary = input("Salário: ")
        if(Validations.notempty(salary) == False):
            continue
        
        dept = input("Departamento: ")
        if(Validations.isvalidtext(dept, True) == False):
            continue
        
        return Employee(0, Validations.normalize(name),
                        email.lower().strip(), 
                        phone, 
                        Validations.normalize(genre), 
                        salary, 
                        Validations.normalize(dept))
   
def __insert():
    Helper.splash("Inserir Funcionários", "Gestão de Funcionários")
    Helper.new_line()
    EMPLOYEES.append(__insert_employee())
    DataContext.save_json(Constants.EMPLOYEE_PATH, EMPLOYEES)
    Helper.system_pause()
    employees_menu()

def __delete():
    Helper.splash("Eliminar Funcionário", "Gestão de Funcionários")
    Helper.new_line()
    id = input("Id do funcionário a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    employee = DataContext.get_by_id(int(id), EMPLOYEES)
    if employee == None:
        print("[red]O funcionário que pretende eliminar não existe![/red]")
        Helper.system_pause()
        employees_menu()
        return
    
    EMPLOYEES.remove(employee)
    if DataContext.save_json(Constants.EMPLOYEE_PATH, EMPLOYEES) == True:
        print("[green]Funcionário eliminado com sucesso![/green]")
    Helper.system_pause()
    employees_menu()

def __update():
    Helper.splash("Alterar Funcionário", "Gestão de Funcionários")
    Helper.new_line()
    id = input("Id do funcionário a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_employee = DataContext.get_by_id(int(id), EMPLOYEES)
    if old_employee == None:
        print("[red]O funcionário que pretende alterar não existe![/red]")
        Helper.system_pause()
        employees_menu()
        return
    
    Helper.new_line()
    new_employee = __insert_employee()
    new_employee.id = old_employee.get_id()
    
    EMPLOYEES.remove(old_employee)
    EMPLOYEES.append(new_employee)
    
    if DataContext.save_json(Constants.EMPLOYEE_PATH, EMPLOYEES) == True:
        print("[green]Funcionário alterado com sucesso![/green]")
    Helper.system_pause()
    employees_menu()

def __search():
    Helper.splash("Encontrar Funcionários", "Gestão de Funcionários")
    Helper.new_line()
    keyword = input("Nome, departamento (ou em branco para listar todos) > ")    
    __generate_employee_table(DataContext.filter_by_name_or_departament(keyword, EMPLOYEES))
    Helper.pause()
    employees_menu()    

def __generate_employee_table(values):
    Helper.new_line()

    table = Table(title=f"Clientes Encontrados ({len(values)})", show_lines=True, expand=True)
    table.add_column("Id", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Genêro", justify="left", style="white")
    table.add_column("Telefone", justify="left", style="white")
    table.add_column("Email", justify="right", style="white")
    table.add_column("Salário", justify="right", style="white", no_wrap=True)
    table.add_column("Departamento", justify="right", style="white")
    
    for x in sorted(values, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_genre(), 
                      x.get_phone(), 
                      x.get_email(), 
                      Helper.to_currency(x.get_salary()),                      
                      x.get_dept())
    print(table)

if __name__ == "__main__":
    employees_menu()