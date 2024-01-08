import os
import json

from rich import print
from helpers.validations import Validations

class DataContext:
    @staticmethod
    def load_json(path):
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                return data
            else:
                DataContext.save_json(path, [])
                return []
        except Exception as error:
            print("\n[red]Ocorreu um erro ao carregar os dados: {}![/red]\n".format(error))
            return []

    @staticmethod
    def save_json(path, data):
        try:
            with open(path, 'w', encoding='utf-8') as file:
                data_to_save = [item.to_dict() for item in data]            
                json.dump(data_to_save, file, indent=4, ensure_ascii=False)
                print("\n[green]Dados guardados com sucesso![/green]")
                return True
        except Exception as error:
            print("[red]Ocorreu um erro ao guardar os dados: {}[/red]\n".format(error))
            return False
        
    @staticmethod
    def filter_type_by_name(value, data):
        if Validations.isempty(value) == True:
            return data
        return list(filter(lambda x: x.get_name() == value, data))

    @staticmethod
    def get_by_id(id, data):    
        return next((x for x in data if x.get_id() == id), None)
    
    @staticmethod
    def filter_by_name_or_departament(value, data):
        if Validations.isempty(value) == True:
            return data
        return list(filter(lambda x: x.get_name() == value or x.get_dept() == value, data))
    
    @staticmethod
    def filter_by_name_or_price(value, data):
        if Validations.isempty(value) == True:
            return data
        return list(filter(lambda x: x.get_name() == value or x.get_price() == value, data))
    
    @staticmethod
    def filter_by_name_price_or_id(value, data):
        if Validations.isempty(value) == True:
            return data
        return list(filter(lambda x: x.get_name() == value or x.get_price() == value or x.get_type_analysis_id() == value, data))
    
    @staticmethod
    def filter_analysis_request(value, data):
        if Validations.isempty(value) == True:
            return data
        return list(filter(lambda x: x.get_type_analysis_id() == value or x.get_client_id() == value or x.get_client_type_id() == value or x.get_created() == value, data))
    
    @staticmethod
    def get_genre():
        choice = input("Género [M/F] (qualquer outro para confuso): ")
        choice = choice.upper().strip()
        
        if choice == "M":
            print("Masculino\n")
            return "Masculino"
        elif choice == "F":
            print("Feminino\n")
            return "Feminino"
        else:
            print("Confuso\n")
            return "Confuso"
        
    @staticmethod
    def get_positive_report():
        choice = input("Resultado [P/N] (qualquer outro para inconclusivo): ")
        choice = choice.upper().strip()
        
        if choice == "P":
            print("Positivo\n")
            return True
        elif choice == "N":
            print("Negativo\n")
            return False
        else:
            print("Inconclusivo\n")
            return False
