

import os
import json

CARPETA_DATOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data"
)

def _ruta(nombre_archivo):
    """Construye la ruta completa a un archivo de datos."""
    return os.path.join(CARPETA_DATOS, nombre_archivo)



def _linea_a_dict(linea):
    """
    Convierte una línea del .txt en un diccionario.

    'id=1|hotel=Palacio de Sal' 
          ↓
    {'id': '1', 'hotel': 'Palacio de Sal'}
    """
    campos = {}
    for par in linea.strip().split("|"):
        if "=" in par:
            clave, valor = par.split("=", 1)
            if valor.startswith("[") and valor.endswith("]"):
                try:
                    valor = json.loads(valor)
                except json.JSONDecodeError:
                    pass
            campos[clave] = valor
    return campos

def _dict_a_linea(diccionario):
    """
    Convierte un diccionario en una línea del .txt.

    {'id': '1', 'hotel': 'Palacio de Sal'}
          ↓
    'id=1|hotel=Palacio de Sal'
    """
    def valor_a_texto(valor):
        if isinstance(valor, list):
            return json.dumps(valor, ensure_ascii=False)
        return valor

    return "|".join(f"{k}={valor_a_texto(v)}" for k, v in diccionario.items())



def leer_reservas():
    """
    Lee todas las reservas del archivo .txt.
    Retorna una lista de diccionarios.
    Si el archivo no existe, retorna lista vacía.
    """
    reservas = []
    ruta = _ruta("reservas.txt")

   
    if not os.path.exists(ruta):
        return reservas

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:                        
                reservas.append(_linea_a_dict(linea))

    return reservas

def guardar_reservas(reservas):
    """
    Escribe la lista completa de reservas en el .txt.
    Sobreescribe todo el archivo (escritura total).
    """
    os.makedirs(CARPETA_DATOS, exist_ok=True)  

    with open(_ruta("reservas.txt"), "w", encoding="utf-8") as archivo:
        for reserva in reservas:
            archivo.write(_dict_a_linea(reserva) + "\n")

def agregar_reserva(datos_reserva):
    """
    Agrega una reserva nueva al archivo.
    Asigna el ID automáticamente.
    """
    reservas = leer_reservas()

    ids = [int(r.get("id", 0)) for r in reservas]
    nuevo_id = str(max(ids) + 1) if ids else "1"

    datos_reserva["id"] = nuevo_id
    reservas.append(datos_reserva)
    guardar_reservas(reservas)
    return nuevo_id

def eliminar_reserva(id_reserva):
    """Elimina la reserva con el ID dado."""
    reservas = leer_reservas()
    reservas = [r for r in reservas if r.get("id") != str(id_reserva)]
    guardar_reservas(reservas)


def actualizar_reserva(id_reserva, datos_actualizados):
    """Actualiza la reserva existente con los nuevos datos."""
    reservas = leer_reservas()
    actualizado = False
    for idx, reserva in enumerate(reservas):
        if reserva.get("id") == str(id_reserva):
            datos_actualizados["id"] = str(id_reserva)
            reservas[idx] = datos_actualizados
            actualizado = True
            break
    if actualizado:
        guardar_reservas(reservas)
    return actualizado


def leer_favoritos():
    """
    Lee todos los favoritos del archivo .txt.
    Retorna lista de diccionarios.
    """
    favoritos = []
    ruta = _ruta("favoritos.txt")

    if not os.path.exists(ruta):
        return favoritos

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                favoritos.append(_linea_a_dict(linea))

    return favoritos

def guardar_favoritos(favoritos):
    """Sobreescribe el archivo con la lista completa."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    with open(_ruta("favoritos.txt"), "w", encoding="utf-8") as archivo:
        for fav in favoritos:
            archivo.write(_dict_a_linea(fav) + "\n")

def agregar_favorito(datos_fav):
    """Agrega un favorito nuevo con ID automático."""
    favoritos = leer_favoritos()

    ids = [int(f.get("id", 0)) for f in favoritos]
    nuevo_id = str(max(ids) + 1) if ids else "1"

    datos_fav["id"] = nuevo_id
    favoritos.append(datos_fav)
    guardar_favoritos(favoritos)
    return nuevo_id

def eliminar_favorito(id_fav):
    """Elimina el favorito con el ID dado."""
    favoritos = leer_favoritos()
    favoritos = [f for f in favoritos
                 if f.get("id") != str(id_fav)]
    guardar_favoritos(favoritos)
    

def leer_usuario():
    """
    Lee los datos del usuario desde usuario.txt
    Retorna un diccionario con sus datos.
    Si el archivo no existe, retorna datos por defecto.
    """
    usuario = {
        "nombre":    "Usuario",
        "membresia": "Member",
        "email":     ""
    }
    ruta = _ruta("usuario.txt")

    if not os.path.exists(ruta):
        return usuario

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if "=" in linea:
                
                clave, valor = linea.split("=", 1)
                usuario[clave] = valor

    return usuario

def guardar_usuario(datos_usuario):
    """
    Guarda los datos del usuario en usuario.txt
    Sobreescribe el archivo completo.
    """
    os.makedirs(CARPETA_DATOS, exist_ok=True)

    with open(_ruta("usuario.txt"), "w", encoding="utf-8") as archivo:
        for clave, valor in datos_usuario.items():
            archivo.write(f"{clave}={valor}\n")

def leer_hoteles():
    """Lee todos los hoteles del archivo .txt."""
    hoteles = []
    ruta = _ruta("hoteles.txt")
    if not os.path.exists(ruta):
        return hoteles
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea:
                hoteles.append(_linea_a_dict(linea))
    return hoteles

def guardar_hoteles(hoteles):
    """Sobreescribe el archivo con la lista completa."""
    os.makedirs(CARPETA_DATOS, exist_ok=True)
    with open(_ruta("hoteles.txt"), "w", encoding="utf-8") as archivo:
        for hotel in hoteles:
            archivo.write(_dict_a_linea(hotel) + "\n")

def agregar_hotel(datos_hotel):
    """Agrega un hotel nuevo con ID automático."""
    hoteles = leer_hoteles()
    ids = [int(h.get("id", 0)) for h in hoteles]
    datos_hotel["id"] = str(max(ids) + 1) if ids else "1"
    hoteles.append(datos_hotel)
    guardar_hoteles(hoteles)
    return datos_hotel["id"]

def eliminar_hotel(id_hotel):
    """Elimina el hotel con el ID dado."""
    hoteles = leer_hoteles()
    hoteles = [h for h in hoteles if h.get("id") != str(id_hotel)]
    guardar_hoteles(hoteles)