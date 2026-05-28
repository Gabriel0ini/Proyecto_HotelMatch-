

import tkinter as tk
from tkinter import ttk
from colores import C
from widgets import boton_naranja, titulo_seccion, card


class PaginaInicio(tk.Frame):
    """
    Cada página es un Frame que recibe:
      - padre: el contenedor donde se monta
      - app:   referencia a la ventana principal
               (para poder navegar desde aquí)
    """
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        

        canvas = tk.Canvas(self, bg=C["main_bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                  command=canvas.yview)

        self.interior = tk.Frame(canvas, bg=C["main_bg"])

        
        self.interior.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.interior, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(-1*(e.delta//120), "units"))

        pad = tk.Frame(self.interior, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=32, pady=28)

        self._seccion_saludo(pad)
        self._seccion_proxima_estancia(pad)
        self._seccion_sugerencias(pad)


    def _seccion_saludo(self, padre):
        """¡Hola de nuevo, {self.app.usuario_actual}! + subtítulo."""
        tk.Label(
            padre,
            text=f"¡Hola de nuevo, {self.app.usuario_actual}!",
            bg=C["main_bg"],
            fg=C["texto_dark"],
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            padre,
            text="Aquí puedes ver y gestionar tus reservas",
            bg=C["main_bg"],
            fg=C["texto_mid"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 20))

    def _seccion_proxima_estancia(self, padre):
        """Card con la próxima reserva confirmada."""

        titulo_seccion(padre, "PRÓXIMA ESTANCIA").pack(anchor="w", pady=(0, 8))

        tarjeta = card(padre)
        tarjeta.pack(fill="x", pady=(0, 24))

        interior = tk.Frame(tarjeta, bg=C["blanco"])
        interior.pack(fill="x", padx=20, pady=18)

        fila_ciudad = tk.Frame(interior, bg=C["blanco"])
        fila_ciudad.pack(anchor="w")

        tk.Label(fila_ciudad, text="📍", bg=C["blanco"],
                 font=("Segoe UI", 9)).pack(side="left")
        tk.Label(fila_ciudad, text="POTOSÍ, BOLIVIA",
                 bg=C["blanco"], fg=C["naranja"],
                 font=("Segoe UI", 8, "bold")).pack(side="left")

        tk.Label(
            interior,
            text="Palacio de Sal",
            bg=C["blanco"],
            fg=C["texto_dark"],
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w", pady=(4, 4))

        
        tk.Label(
            interior,
            text="Experimenta el primer hotel del mundo construido\n"
                 "enteramente de sal, ubicado a las orillas del\n"
                 "majestuoso Salar de Uyuni.",
            bg=C["blanco"],
            fg=C["texto_mid"],
            font=("Segoe UI", 9),
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        fila_datos = tk.Frame(interior, bg=C["blanco"])
        fila_datos.pack(anchor="w", pady=(0, 14))

        col_fecha = tk.Frame(fila_datos, bg=C["blanco"])
        col_fecha.grid(row=0, column=0, padx=(0, 30))

        tk.Label(col_fecha, text="FECHA", bg=C["blanco"],
                 fg=C["texto_light"],
                 font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Label(col_fecha, text="📅  12 Oct, 2023",
                 bg=C["blanco"], fg=C["texto_dark"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        col_hues = tk.Frame(fila_datos, bg=C["blanco"])
        col_hues.grid(row=0, column=1)

        tk.Label(col_hues, text="HUÉSPEDES", bg=C["blanco"],
                 fg=C["texto_light"],
                 font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Label(col_hues, text="👥  2 Adultos",
                 bg=C["blanco"], fg=C["texto_dark"],
                 font=("Segoe UI", 9)).pack(anchor="w")

        boton_naranja(
            interior,
            "GESTIONAR ESTANCIA",
            lambda: self.app.navegar("mis_estancias")  
        ).pack(anchor="w")
    def _seccion_sugerencias(self, padre):
        titulo_seccion(
            padre,
            "HOTELES DISPONIBLES"
        ).pack(anchor="w", pady=(0, 10))

        from datos import leer_hoteles
        hoteles = [h for h in leer_hoteles() if h.get("estado", "").lower() == "activo"]

        if not hoteles:
            tk.Label(
                padre,
                text="No hay hoteles disponibles por el momento.",
                bg=C["main_bg"], fg=C["texto_mid"],
                font=("Segoe UI", 9)
            ).pack(anchor="w")
            return

        contenedor = tk.Frame(padre, bg=C["main_bg"])
        contenedor.pack(anchor="w")

        for hotel in hoteles:
            self._card_hotel(contenedor, hotel)

    def _card_hotel(self, padre, hotel):
        tarjeta = tk.Frame(
            padre,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        tarjeta.pack(side="left", padx=(0, 14))

        # Banner superior con emoji
        banner = tk.Canvas(tarjeta, width=180, height=90,
                           bg="#dde8f0", highlightthickness=0)
        banner.pack()
        banner.create_text(90, 45, text=hotel.get("emoji", "🏨"),
                           font=("Segoe UI", 30))

        info = tk.Frame(tarjeta, bg=C["blanco"])
        info.pack(fill="x", padx=12, pady=(8, 12))

        # Tipo de hotel
        tk.Label(info, text=hotel.get("tipo", "").upper(),
                 bg=C["naranja_suave"], fg=C["naranja"],
                 font=("Segoe UI", 7, "bold"),
                 padx=6, pady=2).pack(anchor="w")

        # Nombre
        tk.Label(info, text=hotel.get("nombre", ""),
                 bg=C["blanco"], fg=C["texto_dark"],
                 font=("Segoe UI", 10, "bold"),
                 wraplength=160).pack(anchor="w", pady=(4, 0))

        # Ciudad
        tk.Label(info, text=f"📍 {hotel.get('ciudad', '')}",
                 bg=C["blanco"], fg=C["texto_mid"],
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(2, 4))

        # Fila rating + habitaciones
        fila = tk.Frame(info, bg=C["blanco"])
        fila.pack(anchor="w")

        tk.Label(fila, text=f"⭐ {hotel.get('rating', '-')}" ,
                 bg=C["blanco"], fg=C["texto_dark"],
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(0, 10))

        tk.Label(fila, text=f"🛏 {hotel.get('habitaciones', '-')} hab.",
                 bg=C["blanco"], fg=C["texto_mid"],
                 font=("Segoe UI", 8)).pack(side="left")