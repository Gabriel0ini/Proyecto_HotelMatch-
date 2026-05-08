
import tkinter as tk
from tkinter import ttk, messagebox
from colores import C
from widgets import boton_naranja, titulo_seccion, separador
from datos import leer_usuario, guardar_usuario, leer_reservas, \
                  leer_favoritos


class PaginaConfiguracion(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        canvas = tk.Canvas(self, bg=C["main_bg"],
                           highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical",
                               command=canvas.yview)

        interior = tk.Frame(canvas, bg=C["main_bg"])
        interior.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=interior, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        pad = tk.Frame(interior, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=32, pady=28)

        self._encabezado(pad)
        self._card_perfil(pad)
        self._card_estadisticas(pad)
        self._card_archivos(pad)


    def _encabezado(self, padre):
        tk.Label(
            padre,
            text="Configuración",
            bg=C["main_bg"],
            fg=C["texto_dark"],
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            padre,
            text="Gestiona tu perfil y preferencias de cuenta.",
            bg=C["main_bg"],
            fg=C["texto_mid"],
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 20))

    def _card_perfil(self, padre):
        """
        Card con formulario para editar los datos del usuario.
        Los datos se leen desde usuario.txt al abrir la página.
        """
        titulo_seccion(padre, "INFORMACIÓN DE PERFIL").pack(
            anchor="w", pady=(0, 8)
        )

        tarjeta = tk.Frame(
            padre,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        tarjeta.pack(fill="x", pady=(0, 20))

        interior = tk.Frame(tarjeta, bg=C["blanco"])
        interior.pack(fill="x", padx=24, pady=20)

        usuario = leer_usuario()


        campos = tk.Frame(interior, bg=C["blanco"])
        campos.pack(fill="x", pady=(0, 16))

        self.var_nombre = tk.StringVar(
            value=usuario.get("nombre", "")
        )
        self._campo_formulario(
            campos,
            etiqueta="Nombre completo",
            variable=self.var_nombre,
            fila=0
        )

    
        self.var_email = tk.StringVar(
            value=usuario.get("email", "")
        )
        self._campo_formulario(
            campos,
            etiqueta="Email",
            variable=self.var_email,
            fila=1
        )

        
        tk.Label(
            campos,
            text="Membresía",
            bg=C["blanco"],
            fg=C["texto_mid"],
            font=("Segoe UI", 9),
            width=16, anchor="w"
        ).grid(row=2, column=0, pady=8, sticky="w")

        self.var_membresia = tk.StringVar(
            value=usuario.get("membresia", "Member")
        )

        combo = ttk.Combobox(
            campos,
            textvariable=self.var_membresia,
            values=["Member", "Premium Member", "VIP Member"],
            state="readonly",      
            font=("Segoe UI", 9),
            width=22
        )
        combo.grid(row=2, column=1, pady=8, sticky="w")

        separador(interior).pack(fill="x", pady=(0, 16))

        boton_naranja(
            interior,
            "GUARDAR CAMBIOS",
            self._guardar_perfil,
            ancho=18
        ).pack(anchor="w")

    def _campo_formulario(self, padre, etiqueta, variable, fila):
        """
        Crea una fila de formulario con label + entry usando grid.
        Reutilizable para cada campo.

        Usamos grid aquí porque tenemos dos columnas
        perfectamente alineadas — ideal para formularios.
        """
        tk.Label(
            padre,
            text=etiqueta,
            bg=C["blanco"],
            fg=C["texto_mid"],
            font=("Segoe UI", 9),
            width=16, anchor="w"
        ).grid(row=fila, column=0, pady=8, sticky="w")

        tk.Entry(
            padre,
            textvariable=variable,
            font=("Segoe UI", 9),
            relief="solid", bd=1,
            width=24
        ).grid(row=fila, column=1, pady=8,
               ipady=4, sticky="w")

    def _card_estadisticas(self, padre):
        """
        Muestra un resumen de los datos del usuario.
        Lee en tiempo real desde los archivos .txt
        """
        titulo_seccion(padre, "RESUMEN DE ACTIVIDAD").pack(
            anchor="w", pady=(0, 8)
        )

        tarjeta = tk.Frame(
            padre,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        tarjeta.pack(fill="x", pady=(0, 20))

        interior = tk.Frame(tarjeta, bg=C["blanco"])
        interior.pack(fill="x", padx=24, pady=20)

        reservas  = leer_reservas()
        favoritos = leer_favoritos()

        confirmadas = sum(
            1 for r in reservas
            if r.get("estado") == "Confirmada"
        )
        finalizadas = sum(
            1 for r in reservas
            if r.get("estado") == "Finalizado"
        )

        stats = [
            ("🏨", "Total reservas",    str(len(reservas))),
            ("✅", "Confirmadas",       str(confirmadas)),
            ("📋", "Finalizadas",       str(finalizadas)),
            ("❤",  "Favoritos",         str(len(favoritos))),
        ]

        fila_stats = tk.Frame(interior, bg=C["blanco"])
        fila_stats.pack(fill="x")

        for icono, etiqueta, valor in stats:
            self._stat_item(fila_stats, icono, etiqueta, valor)

    def _stat_item(self, padre, icono, etiqueta, valor):
        """Bloque individual de estadística."""
        bloque = tk.Frame(
            padre,
            bg="#f8f8f8",
            highlightbackground=C["borde"],
            highlightthickness=1,
            width=120, height=80
        )
        bloque.pack(side="left", padx=(0, 12))
        bloque.pack_propagate(False)

        tk.Label(
            bloque,
            text=icono,
            bg="#f8f8f8",
            font=("Segoe UI", 16)
        ).pack(pady=(10, 0))

        tk.Label(
            bloque,
            text=valor,
            bg="#f8f8f8",
            fg=C["naranja"],
            font=("Segoe UI", 14, "bold")
        ).pack()

        tk.Label(
            bloque,
            text=etiqueta,
            bg="#f8f8f8",
            fg=C["texto_light"],
            font=("Segoe UI", 7)
        ).pack()

    def _card_archivos(self, padre):
        """
        Muestra el estado de los archivos .txt del sistema.
        Verifica si existen y muestra su ruta.
        """
        titulo_seccion(padre, "ARCHIVOS DEL SISTEMA").pack(
            anchor="w", pady=(0, 8)
        )

        tarjeta = tk.Frame(
            padre,
            bg=C["blanco"],
            highlightbackground=C["borde"],
            highlightthickness=1
        )
        tarjeta.pack(fill="x")

        interior = tk.Frame(tarjeta, bg=C["blanco"])
        interior.pack(fill="x", padx=24, pady=16)

        import os
        from datos import CARPETA_DATOS

        archivos = [
            ("👤", "usuario.txt"),
            ("🏨", "reservas.txt"),
            ("❤",  "favoritos.txt"),
        ]

        for icono, nombre_archivo in archivos:
            ruta_completa = os.path.join(CARPETA_DATOS, nombre_archivo)
            existe = os.path.exists(ruta_completa)
            self._fila_archivo(
                interior, icono,
                nombre_archivo, ruta_completa, existe
            )

            if nombre_archivo != "favoritos.txt":
                separador(interior).pack(fill="x")

    def _fila_archivo(self, padre, icono,
                      nombre, ruta, existe):
        """Fila de estado de un archivo del sistema."""
        fila = tk.Frame(padre, bg=C["blanco"])
        fila.pack(fill="x", pady=8)

        tk.Label(
            fila,
            text=f"{icono}  {nombre}",
            bg=C["blanco"],
            fg=C["texto_dark"],
            font=("Segoe UI", 9, "bold"),
            width=18, anchor="w"
        ).pack(side="left")

        ruta_corta = ruta if len(ruta) < 45 else "..." + ruta[-42:]
        tk.Label(
            fila,
            text=ruta_corta,
            bg=C["blanco"],
            fg=C["texto_light"],
            font=("Segoe UI", 7)
        ).pack(side="left", expand=True, anchor="w")

        estado_txt = "✓  OK" if existe else "✗  No encontrado"
        estado_color = C["verde"] if existe else "#e74c3c"

        tk.Label(
            fila,
            text=estado_txt,
            bg=C["blanco"],
            fg=estado_color,
            font=("Segoe UI", 8, "bold")
        ).pack(side="right")


    def _guardar_perfil(self):
        """
        Lee los valores de los campos y los guarda en usuario.txt
        Luego actualiza el sidebar con el nuevo nombre.
        """
        nombre = self.var_nombre.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Campo requerido",
                "El nombre no puede estar vacío."
            )
            return

        guardar_usuario({
            "nombre":    nombre,
            "membresia": self.var_membresia.get(),
            "email":     self.var_email.get().strip()
        })

        self.app.usuario = leer_usuario()
        self.app.actualizar_perfil_sidebar()

        messagebox.showinfo(
            "Guardado",
            f"Perfil actualizado correctamente.\n"
            f"Bienvenido, {nombre}!"
        )