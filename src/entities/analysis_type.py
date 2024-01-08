import random

class AnalysisType:
    def __init__(self, id, name, description, price = 0):
        if(id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = id
        self.name = name
        self.description = description
        self.price = price
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_price(self):
        return self.price
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['name'],
            data['description'],
            data['price']
        )