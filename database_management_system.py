import sqlite3
import datetime
class Employees:
    
    # create employee's table if not exist
    def initilize(self, connection):
        try:
            connection.execute('''CREATE TABLE  Employees(
                Id INT PRIMARY KEY NOT NULL,
                Name TEXT NOT NULL,
                Email TEXT NOT NULL,
                Departement TEXT NOT NULL,
                Post TEXT NOT NULL,
                Embedding TEXT NOT NULL,
                Last_seen DATETIME NOT NULL);''')
            print("employees table created succefully")
        except:
            print("Table already exists")

        

    # add new employee to table 
    def add_new_employee(self, employee, connection):
        id = employee["Id"]
        name = employee["Name"]
        email =  employee["Email"]
        departement = employee["Departement"]
        post = employee["Post"]
        embedding = employee["Embedding"]
        last_seen = employee["Last_seen"]
        connection.execute("INSERT INTO Employees VALUES({},{}, {}, {}, {},{},{});".format( id, name, email, departement, post,embedding, last_seen))
        connection.commit()
        
        print("employee added successfully")
        return True
    
    # delete employee from table
    def delete_employee(self, employee_id , connection):
        self.connection.execute("DELETE FROM Employees WHERE Id={}".format(employee_id))
        connection.commit()
        connection.close()
        print("employee deleted successfully")
        return True

    def update_employee(self, connection , employee):
        
        id = employee["Id"]
        name = employee["Name"]
        email =  employee["Email"]
        departement = employee["Departement"]
        post = employee["Post"]
        embedding = employee["Embedding"]
        last_seen = employee["Last_seen"]
        connection.execute('''UPDATE Employees SET  Name = {},
                                                    Email = {},
                                                    Departement = {},
                                                    Post = {},
                                                    Embedding = {},
                                                    Last_seen = {},
                                                WHERE Id = '{}'
                                                    '''.format(name, email, departement, post,embedding, last_seen, id))
        connection.commit()
        
        print("employee updated succesfully")
        return True
        
        

        
    # get all employees data from table
    def get_employees_data(self, connection):
        self.cursor = connection.execute('''SELECT * FROM Employees''')
        employees = []
        for row in self.cursor:
            employee = dict()
            employee["Id"] = row[0]
            employee["Name"] = row[1]
            employee["Email"] = row[3]
            employee["Departement"] = row[4]
            employee["Post"] = row[5]
            employee["Embedding"] = row[6]
            employee["Last_seen"] = row[7]
            employees.append(employee)

        
        return employees
    
    def get_employee(self , name, connection):
        self.cursor = connection.execute('''SELECT * FROM Employees WHERE Name = {};'''.format(name))
        data = self.cursor[0]
        employee = {}
        employee["Id"] = data[0]
        employee["Name"] = data[1]
        employee["Email"] = data[3]
        employee["Departement"] = data[4]
        employee["Post"] = data[5]
        employee["Last_seen"] = data[6]
        data = None
        self.cursor = None
        
        return employee

        

class Clusters:

    def initilize(self, connection):
        try:
            connection.execute('''CREATE TABLE Clusters (
                Id INT PRIMARY KEY NOT NULL,
                employee_id INT NOT NULL);''')
            print("clusters created successfully")
            connection.commit()
        except:
            print("table clusters already exists")

    def add_new_cluster(self):
        return



class Records:

    def initilize(self, connection):
        try:
            connection.execute('''CREATE TABLE Records (
                Id INT PRIMARY KEY NOT NULL,
                Employees_id TEXT NOT NULL,
                Entering_time DATETIME NOT NULL);''')
            print("records table created succefully")
        except:
            print("table recorda already exists")
    
    def get_historical_data(self):
        self.cursor = self.connection.execute('''SELECT * FROM Records''')
        history = []
        for row in self.cursor:
            record = dict()
            record["Id"] = row[0]
            record["Employee_id"] = row[1]
            record["Entering_time"] = row[2]
            history.append(record)
        
        return history

    def add_new_record(self,record, connection):
        employee_id = record["Employee_id"]
        entering_time = datetime.datetime.today()
        connection.execute('''INSERT INTO Records (Employee_id, Entering_time) 
                            VALUES ({},{});
        '''.format(employee_id, entering_time))
        connection.commit()
        print("record added successfully")
        return True





class db_management_system:

    def __init__(self):
        self.connection = None
        self.cursor = None
        self.employees = Employees()
        self.records = Records()
        self.clusters = Clusters()
        # if database doesn't exist, create new one, if it does, connect it
        self.connection = sqlite3.connect("smart_gate.sqlite")
        print("database connected successfully")
        self.employees.initilize(self.connection)
        self.clusters.initilize(self.connection)
        self.records.initilize(self.connection)

database = db_management_system()




employee = {}
employee["Id"] = 0
employee["Name"] = "mohameder-raouan"
employee["Email"] = "mohamed14@gmail.com"
employee["Departement"] = "engineering"
employee["Post"] = "manager"
employee["Embedding"] = "0.2150,0.251,0.3625,0.2652,0.2515,0.2551,0.25,0.2515"
employee["Last_seen"] = "yesterday"

database.employees.add_new_employee(employee,database.connection )

        


    
    
    
    

    



        
 






