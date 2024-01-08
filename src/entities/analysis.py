import random

class Analysis:
    def __init__(self, type_client_id, name, description, price, type_analysis_id):
        if(type_client_id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = type_client_id
        self.name = name
        self.description = description
        self.price = price
        self.type_analysis_id = type_analysis_id
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_price(self):
        return self.price
    
    def get_type_analysis_id(self):
        return self.type_analysis_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'type_analysis_id': self.type_analysis_id
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['name'],
            data['description'],
            data['price'],
            data['type_analysis_id']
        )