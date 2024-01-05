from entities.user import User
from options.constants import *
from helpers.helper import Helper
from helpers.validations import Validations
from services.data_context import DataContext

from rich.table import Table
from rich import print

USERS = []

def __load_data(text = "Gestão de Utilizadores"):
    Helper.splash(text)
    global USERS
    if USERS == []:
        USERS = [User.from_dict(item) for item in DataContext.load_json(Constants.USER_PATH)]
    print(f"\n[bold]{len(USERS)} utilizadores(s) registrado(s) no sistema.[/bold]\n")

def users_menu():
    __load_data()
    
    print("1. Inserir")
    print("2. Alterar")
    print("3. Filtrar")
    print("4. [red]Eliminar[/red]")
    print("0. Voltar ao Menu Inicial")
    
    choice = input("> ")
    if Validations.isnumber(choice) == False:
        Helper.system_pause()
        users_menu()
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
            users_menu()
            
def __insert_user():
    while True:
        name = input("Nome: ")
        if(Validations.isvalidtext(name) == False):
            continue
        
        email = input("Email: ")
        if(Validations.isvalidemail(email) == False):
            continue
        
        return User(0, Validations.normalize(name), email.lower().strip())
   
def __insert():
    Helper.splash("Inserir Utilizadores", "Gestão de Utlizadores")
    Helper.new_line()
    USERS.append(__insert_user())
    DataContext.save_json(Constants.USER_PATH, USERS)
    Helper.system_pause()
    users_menu()

def __delete():
    Helper.splash("Eliminar Utilizador", "Gestão de Utlizadores")
    Helper.new_line()
    id = input("Id do utilizador a eliminar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __delete()
        return
    
    User = DataContext.get_by_id(int(id), USERS)
    if User == None:
        print("[red]O utlizador que pretende eliminar não existe![/red]")
        Helper.system_pause()
        users_menu()
        return
    
    USERS.remove(User)
    if DataContext.save_json(Constants.USER_PATH, USERS) == True:
        print("[green]Utilizador eliminado com sucesso![/green]")
    Helper.system_pause()
    users_menu()

def __update():
    Helper.splash("Alterar Utilizador", "Gestão de Utlizadores")
    Helper.new_line()
    id = input("Id do utilizador a alterar > ")
    if(Validations.isnumber(id) == False):
        Helper.system_pause()
        __update()
        return
    
    old_user = DataContext.get_by_id(int(id), USERS)
    if old_user == None:
        print("[red]O utilizador que pretende alterar não existe![/red]")
        Helper.system_pause()
        users_menu()
        return
    
    Helper.new_line()
    new_user = __insert_user()
    new_user.id = old_user.get_id()
    
    USERS.remove(old_user)
    USERS.append(new_user)
    
    if DataContext.save_json(Constants.USER_PATH, USERS) == True:
        print("[green]Utilizador alterado com sucesso![/green]")
    Helper.system_pause()
    users_menu()

def __search():
    Helper.splash("Encontrar Utilizador", "Gestão de Utilizadores")
    Helper.new_line()
    keyword = input("Nome (ou em branco para listar todos) > ")    
    __generate_employee_table(DataContext.filter_type_by_name(keyword, USERS))
    Helper.pause()
    users_menu()    

def __generate_employee_table(values):
    Helper.new_line()

    table = Table(title=f"Utilizadores Encontrados ({len(values)})", show_lines=True)
    table.add_column("Id", justify="left", style="cyan", no_wrap=True)
    table.add_column("Nome", style="cyan")
    table.add_column("Email", justify="left", style="white")
    table.add_column("Função", justify="left", style="white")
    
    for x in sorted(values, key=lambda x: x.get_name()):
        table.add_row(str(x.get_id()), 
                      x.get_name(), 
                      x.get_email(), 
                      x.get_role())
    
    print(table)

if __name__ == "__main__":
    users_menu()