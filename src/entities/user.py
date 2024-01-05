import random
from datetime import datetime

class User:
    def __init__(self, name, email, phone, genre):
        self.name = name
        self.email = email
        self.role = "USER" #change to enum later on
        self.created = datetime.now()
        self.id = random.randint(1, 999999)
        
        if not instance(genre, Genre):
            raise ValueError('Genêro inválido.')
        
        self.genre = genre
        
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_phone(self):
        return self.phone
    
    def get_role(self):
        return self.role
    
    def get_created(self):
        return self.created
    
    
    