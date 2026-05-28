import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from colores import C
from widgets import boton_naranja, titulo_seccion, separador
from datos   import leer_reservas, agregar_reserva, eliminar_reserva, actualizar_reserva


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

        btn_editar = tk.Label(
            fila_bottom,
            text="✎  Editar",
            bg=C["blanco"], fg="#2a4d8f",
            font=("Segoe UI", 8),
            cursor="hand2"
        )
        btn_editar.pack(side="right", padx=(0, 10))
        btn_editar.bind(
            "<Button-1>",
            lambda e, res=reserva: self._abrir_formulario(res)
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
    def _abrir_formulario(self, reserva=None):
        """
        Abre una ventana emergente (Toplevel) para crear o editar una reserva.
        """
        ventana = tk.Toplevel(self)
        titulo = "Editar Reserva" if reserva else "Nueva Reserva"
        ventana.title(titulo)
        ventana.geometry("440x660")
        ventana.resizable(False, True)
        ventana.configure(bg=C["main_bg"])

        ventana.transient(self.app)
        ventana.grab_set()

        FormularioReserva(
            ventana,
            self.app,
            self._renderizar_lista,
            reserva_prellenada=reserva
        )


class FormularioReserva:
    """
    Formulario modal para crear una nueva reserva.
    
    Es una CLASE SEPARADA dentro del mismo archivo
    porque tiene su propia lógica y estado.
    Separar responsabilidades = código más limpio.
    """
    def __init__(self, ventana, app, callback_actualizar, reserva_prellenada=None, hotel_prellenado=None):
        self.ventana = ventana
        self.app = app
        self.callback_actualizar = callback_actualizar
        self.reserva_prellenada = reserva_prellenada
        self.hotel_prellenado = hotel_prellenado
        self._construir()

    def _construir(self):
        pad = tk.Frame(self.ventana, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=28, pady=24)

        titulo_form = "Editar Reserva" if self.reserva_prellenada else "Nueva Reserva"
        tk.Label(pad, text=titulo_form,
             bg=C["main_bg"], fg=C["texto_dark"],
             font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=(0, 20))

        nombre_hotel = ""
        ciudad_hotel = ""
        precio_hotel = "100"
        if self.reserva_prellenada:
            nombre_hotel = self.reserva_prellenada.get("hotel", "")
            ciudad_hotel = self.reserva_prellenada.get("ciudad", "")
            precio_hotel = self.reserva_prellenada.get("precio", "100")
        elif self.hotel_prellenado:
            nombre_hotel = self.hotel_prellenado.get("nombre", "")
            ciudad_hotel = self.hotel_prellenado.get("ciudad", "")
            precio_hotel = self.hotel_prellenado.get("precio", "100")

        self.vars = {}

    # Hotel (readonly)
        self._campo_readonly(pad, "Hotel", "hotel", nombre_hotel)

    # Ciudad (readonly)
        self._campo_readonly(pad, "Ciudad", "ciudad", ciudad_hotel)

    # Fechas de entrada y salida
        tk.Label(pad, text="Fechas",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))

        frame_fechas = tk.Frame(pad, bg=C["main_bg"])
        frame_fechas.pack(fill="x")

        self.vars["check_in"] = tk.StringVar(value="Seleccionar fecha")
        self.vars["check_out"] = tk.StringVar(value="Seleccionar fecha")
        if self.reserva_prellenada:
            self.vars["check_in"].set(self.reserva_prellenada.get("check_in", self.reserva_prellenada.get("fecha", "Seleccionar fecha").split(" - ")[0]))
            self.vars["check_out"].set(self.reserva_prellenada.get("check_out", self.reserva_prellenada.get("fecha", "Seleccionar fecha").split(" - ")[-1]))

        campo_entrada = tk.Frame(frame_fechas, bg=C["main_bg"])
        campo_entrada.pack(side="left", fill="x", expand=True, padx=(0, 4))
        tk.Label(campo_entrada, text="Entrada",
             bg=C["main_bg"], fg=C["texto_light"],
             font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Entry(campo_entrada, textvariable=self.vars["check_in"],
             font=("Segoe UI", 9), relief="solid", bd=1,
             state="readonly", readonlybackground="#f0f0f0").pack(
             side="left", fill="x", expand=True, ipady=4)
        tk.Button(campo_entrada, text="📅", font=("Segoe UI", 10),
              relief="flat", bg=C["naranja"], fg="white",
              cursor="hand2", padx=6,
              command=lambda: self._abrir_calendario("check_in")).pack(side="left", padx=(4, 0))

        campo_salida = tk.Frame(frame_fechas, bg=C["main_bg"])
        campo_salida.pack(side="left", fill="x", expand=True, padx=(4, 0))
        tk.Label(campo_salida, text="Salida",
             bg=C["main_bg"], fg=C["texto_light"],
             font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Entry(campo_salida, textvariable=self.vars["check_out"],
             font=("Segoe UI", 9), relief="solid", bd=1,
             state="readonly", readonlybackground="#f0f0f0").pack(
             side="left", fill="x", expand=True, ipady=4)
        tk.Button(campo_salida, text="📅", font=("Segoe UI", 10),
              relief="flat", bg=C["naranja"], fg="white",
              cursor="hand2", padx=6,
              command=lambda: self._abrir_calendario("check_out")).pack(side="left", padx=(4, 0))

    # Huéspedes (Combobox)
        tk.Label(pad, text="Huéspedes",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars["huespedes"] = tk.StringVar(value=self.reserva_prellenada.get("huespedes", "1 Adulto") if self.reserva_prellenada else "1 Adulto")
        ttk.Combobox(pad, textvariable=self.vars["huespedes"],
                     values=["1 Adulto", "2 Adultos", "3 Adultos", "4 Adultos"],
                 state="readonly", font=("Segoe UI", 9)).pack(
                 fill="x", ipady=3)

    # Habitación (Combobox)
        tk.Label(pad, text="Habitación",
             bg=C["main_bg"], fg=C["texto_mid"],
             font=("Segoe UI", 9)).pack(anchor="w", pady=(8, 2))
        self.vars["habitacion"] = tk.StringVar(value=self.reserva_prellenada.get("habitacion", "Simple") if self.reserva_prellenada else "Simple")
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
        self.vars["estado"] = tk.StringVar(value=self.reserva_prellenada.get("estado", "Confirmada") if self.reserva_prellenada else "Confirmada")
        ttk.Combobox(pad, textvariable=self.vars["estado"],
                 values=["Confirmada", "Pendiente"],
                 state="readonly", font=("Segoe UI", 9)).pack(
                 fill="x", ipady=3, pady=(0, 16))

    # Botones
        fila_btns = tk.Frame(pad, bg=C["main_bg"])
        fila_btns.pack(fill="x")

        btn_confirm = tk.Button(
            fila_btns,
            text="Confirmar",
            command=lambda: self._guardar(confirmar=True),
            bg=C["naranja"], fg=C["blanco"],
            activebackground="#c94208",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=14, pady=8
        )
        btn_confirm.pack(side="left")

        btn_guardar = tk.Button(
            fila_btns,
            text="Guardar",
            command=lambda: self._guardar(confirmar=False),
            bg=C["naranja"], fg=C["blanco"],
            activebackground="#c94208",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=14, pady=8
        )
        btn_guardar.pack(side="left", padx=(8, 0))

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

        hotel = self.vars["hotel"].get().strip()
        ciudad = self.vars["ciudad"].get().strip()
        check_in = self.vars["check_in"].get().strip()
        check_out = self.vars["check_out"].get().strip()

        if not hotel or not ciudad or not check_in or not check_out:
            messagebox.showwarning(
                "Campos requeridos",
                "Hotel, ciudad, fecha de entrada y fecha de salida son obligatorios.",
                parent=self.ventana
            )
            return

        fecha_entrada = self._parse_fecha(check_in)
        fecha_salida = self._parse_fecha(check_out)
        if fecha_entrada is None or fecha_salida is None:
            messagebox.showwarning(
                "Fecha inválida",
                "Selecciona fechas válidas para entrada y salida.",
                parent=self.ventana
            )
            return

        hoy = datetime.date.today()
        if fecha_entrada < hoy or fecha_salida < hoy:
            messagebox.showwarning(
                "Fecha en el pasado",
                "No puedes reservar fechas que ya hayan pasado.",
                parent=self.ventana
            )
            return

        if fecha_salida < fecha_entrada:
            messagebox.showwarning(
                "Rango inválido",
                "La fecha de salida debe ser posterior a la fecha de entrada.",
                parent=self.ventana
            )
            return

        fecha = f"{check_in} - {check_out}"

        reservas_existentes = leer_reservas()
        for r in reservas_existentes:
            if r.get("id") == str(self.reserva_prellenada.get("id", "")):
                continue
            if (r.get("hotel", "").lower() == hotel.lower() and
                    r.get("fecha", "").lower() == fecha.lower()):
                messagebox.showwarning(
                    "Reserva duplicada",
                    f"Ya tienes una reserva en {hotel} para esas fechas.",
                    parent=self.ventana
                )
                return

        nueva = {
            "hotel": hotel,
            "ciudad": ciudad,
            "fecha": fecha,
            "check_in": check_in,
            "check_out": check_out,
            "huespedes": self.vars["huespedes"].get().strip(),
            "habitacion": self.vars["habitacion"].get().strip(),
            "precio": self.vars["precio"].get().strip(),
            "estado": self.vars["estado"].get().strip(),
        }

        if self.reserva_prellenada and self.reserva_prellenada.get("id"):
            actualizar_reserva(self.reserva_prellenada["id"], nueva)
            mensaje = f"La reserva en {hotel} fue actualizada correctamente."
            titulo = "Reserva actualizada"
        else:
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

    def _abrir_calendario(self, campo):
        self._campo_fecha_activa = campo

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
        if getattr(self, '_campo_fecha_activa', None) == "check_in":
            self.vars["check_in"].set(fecha_str)
            try:
                fecha_entrada = self._parse_fecha(fecha_str)
                fecha_salida = self._parse_fecha(self.vars["check_out"].get())
                if fecha_salida is None or fecha_salida <= fecha_entrada:
                    siguiente = fecha_entrada + datetime.timedelta(days=1)
                    self.vars["check_out"].set(
                        f"{siguiente.day:02d} {nombres_mes[siguiente.month]}, {siguiente.year}"
                    )
            except Exception:
                pass
        else:
            self.vars["check_out"].set(fecha_str)
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

    def _parse_fecha(self, fecha_str):
        fecha_str = fecha_str.strip()
        if not fecha_str or fecha_str.lower().startswith("seleccionar"):
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
