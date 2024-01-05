import random
from datetime import datetime

class Client():
    def __init__(self, name, email, phone, genre, birthdate, address, dept):
        self.id = random.randint(1, 999999)
        self.created = datetime.now()
        self.name = name
        self.email = email
        self.phone = phone
        self.genre = genre
        self.birthdate = birthdate
        self.address = address
        self.dept = dept
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
        
    def get_birthdate(self):
        return self.birthdate
    
    def get_address(self):
        return self.address   
    
    def get_dept(self):
        return self.dept
    
    def get_genre(self):
        return self.genre
    
    def to_dict(self):
        return {
            'id': self.id,
            'created': self.created.isoformat(),
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'genre': self.genre,
            'birthdate': self.birthdate,
            'address': self.address,
            'dept': self.dept,
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['name'],
            data['email'],
            data['phone'],
            data['genre'],
            data['birthdate'],
            data['address'],
            data['dept'],
        )