import mysql.connector
from mysql.connector import Error

datos = {'host':'DOMINIO',
'database':'NOMBRE DE BASE DE DATOS',
'user':'USUARIO',
'password':'CONTRASEÑA'
}

#Manejador de base de datos
class db:
    #Metodo de conexión
    def __init__(self,data_connection):
        try:
            self.db = mysql.connector.connect(**data_connection)
            self.msg = "Conexión alcanzada"
            if not self.db.is_connected():
                self.msg = "Conexión no alcanzada"
        except Error as e:
            self.msg = str(e)
    #Método de creación de tablas
    #EL CREADOR DE TABLAS PODRÏA AGREGARSE A INTERFAZ MAESTRA (NO CLIENTE)
    def create_table(self):
        cursor = self.db.cursor()
        try:
            cursor.execute('''CREATE TABLE Especies(
                            ESPECIE_ID int NOT NULL AUTO_INCREMENT,
                            ESPECIE varchar(255) NOT NULL,
                            PRIMARY KEY (ESPECIE_ID));''')
            self.msg = "Tabla creada de manera exitosa"
        except:
            self.msg = "Tabla no creada de manera exitosa"
    def delete_table(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("DROP TABLE Especies")
            self.msg = "Tabla borrada de manera exitosa"
        except:
            self.msg = "Algo falló en la eliminación"
    #Visor de tablas
    def view_tablas(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("SHOW TABLES;")
            for x in cursor:
                print(x)
            self.msg = "Consulta de tablas exitosa"
        except:
            self.msg = "Algo falló en la consulta"
    #Método de inserción de datos
    def insert_record(self):
        cursor = self.db.cursor()
        species = input("Introduzca el nombre de la especie: ")
        try:
            cursor.execute('''INSERT INTO Especies (ESPECIE)
            VALUES("'''+species+'");')
            self.msg = "Registro exitoso"
        except:
            self.msg = "Algo falló al hacer el registro"
    #Consulta de tablas
    def view_records(self):
        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT * FROM Especies;")
            for x in cursor:
                print(x)
            self.msg = "Consulta exitosa"
        except:
            self.msg = "Algo falló en la consulta"
    #Método de cerradura
    def close_connection(self):
        self.db.close()
        self.msg = "Conexión terminada"


base_de_datos = db(datos)
print(base_de_datos.msg)
#base_de_datos.create_table()
#print(base_de_datos.msg)
#base_de_datos.delete_table()
#print(base_de_datos.msg)
base_de_datos.view_tablas()
print(base_de_datos.msg)
#base_de_datos.insert_record()
#print(base_de_datos.msg)
base_de_datos.view_records()
print(base_de_datos.msg)
base_de_datos.close_connection()
print(base_de_datos.msg)
