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

        boton_naranja(
            interior,
            "+ NUEVA RESERVA",
            self._abrir_formulario,
            ancho=16
        ).pack(side="right")


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
            text="Pulsa '+ NUEVA RESERVA' para comenzar.",
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
    def __init__(self, ventana, app, callback_actualizar):
        self.ventana = ventana
        self.app     = app
        
        self.callback_actualizar = callback_actualizar

        self._construir()

    def _construir(self):
        pad = tk.Frame(self.ventana, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(
            pad,
            text="Nueva Reserva",
            bg=C["main_bg"], fg=C["texto_dark"],
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 20))

        campos_config = [
            ("Hotel",       "hotel",      ""),
            ("Ciudad",      "ciudad",     ""),
            ("Fecha",       "fecha",      "01 Ene, 2025"),
            ("Huéspedes",   "huespedes",  "2 Adultos"),
            ("Habitación",  "habitacion", "Habitación Estándar"),
            ("Precio/noche","precio",     "100"),
        ]

        self.vars = {}

        for etiqueta, clave, default in campos_config:
            self._campo(pad, etiqueta, clave, default)

        tk.Label(
            pad,
            text="Estado",
            bg=C["main_bg"], fg=C["texto_mid"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(8, 2))

        self.vars["estado"] = tk.StringVar(value="Confirmada")
        ttk.Combobox(
            pad,
            textvariable=self.vars["estado"],
            values=["Confirmada", "Pendiente", "Finalizado"],
            state="readonly",
            font=("Segoe UI", 9)
        ).pack(fill="x", ipady=3, pady=(0, 16))

        
        fila_btns = tk.Frame(pad, bg=C["main_bg"])
        fila_btns.pack(fill="x")

        boton_naranja(
            fila_btns, "GUARDAR", self._guardar, ancho=14
        ).pack(side="left")

        tk.Label(
            fila_btns,
            text="Cancelar",
            bg=C["main_bg"], fg=C["texto_light"],
            font=("Segoe UI", 9),
            cursor="hand2"
        ).pack(side="left", padx=12)

        fila_btns.winfo_children()[1].bind(
            "<Button-1>", lambda e: self.ventana.destroy()
        )

    def _campo(self, padre, etiqueta, clave, default):
        """Genera label + entry para cada campo del formulario."""
        tk.Label(
            padre,
            text=etiqueta,
            bg=C["main_bg"], fg=C["texto_mid"],
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(8, 2))

        self.vars[clave] = tk.StringVar(value=default)

        tk.Entry(
            padre,
            textvariable=self.vars[clave],
            font=("Segoe UI", 9),
            relief="solid", bd=1
        ).pack(fill="x", ipady=4)

    def _guardar(self):
        """Valida y guarda la nueva reserva."""
        hotel  = self.vars["hotel"].get().strip()
        ciudad = self.vars["ciudad"].get().strip()

        if not hotel or not ciudad:
            messagebox.showwarning(
                "Campos requeridos",
                "Hotel y ciudad son obligatorios.",
                parent=self.ventana
            )
            return

        nueva = {k: v.get().strip() for k, v in self.vars.items()}

        agregar_reserva(nueva)

        self.ventana.destroy()          
        self.callback_actualizar()      