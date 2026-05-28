import tkinter as tk
from tkinter import messagebox, ttk
import datetime
from hotelmatch.colores import C

# ─────────────────────────────────────────────
#  Datos de ejemplo (simulan archivos .txt)
# ─────────────────────────────────────────────
hoteles = [
    {"id": "HM-9021", "nombre": "LOS TAJIBOS",          "ciudad": "Santa Cruz, Bolivia",   "habitaciones": 208, "rating": 4.9, "estado": "Activo",       "tipo": "LUXURY SEGMENT"},
    {"id": "HM-8822", "nombre": "GRAN HOTEL PARIS",     "ciudad": "La Paz, Bolivia",       "habitaciones": 16,  "rating": 4.7, "estado": "Activo",       "tipo": "URBAN CONCEPT"},
    {"id": "HM-1045", "nombre": "GRAN HOTEL COCHABAMBA","ciudad": "Cochabamba, Bolivia",   "habitaciones": 130, "rating": 4.2, "estado": "Mantenimiento","tipo": "WINTER PEAK"},
]

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
        self._construir()

    def _construir(self):
        # Header
        header = tk.Frame(self, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))
        etiqueta_titulo(header, "Propiedades",
                        "Gestión editorial y supervisión de activos hoteleros.")

        # Tarjetas de resumen
        frame_cards = tk.Frame(self, bg=C["main_bg"])
        frame_cards.pack(fill="x", padx=28, pady=(0, 16))

        resumen = [
            ("🏨", "TOTAL ACTIVAS",       "24"),
            ("🛏", "TOTAL HABITACIONES",  "1,482"),
            ("🔧", "BAJO MANTENIMIENTO",  "03"),
        ]
        for icono, etiqueta, valor in resumen:
            c = tarjeta(frame_cards)
            c.pack(side="left", padx=(0, 12), pady=4, ipadx=20, ipady=14)
            tk.Label(c, text=icono, font=("Segoe UI", 20),
                     bg=C["card_bg"], fg=C["naranja"]).pack(anchor="w", padx=16, pady=(12, 0))
            tk.Label(c, text=etiqueta, font=("Segoe UI", 8),
                     bg=C["card_bg"], fg=C["texto_light"]).pack(anchor="w", padx=16)
            tk.Label(c, text=valor, font=("Segoe UI", 20, "bold"),
                     bg=C["card_bg"], fg=C["texto_dark"]).pack(anchor="w", padx=16, pady=(0, 12))

        # Lista de hoteles
        separador(self, C["borde"]).pack(fill="x", padx=28, pady=4)
        lista_frame = tk.Frame(self, bg=C["main_bg"])
        lista_frame.pack(fill="both", expand=True, padx=28, pady=8)

        for hotel in hoteles:
            self._fila_hotel(lista_frame, hotel)

        # Botón nuevo registro
        frame_btn = tk.Frame(self, bg=C["main_bg"])
        frame_btn.pack(fill="x", padx=28, pady=12)
        boton_naranja(frame_btn, "+ Nuevo Registro",
                      lambda: messagebox.showinfo("Nuevo", "Formulario de nuevo hotel")).pack(side="left")

    def _fila_hotel(self, padre, hotel):
        fila = tarjeta(padre)
        fila.pack(fill="x", pady=5)

        # Tipo
        tk.Label(fila, text=hotel["tipo"],
                 font=("Segoe UI", 8, "bold"),
                 fg=C["naranja"], bg=C["card_bg"]).grid(row=0, column=0, sticky="w", padx=16, pady=(10, 0))

        # Nombre
        tk.Label(fila, text=hotel["nombre"],
                 font=("Segoe UI", 13, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).grid(row=1, column=0, sticky="w", padx=16)

        # Info
        info = f"📍 {hotel['ciudad']}    🛏 {hotel['habitaciones']} Habitaciones    ⭐ {hotel['rating']} Rating"
        tk.Label(fila, text=info,
                 font=("Segoe UI", 9),
                 fg=C["texto_light"], bg=C["card_bg"]).grid(row=2, column=0, sticky="w", padx=16, pady=(0, 10))

        # Estado
        color = C["verde"] if hotel["estado"] == "Activo" else C["amarillo"]
        chip_estado(fila, f"● {hotel['estado']}", color).grid(row=0, column=1, sticky="e", padx=16, pady=(10, 0))
        tk.Label(fila, text=f"ID: {hotel['id']}",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).grid(row=1, column=1, sticky="e", padx=16)

        fila.columnconfigure(0, weight=1)

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
        header = tk.Frame(self, bg=C["main_bg"])
        header.pack(fill="x", padx=28, pady=(24, 0))
        etiqueta_titulo(header, "Reservas",
                        "Calendario maestro de ocupación y gestión editorial.")

        contenido = tk.Frame(self, bg=C["main_bg"])
        contenido.pack(fill="both", expand=True, padx=28, pady=8)

        # Columna izquierda — estadísticas + calendario
        col_izq = tk.Frame(contenido, bg=C["main_bg"])
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 12))

        # Tarjetas resumen
        frame_stats = tk.Frame(col_izq, bg=C["main_bg"])
        frame_stats.pack(fill="x", pady=(0, 12))

        for etiqueta, valor in [("TOTAL RESERVAS", "1,284"), ("TASA DE OCUPACIÓN", "92.4%")]:
            c = tarjeta(frame_stats)
            c.pack(side="left", padx=(0, 12), ipadx=20, ipady=10)
            tk.Label(c, text=etiqueta, font=("Segoe UI", 8),
                     fg=C["texto_light"], bg=C["card_bg"]).pack(anchor="w", padx=14, pady=(10, 0))
            tk.Label(c, text=valor, font=("Segoe UI", 20, "bold"),
                     fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=14, pady=(0, 10))

        # Calendario
        self.frame_cal = tarjeta(col_izq)
        self.frame_cal.pack(fill="both", expand=True)
        self._dibujar_calendario()

        # Columna derecha — próximas reservas
        col_der = tk.Frame(contenido, bg=C["main_bg"], width=260)
        col_der.pack(side="right", fill="y")
        col_der.pack_propagate(False)

        tk.Label(col_der, text="Próximas Reservas",
                 font=("Segoe UI", 12, "bold"),
                 fg=C["texto_dark"], bg=C["main_bg"]).pack(anchor="w", pady=(0, 8))

        for r in reservas:
            self._tarjeta_reserva(col_der, r)

        boton_naranja(col_der, "+ NUEVO REGISTRO",
                      lambda: messagebox.showinfo("Nueva", "Formulario nueva reserva"), ancho=22).pack(pady=16)

    def _dibujar_calendario(self):
        for w in self.frame_cal.winfo_children():
            w.destroy()

        nombre_mes = ["", "Enero","Febrero","Marzo","Abril","Mayo","Junio",
                      "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"][self.mes]

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
                    bg = C["naranja"] if es_hoy else C["card_bg"]
                    fg = C["blanco"] if es_hoy else C["texto_dark"]
                    tk.Label(grid, text=str(dia_num),
                             font=("Segoe UI", 9, "bold" if es_hoy else "normal"),
                             bg=bg, fg=fg, width=5, height=2).grid(row=fila, column=col)
                    dia_num += 1

    def _mes_anterior(self):
        if self.mes == 1:
            self.mes = 12; self.anio -= 1
        else:
            self.mes -= 1
        self._dibujar_calendario()

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

        tk.Label(c, text=r["cliente"],
                 font=("Segoe UI", 10, "bold"),
                 fg=C["texto_dark"], bg=C["card_bg"]).pack(anchor="w", padx=10, pady=(8, 0))
        tk.Label(c, text=r["id_cliente"],
                 font=("Segoe UI", 8),
                 fg=C["texto_light"], bg=C["card_bg"]).pack(anchor="w", padx=10)

        fila = tk.Frame(c, bg=C["card_bg"])
        fila.pack(fill="x", padx=10, pady=2)
        tk.Label(fila, text=f"Check-in: {r['checkin']}",
                 font=("Segoe UI", 8), fg=C["texto_light"],
                 bg=C["card_bg"]).pack(side="left")
        tk.Label(fila, text=r["monto"],
                 font=("Segoe UI", 9, "bold"),
                 fg=C["naranja"], bg=C["card_bg"]).pack(side="right")

        color = C["verde"] if r["estado"] == "CONFIRMADA" else C["amarillo"]
        chip_estado(c, r["estado"], color).pack(anchor="w", padx=10, pady=(0, 8))

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
