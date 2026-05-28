import tkinter as tk
from tkinter import ttk, messagebox
from colores import C
from widgets import titulo_seccion, separador, etiqueta_tag, boton_naranja
from datos   import leer_favoritos, eliminar_favorito


class PaginaFavoritos(tk.Frame):
    def __init__(self, padre, app):
        super().__init__(padre, bg=C["main_bg"])
        self.app = app
        self._construir()

    def _construir(self):
        self._barra_superior()
        self._area_scroll()


    def _barra_superior(self):
        """
        Encabezado fijo con título y contador de favoritos.
        El contador se actualiza cada vez que se elimina uno.
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
            text="❤  Mis Favoritos",
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")

        total = len(leer_favoritos())
        self._lbl_contador = tk.Label(
            interior,
            text=self._texto_contador(total),
            bg=C["blanco"], fg=C["texto_light"],
            font=("Segoe UI", 9)
        )
        self._lbl_contador.pack(side="right", padx=(0, 4))

    def _texto_contador(self, total):
        """Genera el texto del contador según la cantidad."""
        if total == 0:
            return "Sin favoritos"
        elif total == 1:
            return "1 destino guardado"
        else:
            return f"{total} destinos guardados"


    def _area_scroll(self):
        self._canvas = tk.Canvas(
            self, bg=C["main_bg"], highlightthickness=0)
        scroll = ttk.Scrollbar(
            self, orient="vertical", command=self._canvas.yview)

        self._frame_lista = tk.Frame(self._canvas, bg=C["main_bg"])

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
        Limpia y redibuja todas las cards.
        También actualiza el contador del encabezado.
        """
        for w in self._frame_lista.winfo_children():
            w.destroy()

        favoritos = leer_favoritos()

        self._lbl_contador.config(
            text=self._texto_contador(len(favoritos))
        )

        pad = tk.Frame(self._frame_lista, bg=C["main_bg"])
        pad.pack(fill="both", expand=True, padx=28, pady=20)

        if not favoritos:
            self._estado_vacio(pad)
            return

        for fav in favoritos:
            self._card_favorito(pad, fav)

    def _estado_vacio(self, padre):
        """Pantalla cuando no hay favoritos guardados."""
        tk.Label(
            padre,
            text="🤍",
            bg=C["main_bg"],
            font=("Segoe UI", 42)
        ).pack(pady=(60, 8))

        tk.Label(
            padre,
            text="No tienes favoritos aún",
            bg=C["main_bg"], fg=C["texto_dark"],
            font=("Segoe UI", 14, "bold")
        ).pack()

        tk.Label(
            padre,
            text="Los destinos que guardes aparecerán aquí.",
            bg=C["main_bg"], fg=C["texto_light"],
            font=("Segoe UI", 9)
        ).pack(pady=(4, 24))

        boton_naranja(
            padre,
            "EXPLORAR DESTINOS",
            lambda: self.app.navegar("inicio"),
            ancho=20
        ).pack()

    # ── Card de favorito ──────────────────────────────────

    def _card_favorito(self, padre, fav):
        """
        Estructura de la card:
        ┌──────────────────────────────────────────┐
        │  [TAG tipo]                   ★ 4.8      │
        │  Nombre del destino                      │
        │  📍 Ciudad                               │
        │  Descripción del lugar...                │
        │  ─────────────────────────────────────   │
        │  💰 $120/noche         [🗑 Quitar]       │
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

        # ── Fila 1: tag tipo + rating ──────────────────
        fila_top = tk.Frame(interior, bg=C["blanco"])
        fila_top.pack(fill="x", pady=(0, 8))

        # Tag de categoría (usa tu widget existente)
        tipo = fav.get("tipo", "")
        tipo_clave = "hist" if "Hist" in tipo or "hist" in tipo else "trop"
        etiqueta_tag(fila_top, tipo, tipo_clave).pack(side="left")

        # Rating con estrella
        rating = fav.get("rating", "")
        tk.Label(
            fila_top,
            text=f"★  {rating}",
            bg=C["blanco"], fg=C["naranja"],
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

        # ── Fila 2: nombre ─────────────────────────────
        tk.Label(
            interior,
            text=fav.get("nombre", "Destino"),
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 4))

        # ── Fila 3: ciudad ─────────────────────────────
        tk.Label(
            interior,
            text=f"📍  {fav.get('ciudad', '')}",
            bg=C["blanco"], fg=C["texto_mid"],
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(0, 8))

        # ── Fila 4: descripción ────────────────────────
        # wraplength limita el ancho del texto en píxeles
        # Es el equivalente a max-width en CSS
        tk.Label(
            interior,
            text=fav.get("descripcion", ""),
            bg=C["blanco"], fg=C["texto_mid"],
            font=("Segoe UI", 9),
            wraplength=520,
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        # ── Separador ──────────────────────────────────
        separador(interior).pack(fill="x", pady=(0, 10))

# ... (Mantén todo igual en tu archivo hasta llegar a la Fila 5 dentro de _card_favorito)

        # ── Fila 5: precio + botón quitar + botón ver hoteles ─────────────
        fila_bottom = tk.Frame(interior, bg=C["blanco"])
        fila_bottom.pack(fill="x")

        precio = fav.get("precio", "0")
        tk.Label(
            fila_bottom,
            text=f"💰  ${precio} / noche",
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        # Botón quitar con hover (Existente)
        id_fav = fav.get("id")
        self._boton_quitar(fila_bottom, id_fav)

        # REFACTOR: Añadimos el nuevo botón para ver los hoteles de esa ciudad
        ciudad_destino = fav.get("ciudad", "")
        self._boton_ver_hoteles(fila_bottom, ciudad_destino)

    def _boton_ver_hoteles(self, padre, ciudad):
        """Botón interactivo para filtrar la lista de inicio por ciudad."""
        btn_ver = tk.Label(
            padre,
            text="🔍  Ver Hoteles",
            bg=C["blanco"], fg=C["naranja"],
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        # Lo posicionamos a la derecha, dejando un espacio con el botón quitar
        btn_ver.pack(side="right", padx=(0, 16))

        # Efecto Hover
        btn_ver.bind("<Enter>", lambda e: btn_ver.config(fg=C["texto_dark"]))
        btn_ver.bind("<Leave>", lambda e: btn_ver.config(fg=C["naranja"]))
        
        # Acción al hacer click
        btn_ver.bind(
            "<Button-1>",
            lambda e, c=ciudad: self._filtrar_y_navegar(c)
        )

    def _boton_quitar(self, padre, id_fav):
        """Crea el botón/etiqueta para quitar un favorito y lo enlaza a la confirmación."""
        btn_quitar = tk.Label(
            padre,
            text="🗑  Quitar",
            bg=C["blanco"], fg=C["texto_mid"],
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )
        btn_quitar.pack(side="right", padx=(0, 8))

        # Hover
        btn_quitar.bind("<Enter>", lambda e: btn_quitar.config(fg=C["texto_dark"]))
        btn_quitar.bind("<Leave>", lambda e: btn_quitar.config(fg=C["texto_mid"]))

        # Click -> confirmar y eliminar
        btn_quitar.bind("<Button-1>", lambda e, i=id_fav: self._confirmar_quitar(i))

    # ── Acciones ──────────────────────────────────────────

    # REFACTOR: Nueva acción para conectar con la App principal
    def _filtrar_y_navegar(self, ciudad_completa):
        """Limpia el formato de la ciudad, define el filtro global y navega al inicio."""
        # Si la ciudad viene como "Santa Cruz, Bolivia", extraemos solo "Santa Cruz"
        ciudad_limpia = ciudad_completa.split(",")[0].strip()
        
        # Guardamos el filtro en la instancia principal de la aplicación
        setattr(self.app, 'filtro_ciudad', ciudad_limpia)
        
        # Redireccionamos a la página de inicio
        self.app.navegar("inicio")

    def _confirmar_quitar(self, id_fav):
        """Pregunta confirmación y elimina el favorito si el usuario acepta."""
        respuesta = messagebox.askyesno(
            "Quitar favorito",
            "¿Estás seguro de que quieres quitar este favorito?"
        )
        if not respuesta:
            return

        try:
            eliminar_favorito(id_fav)
        except Exception:
            messagebox.showerror("Error", "No se pudo eliminar el favorito.")
            return

        # Refrescar la lista y el contador
        self._renderizar_lista()
        messagebox.showinfo("Eliminado", "Favorito eliminado correctamente.")