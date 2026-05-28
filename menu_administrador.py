import os
import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from hotelmatch.colores import C
from hotelmatch.datos import leer_hoteles, agregar_hotel, eliminar_hotel



reservas = [
    {"id": "#RES-001", "cliente": "Julian Arce",    "id_cliente": "#HM-48291", "checkin": "12 Oct 2024", "habitacion": "Deluxe Vista Mar",  "estado": "CONFIRMADA", "monto": "Bs450.00"},
    {"id": "#RES-002", "cliente": "Mateo Paz",      "id_cliente": "#HM-48305", "checkin": "14 Oct 2024", "habitacion": "Standard King",     "estado": "PENDIENTE",  "monto": "Bs280.00"},
    {"id": "#RES-003", "cliente": "Elena Rodriguez","id_cliente": "#HM-48312", "checkin": "15 Oct 2024", "habitacion": "Penthouse Loft",    "estado": "CONFIRMADA", "monto": "Bs890.00"},
]

reportes = [
    {"asunto": "Fuga de agua masiva",       "ubicacion": "Suite Presidencial - Baño B", "prioridad": "CRÍTICA", "estado": "Urgente",    "asignado": "RM"},
    {"asunto": "Aire Acond. No Enfría",     "ubicacion": "Habitación 402 - Ala Norte",  "prioridad": "MEDIA",   "estado": "Programada", "asignado": "JC"},
    {"asunto": "Cambio luminaria pasillo",  "ubicacion": "Área Común - Lobby",          "prioridad": "BAJA",    "estado": "Pendiente",  "asignado": ""},
]

config_admin = {
    "nombre":   "Admin User",
    "correo":   "admin@hotelmatch.com",
    "rol":      "Super Administrador",
    "zona":     "GMT-5 (Lima, Bogota)",
}

# ─────────────────────────────────────────────
#  Widgets reutilizables
# ─────────────────────────────────────────────

def separador(padre, color="#2a2a4e"):
    return tk.Frame(padre, bg=color, height=1)

def tarjeta(padre, **kwargs):
    return tk.Frame(padre, bg=C["card_bg"],
                    highlightthickness=1,
                    highlightbackground=C["borde"],
                    **kwargs)

def etiqueta_titulo(padre, texto, subtexto=""):
    tk.Label(padre, text=texto,
             font=("Segoe UI", 22, "bold"),
             fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w")
    if subtexto:
        tk.Label(padre, text=subtexto,
                 font=("Segoe UI", 10),
                 fg=C["texto_light"], bg=C["main_bg"]).pack(anchor="w", pady=(0, 16))

def boton_naranja(padre, texto, comando, ancho=20):
    btn = tk.Button(padre, text=texto, command=comando,
                    bg=C["naranja"], fg=C["blanco"],
                    font=("Segoe UI", 9, "bold"),
                    relief="flat", cursor="hand2",
                    padx=14, pady=8, width=ancho)
    btn.bind("<Enter>", lambda e: btn.config(bg="#c94208"))
    btn.bind("<Leave>", lambda e: btn.config(bg=C["naranja"]))
    return btn

def chip_estado(padre, texto, color_bg, color_texto="#ffffff"):
    return tk.Label(padre, text=texto,
                    bg=color_bg, fg=color_texto,
                    font=("Segoe UI", 8, "bold"),
                    padx=8, pady=3)

# ─────────────────────────────────────────────
#  PÁGINA: Propiedades
# ─────────────────────────────────────────────

class PaginaPropiedades(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self.frame_formulario = None
        self._construir()

    def _construir(self):
        canvas = tk.Canvas(self, bg=C["main_bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.interior = tk.Frame(canvas, bg=C["main_bg"])

        self.interior.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.interior, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        header = tk.Frame(self.interior, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))
        etiqueta_titulo(header, "Propiedades",
                        "Gestión editorial y supervisión de activos hoteleros.")

        self.frame_cards = tk.Frame(self.interior, bg=C["main_bg"])
        self.frame_cards.pack(fill="x", padx=28, pady=(0, 16))
        self._actualizar_cards()

        separador(self.interior, C["borde"]).pack(fill="x", padx=28, pady=4)

        self.lista_frame = tk.Frame(self.interior, bg=C["main_bg"])
        self.lista_frame.pack(fill="x", padx=28, pady=8)
        self._actualizar_lista()

        frame_btn = tk.Frame(self.interior, bg=C["main_bg"])
        frame_btn.pack(fill="x", padx=28, pady=(4, 0))
        boton_naranja(frame_btn, "+ Nuevo Registro",
                      self._mostrar_formulario).pack(side="left")

        self.area_form = tk.Frame(self.interior, bg=C["main_bg"])
        self.area_form.pack(fill="x", padx=28, pady=8)

    def _actualizar_cards(self):
        for w in self.frame_cards.winfo_children():
            w.destroy()
        hoteles = leer_hoteles()
        activos = sum(1 for h in hoteles if h.get("estado") == "Activo")
        mantenimiento = sum(1 for h in hoteles if h.get("estado") == "Mantenimiento")
        total_hab = sum(int(h.get("habitaciones", 0)) for h in hoteles)

        resumen = [
            ("🏨", "TOTAL ACTIVAS",      str(activos)),
            ("🛏", "TOTAL HABITACIONES", f"{total_hab:,}"),
            ("🔧", "BAJO MANTENIMIENTO", f"{mantenimiento:02d}"),
        ]
        for icono, etiqueta, valor in resumen:
            c = tarjeta(self.frame_cards)
            c.pack(side="left", padx=(0, 12), pady=4, ipadx=20, ipady=14)
            tk.Label(c, text=icono, font=("Segoe UI", 20),
                     bg=C["card_bg"], fg=C["naranja"]).pack(anchor="w", padx=16, pady=(12, 0))
            tk.Label(c, text=etiqueta, font=("Segoe UI", 8),
                     bg=C["card_bg"], fg=C["texto_light"]).pack(anchor="w", padx=16)
            tk.Label(c, text=valor, font=("Segoe UI", 20, "bold"),
                     bg=C["card_bg"], fg=C["texto_dark"]).pack(anchor="w", padx=16, pady=(0, 12))

    def _actualizar_lista(self):
        for w in self.lista_frame.winfo_children():
            w.destroy()
        for hotel in leer_hoteles():
            self._fila_hotel(self.lista_frame, hotel)

    def _fila_hotel(self, padre, hotel):
        fila = tarjeta(padre)
        fila.pack(fill="x", pady=5)

        tipo_texto = hotel.get("tipo", "")
        if isinstance(tipo_texto, list):
            tipo_texto = ", ".join(tipo_texto)
        tk.Label(fila, text=tipo_texto,
                 font=("Segoe UI", 8, "bold"),
                 fg=C["naranja"], bg=C["card_bg"]).grid(row=0, column=0, sticky="w", padx=16, pady=(10, 0))
        tk.Label(fila, text=hotel.get("nombre", ""),
                 font=("Segoe UI", 13, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).grid(row=1, column=0, sticky="w", padx=16)

        tipo_texto = hotel.get("tipo", "")
        if isinstance(tipo_texto, list):
            tipo_texto = ", ".join(tipo_texto)

        info = f"📍 {hotel.get('ciudad','')}    🛏 {hotel.get('habitaciones','')} Habitaciones"
        tk.Label(fila, text=info,
                 font=("Segoe UI", 9),
                 fg=C["texto_light"], bg=C["card_bg"]).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 10))

        color = C["verde"] if hotel.get("estado") == "Activo" else C["amarillo"]
        chip_estado(fila, f"● {hotel.get('estado','')}", color).grid(row=0, column=1, sticky="e", padx=16, pady=(10, 0))
        tk.Label(fila, text=f"ID: {hotel.get('id','')}",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).grid(row=1, column=1, sticky="e", padx=16)

        tk.Label(fila, text="✕", font=("Segoe UI", 10), fg=C["rojo"],
                 bg=C["card_bg"], cursor="hand2").grid(row=2, column=1, sticky="e", padx=16, pady=(0, 10))
        fila.winfo_children()[-1].bind("<Button-1>",
            lambda e, id=hotel.get("id"): self._eliminar(id))

        fila.columnconfigure(0, weight=1)

    def _eliminar(self, id_hotel):
        if messagebox.askyesno("Confirmar", "¿Eliminar este hotel?"):
            eliminar_hotel(id_hotel)
            self._actualizar_lista()
            self._actualizar_cards()

    def _mostrar_formulario(self):
        for w in self.area_form.winfo_children():
            w.destroy()

        form = tarjeta(self.area_form)
        form.pack(fill="x", pady=8)

        tk.Label(form, text="NUEVO HOTEL", font=("Segoe UI", 10, "bold"),
                 fg=C["naranja"], bg=C["card_bg"]).grid(row=0, column=0, columnspan=4,
                 sticky="w", padx=16, pady=(14, 8))

        campos = [
            ("Nombre",       "nombre"),
            ("Ciudad",       "ciudad"),
            ("Habitaciones", "habitaciones"),
            ("Descripción",  "descripcion"),
        ]

        entradas = {}
        for i, (etiqueta, clave) in enumerate(campos):
            col = (i % 2) * 2
            row = (i // 2) + 1
            tk.Label(form, text=etiqueta, font=("Segoe UI", 8),
                     fg=C["texto_mid"], bg=C["card_bg"]).grid(
                     row=row, column=col, sticky="w", padx=(16, 4), pady=4)
            entrada = tk.Entry(form, font=("Segoe UI", 9), width=24,
                               relief="solid", bd=1)
            entrada.grid(row=row, column=col + 1, sticky="w", padx=(0, 16), pady=4)
            entradas[clave] = entrada

        tipo_opciones = [
            "Luxury Segment",
            "Urban Concept",
            "Winter Peak",
            "Business",
            "Resort",
            "Boutique",
            "Familiar",
        ]
        tipo_vars = {}
        fila_tipo = len(campos) // 2 + 1
        tk.Label(form, text="Tipo", font=("Segoe UI", 8),
                 fg=C["texto_mid"], bg=C["card_bg"]).grid(
                 row=fila_tipo, column=0, sticky="nw", padx=(16, 4), pady=4)
        tipo_frame = tk.Frame(form, bg=C["card_bg"])
        tipo_frame.grid(row=fila_tipo, column=1, columnspan=3,
                        sticky="w", padx=(0, 16), pady=4)
        for i, opcion in enumerate(tipo_opciones):
            var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(tipo_frame, text=opcion, variable=var,
                                bg=C["card_bg"], fg=C["texto_dark"],
                                activebackground=C["card_bg"], selectcolor=C["card_bg"],
                                font=("Segoe UI", 8), anchor="w")
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=(0, 14), pady=2)
            tipo_vars[opcion] = var

        tk.Label(form, text="Estado", font=("Segoe UI", 8),
                 fg=C["texto_mid"], bg=C["card_bg"]).grid(
                 row=len(campos) // 2 + 2, column=0, sticky="w", padx=(16, 4), pady=4)
        estado_var = tk.StringVar(value="Activo")
        tk.OptionMenu(form, estado_var, "Activo", "Mantenimiento", "Inactivo").grid(
                 row=len(campos) // 2 + 2, column=1, sticky="w", pady=4)

        fila_btn = len(campos) // 2 + 3
        boton_naranja(form, "Guardar Hotel",
                      lambda: self._guardar(entradas, tipo_vars, estado_var, form)).grid(
                      row=fila_btn, column=0, columnspan=2, padx=16, pady=(8, 14), sticky="w")
        tk.Label(form, text="Cancelar", font=("Segoe UI", 9),
                 fg=C["rojo"], bg=C["card_bg"], cursor="hand2").grid(
                 row=fila_btn, column=2, columnspan=2, sticky="w", pady=(8, 14))
        form.winfo_children()[-1].bind("<Button-1>",
            lambda e: [w.destroy() for w in self.area_form.winfo_children()])

    def _guardar(self, entradas, tipo_vars, estado_var, form):
        datos = {clave: entrada.get().strip() for clave, entrada in entradas.items()}
        tipos_seleccionados = [tipo for tipo, var in tipo_vars.items() if var.get()]
        datos["tipo"] = tipos_seleccionados
        datos["estado"] = estado_var.get()

        if not datos["nombre"] or not datos["ciudad"]:
            messagebox.showwarning("Campos vacíos", "Nombre y Ciudad son obligatorios.")
            return

        if not tipos_seleccionados:
            messagebox.showwarning("Tipo requerido", "Debes seleccionar al menos un tipo de hotel.")
            return

        agregar_hotel(datos)
        messagebox.showinfo("Éxito", f"Hotel '{datos['nombre']}' guardado correctamente.")

        for w in self.area_form.winfo_children():
            w.destroy()
        self._actualizar_lista()
        self._actualizar_cards()
    

# ─────────────────────────────────────────────
#  PÁGINA: Reservas
# ─────────────────────────────────────────────

class PaginaReservas(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self.anio  = 2024
        self.mes   = 10
        self._construir()

    def _construir(self):
        # 1. FORZAR LA LECTURA DE RESERVAS AL PRINCIPIO
        # Cargamos los datos del archivo plano de inmediato en una variable de la clase
        self.reservas = self._leer_reservas()

        # Título de la sección
        tk.Label(self, text="Calendario de Ocupación",
                 font=("Segoe UI", 16, "bold"),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w", padx=28, pady=20)

        contenido = tk.Frame(self, bg=C["main_bg"])
        contenido.pack(fill="both", expand=True, padx=28)

        # Columna izquierda — Calendario
        col_izq = tk.Frame(contenido, bg=C["main_bg"])
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 20))

        # Barra del mes
        barra_mes = tk.Frame(col_izq, bg=C["main_bg"])
        barra_mes.pack(fill="x", pady=(0, 10))

        self.lbl_mes = tk.Label(barra_mes, font=("Segoe UI", 12, "bold"),
                                fg=C["texto_dark"], bg=C["main_bg"])
        self.lbl_mes.pack(side="left")

        btn_der = tk.Button(barra_mes, text="▶", font=("Segoe UI", 9),
                            bg=C["card_bg"], fg=C["texto_dark"], relief="flat",
                            command=lambda: self._cambiar_mes(1))
        btn_der.pack(side="right", padx=2)

        btn_izq = tk.Button(barra_mes, text="◀", font=("Segoe UI", 9),
                            bg=C["card_bg"], fg=C["texto_dark"], relief="flat",
                            command=lambda: self._cambiar_mes(-1))
        btn_izq.pack(side="right", padx=2)

        # Mapeamos los días para el calendario usando la lista que acabamos de leer
        self.reservas_por_dia = self._mapear_reservas_por_dia(
            self.reservas,
            self.anio,
            self.mes
        )

        # Construir contenedor del calendario físico
        self.frame_cal = tarjeta(col_izq)
        self.frame_cal.pack(fill="both", expand=True)
        
        # Dibujamos las celdas del calendario
        self._dibujar_calendario()

        # Columna derecha — próximas reservas
        col_der = tk.Frame(contenido, bg=C["main_bg"], width=260)
        col_der.pack(side="right", fill="y")
        col_der.pack_propagate(False)

        tk.Label(col_der, text="Próximas Reservas",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w", pady=(0, 8))

        # 2. RENDERIZAR LAS TARJETAS DERECHAS
        # Si la lista tiene elementos leídos, dibujará cada tarjeta con su información real
        if self.reservas:
            for r in self.reservas:
                self._tarjeta_reserva(col_der, r)
        else:
            # Mensaje decorativo en caso de que el archivo reservas.txt esté vacío
            tk.Label(col_der, text="No hay reservas en reservas.txt",
                     font=("Segoe UI", 9, "italic"),
                     fg=C["texto_light"], bg=C["main_bg"]).pack(anchor="w", pady=10)
    def _dibujar_calendario(self):
        for w in self.frame_cal.winfo_children():
            w.destroy()

        nombre_mes = ["", "Enero","Febrero","Marzo","Abril","Mayo","Junio",
                      "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][self.mes]

        self.reservas = self._leer_reservas()
        self.reservas_por_dia = self._mapear_reservas_por_dia(self.reservas, self.anio, self.mes)

        # Navegación
        nav = tk.Frame(self.frame_cal, bg=C["card_bg"])
        nav.pack(fill="x", padx=14, pady=10)
        tk.Label(nav, text=f"{nombre_mes} {self.anio}",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(side="left")

        tk.Button(nav, text=">", command=self._mes_siguiente,
                  bg=C["card_bg"], fg=C["texto_dark"],
                  relief="flat", font=("Segoe UI", 11), cursor="hand2").pack(side="right")
        tk.Button(nav, text="HOY", command=self._ir_hoy,
                  bg=C["borde"], fg=C["texto_dark"],
                  relief="flat", font=("Segoe UI", 9), padx=6, cursor="hand2").pack(side="right", padx=4)
        tk.Button(nav, text="<", command=self._mes_anterior,
                  bg=C["card_bg"], fg=C["texto_dark"],
                  relief="flat", font=("Segoe UI", 11), cursor="hand2").pack(side="right")

        # Días de semana
        dias_sem = ["DOM", "LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB"]
        grid = tk.Frame(self.frame_cal, bg=C["card_bg"])
        grid.pack(fill="both", expand=True, padx=10, pady=4)

        for col, dia in enumerate(dias_sem):
            tk.Label(grid, text=dia, font=("Segoe UI", 8),
                     fg=C["texto_light"], bg=C["card_bg"],
                     width=5).grid(row=0, column=col, pady=4)

        # Días del mes
# Días del mes (Reemplaza este fragmento interno dentro de tu función actual)
        primer_dia = datetime.date(self.anio, self.mes, 1).weekday()
        primer_dia = (primer_dia + 1) % 7  # ajuste DOM=0
        dias_mes = (datetime.date(self.anio, self.mes % 12 + 1, 1)
                    - datetime.timedelta(days=1)).day if self.mes < 12 else 31

        hoy = datetime.date.today()
        dia_num = 1
        for fila in range(1, 7):
            for col in range(7):
                idx = (fila - 1) * 7 + col
                if idx < primer_dia or dia_num > dias_mes:
                    tk.Label(grid, text="", bg=C["card_bg"],
                             width=5, height=2).grid(row=fila, column=col)
                else:
                    es_hoy = (dia_num == hoy.day and
                              self.mes == hoy.month and
                              self.anio == hoy.year)
                    reservado = self.reservas_por_dia.get(dia_num)
                    
                    if reservado:
                        reserva = reservado[0]
                        color = reserva.get("color_hex", "#10B981")
                        
                        # CREACIÓN DE BOTÓN VISUAL: Muestra el número con el color único de fondo del hotel
                        btn = tk.Button(grid, text=str(dia_num),
                                        font=("Segoe UI", 9, "bold"),
                                        bg=color, fg=C["blanco"],
                                        activebackground=color, activeforeground=C["blanco"],
                                        relief="flat", width=5, height=2,
                                        cursor="hand2", bd=0,
                                        command=lambda d=dia_num: self._mostrar_detalle_dia(d))
                        btn.grid(row=fila, column=col, padx=2, pady=2)
                        
                        # Efecto visual: Resaltar ligeramente al pasar el mouse por encima
                        btn.bind("<Enter>", lambda e, b=btn: b.config(relief="groove"))
                        btn.bind("<Leave>", lambda e, b=btn: b.config(relief="flat"))
                    else:
                        bg = C["naranja"] if es_hoy else C["card_bg"]
                        fg = C["blanco"] if es_hoy else C["texto_dark"]
                        tk.Label(grid, text=str(dia_num),
                                 font=("Segoe UI", 9, "bold" if es_hoy else "normal"),
                                 bg=bg, fg=fg, width=5, height=2).grid(row=fila, column=col, padx=2, pady=2)
                    dia_num += 1

    def _mes_anterior(self):
        if self.mes == 1:
            self.mes = 12; self.anio -= 1
        else:
            self.mes -= 1
        self._dibujar_calendario()

    def _leer_reservas(self):
        ruta_root = os.path.join(os.path.dirname(__file__), "reservas.txt")
        ruta_hotelmatch = os.path.join(
            os.path.dirname(__file__), "hotelmatch", "data", "reservas.txt"
        )
        ruta = ruta_hotelmatch if os.path.exists(ruta_hotelmatch) else ruta_root

        reservas_lista = []
        if not os.path.exists(ruta):
            return reservas_lista

        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue

                datos_reserva = {}
                partes = linea.split("|")
                for parte in partes:
                    if "=" in parte:
                        clave, valor = parte.split("=", 1)
                        datos_reserva[clave.strip()] = valor.strip()

                codigo = f"#RES-{datos_reserva.get('id', '000')}"
                cliente = "Huésped Registrado"
                hotel_nombre = datos_reserva.get("hotel", "Hotel Desconocido")
                monto = datos_reserva.get("precio", "0")
                estado = datos_reserva.get("estado", "Confirmada")

                colores_hoteles = {
                    "los tajibos": "#3b82f6",
                    "gran hotel paris": "#2a2a4e",
                    "skyline loft madrid": "#10b981"
                }
                color_hex = colores_hoteles.get(hotel_nombre.lower(), C["naranja"])

                check_in_str = datos_reserva.get("fecha", "Seleccionar fecha")
                if check_in_str == "Seleccionar fecha":
                    id_num = int(datos_reserva.get('id', '1'))
                    offset_dia = 5 + (id_num * 4) % 20
                    fecha_entrada = datetime.date(self.anio, self.mes, offset_dia)
                    fecha_salida = fecha_entrada + datetime.timedelta(days=2)
                elif " - " in check_in_str:
                    partes_fecha = check_in_str.split(" - ", 1)
                    fecha_entrada = self._parse_fecha(partes_fecha[0])
                    fecha_salida = self._parse_fecha(partes_fecha[1])
                    if fecha_entrada is None or fecha_salida is None:
                        continue
                else:
                    fecha_entrada = self._parse_fecha(check_in_str)
                    if fecha_entrada is None:
                        continue
                    fecha_salida = fecha_entrada + datetime.timedelta(days=2)

                reservas_lista.append({
                    "codigo": codigo,
                    "cliente": cliente,
                    "hotel_nombre": hotel_nombre,
                    "color_hex": color_hex,
                    "check_in": fecha_entrada,
                    "check_out": fecha_salida,
                    "monto": monto,
                    "estado": estado,
                })
        return reservas_lista

    def _parse_fecha(self, fecha_str):
        fecha_str = fecha_str.strip()
        if not fecha_str:
            return None

        meses = {
            "Ene": "Jan", "Feb": "Feb", "Mar": "Mar", "Abr": "Apr",
            "May": "May", "Jun": "Jun", "Jul": "Jul", "Ago": "Aug",
            "Sep": "Sep", "Oct": "Oct", "Nov": "Nov", "Dic": "Dec"
        }
        for esp, eng in meses.items():
            if esp in fecha_str:
                fecha_str = fecha_str.replace(esp, eng)

        formatos = [
            "%Y-%m-%d",
            "%d %b, %Y",
            "%d %b %Y",
            "%d %B, %Y",
            "%d %B %Y"
        ]

        for fmt in formatos:
            try:
                return datetime.datetime.strptime(fecha_str, fmt).date()
            except ValueError:
                continue

        return None

    def _mapear_reservas_por_dia(self, reservas, anio, mes):
        dias_veh = {}
        primer_dia_mes = datetime.date(anio, mes, 1)
        if mes == 12:
            ultimo_dia_mes = datetime.date(anio, 12, 31)
        else:
            ultimo_dia_mes = datetime.date(anio, mes + 1, 1) - datetime.timedelta(days=1)

        for reserva in reservas:
            inicio = max(reserva["check_in"], primer_dia_mes)
            fin = min(reserva["check_out"], ultimo_dia_mes)
            if inicio > fin:
                continue
            fecha_actual = inicio
            while fecha_actual <= fin:
                dia = fecha_actual.day
                dias_veh.setdefault(dia, []).append(reserva)
                fecha_actual += datetime.timedelta(days=1)
        return dias_veh

    def _mostrar_detalle_dia(self, dia):
        reservas = self.reservas_por_dia.get(dia, [])
        if not reservas:
            return

        fecha = datetime.date(self.anio, self.mes, dia)
        ventana = tk.Toplevel(self)
        ventana.title(f"Reservas {fecha.isoformat()}")
        ventana.geometry("420x260")
        ventana.configure(bg=C["main_bg"])
        ventana.transient(self)
        ventana.grab_set()

        tk.Label(ventana, text=f"Reservas para {fecha.strftime('%d %b %Y')}",
                 bg=C["main_bg"], fg=C["texto_dark"],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=16, pady=(16, 8))

        detalle_frame = tk.Frame(ventana, bg=C["main_bg"])
        detalle_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        for reserva in reservas:
            bloque = tk.Frame(detalle_frame, bg=C["main_bg"], bd=1,
                              relief="solid", highlightbackground=C["borde"],
                              highlightthickness=1)
            bloque.pack(fill="x", pady=6)

            tk.Label(bloque, text=f"{reserva['hotel_nombre']} — {reserva['estado']}",
                     bg=C["main_bg"], fg=C["texto_dark"],
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 0))
            tk.Label(bloque, text=f"Código: {reserva['codigo']} | Cliente: {reserva['cliente']}",
                     bg=C["main_bg"], fg=C["texto_light"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(2, 0))
            tk.Label(bloque, text=f"{reserva['check_in'].isoformat()} → {reserva['check_out'].isoformat()}",
                     bg=C["main_bg"], fg=C["texto_light"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(2, 0))
            tk.Label(bloque, text=f"Monto: Bs{reserva['monto']} | Color: {reserva['color_hex']}",
                     bg=C["main_bg"], fg=C["texto_light"],
                     font=("Segoe UI", 9)).pack(anchor="w", padx=10, pady=(2, 8))

    def _mes_siguiente(self):
        if self.mes == 12:
            self.mes = 1; self.anio += 1
        else:
            self.mes += 1
        self._dibujar_calendario()

    def _ir_hoy(self):
        hoy = datetime.date.today()
        self.mes = hoy.month; self.anio = hoy.year
        self._dibujar_calendario()

    def _tarjeta_reserva(self, padre, r):
        c = tarjeta(padre)
        c.pack(fill="x", pady=5, ipadx=10, ipady=8)

        # Nombre del Cliente leído del archivo txt
        tk.Label(c, text=r["cliente"],
                 font=("Segoe UI", 10, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=10, pady=(8, 0))
        
        # Muestra el nombre del Hotel asignado
        tk.Label(c, text=r["hotel_nombre"],
                 font=("Segoe UI", 8, "bold"),
                 fg=C["texto_light"], bg=C["card_bg"]).pack(anchor="w", padx=10)

        fila = tk.Frame(c, bg=C["card_bg"])
        fila.pack(fill="x", padx=10, pady=2)
        
        # Formatear la fecha datetime.date para que se vea amigable (Ej: 12 Oct 2024)
        fecha_amigable = r["check_in"].strftime("%d %b %Y") if isinstance(r["check_in"], datetime.date) else str(r["check_in"])
        
        tk.Label(fila, text=f"Entrada: {fecha_amigable}",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).pack(side="left")
                 
        # Precio o Monto total
        tk.Label(fila, text=f"Bs{r['monto']}",
                 font=("Segoe UI", 9, "bold"),
                 fg=C["naranja"], bg=C["card_bg"]).pack(side="right")

        # Estado visual de la reserva
        estado_texto = r["estado"].upper()
        color = C["verde"] if estado_texto == "CONFIRMADA" else C["amarillo"]
        chip_estado(c, estado_texto, color).pack(anchor="w", padx=10, pady=(0, 8))
# ─────────────────────────────────────────────
#  PÁGINA: Ingresos
# ─────────────────────────────────────────────

class PaginaIngresos(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        header = tk.Frame(self, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))
        etiqueta_titulo(header, "Resumen Financiero",
                        "Panel de control de ingresos y rendimiento editorial de HotelMatch.")

        # Tarjetas métricas
        frame_metricas = tk.Frame(self, bg=C["main_bg"])
        frame_metricas.pack(fill="x", padx=28, pady=(0, 16))

        metricas = [
            ("💰", "INGRESOS BRUTOS",  "Bs142,850"),
            ("📊", "ADR",              "Bs215.40"),
            ("%",  "OCCUPATION RATE",  "84.2%"),
            ("📈", "OPERATING MARGIN", "28.5%"),
        ]
        for icono, etiqueta, valor in metricas:
            c = tarjeta(frame_metricas)
            c.pack(side="left", padx=(0, 10), ipadx=14, ipady=10)
            tk.Label(c, text=f"{icono}  {etiqueta}",
                     font=("Segoe UI", 8), fg=C["texto_light"],
                     bg=C["card_bg"]).pack(anchor="w", padx=12, pady=(10, 0))
            tk.Label(c, text=valor,
                     font=("Segoe UI", 18, "bold"),
                     fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=12, pady=(0, 10))

        # Sección evolución mensual
        contenido = tk.Frame(self, bg=C["main_bg"])
        contenido.pack(fill="both", expand=True, padx=28, pady=4)

        col_izq = tarjeta(contenido)
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(col_izq, text="Evolución Mensual",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=16, pady=(14, 0))
        tk.Label(col_izq, text="Comparativa de ingresos brutos 2024",
                 font=("Segoe UI", 9), fg=C["naranja"],
                 bg=C["card_bg"]).pack(anchor="w", padx=16)

        # Gráfico de barras simple con Canvas
        canvas = tk.Canvas(col_izq, bg=C["card_bg"], height=160,
                           highlightthickness=0)
        canvas.pack(fill="x", padx=16, pady=16)

        meses = ["ENE","FEB","MAR","ABR","MAY","JUN"]
        valores = [45, 62, 58, 80, 95, 142]
        max_val = max(valores)
        ancho_barra = 40
        espacio = 30
        base_y = 140

        for i, (mes, val) in enumerate(zip(meses, valores)):
            x = 30 + i * (ancho_barra + espacio)
            alto = int((val / max_val) * 110)
            color = C["naranja"] if i == len(valores) - 1 else "#e0e0e0"
            canvas.create_rectangle(x, base_y - alto, x + ancho_barra,
                                    base_y, fill=color, outline="")
            canvas.create_text(x + ancho_barra // 2, base_y + 12,
                               text=mes, font=("Segoe UI", 8),
                               fill=C["texto_light"])
            if i == len(valores) - 1:
                canvas.create_text(x + ancho_barra // 2, base_y - alto - 12,
                                   text=f"Bs{val}k",
                                   font=("Segoe UI", 8, "bold"),
                                   fill=C["texto_dark"])

        # Panel proyección
        col_der = tk.Frame(contenido, bg="#1e1e2e", width=220)
        col_der.pack(side="right", fill="y")
        col_der.pack_propagate(False)

        tk.Label(col_der, text="PROYECCIÓN 2024",
                 font=("Segoe UI", 8), fg="#888899",
                 bg="#1e1e2e").pack(anchor="w", padx=16, pady=(16, 4))
        tk.Label(col_der, text="Crecimiento\nSostenido",
                 font=("Segoe UI", 14, "bold"),
                 fg=C["blanco"], bg="#1e1e2e",
                 justify="left").pack(anchor="w", padx=16)
        tk.Label(col_der,
                 text="HotelMatch proyecta un\ncrecimiento del 18% anual\nbasado en tarifas dinámicas.",
                 font=("Segoe UI", 8), fg="#888899",
                 bg="#1e1e2e", justify="left").pack(anchor="w", padx=16, pady=8)

        for punto in ["● Incremento en Direct Booking",
                      "● Reducción de Costes",
                      "● Fidelización de Clientes VIP"]:
            tk.Label(col_der, text=punto, font=("Segoe UI", 8),
                     fg=C["naranja"], bg="#1e1e2e").pack(anchor="w", padx=16, pady=1)

        boton_naranja(col_der, "Descargar Reporte",
                      lambda: messagebox.showinfo("Reporte", "Generando reporte..."),
                      ancho=18).pack(pady=16, padx=16, fill="x")

        # Tabla de ingresos recientes
        tabla_frame = tarjeta(self)
        tabla_frame.pack(fill="x", padx=28, pady=12)
        tk.Label(tabla_frame, text="Recent Revenue Details",
                 font=("Segoe UI", 11, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=16, pady=(12, 4))

        cols = ["ID RESERVA", "FECHA", "PROPIEDAD", "ESTADO", "MONTO"]
        cabecera = tk.Frame(tabla_frame, bg="#f8f8fa")
        cabecera.pack(fill="x", padx=16)
        for col in cols:
            tk.Label(cabecera, text=col, font=("Segoe UI", 8, "bold"),
                     fg=C["texto_light"], bg="#f8f8fa",
                     width=16, anchor="w").pack(side="left", pady=6)

        datos = [
            ("#RES-2940", "12 Jun, 2024", "Skyline Loft Madrid", "COMPLETADO", "Bs1,240.00"),
            ("#RES-2939", "11 Jun, 2024", "Los Tajibos",         "CONFIRMADA", "Bs890.00"),
            ("#RES-2938", "10 Jun, 2024", "Gran Hotel Paris",    "PENDIENTE",  "Bs450.00"),
        ]
        for fila_d in datos:
            fila = tk.Frame(tabla_frame, bg=C["card_bg"])
            fila.pack(fill="x", padx=16)
            separador(fila, C["borde"]).pack(fill="x")
            fila_c = tk.Frame(fila, bg=C["card_bg"])
            fila_c.pack(fill="x")
            for i, val in enumerate(fila_d):
                color = C["texto_dark"]
                if i == 3:
                    color = C["verde"] if val == "COMPLETADO" else C["naranja"]
                if i == 4:
                    color = C["naranja"]
                tk.Label(fila_c, text=val, font=("Segoe UI", 9),
                         fg=color, bg=C["card_bg"],
                         width=16, anchor="w").pack(side="left", pady=6)

# ─────────────────────────────────────────────
#  PÁGINA: Mantenimiento
# ─────────────────────────────────────────────

class PaginaMantenimiento(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        # Header con botón
        header = tk.Frame(self, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))

        tk.Label(header, text="Gestión de Mantenimiento",
                 font=("Segoe UI", 22, "bold"),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(side="left", anchor="w")
        boton_naranja(header, "+ Nuevo Reporte",
                      self._nuevo_reporte, ancho=16).pack(side="right")

        tk.Label(self, text="Control editorial de activos y reparaciones críticas.",
                 font=("Segoe UI", 10), fg=C["texto_light"],
                 bg=C["main_bg"]).pack(anchor="w", padx=28, pady=(0, 16))

        # Tarjetas métricas
        frame_metricas = tk.Frame(self, bg=C["main_bg"])
        frame_metricas.pack(fill="x", padx=28, pady=(0, 16))

        metricas = [
            ("📋", "12", "Activos",   "Tareas en progreso actualmente"),
            ("⚠",  "03", "Urgente",   "Requieren atención inmediata"),
            ("📅", "08", "Hoy",       "Programados para el cierre del día"),
            ("👷", "05", "Personal",  "Técnicos activos en sitio"),
        ]
        colores_num = [C["texto_dark"], C["rojo"], C["azul"], C["texto_dark"]]
        for (icono, num, titulo, desc), color_n in zip(metricas, colores_num):
            c = tarjeta(frame_metricas)
            c.pack(side="left", padx=(0, 10), ipadx=14, ipady=8)
            tk.Label(c, text=icono, font=("Segoe UI", 16),
                     bg=C["card_bg"], fg=C["naranja"]).pack(anchor="w", padx=14, pady=(10, 0))
            tk.Label(c, text=num, font=("Segoe UI", 20, "bold"),
                     bg=C["card_bg"], fg=color_n).pack(anchor="w", padx=14)
            tk.Label(c, text=titulo, font=("Segoe UI", 9, "bold"),
                     bg=C["card_bg"], fg=C["texto_dark"]).pack(anchor="w", padx=14)
            tk.Label(c, text=desc, font=("Segoe UI", 8),
                     bg=C["card_bg"], fg=C["texto_light"],
                     wraplength=130, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

        # Tabla de tareas
        tabla = tarjeta(self)
        tabla.pack(fill="both", expand=True, padx=28, pady=4)

        tk.Label(tabla, text="Lista de Tareas Pendientes",
                 font=("Segoe UI", 11, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=16, pady=(12, 4))

        cols = ["ASUNTO DEL REPORTE", "UBICACIÓN / ACTIVO", "PRIORIDAD", "ESTADO", "ASIGNADO", "ACCIONES"]
        cab = tk.Frame(tabla, bg="#f8f8fa")
        cab.pack(fill="x", padx=16)
        anchos = [22, 22, 10, 12, 10, 8]
        for col, ancho in zip(cols, anchos):
            tk.Label(cab, text=col, font=("Segoe UI", 8, "bold"),
                     fg=C["texto_light"], bg="#f8f8fa",
                     width=ancho, anchor="w").pack(side="left", pady=6)

        color_prioridad = {"CRÍTICA": C["rojo"], "MEDIA": C["amarillo"], "BAJA": "#94a3b8"}
        color_estado    = {"Urgente": C["rojo"], "Programada": C["azul"], "Pendiente": "#94a3b8"}

        for r in reportes:
            self._fila_reporte(tabla, r, anchos, color_prioridad, color_estado)

        tk.Label(tabla, text="Mostrando 3 de 12 reportes activos",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).pack(anchor="w", padx=16, pady=8)

    def _fila_reporte(self, padre, r, anchos, cp, ce):
        fila = tk.Frame(padre, bg=C["card_bg"])
        fila.pack(fill="x", padx=16)
        separador(fila, C["borde"]).pack(fill="x")
        contenido = tk.Frame(fila, bg=C["card_bg"])
        contenido.pack(fill="x")

        valores = [r["asunto"], r["ubicacion"], r["prioridad"], r["estado"],
                   r["asignado"] if r["asignado"] else "Sin asignar", "···"]
        colores  = [C["texto_dark"], C["texto_light"],
                    cp.get(r["prioridad"], "#888"),
                    ce.get(r["estado"], "#888"),
                    C["texto_dark"], C["texto_light"]]

        for val, color, ancho in zip(valores, colores, anchos):
            tk.Label(contenido, text=val, font=("Segoe UI", 9),
                     fg=color, bg=C["card_bg"],
                     width=ancho, anchor="w").pack(side="left", pady=8)

    def _nuevo_reporte(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Reporte de Mantenimiento")
        ventana.geometry("380x280")
        ventana.configure(bg=C["main_bg"])

        tk.Label(ventana, text="Nuevo Reporte",
                 font=("Segoe UI", 14, "bold"),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(pady=(16, 8))

        campos = {}
        for campo, placeholder in [("Asunto", "Describe el problema"),
                                    ("Ubicación", "Habitación / Área"),]:
            tk.Label(ventana, text=campo, font=("Segoe UI", 9),
                     fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w", padx=24)
            e = tk.Entry(ventana, font=("Segoe UI", 10),
                         relief="flat", bg="#f0f0f0",
                         highlightthickness=1, highlightbackground=C["borde"])
            e.pack(fill="x", padx=24, ipady=6, pady=(0, 8))
            e.insert(0, placeholder)
            campos[campo] = e

        tk.Label(ventana, text="Prioridad", font=("Segoe UI", 9),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w", padx=24)
        var_prioridad = tk.StringVar(value="Media")
        combo = ttk.Combobox(ventana, textvariable=var_prioridad,
                             values=["Alta", "Media", "Baja"], state="readonly")
        combo.pack(fill="x", padx=24, pady=(0, 12))

        def guardar():
            reportes.append({
                "asunto":    campos["Asunto"].get(),
                "ubicacion": campos["Ubicación"].get(),
                "prioridad": var_prioridad.get().upper(),
                "estado":    "Pendiente",
                "asignado":  ""
            })
            messagebox.showinfo("Éxito", "Reporte creado correctamente.")
            ventana.destroy()

        boton_naranja(ventana, "Crear Reporte", guardar, ancho=24).pack(pady=4)

# ─────────────────────────────────────────────
#  PÁGINA: Configuración
# ─────────────────────────────────────────────

class PaginaConfiguracion(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        header = tk.Frame(self, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))

        tk.Label(header, text="SISTEMA DE GESTIÓN",
                 font=("Segoe UI", 8, "bold"),
                 fg=C["naranja"], bg=C["main_bg"]).pack(anchor="w")
        etiqueta_titulo(header, "Configuración",
                        "Personaliza tu entorno editorial y gestiona los privilegios de acceso.")

        contenido = tk.Frame(self, bg=C["main_bg"])
        contenido.pack(fill="both", expand=True, padx=28, pady=4)

        # Perfil del administrador
        col_izq = tarjeta(contenido)
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=4)

        tk.Label(col_izq, text="👤  Perfil del Administrador",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=16, pady=(16, 12))

        self.entradas = {}
        campos_perfil = [
            ("NOMBRE COMPLETO",    "nombre",  config_admin["nombre"]),
            ("CORREO ELECTRÓNICO", "correo",  config_admin["correo"]),
            ("ROL EDITORIAL",      "rol",     config_admin["rol"]),
            ("ZONA HORARIA",       "zona",    config_admin["zona"]),
        ]
        frame_campos = tk.Frame(col_izq, bg=C["card_bg"])
        frame_campos.pack(fill="x", padx=16, pady=(0, 16))

        for i, (etiqueta, clave, valor) in enumerate(campos_perfil):
            col = i % 2
            fila = i // 2
            f = tk.Frame(frame_campos, bg=C["card_bg"])
            f.grid(row=fila, column=col, padx=8, pady=6, sticky="w")

            tk.Label(f, text=etiqueta, font=("Segoe UI", 8),
                     fg=C["texto_light"], bg=C["card_bg"]).pack(anchor="w")
            entrada = tk.Entry(f, font=("Segoe UI", 10),
                               relief="flat", bg="#f0f0f0", width=26,
                               highlightthickness=1,
                               highlightbackground=C["borde"])
            entrada.insert(0, valor)
            entrada.pack(ipady=6)
            self.entradas[clave] = entrada

        # Columna derecha — Preferencias
        col_der = tarjeta(contenido)
        col_der.pack(side="right", fill="y", pady=4)
        col_der.pack_propagate(False)
        col_der.configure(width=220)

        tk.Label(col_der, text="⚙  Preferencias",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=16, pady=(16, 8))

        # Modo oscuro toggle
        frame_modo = tk.Frame(col_der, bg=C["card_bg"])
        frame_modo.pack(fill="x", padx=16, pady=4)
        tk.Label(frame_modo, text="Modo Oscuro",
                 font=("Segoe UI", 10, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(side="left")
        self.var_oscuro = tk.BooleanVar(value=False)
        tk.Checkbutton(frame_modo, variable=self.var_oscuro,
                       bg=C["card_bg"],
                       activebackground=C["card_bg"]).pack(side="right")
        tk.Label(col_der, text="Reduce el cansancio visual",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).pack(anchor="w", padx=16)

        separador(col_der, C["borde"]).pack(fill="x", padx=16, pady=12)

        tk.Label(col_der, text="IDIOMA DEL SISTEMA",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).pack(anchor="w", padx=16)
        self.var_idioma = tk.StringVar(value="Español (ES)")
        combo_idioma = ttk.Combobox(col_der, textvariable=self.var_idioma,
                                    values=["Español (ES)", "English (EN)"],
                                    state="readonly", width=20)
        combo_idioma.pack(padx=16, pady=6)

        # Botones guardar / descartar
        frame_botones = tk.Frame(self, bg=C["main_bg"])
        frame_botones.pack(fill="x", padx=28, pady=16)

        tk.Button(frame_botones, text="Descartar",
                  command=self._descartar,
                  bg=C["main_bg"], fg=C["texto_dark"],
                  relief="flat", font=("Segoe UI", 10),
                  cursor="hand2").pack(side="right", padx=8)
        boton_naranja(frame_botones, "Guardar Cambios",
                      self._guardar, ancho=16).pack(side="right")

    def _guardar(self):
        for clave, entrada in self.entradas.items():
            config_admin[clave] = entrada.get()
        messagebox.showinfo("Éxito", "Configuración guardada correctamente.")

    def _descartar(self):
        for clave, entrada in self.entradas.items():
            entrada.delete(0, "end")
            entrada.insert(0, config_admin[clave])

# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────

class MenuAdministrador(tk.Tk):
    def __init__(self):
        super().__init__()
        self._pagina_actual = None
        self._paginas = {
            "propiedades":   PaginaPropiedades,
            "reservas":      PaginaReservas,
            "ingresos":      PaginaIngresos,
            "mantenimiento": PaginaMantenimiento,
            "configuracion": PaginaConfiguracion,
        }
        self._configurar_ventana()
        self._construir_layout()
        self.navegar("propiedades")

    def _configurar_ventana(self):
        self.title("HotelMatch — Administrador")
        self.geometry("950x650")
        self.minsize(860, 560)
        self.configure(bg=C["sidebar_bg"])

    def _construir_layout(self):
        self.sidebar = tk.Frame(self, bg=C["sidebar_bg"], width=185)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.area_principal = tk.Frame(self, bg=C["main_bg"])
        self.area_principal.pack(side="left", fill="both", expand=True)

        self._construir_sidebar()

    def navegar(self, nombre_pagina):
        if self._pagina_actual == nombre_pagina:
            return
        for widget in self.area_principal.winfo_children():
            widget.destroy()
        ClasePagina = self._paginas[nombre_pagina]
        nueva_pagina = ClasePagina(self.area_principal, self)
        nueva_pagina.pack(fill="both", expand=True)
        self._pagina_actual = nombre_pagina
        self._actualizar_sidebar(nombre_pagina)

    def _actualizar_sidebar(self, pagina_activa):
        for nombre, btn_frame in self._botones_nav.items():
            activo = (nombre == pagina_activa)
            bg = C["naranja"] if activo else C["sidebar_bg"]
            btn_frame.config(bg=bg)
            for hijo in btn_frame.winfo_children():
                try:
                    hijo.config(bg=bg)
                except tk.TclError:
                    pass

    def _construir_sidebar(self):
        self._botones_nav = {}

        # Logo
        frame_logo = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        frame_logo.pack(fill="x", padx=14, pady=(20, 2))
        tk.Label(frame_logo, text="<HOTEL>", bg=C["sidebar_bg"],
                 fg=C["naranja"], font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(frame_logo, text=" MATCH",  bg=C["sidebar_bg"],
                 fg=C["blanco"],  font=("Segoe UI", 12, "bold")).pack(side="left")

        tk.Label(self.sidebar, text="EDITORIAL ADMIN",
                 bg=C["sidebar_bg"], fg="#555577",
                 font=("Segoe UI", 7)).pack(anchor="w", padx=14)

        separador(self.sidebar).pack(fill="x", padx=10, pady=12)

        # Botones de navegación
        nav_items = [
            ("propiedades",   "⊞", "Propiedades"),
            ("reservas",      "📅", "Reservas"),
            ("ingresos",      "💰", "Ingresos"),
            ("mantenimiento", "🔧", "Mantenimiento"),
            ("configuracion", "⚙", "Configuración"),
        ]
        for clave, icono, etiqueta in nav_items:
            self._crear_boton_nav(clave, icono, etiqueta)

        # Botón nuevo registro abajo
        separador(self.sidebar).pack(side="bottom", fill="x", padx=10)
        frame_btn = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        frame_btn.pack(side="bottom", fill="x", padx=10, pady=14)
        boton_naranja(frame_btn, "Nuevo Registro",
                      lambda: messagebox.showinfo("Nuevo", "Selecciona una sección primero."),
                      ancho=16).pack(fill="x")

        # Perfil admin
        perfil = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        perfil.pack(side="bottom", fill="x", padx=10, pady=8)
        tk.Label(perfil, text="AD", bg=C["naranja"], fg=C["blanco"],
                 font=("Segoe UI", 10, "bold"),
                 width=3, height=1).pack(side="left", padx=(0, 8))
        datos = tk.Frame(perfil, bg=C["sidebar_bg"])
        datos.pack(side="left")
        tk.Label(datos, text="Admin User", bg=C["sidebar_bg"],
                 fg=C["blanco"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(datos, text="Super Administrador", bg=C["sidebar_bg"],
                 fg=C["texto_light"], font=("Segoe UI", 7)).pack(anchor="w")

    def _crear_boton_nav(self, clave, icono, etiqueta):
        contenedor = tk.Frame(self.sidebar, bg=C["sidebar_bg"], cursor="hand2")
        contenedor.pack(fill="x", padx=10, pady=1)

        lbl = tk.Label(contenedor,
                       text=f"  {icono}   {etiqueta}",
                       bg=C["sidebar_bg"], fg="#ccccdd",
                       font=("Segoe UI", 10), anchor="w",
                       padx=8, pady=10)
        lbl.pack(fill="x")

        for widget in (contenedor, lbl):
            widget.bind("<Button-1>", lambda e, c=clave: self.navegar(c))

        def hover_on(e, f=contenedor, l=lbl):
            if self._pagina_actual != clave:
                f.config(bg="#2a2a4e"); l.config(bg="#2a2a4e")

        def hover_off(e, f=contenedor, l=lbl):
            if self._pagina_actual != clave:
                f.config(bg=C["sidebar_bg"]); l.config(bg=C["sidebar_bg"])

        contenedor.bind("<Enter>", hover_on)
        contenedor.bind("<Leave>", hover_off)
        lbl.bind("<Enter>", hover_on)
        lbl.bind("<Leave>", hover_off)

        self._botones_nav[clave] = contenedor


# ─────────────────────────────────────────────
#  Punto de entrada
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = MenuAdministrador()
    app.mainloop()
