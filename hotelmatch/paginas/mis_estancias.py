import tkinter as tk
from tkinter import ttk, messagebox
from colores import C
from widgets import boton_naranja, titulo_seccion, separador
from datos   import leer_reservas, agregar_reserva, eliminar_reserva


class PaginaMisEstancias(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        self._barra_superior()
        self._area_scroll()


    def _barra_superior(self):
        """
        Encabezado fijo (no hace scroll) con título + botón añadir.
        Usamos pack(fill="x") para que ocupe todo el ancho.
        """
        barra = tk.Frame(
            self,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        barra.pack(fill="x")

        interior = tk.Frame(barra, bg=C["blanco"])
        interior.pack(fill="x", padx=28, pady=14)

        tk.Label(
            interior,
            text="Mis Estancias",
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")


    def _area_scroll(self):
        """
        Canvas + Scrollbar para listar todas las reservas.
        Mismo patrón que en inicio.py y configuracion.py.
        """
        self._canvas = tk.Canvas(
            self, bg=C["main_bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(
            self, orient="vertical", command=self._canvas.yview)

        self._frame_lista = tk.Frame(
            self._canvas, bg=C["main_bg"])

        self._frame_lista.bind(
            "<Configure>",
            lambda e: self._canvas.configure(
                scrollregion=self._canvas.bbox("all")
            )
        )

        self._canvas.create_window(
            (0, 0), window=self._frame_lista, anchor="nw")
        self._canvas.configure(yscrollcommand=scroll.set)

        self._canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self._canvas.bind_all(
            "<MouseWheel>",
            lambda e: self._canvas.yview_scroll(
                -1 * (e.delta // 120), "units")
        )

        self._renderizar_lista()

    def _renderizar_lista(self):
        """
        Lee las reservas del archivo y dibuja una card por cada una.
        También se llama después de agregar/eliminar para refrescar.
        """
        for w in self._frame_lista.winfo_children():
            w.destroy()

        pad = tk.Frame(self._frame_lista, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=28, pady=20)

        reservas = leer_reservas()

        if not reservas:
            self._estado_vacio(pad)
            return

        for reserva in reservas:
            self._card_reserva(pad, reserva)

    def _estado_vacio(self, padre):
        """Mensaje cuando no hay reservas."""
        tk.Label(
            padre,
            text="🏨",
            bg=C["main_bg"],
            font=("Segoe UI", 40)
        ).pack(pady=(60, 8))

        tk.Label(
            padre,
            text="No tienes reservas aún",
            bg=C["main_bg"], fg=C["texto_dark"],
            font=("Segoe UI", 14, "bold")
        ).pack()

        tk.Label(
            padre,
            text="Ve a Inicio y selecciona un hotel para reservar.",
            bg=C["main_bg"], fg=C["texto_light"],
            font=("Segoe UI", 9)
        ).pack(pady=(4, 0))


    def _card_reserva(self, padre, reserva):
        """
        Tarjeta que muestra los datos de UNA reserva.

        Estructura visual:
        ┌──────────────────────────────────────────┐
        │  📍 CIUDAD          [estado: badge]       │
        │  Nombre del Hotel                         │
        │  🗓 Fecha  👥 Huéspedes  🛏 Habitación    │
        │  💰 $precio/noche    [ELIMINAR]            │
        └──────────────────────────────────────────┘
        """
        tarjeta = tk.Frame(
            padre,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        tarjeta.pack(fill="x", pady=(0, 12))

        interior = tk.Frame(tarjeta, bg=C["blanco"])
        interior.pack(fill="x", padx=20, pady=16)

        fila_top = tk.Frame(interior, bg=C["blanco"])
        fila_top.pack(fill="x", pady=(0, 4))

        tk.Label(
            fila_top,
            text=f"📍  {reserva.get('ciudad','').upper()}",
            bg=C["blanco"], fg=C["naranja"],
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        estado = reserva.get("estado", "")
        color_estado = C["verde"] if estado == "Confirmada" else C["texto_light"]

        tk.Label(
            fila_top,
            text=f"● {estado}",
            bg=C["blanco"], fg=color_estado,
            font=("Segoe UI", 8, "bold")
        ).pack(side="right")

        tk.Label(
            interior,
            text=reserva.get("hotel", "Hotel"),
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 8))

        fila_detalles = tk.Frame(interior, bg=C["blanco"])
        fila_detalles.pack(anchor="w", pady=(0, 12))

        detalles = [
            ("FECHA",       f"📅  {reserva.get('fecha','')}"),
            ("HUÉSPEDES",   f"👥  {reserva.get('huespedes','')}"),
            ("HABITACIÓN",  f"🛏  {reserva.get('habitacion','')}"),
        ]

        for etiqueta, valor in detalles:
            col = tk.Frame(fila_detalles, bg=C["blanco"])
            col.pack(side="left", padx=(0, 24))

            tk.Label(
                col,
                text=etiqueta,
                bg=C["blanco"], fg=C["texto_light"],
                font=("Segoe UI", 7, "bold")
            ).pack(anchor="w")

            tk.Label(
                col,
                text=valor,
                bg=C["blanco"], fg=C["texto_dark"],
                font=("Segoe UI", 9)
            ).pack(anchor="w")

        separador(interior).pack(fill="x", pady=(0, 10))

        fila_bottom = tk.Frame(interior, bg=C["blanco"])
        fila_bottom.pack(fill="x")

        precio = reserva.get("precio", "0")
        tk.Label(
            fila_bottom,
            text=f"💰  ${precio} / noche",
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        id_reserva = reserva.get("id")
        btn_eliminar = tk.Label(
            fila_bottom,
            text="🗑  Eliminar",
            bg=C["blanco"], fg="#e74c3c",
            font=("Segoe UI", 8),
            cursor="hand2"
        )
        btn_eliminar.pack(side="right")
        btn_eliminar.bind(
            "<Button-1>",
            lambda e, rid=id_reserva: self._confirmar_eliminar(rid)
        )


    def _confirmar_eliminar(self, id_reserva):
        """
        Pide confirmación antes de eliminar.
        messagebox.askyesno() → retorna True/False
        """
        confirmado = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar esta reserva?\n"
            "Esta acción no se puede deshacer."
        )
        if confirmado:
            eliminar_reserva(id_reserva)
            self._renderizar_lista()  
    def _abrir_formulario(self):
        """
        Abre una ventana emergente (Toplevel) para crear reserva.
        
        ¿Por qué Toplevel y no una nueva página?
        Porque es una acción modal — el usuario DEBE completarla
        o cancelarla antes de seguir navegando.
        Toplevel es el equivalente a un "dialog" en otros frameworks.
        """
        ventana = tk.Toplevel(self)
        ventana.title("Nueva Reserva")
        ventana.geometry("420x480")
        ventana.resizable(False, False)
        ventana.configure(bg=C["main_bg"])

        ventana.transient(self.app) 
        ventana.grab_set()          

        FormularioReserva(ventana, self.app, self._renderizar_lista)


class FormularioReserva:
    """
    Formulario modal para crear una nueva reserva.
    
    Es una CLASE SEPARADA dentro del mismo archivo
    porque tiene su propia lógica y estado.
    Separar responsabilidades = código más limpio.
    """
    def __init__(self, ventana, app, callback_actualizar, hotel_prellenado=None):
        self.ventana = ventana
        self.app = app
        self.callback_actualizar = callback_actualizar
        self.hotel_prellenado = hotel_prellenado
        self._construir()

    def _construir(self):
        pad = tk.Frame(self.ventana, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(pad, text="Nueva Reserva",
             bg=C["main_bg"], fg=C["texto_dark"],
             font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 20))

        nombre_hotel = self.hotel_prellenado.get("nombre", "") if self.hotel_prellenado else ""
        ciudad_hotel = self.hotel_prellenado.get("ciudad", "") if self.hotel_prellenado else ""
        precio_hotel = self.hotel_prellenado.get("precio", "100") if self.hotel_prellenado else "100"

        self.vars = {}

    # Hotel (readonly)
        self._campo_readonly(pad, "Hotel", "hotel", nombre_hotel)

    # Ciudad (readonly)
        self._campo_readonly(pad, "Ciudad", "ciudad", ciudad_hotel)

    # Fecha con calendario
        tk.Label(pad, text="Fecha",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))

        frame_fecha = tk.Frame(pad, bg=C["main_bg"])
        frame_fecha.pack(fill="x")

        self.vars["fecha"] = tk.StringVar(value="Seleccionar fecha")
        tk.Entry(frame_fecha, textvariable=self.vars["fecha"],
             font=("Segoe UI", 9), relief="solid", bd=1,
             state="readonly", readonlybackground="#f0f0f0").pack(
             side="left", fill="x", expand=True, ipady=4)

        tk.Button(frame_fecha, text="📅", font=("Segoe UI", 10),
              relief="flat", bg=C["naranja"], fg="white",
              cursor="hand2", padx=6,
              command=self._abrir_calendario).pack(side="left", padx=(4, 0))

    # Huéspedes (Combobox)
        tk.Label(pad, text="Huéspedes",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars["huespedes"] = tk.StringVar(value="1 Adulto")
        ttk.Combobox(pad, textvariable=self.vars["huespedes"],
                     values=["1 Adulto", "2 Adultos", "3 Adultos", "4 Adultos"],
                 state="readonly", font=("Segoe UI", 9)).pack(
                 fill="x", ipady=3)

    # Habitación (Combobox)
        tk.Label(pad, text="Habitación",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars["habitacion"] = tk.StringVar(value="Simple")
        ttk.Combobox(pad, textvariable=self.vars["habitacion"],
                 values=["Simple", "Doble", "Suite"],
                 state="readonly", font=("Segoe UI", 9)).pack(
                 fill="x", ipady=3)

    # Precio (readonly)
        self._campo_readonly(pad, "Precio/noche", "precio", precio_hotel)

    # Estado
        tk.Label(pad, text="Estado",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars["estado"] = tk.StringVar(value="Confirmada")
        ttk.Combobox(pad, textvariable=self.vars["estado"],
                 values=["Confirmada", "Pendiente"],
                 state="readonly", font=("Segoe UI", 9)).pack(
                 fill="x", ipady=3, pady=(0, 16))

    # Botones
        fila_btns = tk.Frame(pad, bg=C["main_bg"])
        fila_btns.pack(fill="x")

        boton_naranja(
            fila_btns,
            "Confirmar",
            lambda: self._guardar(confirmar=True),
            ancho=14
        ).pack(side="left")

        boton_naranja(
            fila_btns,
            "Guardar",
            lambda: self._guardar(confirmar=False),
            ancho=14
        ).pack(side="left", padx=(8, 0))

        lbl_cancelar = tk.Label(
            fila_btns,
            text="Cancelar",
            bg=C["main_bg"], fg=C["texto_light"],
            font=("Segoe UI", 9), cursor="hand2"
        )
        lbl_cancelar.pack(side="left", padx=12)
        lbl_cancelar.bind("<Button-1>", lambda e: self.ventana.destroy())

    def _campo(self, padre, etiqueta, clave, default, readonly=False):
        tk.Label(
            padre,
            text=etiqueta,
            bg=C["main_bg"], fg=C["texto_mid"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(8, 2))

        self.vars[clave] = tk.StringVar(value=default)

        estado_entry = "readonly" if readonly else "normal"
        tk.Entry(
            padre,
            textvariable=self.vars[clave],
            font=("Segoe UI", 9),
            relief="solid", bd=1,
            state=estado_entry,
            readonlybackground="#f0f0f0"
        ).pack(fill="x", ipady=4)

    def _guardar(self, confirmar=False):
        if confirmar:
            self.vars["estado"].set("Confirmada")

        hotel  = self.vars["hotel"].get().strip()
        ciudad = self.vars["ciudad"].get().strip()
        fecha  = self.vars["fecha"].get().strip()

        if not hotel or not ciudad or not fecha:
            messagebox.showwarning(
                "Campos requeridos",
                "Hotel, ciudad y fecha son obligatorios.",
                parent=self.ventana
            )
            return

        # Validar duplicado: mismo hotel + misma fecha
        reservas_existentes = leer_reservas()
        for r in reservas_existentes:
            if (r.get("hotel", "").lower() == hotel.lower() and
                    r.get("fecha", "").lower() == fecha.lower()):
                messagebox.showwarning(
                    "Reserva duplicada",
                    f"Ya tienes una reserva en {hotel} para esa fecha.",
                    parent=self.ventana
                )
                return

        nueva = {k: v.get().strip() for k, v in self.vars.items()}
        agregar_reserva(nueva)

        estado_actual = self.vars["estado"].get()
        if estado_actual == "Confirmada":
            mensaje = f"Tu reserva en {hotel} fue confirmada correctamente."
            titulo = "¡Reserva confirmada!"
        else:
            mensaje = f"Tu reserva en {hotel} fue guardada como pendiente."
            titulo = "Reserva guardada"

        messagebox.showinfo(
            titulo,
            mensaje,
            parent=self.ventana
        )

        self.ventana.destroy()
        self.callback_actualizar()

    def _campo_readonly(self, padre, etiqueta, clave, valor):
        tk.Label(padre, text=etiqueta,
                bg=C["main_bg"], fg=C["texto_mid"],
                font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars[clave] = tk.StringVar(value=valor)
        tk.Entry(padre, textvariable=self.vars[clave],
                font=("Segoe UI", 9), relief="solid", bd=1,
                state="readonly", readonlybackground="#f0f0f0").pack(
                fill="x", ipady=4)

    def _abrir_calendario(self):
        top = tk.Toplevel(self.ventana)
        top.title("Seleccionar fecha")
        top.geometry("300x280")
        top.resizable(False, False)
        top.configure(bg=C["main_bg"])
        top.transient(self.ventana)
        top.grab_set()

        import datetime
        hoy = datetime.date.today()
        self._cal_anio = hoy.year
        self._cal_mes = hoy.month
        self._cal_top = top

        self._frame_cal = tk.Frame(top, bg=C["main_bg"])
        self._frame_cal.pack(fill="both", expand=True, padx=12, pady=12)
        self._dibujar_calendario()

    def _dibujar_calendario(self):
        import datetime
        for w in self._frame_cal.winfo_children():
            w.destroy()

        nombres_mes = ["","Enero","Febrero","Marzo","Abril","Mayo","Junio",
                    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

        # Navegación
        nav = tk.Frame(self._frame_cal, bg=C["main_bg"])
        nav.pack(fill="x", pady=(0, 8))

        tk.Button(nav, text="<", command=self._mes_anterior_cal,
                relief="flat", bg=C["main_bg"], fg=C["texto_dark"],
                font=("Segoe UI", 11), cursor="hand2").pack(side="left")
        tk.Label(nav, text=f"{nombres_mes[self._cal_mes]} {self._cal_anio}",
                bg=C["main_bg"], fg=C["texto_dark"],
                font=("Segoe UI", 10, "bold")).pack(side="left", expand=True)
        tk.Button(nav, text=">", command=self._mes_siguiente_cal,
                relief="flat", bg=C["main_bg"], fg=C["texto_dark"],
                font=("Segoe UI", 11), cursor="hand2").pack(side="right")

        # Días semana
        grid = tk.Frame(self._frame_cal, bg=C["main_bg"])
        grid.pack()
        for col, dia in enumerate(["Do","Lu","Ma","Mi","Ju","Vi","Sá"]):
            tk.Label(grid, text=dia, font=("Segoe UI", 8),
                    fg=C["texto_light"], bg=C["main_bg"],
                    width=4).grid(row=0, column=col)

        # Días del mes
        import datetime
        primer_dia = (datetime.date(self._cal_anio, self._cal_mes, 1).weekday() + 1) % 7
        if self._cal_mes == 12:
            dias_mes = 31
        else:
            dias_mes = (datetime.date(self._cal_anio, self._cal_mes + 1, 1)
                        - datetime.timedelta(days=1)).day

        hoy = datetime.date.today()
        dia_num = 1
        for fila in range(1, 7):
            for col in range(7):
                idx = (fila - 1) * 7 + col
                if idx < primer_dia or dia_num > dias_mes:
                    tk.Label(grid, text="", bg=C["main_bg"],
                            width=4, height=2).grid(row=fila, column=col)
                else:
                    es_hoy = (dia_num == hoy.day and
                            self._cal_mes == hoy.month and
                            self._cal_anio == hoy.year)
                    bg = C["naranja"] if es_hoy else C["main_bg"]
                    fg = "white" if es_hoy else C["texto_dark"]
                    btn = tk.Label(grid, text=str(dia_num),
                                font=("Segoe UI", 9),
                                bg=bg, fg=fg, width=4, height=2,
                                cursor="hand2")
                    btn.grid(row=fila, column=col)
                    btn.bind("<Button-1>",
                        lambda e, d=dia_num: self._seleccionar_dia(d))
                    dia_num += 1

    def _seleccionar_dia(self, dia):
        nombres_mes = ["","Ene","Feb","Mar","Abr","May","Jun",
                    "Jul","Ago","Sep","Oct","Nov","Dic"]
        fecha_str = f"{dia:02d} {nombres_mes[self._cal_mes]}, {self._cal_anio}"
        self.vars["fecha"].set(fecha_str)
        self._cal_top.destroy()

    def _mes_anterior_cal(self):
        if self._cal_mes == 1:
            self._cal_mes = 12; self._cal_anio -= 1
        else:
            self._cal_mes -= 1
        self._dibujar_calendario()

    def _mes_siguiente_cal(self):
        if self._cal_mes == 12:
            self._cal_mes = 1; self._cal_anio += 1
        else:
            self._cal_mes += 1
        self._dibujar_calendario()