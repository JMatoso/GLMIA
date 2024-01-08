import random
from datetime import datetime

class AnalysisReport:
    def __init__(self, id, type_analysis_id, client_id, client_type_id, description, positive, created = datetime.now()):
        if(id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = id
        self.type_analysis_id = type_analysis_id
        self.client_id = client_id
        self.client_type_id = client_type_id
        self.created = created
        self.description = description
        self.positive = positive
    
    def get_id(self):
        return self.id
    
    def get_type_analysis_id(self):
        return self.type_analysis_id
    
    def get_client_id(self):
        return self.client_id
    
    def get_client_type_id(self):
        return self.client_type_id
    
    def get_description(self):
        return self.description
    
    def get_positive(self):
        return self.positive
    
    def get_created(self):
        return self.created
    
    def to_dict(self):
        return {
            'id': self.id,
            'type_analysis_id': self.type_analysis_id,
            'client_id': self.client_id,
            'client_type_id': self.client_type_id,
            'description': self.description,
            'positive': self.positive,
            'created': self.created.isoformat()
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['type_analysis_id'],
            data['client_id'],
            data['client_type_id'],
            data['description'],
            data['positive'],
            datetime.fromisoformat(data['created'])
        )