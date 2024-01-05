import os
import json

from rich import print

class DataContext:
    @staticmethod
    def load_json(path):
        try:
            if os.path.isfile(path):
                with open(path, 'r') as file:
                    data = json.load(file)
                return data
            else:
                DataContext.save_json(path, [])
                return []
        except:
            print("\n[red]Ocorreu um erro ao carregar os dados, tente novamente![/red]")
            return []

    @staticmethod
    def save_json(path, data):
        try:
            with open(path, 'w') as file:
                data_to_save = [item.to_dict() for item in data]            
                json.dump(data_to_save, file, indent=4)
                print("\n[green]Dados guardados com sucesso![/green]")
                return True
        except Exception as error:
            print("[red]Ocorreu um erro ao guardar os dados: {}[/red]\n".format(error))
            return False
