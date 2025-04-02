#control/ControlEntidad.py
import os
from pprint import pprint
import psycopg2
from psycopg2 import errors
from control.ControlConexion import ControlConexion
from modelo.Entidad import Entidad


class ControlEntidad:
    def __init__(self, nombre_tabla):
        self.tabla = nombre_tabla
        self.objControlConexion = ControlConexion()  
    def validarIngreso(self, clave_primaria, valorCp,contrasena,valorCo):
        valido = False
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )

            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return None 
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla} WHERE {clave_primaria} = %s AND {contrasena} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valorCp,valorCo])

            resultado = cursor.fetchone()  # Obtener el primer resultado
            
            if resultado:
                valido=True
        except psycopg2.Error as e:
            print(f"Error al buscar en {self.tabla} por ID: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return valido
 
    def guardar(self, entidad):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False 
            cursor = conexion.cursor()

            propiedades = entidad.obtener_propiedades()
            campos = propiedades.keys()
            valores = propiedades.values()
            placeholders = ", ".join(["%s"] * len(campos))
            print("placeholders=",placeholders)
            query_campos = ", ".join(campos)
            print("query_campos=",query_campos)
            sql = f"INSERT INTO {self.tabla} ({query_campos}) VALUES ({placeholders})"
            print("sql=",sql)
            cursor.execute(sql, list(valores))
            conexion.commit()
            resultado = True

        except psycopg2.Error as e:
            print(f"Error al guardar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado

    def modificar(self, clave_primaria, valor, entidad):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False 
            cursor = conexion.cursor()

            propiedades = entidad.obtener_propiedades()
            actualizaciones = []
            valores = []
            for campo, valor_campo in propiedades.items():
                if campo != clave_primaria:
                    actualizaciones.append(f"{campo} = %s")
                    valores.append(valor_campo)

            valores.append(valor)  # El valor de la clave primaria para el WHERE
            sql = f"UPDATE {self.tabla} SET {', '.join(actualizaciones)} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, valores)
            conexion.commit()
            resultado = True

        except psycopg2.Error as e:
            print(f"Error al actualizar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado

    def borrar(self, clave_primaria, valor):
        resultado = False
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return False            
            cursor = conexion.cursor()
            
            sql = f"DELETE FROM {self.tabla} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valor])
            conexion.commit()
            resultado = True

        except psycopg2.Error as e:
            print(f"Error al eliminar en {self.tabla}: {e.pgerror}")
            conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            conexion.rollback()
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        return resultado
    def buscarPorId(self, clave_primaria, valor):
        entidad = None
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return None 
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla} WHERE {clave_primaria} = %s"
            print("sql=",sql)
            cursor.execute(sql, [valor])

            resultado = cursor.fetchone()  # Obtener el primer resultado
            
            # Si hay un resultado, construye un objeto Entidad a partir de él.
            if resultado:
                columnas = [desc[0] for desc in cursor.description]  # obtener los nombres de las columnas
                propiedades = dict(zip(columnas, resultado))  # mapea las columnas a sus valores correspondientes
                entidad = Entidad(propiedades)

        except psycopg2.Error as e:
            print(f"Error al buscar en {self.tabla} por ID: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            cursor.close()
            self.objControlConexion.cerrarBd()
        
        return entidad  # Retorna un objeto Entidad o None si no se encuentra el registro.

    def listar(self):
        resultados = []
        conexion = None
        cursor = None
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            if not conexion:
                print("No se pudo establecer una conexión a la base de datos.")
                return []  # Retorna una lista vacía en caso de fallo de conexión
            cursor = conexion.cursor()

            sql = f"SELECT * FROM {self.tabla}"
            cursor.execute(sql)
            resultados = cursor.fetchall()  # Obtener todos los resultados
        except psycopg2.Error as e:
            print(f"Error al listar {self.tabla}: {e.pgerror}")
            if conexion:
                conexion.rollback()
        except Exception as e:
            print(f"Error inesperado: {e}")
            if conexion:
                conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if self.objControlConexion and conexion:
                self.objControlConexion.cerrarBd()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]
        
        # Convertir cada fila de resultados en un objeto Entidad
        entidades = [Entidad(dict(zip(columnas, row))) for row in resultados]
        return entidades

    def consultar(self, consulta, parametros=None):
        """
        Ejecuta una consulta personalizada en la base de datos y devuelve los resultados.

        :param consulta: str, la consulta SQL a ejecutar.
        :param parametros: tuple, los parámetros de la consulta (opcional).
        :return: list, los resultados de la consulta.
        """
        resultados = []
        conexion = None
        cursor = None
        try:
            conexion = self.objControlConexion.abrirBd(
                            servidor=os.getenv("SERV"),
                            usuario=os.getenv("USUA"),
                            password=os.getenv("PASSW"),
                            db=os.getenv("BDAT"),
                            puerto=os.getenv("PORT")
                        )
            cursor = conexion.cursor()

            cursor.execute(consulta, parametros if parametros else ())
            resultados = cursor.fetchall()  # Obtener todos los resultados

        except psycopg2.Error as e:
            print(f"Error al realizar la consulta en {self.tabla}: {e.pgerror}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        finally:
            if cursor:
                cursor.close()
            if self.objControlConexion and conexion:
                self.objControlConexion.cerrarBd()

        # Obtener los nombres de las columnas
        columnas = [desc[0] for desc in cursor.description]

        # Convertir cada fila de resultados en un objeto Entidad
        entidades = [Entidad(dict(zip(columnas, row))) for row in resultados]

        return entidades


