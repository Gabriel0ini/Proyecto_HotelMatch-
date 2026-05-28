import sys
import tkinter as tk
from colores import C
from widgets import separador, boton_naranja

import tkinter as tk
from colores import C
from widgets import separador, boton_naranja

from paginas.inicio         import PaginaInicio
from paginas.mis_estancias  import PaginaMisEstancias
from paginas.favoritos      import PaginaFavoritos
from paginas.configuracion  import PaginaConfiguracion

USUARIO_ACTUAL = sys.argv[1] if len(sys.argv) > 1 else "Usuario"


def obtener_iniciales(nombre_usuario):
    nombre_usuario = nombre_usuario.strip()
    if not nombre_usuario:
        return "U"

    partes = nombre_usuario.split()
    if len(partes) == 1:
        return partes[0][0].upper()

    return (partes[0][0] + partes[-1][0]).upper()


class HotelMatchApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self._pagina_actual = None
        self.usuario_actual = USUARIO_ACTUAL
   
        self._paginas = {
            "inicio":         PaginaInicio,
            "mis_estancias":  PaginaMisEstancias,
            "favoritos":      PaginaFavoritos,
            "configuracion":  PaginaConfiguracion,
        }

        self._configurar_ventana()
        self._construir_layout()

        self.navegar("inicio")

    def _configurar_ventana(self):
        self.title("HotelMatch")
        self.geometry("900x600")
        self.minsize(800, 500)
        self.configure(bg=C["sidebar_bg"])

    def _construir_layout(self):
        self.sidebar = tk.Frame(self, bg=C["sidebar_bg"], width=170)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.area_principal = tk.Frame(self, bg=C["main_bg"])
        self.area_principal.pack(side="left", fill="both", expand=True)

        self._construir_sidebar()


    def navegar(self, nombre_pagina):
        """
        Destruye el contenido actual y carga la nueva página.

        ¿Por qué destroy() y no hide()?
        Tkinter no tiene hide() nativo eficiente.
        Destruir y recrear es más limpio para proyectos medianos.
        (Para apps muy grandes usaríamos tkraise() con frames apilados)
        """
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
        """Resalta el botón activo y normaliza los demás."""
        for nombre, btn_frame in self._botones_nav.items():
            activo = (nombre == pagina_activa)
            bg = C["naranja"] if activo else C["sidebar_bg"]
            fg = C["blanco"]

            btn_frame.config(bg=bg)
            for hijo in btn_frame.winfo_children():
                try:
                    hijo.config(bg=bg, fg=fg)
                except tk.TclError:
                    pass    


    def _construir_sidebar(self):
        self._botones_nav = {}   
       
        frame_logo = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        frame_logo.pack(fill="x", padx=14, pady=(20, 2))

        tk.Label(frame_logo, text="<HOTEL>", bg=C["sidebar_bg"],
                 fg=C["naranja"], font=("Segoe UI", 12, "bold")).pack(side="left")
        tk.Label(frame_logo, text=" MATCH",  bg=C["sidebar_bg"],
                 fg=C["blanco"],  font=("Segoe UI", 12, "bold")).pack(side="left")

        tk.Label(self.sidebar, text=f"USUARIO({self.usuario_actual.upper()})",
                 bg=C["sidebar_bg"], fg="#555577",
                 font=("Segoe UI", 7)).pack(anchor="w", padx=14)

        separador(self.sidebar).pack(fill="x", padx=10, pady=12)

        # Botones de navegación
        nav_items = [
            ("inicio",        "⊞", "Inicio"),
            ("mis_estancias", "≡", "Mis Estancias"),
            ("favoritos",     "♡", "Favoritos"),
            ("configuracion", "⚙", "Configuración"),
        ]

        for clave, icono, etiqueta in nav_items:
            self._crear_boton_nav(clave, icono, etiqueta)

        self._construir_perfil()

    def _crear_boton_nav(self, clave, icono, etiqueta):
        """
        Crea un botón y lo registra en self._botones_nav
        para poder cambiar su color cuando se navega.
        """
        contenedor = tk.Frame(self.sidebar, bg=C["sidebar_bg"], cursor="hand2")
        contenedor.pack(fill="x", padx=10, pady=1)

        lbl = tk.Label(
            contenedor,
            text=f"  {icono}   {etiqueta}",
            bg=C["sidebar_bg"],
            fg=C["sidebar_txt"],
            font=("Segoe UI", 10),
            anchor="w",
            padx=8, pady=10
        )
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

    def _construir_perfil(self):
        separador(self.sidebar).pack(side="bottom", fill="x", padx=10)

        perfil = tk.Frame(self.sidebar, bg=C["sidebar_bg"])
        perfil.pack(side="bottom", fill="x", padx=10, pady=12)

        iniciales = obtener_iniciales(USUARIO_ACTUAL)
        tk.Label(perfil, text=iniciales, bg=C["naranja"], fg=C["blanco"],
                 font=("Segoe UI", 10, "bold"),
                 width=3, height=1).pack(side="left", padx=(0, 8))

        datos = tk.Frame(perfil, bg=C["sidebar_bg"])
        datos.pack(side="left")

        tk.Label(datos, text=USUARIO_ACTUAL.upper(), bg=C["sidebar_bg"],
                 fg=C["blanco"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(datos, text="Premium Member", bg=C["sidebar_bg"],
                 fg=C["texto_light"], font=("Segoe UI", 7)).pack(anchor="w")


if __name__ == "__main__":
    app = HotelMatchApp()
    app.mainloop()