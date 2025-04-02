#modelo/Entidad.py
class Entidad:
    def __init__(self, propiedades=None):
        # Inicializador de la clase.
        # Si no se proveen propiedades, se inicializa con un diccionario vacío.
        if propiedades is None:
            propiedades = {}       
        # Establece un atributo privado que almacena las propiedades en un diccionario.
        self.__propiedades = propiedades
    def __setattr__(self, nombre, valor):
        # Método  que se invoca al intentar establecer un atributo en una instancia.

        # Si si se intenta asignar al atributo especial __propiedades,
        # se utiliza el comportamiento de asignación por defecto.
        if nombre == "_Entidad__propiedades":
            super().__setattr__(nombre, valor)
        else:
            # Si no, se almacena el atributo dentro del diccionario __propiedades.
            self.__propiedades[nombre] = valor
    def __getattr__(self, nombre):
        # Método  que se invoca al intentar obtener un atributo que no ha sido definido.
        # se intenta obtener el atributo del diccionario __propiedades.
        try:
            return self.__propiedades[nombre]
        except KeyError:
            # Si el atributo no existe, se lanza una excepción.
            raise AttributeError(f"Propiedad no definida: {nombre}")
    def obtener_propiedades(self):
        # Devuelve el diccionario completo de propiedades.
        return self.__propiedades


