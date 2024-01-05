import random

class User:
    def __init__(self, user_id, name, email, role = "USER"):
        self.name = name
        self.email = email
        self.role = role #change to enum later on
        if(user_id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = user_id
        
    def get_id(self):
        return self.id
        
    def get_name(self):
        return self.name
    
    def get_email(self):
        return self.email
    
    def get_role(self):
        return self.role
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['name'],
            data['email'],
            data['role']
        )
    
    
    