class Parent():
    def __init__(self):
        self.name = 'a parent'
        
        
    def polymorphism(self):
        if isinstance(self, Child):
            print('object is indeed a child')
        

class Child(Parent):
    def __init__(self):
        super().__init__()
        self.name = 'a child tho'
        
    def hello(self):
        print("hello")
        
        
child = Child()

child.polymorphism()