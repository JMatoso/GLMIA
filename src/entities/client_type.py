import random

class ClientType:
    def __init__(self, type_client_id, name, description):
        if(type_client_id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = type_client_id
        self.name = name
        self.description = description
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['name'],
            data['description']
        )