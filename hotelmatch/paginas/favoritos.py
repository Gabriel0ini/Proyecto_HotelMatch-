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

        # ── Fila 5: precio + botón quitar ─────────────
        fila_bottom = tk.Frame(interior, bg=C["blanco"])
        fila_bottom.pack(fill="x")

        precio = fav.get("precio", "0")
        tk.Label(
            fila_bottom,
            text=f"💰  ${precio} / noche",
            bg=C["blanco"], fg=C["texto_dark"],
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        # Botón quitar con hover
        id_fav = fav.get("id")
        self._boton_quitar(fila_bottom, id_fav)

    def _boton_quitar(self, padre, id_fav):
        """
        Botón 'Quitar de favoritos' con efecto hover rojo.
        Mismo patrón que boton_naranja pero en rojo.
        """
        btn = tk.Label(
            padre,
            text="🗑  Quitar",
            bg=C["blanco"], fg="#e74c3c",
            font=("Segoe UI", 8),
            cursor="hand2"
        )
        btn.pack(side="right")

        # Hover: más oscuro al pasar el mouse
        btn.bind("<Enter>", lambda e: btn.config(fg="#c0392b"))
        btn.bind("<Leave>", lambda e: btn.config(fg="#e74c3c"))
        btn.bind(
            "<Button-1>",
            lambda e, rid=id_fav: self._confirmar_quitar(rid)
        )

    # ── Acciones ──────────────────────────────────────────

    def _confirmar_quitar(self, id_fav):
        """Confirma antes de eliminar el favorito."""
        confirmado = messagebox.askyesno(
            "Quitar favorito",
            "¿Quitar este destino de tus favoritos?"
        )
        if confirmado:
            eliminar_favorito(id_fav)
            self._renderizar_lista()   