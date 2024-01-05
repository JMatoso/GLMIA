import random
class Employee():
    def __init__(self, employee_id, name, email, phone, genre, salary, dept):
        if(employee_id == 0):
            self.id = random.randint(1000, 9999)
        else:
            self.id = employee_id
        self.name = name
        self.email = email
        self.phone = phone
        self.dept = dept
        self.genre = genre
        self.salary = salary
        
    def get_salary(self):
        return self.salary
    
    def get_dept(self):
        return self.dept

    def get_genre(self):
        return self.genre
    
    def get_phone(self):
        return self.phone
    
    def get_email(self):
        return self.email
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'genre': self.genre,
            'salary': self.salary,
            'dept': self.dept,
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id'],
            data['name'],
            data['email'],
            data['phone'],
            data['genre'],
            data['salary'],
            data['dept'],
        )