#!/usr/bin/env python3
"""Convierte temperaturas entre Celsius y Fahrenheit desde la línea de comandos.

Ejemplos:
    python convertir_temperatura.py 100 --de C --a F
    python convertir_temperatura.py 32 --de F --a C
    python convertir_temperatura.py -40 --de C
"""

import argparse
import math
import sys
from typing import Optional, Sequence

ESCALAS = ("C", "F")
# Cero absoluto en cada escala (se compara en la escala de origen para evitar
# errores de redondeo al convertir antes de validar).
CERO_ABSOLUTO = {"C": -273.15, "F": -459.67}


def celsius_a_fahrenheit(celsius: float) -> float:
    """Convierte grados Celsius a Fahrenheit."""
    return celsius * 9 / 5 + 32


def fahrenheit_a_celsius(fahrenheit: float) -> float:
    """Convierte grados Fahrenheit a Celsius."""
    return (fahrenheit - 32) * 5 / 9


def convertir(valor: float, origen: str, destino: str) -> float:
    """Convierte `valor` de la escala `origen` a la escala `destino`.

    Lanza ValueError si el valor no es finito, está por debajo del cero
    absoluto o si las escalas no son válidas.
    """
    origen = origen.upper()
    destino = destino.upper()
    if origen not in ESCALAS or destino not in ESCALAS:
        raise ValueError(f"Las escalas válidas son: {', '.join(ESCALAS)}.")
    if not math.isfinite(valor):
        raise ValueError("El valor debe ser un número finito.")

    if valor < CERO_ABSOLUTO[origen]:
        raise ValueError("La temperatura no puede estar por debajo del cero absoluto.")

    if origen == destino:
        return float(valor)
    if destino == "F":
        return celsius_a_fahrenheit(valor)
    return fahrenheit_a_celsius(valor)


def decimales_valido(texto: str) -> int:
    """Valida el argumento --decimales (entero >= 0) para argparse."""
    try:
        numero = int(texto)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{texto}' no es un entero válido.")
    if numero < 0:
        raise argparse.ArgumentTypeError("no puede ser negativo.")
    return numero


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convierte temperaturas entre Celsius (C) y Fahrenheit (F)."
    )
    parser.add_argument("valor", type=float, help="Temperatura a convertir.")
    parser.add_argument(
        "--de",
        dest="origen",
        required=True,
        type=str.upper,
        choices=ESCALAS,
        help="Escala de origen: C o F.",
    )
    parser.add_argument(
        "--a",
        dest="destino",
        type=str.upper,
        choices=ESCALAS,
        help="Escala de destino: C o F (por defecto, la contraria a la de origen).",
    )
    parser.add_argument(
        "--decimales",
        type=decimales_valido,
        default=2,
        help="Número de decimales del resultado (por defecto 2).",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = crear_parser().parse_args(argv)
    destino = args.destino or ("F" if args.origen == "C" else "C")

    try:
        resultado = convertir(args.valor, args.origen, destino)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(
        f"{args.valor:g} °{args.origen} = {resultado:.{args.decimales}f} °{destino}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
