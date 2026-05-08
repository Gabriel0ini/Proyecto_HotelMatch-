

import tkinter as tk
from hotelmatch.colores  import C


def boton_naranja(padre, texto, comando, ancho=18):
    """
    Botón naranja con efecto hover.
    Tkinter no tiene border-radius, así que
    usamos un Label estilizado (más flexible que Button).
    """
    btn = tk.Label(
        padre,
        text=texto,
        bg=C["naranja"],
        fg=C["blanco"],
        font=("Segoe UI", 9, "bold"),
        padx=16, pady=8,
        cursor="hand2",
        width=ancho
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=C["naranja_lt"]))
    btn.bind("<Leave>", lambda e: btn.config(bg=C["naranja"]))
    btn.bind("<Button-1>", lambda e: comando())
    return btn


def separador(padre, color="#2a2a4e"):
    """Línea horizontal de 1px (equivalente a <hr>)."""
    return tk.Canvas(
        padre,
        bg=color,
        height=1,
        highlightthickness=0
    )


def etiqueta_tag(padre, texto, tipo="hist"):
    """
    Tag de categoría de colores (ej: PATRIMONIO HISTÓRICO).
    tipo puede ser 'hist' o 'trop'
    """
    bg = C["tag_hist_bg"] if tipo == "hist" else C["tag_trop_bg"]
    fg = C["tag_hist_fg"] if tipo == "hist" else C["tag_trop_fg"]
    return tk.Label(
        padre,
        text=texto.upper(),
        bg=bg, fg=fg,
        font=("Segoe UI", 7, "bold"),
        padx=6, pady=2
    )


def titulo_seccion(padre, texto, color=None):
    """
    Texto pequeño en naranja en mayúsculas
    que encabeza cada sección (ej: 'PRÓXIMA ESTANCIA').
    """
    return tk.Label(
        padre,
        text=texto,
        bg=padre["bg"],
        fg=color or C["naranja"],
        font=("Segoe UI", 8, "bold")
    )


def card(padre, **kwargs):
    """
    Frame con borde simulado.
    Tkinter no tiene box-shadow ni border-radius,
    usamos highlightbackground como alternativa.
    """
    return tk.Frame(
        padre,
        bg=C["blanco"],
        highlightbackground=C["borde"],
        highlightthickness=1,
        **kwargs
    )