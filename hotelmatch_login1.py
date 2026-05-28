import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
import sys
# ─────────────────────────────────────────────
#  Colores y fuentes
# ─────────────────────────────────────────────
COLOR_FONDO_OSCURO   = "#1a1a1a"
COLOR_FONDO_CLARO    = "#f5f5f5"
COLOR_FONDO_SALMON   = "#fff0eb"
COLOR_BLANCO         = "#ffffff"
COLOR_NARANJA        = "#d4451a"
COLOR_NARANJA_HOVER  = "#b83a14"
COLOR_TEXTO_OSCURO   = "#1a1a1a"
COLOR_TEXTO_GRIS     = "#888888"
COLOR_BORDE          = "#e0e0e0"

FUENTE_MARCA    = ("Courier New", 14, "bold")
FUENTE_TITULO   = ("Courier New", 22, "bold")
FUENTE_ETIQUETA = ("Helvetica", 10)
FUENTE_ENTRADA  = ("Helvetica", 11)
FUENTE_PEQUEÑA  = ("Helvetica", 9)
FUENTE_ENLACE   = ("Helvetica", 9, "underline")
FUENTE_BOTON    = ("Helvetica", 10, "bold")
FUENTE_PIE      = ("Helvetica", 9)

ANCHO_VENTANA = 900
ALTO_VENTANA  = 860

# ─────────────────────────────────────────────
#  Archivos de almacenamiento (.txt)
# ─────────────────────────────────────────────
ARCHIVO_USUARIOS      = "usuarios.txt"
ARCHIVO_ADMINISTRADOR = "administrador.txt"
SEPARADOR             = "|"

# Formato usuarios.txt (una línea por usuario):
#   usuario|contraseña|pregunta_secreta|respuesta_secreta
#
# Formato administrador.txt (una sola línea):
#   usuario_admin|contraseña_admin


def inicializar_archivos():
    """Crea los archivos de datos con valores por defecto si no existen."""
    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
            # Usuario de prueba inicial
            archivo.write("usuario123|abc123|Nombre de tu mascota|firulais\n")

    if not os.path.exists(ARCHIVO_ADMINISTRADOR):
        with open(ARCHIVO_ADMINISTRADOR, "w", encoding="utf-8") as archivo:
            archivo.write("admin123|admin2024\n")


# ── Operaciones sobre usuarios ────────────────

def cargar_usuarios():
    """Lee usuarios.txt y retorna una lista de diccionarios."""
    lista_usuarios = []
    if not os.path.exists(ARCHIVO_USUARIOS):
        return lista_usuarios

    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(SEPARADOR)
            if len(partes) == 4:
                lista_usuarios.append({
                    "usuario":           partes[0],
                    "contrasena":        partes[1],
                    "pregunta_secreta":  partes[2],
                    "respuesta_secreta": partes[3].lower()
                })
    return lista_usuarios


def guardar_usuarios(lista_usuarios):
    """Escribe la lista completa de usuarios en usuarios.txt."""
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        for u in lista_usuarios:
            linea = SEPARADOR.join([
                u["usuario"],
                u["contrasena"],
                u["pregunta_secreta"],
                u["respuesta_secreta"]
            ])
            archivo.write(linea + "\n")


def buscar_usuario(nombre_usuario):
    """Busca un usuario por nombre (ignora mayúsculas/minúsculas)."""
    for u in cargar_usuarios():
        if u["usuario"].lower() == nombre_usuario.lower():
            return u
    return None


def registrar_usuario(usuario, contrasena, pregunta, respuesta):
    """Agrega un nuevo usuario al archivo."""
    lista = cargar_usuarios()
    lista.append({
        "usuario":           usuario,
        "contrasena":        contrasena,
        "pregunta_secreta":  pregunta,
        "respuesta_secreta": respuesta.lower()
    })
    guardar_usuarios(lista)


def actualizar_contrasena_usuario(nombre_usuario, nueva_contrasena):
    """Cambia la contraseña de un usuario existente en el archivo."""
    lista = cargar_usuarios()
    for u in lista:
        if u["usuario"].lower() == nombre_usuario.lower():
            u["contrasena"] = nueva_contrasena
            break
    guardar_usuarios(lista)


# ── Operaciones sobre administrador ──────────

def cargar_administrador():
    """Lee administrador.txt y retorna un diccionario con las credenciales."""
    if not os.path.exists(ARCHIVO_ADMINISTRADOR):
        return {"usuario": "admin123", "contrasena": "admin2024"}

    with open(ARCHIVO_ADMINISTRADOR, "r", encoding="utf-8") as archivo:
        linea = archivo.readline().strip()

    partes = linea.split(SEPARADOR)
    if len(partes) == 2:
        return {"usuario": partes[0], "contrasena": partes[1]}
    return {"usuario": "admin123", "contrasena": "admin2024"}


def guardar_contrasena_administrador(nueva_contrasena):
    """Actualiza la contraseña del administrador en el archivo."""
    datos_admin = cargar_administrador()
    with open(ARCHIVO_ADMINISTRADOR, "w", encoding="utf-8") as archivo:
        archivo.write(f"{datos_admin['usuario']}{SEPARADOR}{nueva_contrasena}\n")


# ─────────────────────────────────────────────
#  Utilidades de interfaz gráfica
# ─────────────────────────────────────────────

def limpiar_frame(frame):
    """Elimina todos los widgets de un contenedor."""
    for widget in frame.winfo_children():
        widget.destroy()


def crear_entrada(padre, placeholder="", mostrar="", **kwargs):
    """Crea un campo de texto con placeholder y estilo HotelMatch."""
    entrada = tk.Entry(
        padre,
        font=FUENTE_ENTRADA,
        relief="flat",
        bg="#f0f0f0",
        fg=COLOR_TEXTO_OSCURO,
        insertbackground=COLOR_TEXTO_OSCURO,
        highlightthickness=1,
        highlightbackground=COLOR_BORDE,
        highlightcolor=COLOR_NARANJA,
        show=mostrar,
        **kwargs
    )
    if placeholder and not mostrar:
        entrada.insert(0, placeholder)
        entrada.config(fg=COLOR_TEXTO_GRIS)

        def al_enfocar(evento):
            if entrada.get() == placeholder:
                entrada.delete(0, "end")
                entrada.config(fg=COLOR_TEXTO_OSCURO)

        def al_desenfocar(evento):
            if entrada.get() == "":
                entrada.insert(0, placeholder)
                entrada.config(fg=COLOR_TEXTO_GRIS)

        entrada.bind("<FocusIn>",  al_enfocar)
        entrada.bind("<FocusOut>", al_desenfocar)

    return entrada


def crear_boton(padre, texto, comando, ancho=34):
    """Crea un botón naranja con efecto hover."""
    boton = tk.Button(
        padre,
        text=texto,
        command=comando,
        bg=COLOR_NARANJA,
        fg=COLOR_BLANCO,
        font=FUENTE_BOTON,
        relief="flat",
        cursor="hand2",
        activebackground=COLOR_NARANJA_HOVER,
        activeforeground=COLOR_BLANCO,
        width=ancho,
        pady=10
    )
    boton.bind("<Enter>", lambda e: boton.config(bg=COLOR_NARANJA_HOVER))
    boton.bind("<Leave>", lambda e: boton.config(bg=COLOR_NARANJA))
    return boton


def crear_enlace(padre, texto, comando):
    """Crea una etiqueta estilo enlace (naranja, subrayada, clickeable)."""
    etiqueta = tk.Label(
        padre,
        text=texto,
        font=FUENTE_ENLACE,
        fg=COLOR_NARANJA,
        bg=COLOR_BLANCO,
        cursor="hand2"
    )
    etiqueta.bind("<Button-1>", lambda e: comando())
    return etiqueta


def dibujar_logo(padre):
    """Muestra la imagen del logo HotelMatch"""
    try:
        imagen_original = Image.open("logo.png")
        imagen_original = imagen_original.resize((220, 60))  # ajusta el tamaño
        imagen_logo = ImageTk.PhotoImage(imagen_original)

        etiqueta_logo = tk.Label(padre, image=imagen_logo, bg=COLOR_BLANCO)
        etiqueta_logo.image = imagen_logo  # referencia para evitar que el GC la elimine
        return etiqueta_logo
    except FileNotFoundError:
        # Si no encuentra la imagen, usa el logo de texto como respaldo
        frame_logo = tk.Frame(padre, bg=COLOR_BLANCO)
        tk.Label(frame_logo, text="≡ ", font=("Courier New", 20, "bold"),
                 fg=COLOR_TEXTO_OSCURO, bg=COLOR_BLANCO).pack(side="left")
        tk.Label(frame_logo, text="<Hotel>", font=("Courier New", 20, "bold"),
                 fg=COLOR_NARANJA, bg=COLOR_BLANCO).pack(side="left")
        tk.Label(frame_logo, text="Match", font=("Courier New", 20, "bold"),
                 fg=COLOR_TEXTO_OSCURO, bg=COLOR_BLANCO).pack(side="left")
        return frame_logo


# ─────────────────────────────────────────────
#  Clase principal de la aplicación
# ─────────────────────────────────────────────

class AplicacionHotelMatch(tk.Tk):

    def __init__(self):
        super().__init__()
        inicializar_archivos()

        self.title("HotelMatch")
        self.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO_OSCURO)

        # Barra superior oscura (muestra título de la pantalla actual)
        # barra_superior = tk.Frame(self, bg=COLOR_FONDO_OSCURO, height=28)
        # barra_superior.pack(fill="x")
        # self.etiqueta_pagina = tk.Label(
        #     barra_superior, text="Inicio de Sesion",
        #     font=FUENTE_PEQUEÑA, fg="#aaaaaa", bg=COLOR_FONDO_OSCURO
        # )
        # self.etiqueta_pagina.pack(side="left", padx=12, pady=4)

        # Barra de marca blanca
        barra_marca = tk.Frame(self, bg=COLOR_BLANCO, height=48)
        barra_marca.pack(fill="x")
        barra_marca.pack_propagate(False)
        tk.Label(barra_marca, text="HotelMatch",
                 font=FUENTE_MARCA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(side="left", padx=20, pady=10)

        # Contenedor principal (aquí se renderizan las pantallas)
        self.contenedor = tk.Frame(self, bg=COLOR_FONDO_CLARO)
        self.contenedor.pack(fill="both", expand=True)

        # Pie de página
        pie = tk.Frame(self, bg=COLOR_FONDO_OSCURO, height=34)
        pie.pack(fill="x")
        tk.Label(pie, text="Desarrollado por ",
                 font=FUENTE_PIE, fg="#aaaaaa",
                 bg=COLOR_FONDO_OSCURO).pack(side="left", padx=12, pady=8)
        tk.Label(pie, text="NextLevel",
                 font=FUENTE_PIE, fg=COLOR_NARANJA,
                 bg=COLOR_FONDO_OSCURO).pack(side="left")

        self.mostrar_inicio_sesion()

    # ── Utilidades de pantalla ────────────────

    def cambiar_pagina(self, titulo):
        """Actualiza el título y limpia el contenedor."""
        # self.etiqueta_pagina.config(text=titulo)
        limpiar_frame(self.contenedor)

    def crear_tarjeta(self, ancho=420):
        """Coloca fondo salmón y retorna la tarjeta blanca centrada."""
        fondo = tk.Frame(self.contenedor, bg=COLOR_FONDO_SALMON)
        fondo.place(relwidth=1, relheight=1)
        tarjeta = tk.Frame(
            fondo, bg=COLOR_BLANCO, bd=0,
            highlightthickness=1,
            highlightbackground=COLOR_BORDE
        )
        tarjeta.place(relx=0.5, rely=0.5, anchor="center", width=ancho)
        return tarjeta

    # ══════════════════════════════════════════
    #  PANTALLA 1 — Inicio de Sesión Usuario
    # ══════════════════════════════════════════

    def mostrar_inicio_sesion(self):
        self.cambiar_pagina("Inicio de Sesion")
        tarjeta = self.crear_tarjeta(420)

        dibujar_logo(tarjeta).pack(pady=(30, 4))
        tk.Label(tarjeta, text="Inicio Sesion",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(pady=(10, 4))

        # Campos de entrada
        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        tk.Label(frame_campos, text="Usuario",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_usuario = crear_entrada(frame_campos, "usuario123")
        entrada_usuario.pack(fill="x", ipady=8)

        tk.Label(frame_campos, text="Contraseña",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_contrasena = crear_entrada(frame_campos, mostrar="•")
        entrada_contrasena.pack(fill="x", ipady=8)

        # Enlace recuperar contraseña
        frame_recuperar = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_recuperar.pack(padx=40, fill="x", pady=(8, 0))
        tk.Label(frame_recuperar, text="¿Olvidaste tu contraseña?  ",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(side="left")
        crear_enlace(frame_recuperar, "Recuperar contraseña",
                     self.mostrar_recuperar_paso1).pack(side="left")

        # Recordar datos
        variable_recordar = tk.BooleanVar()
        frame_recordar = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_recordar.pack(padx=40, anchor="w", pady=(6, 0))
        tk.Checkbutton(
            frame_recordar, text=" Recordar mis datos",
            variable=variable_recordar,
            font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
            bg=COLOR_BLANCO, activebackground=COLOR_BLANCO
        ).pack()

        def accion_iniciar_sesion():
            nombre = entrada_usuario.get().strip()
            clave  = entrada_contrasena.get().strip()

            if not nombre or not clave:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            usuario_encontrado = buscar_usuario(nombre)
            if usuario_encontrado and usuario_encontrado["contrasena"] == clave:
                self.destroy()  # cierra la ventana del login
                subprocess.Popen([sys.executable, "hotelmatch/reservahoteles.py", nombre])
               #  messagebox.showinfo(
                  #  "Bienvenido",
                 #   f"¡Bienvenido, {nombre}!\n(Aquí se carga el menú de usuario)"
                #
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(18, 0))
        crear_boton(frame_boton, "INICIAR SESION",
                    accion_iniciar_sesion).pack(fill="x", ipady=4)

        # Enlace a registro
        frame_registro = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_registro.pack(pady=(12, 0))
        tk.Label(frame_registro, text="¿No tienes cuenta?  ",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(side="left")
        crear_enlace(frame_registro, "Regístrate ahora",
                     self.mostrar_registro).pack(side="left")

        # Enlace a login administrador
        frame_admin = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_admin.pack(pady=(8, 30))
        tk.Label(frame_admin, text="¿Eres Administrador?  ",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(side="left")
        crear_enlace(frame_admin, "Inicia Sesion como Administrador",
                     self.mostrar_inicio_administrador).pack(side="left")

    # ══════════════════════════════════════════
    #  PANTALLA 2 — Registro de Usuario
    # ══════════════════════════════════════════

    def mostrar_registro(self):
        self.cambiar_pagina("Registro Usuario")
        tarjeta = self.crear_tarjeta(440)

        dibujar_logo(tarjeta).pack(pady=(30, 4))
        tk.Label(tarjeta, text="Registro",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack()
        tk.Label(tarjeta, text="Únete a la plataforma HotelMatch",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(pady=(2, 6))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        def agregar_campo(etiqueta, placeholder="", mostrar=""):
            tk.Label(frame_campos, text=etiqueta,
                     font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                     bg=COLOR_BLANCO).pack(anchor="w", pady=(8, 2))
            campo = crear_entrada(frame_campos, placeholder, mostrar=mostrar)
            campo.pack(fill="x", ipady=8)
            return campo

        entrada_usuario    = agregar_campo("Usuario", "abelito123")
        entrada_contrasena = agregar_campo("Contraseña", mostrar="•")
        entrada_confirmar  = agregar_campo("Confirmar contraseña", mostrar="•")
        entrada_pregunta   = agregar_campo("Pregunta secreta",
                                           "Nombre de tu mascota")
        entrada_respuesta  = agregar_campo("Respuesta secreta", "Firulais")

        def accion_crear_cuenta():
            usuario    = entrada_usuario.get().strip()
            contrasena = entrada_contrasena.get().strip()
            confirmar  = entrada_confirmar.get().strip()
            pregunta   = entrada_pregunta.get().strip()
            respuesta  = entrada_respuesta.get().strip()

            if not all([usuario, contrasena, confirmar, pregunta, respuesta]):
                messagebox.showerror("Error", "Completa todos los campos.")
                return
            if contrasena != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return
            if buscar_usuario(usuario):
                messagebox.showerror("Error",
                    "El nombre de usuario ya existe.")
                return

            registrar_usuario(usuario, contrasena, pregunta, respuesta)
            messagebox.showinfo("¡Éxito!", "Cuenta creada correctamente.")
            self.mostrar_inicio_sesion()

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(18, 0))
        crear_boton(frame_boton, "CREAR CUENTA",
                    accion_crear_cuenta).pack(fill="x", ipady=4)

        frame_volver = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_volver.pack(pady=(12, 30))
        tk.Label(frame_volver, text="¿Ya tienes una cuenta?  ",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(side="left")
        crear_enlace(frame_volver, "Iniciar sesión",
                     self.mostrar_inicio_sesion).pack(side="left")

    # ══════════════════════════════════════════
    #  PANTALLA 3 — Recuperar Contraseña (Paso 1)
    # ══════════════════════════════════════════

    def mostrar_recuperar_paso1(self):
        self.cambiar_pagina("Recuperar Contraseña Usuario 1")
        tarjeta = self.crear_tarjeta(420)

        dibujar_logo(tarjeta).pack(pady=(34, 4))
        tk.Label(tarjeta, text="Recuperar Contraseña",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(pady=(10, 4))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        tk.Label(frame_campos, text="Usuario",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_usuario = crear_entrada(frame_campos, "Abelito18")
        entrada_usuario.pack(fill="x", ipady=8)

        def accion_buscar_cuenta():
            nombre = entrada_usuario.get().strip()
            usuario_encontrado = buscar_usuario(nombre)
            if usuario_encontrado:
                self.mostrar_recuperar_paso2(usuario_encontrado)
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(22, 40))
        crear_boton(frame_boton, "BUSCAR CUENTA",
                    accion_buscar_cuenta).pack(fill="x", ipady=4)

    # ══════════════════════════════════════════
    #  PANTALLA 4 — Recuperar Contraseña (Paso 2)
    # ══════════════════════════════════════════

    def mostrar_recuperar_paso2(self, datos_usuario):
        self.cambiar_pagina("Recuperar Contraseña Usuario 2")
        tarjeta = self.crear_tarjeta(420)

        dibujar_logo(tarjeta).pack(pady=(30, 4))
        tk.Label(tarjeta, text="Recuperar Contraseña",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(pady=(10, 4))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        # Usuario (solo lectura)
        tk.Label(frame_campos, text="Usuario",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(8, 2))
        entrada_usuario = crear_entrada(frame_campos, datos_usuario["usuario"])
        entrada_usuario.pack(fill="x", ipady=8)
        entrada_usuario.config(state="disabled")

        # Pregunta secreta (solo lectura)
        tk.Label(frame_campos, text="Pregunta Secreta",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_pregunta = crear_entrada(
            frame_campos, datos_usuario["pregunta_secreta"])
        entrada_pregunta.pack(fill="x", ipady=8)
        entrada_pregunta.config(state="disabled")

        # Respuesta secreta
        tk.Label(frame_campos, text="Respuesta secreta",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_respuesta = crear_entrada(frame_campos, "Firulais")
        entrada_respuesta.pack(fill="x", ipady=8)

        def accion_validar_respuesta():
            respuesta_ingresada = entrada_respuesta.get().strip().lower()
            if respuesta_ingresada == datos_usuario["respuesta_secreta"]:
                self.mostrar_recuperar_paso3(datos_usuario)
            else:
                messagebox.showerror("Error", "Respuesta incorrecta.")

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(22, 40))
        crear_boton(frame_boton, "VALIDAR RESPUESTA",
                    accion_validar_respuesta).pack(fill="x", ipady=4)

    # ══════════════════════════════════════════
    #  PANTALLA 5 — Recuperar Contraseña (Paso 3)
    # ══════════════════════════════════════════

    def mostrar_recuperar_paso3(self, datos_usuario):
        self.cambiar_pagina("Recuperar Contraseña Usuario 3")
        tarjeta = self.crear_tarjeta(420)

        dibujar_logo(tarjeta).pack(pady=(26, 4))
        tk.Label(tarjeta, text="¡Validacion Exitosa!",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(pady=(8, 4))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        # Usuario (solo lectura)
        tk.Label(frame_campos, text="Usuario",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(8, 2))
        entrada_usuario = crear_entrada(frame_campos, datos_usuario["usuario"])
        entrada_usuario.pack(fill="x", ipady=8)
        entrada_usuario.config(state="disabled")

        # Contraseña actual (solo lectura)
        tk.Label(frame_campos, text="Tu contraseña es:",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_actual = crear_entrada(
            frame_campos, datos_usuario["contrasena"])
        entrada_actual.pack(fill="x", ipady=8)
        entrada_actual.config(state="disabled")

        # Nueva contraseña
        tk.Label(frame_campos, text="Nueva contraseña:",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_nueva = crear_entrada(frame_campos, mostrar="•")
        entrada_nueva.pack(fill="x", ipady=8)

        # Confirmar nueva contraseña
        tk.Label(frame_campos, text="Confirmar nueva contraseña",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_confirmar = crear_entrada(frame_campos, mostrar="•")
        entrada_confirmar.pack(fill="x", ipady=8)

        def accion_cambiar_contrasena():
            nueva     = entrada_nueva.get().strip()
            confirmar = entrada_confirmar.get().strip()

            # Si no ingresó nueva contraseña, solo vuelve al inicio
            if not nueva and not confirmar:
                self.mostrar_inicio_sesion()
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            actualizar_contrasena_usuario(datos_usuario["usuario"], nueva)
            messagebox.showinfo("¡Éxito!",
                "Contraseña actualizada correctamente.")
            self.mostrar_inicio_sesion()

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(18, 40))
        crear_boton(frame_boton, "VOLVER AL INICIO DE SESION",
                    accion_cambiar_contrasena).pack(fill="x", ipady=4)

    # ══════════════════════════════════════════
    #  PANTALLA 6 — Inicio de Sesión Administrador
    # ══════════════════════════════════════════

    def mostrar_inicio_administrador(self):
        self.cambiar_pagina("Inicio de Sesion Administrador")
        tarjeta = self.crear_tarjeta(420)

        dibujar_logo(tarjeta).pack(pady=(34, 4))
        tk.Label(tarjeta, text="Inicio Sesion Administrador",
                 font=("Courier New", 18, "bold"),
                 fg=COLOR_TEXTO_OSCURO, bg=COLOR_BLANCO).pack(pady=(10, 4))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        tk.Label(frame_campos, text="Usuario Admin",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_usuario = crear_entrada(frame_campos, "admin123")
        entrada_usuario.pack(fill="x", ipady=8)

        tk.Label(frame_campos, text="Contraseña Admin",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_contrasena = crear_entrada(frame_campos, mostrar="•")
        entrada_contrasena.pack(fill="x", ipady=8)

        # Enlace recuperar acceso administrador
        frame_recuperar = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_recuperar.pack(padx=40, fill="x", pady=(8, 0))
        tk.Label(frame_recuperar, text="¿Olvidaste la contraseña?  ",
                 font=FUENTE_PEQUEÑA, fg=COLOR_TEXTO_GRIS,
                 bg=COLOR_BLANCO).pack(side="left")
        crear_enlace(frame_recuperar, "Recuperar Acceso Administrador",
                     self.mostrar_recuperar_administrador).pack(side="left")

        def accion_iniciar_admin():
            nombre = entrada_usuario.get().strip()
            clave  = entrada_contrasena.get().strip()
            datos_admin = cargar_administrador()
            if nombre == datos_admin["usuario"] and \
               clave  == datos_admin["contrasena"]:
                   self.destroy()
                   subprocess.Popen([sys.executable, "menu_administrador.py"])
                #messagebox.showinfo(
                 #   "Bienvenido",
                  #  "¡Bienvenido, Administrador!\n"
                   # "(Aquí se carga el menú de administrador)"
               # )
            else:
                messagebox.showerror("Error",
                    "Credenciales de administrador incorrectas.")

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(20, 40))
        crear_boton(frame_boton, "INICIAR SESION",
                    accion_iniciar_admin).pack(fill="x", ipady=4)

    # ══════════════════════════════════════════
    #  PANTALLA 7 — Recuperar Acceso Administrador
    # ══════════════════════════════════════════

    def mostrar_recuperar_administrador(self):
        self.cambiar_pagina("Recuperar Acceso Administrador")
        tarjeta = self.crear_tarjeta(440)

        # Código secreto definido directamente en el código
        CODIGO_SECRETO_ADMIN = "HOTEL_123456789"

        dibujar_logo(tarjeta).pack(pady=(30, 4))
        tk.Label(tarjeta, text="Recuperar Acceso\nAdministrador",
                 font=FUENTE_TITULO, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO, justify="center").pack(pady=(8, 4))

        frame_campos = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_campos.pack(padx=40, fill="x")

        tk.Label(frame_campos, text="Codigo Secreto",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_codigo = crear_entrada(frame_campos, "HOTEL_123456789")
        entrada_codigo.pack(fill="x", ipady=8)

        # Variable de control para saber si el código fue validado
        codigo_validado = [False]

        def accion_validar_codigo():
            codigo_ingresado = entrada_codigo.get().strip()
            if codigo_ingresado == CODIGO_SECRETO_ADMIN:
                codigo_validado[0] = True
                messagebox.showinfo("Validado",
                    "Código correcto. Ingresa tu nueva contraseña.")
            else:
                messagebox.showerror("Error", "Código secreto incorrecto.")

        frame_btn_validar = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_btn_validar.pack(padx=40, fill="x", pady=(10, 0))
        crear_boton(frame_btn_validar, "VALIDAR CODIGO",
                    accion_validar_codigo).pack(fill="x", ipady=4)

        tk.Label(frame_campos, text="Nueva Contraseña:",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(14, 2))
        entrada_nueva = crear_entrada(frame_campos, mostrar="•")
        entrada_nueva.pack(fill="x", ipady=8)

        tk.Label(frame_campos, text="Confirmar contraseña:",
                 font=FUENTE_ETIQUETA, fg=COLOR_TEXTO_OSCURO,
                 bg=COLOR_BLANCO).pack(anchor="w", pady=(10, 2))
        entrada_confirmar = crear_entrada(frame_campos, mostrar="•")
        entrada_confirmar.pack(fill="x", ipady=8)

        def accion_cambiar_contrasena_admin():
            if not codigo_validado[0]:
                messagebox.showerror("Error",
                    "Primero valida el código secreto.")
                return

            nueva     = entrada_nueva.get().strip()
            confirmar = entrada_confirmar.get().strip()

            # Si no ingresó nueva contraseña, solo vuelve al inicio
            if not nueva and not confirmar:
                self.mostrar_inicio_administrador()
                return
            if nueva != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            guardar_contrasena_administrador(nueva)
            messagebox.showinfo("¡Éxito!",
                "Contraseña de administrador actualizada correctamente.")
            self.mostrar_inicio_administrador()

        frame_boton = tk.Frame(tarjeta, bg=COLOR_BLANCO)
        frame_boton.pack(padx=40, fill="x", pady=(14, 36))
        crear_boton(
            frame_boton,
            "CAMBIO DE CONTRASEÑA\nVOLVER AL INICIO DE SESION",
            accion_cambiar_contrasena_admin
        ).pack(fill="x", ipady=4)


# ─────────────────────────────────────────────
#  Punto de entrada de la aplicación
# ─────────────────────────────────────────────

if __name__ == "__main__":
    aplicacion = AplicacionHotelMatch()
    aplicacion.mainloop()
