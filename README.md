# Conversor de temperaturas (Celsius ↔ Fahrenheit)

Script de línea de comandos en Python para convertir temperaturas entre Celsius y Fahrenheit.

## Requisitos

- Python 3.8 o superior.
- Sin dependencias externas (solo biblioteca estándar).

## Uso

```bash
python convertir_temperatura.py VALOR --de {C,F} [--a {C,F}] [--decimales N]
```

Ejemplos:

```bash
python convertir_temperatura.py 100 --de C --a F   # 100 °C = 212.00 °F
python convertir_temperatura.py 32 --de F --a C    # 32 °F = 0.00 °C
python convertir_temperatura.py -40 --de C         # destino implícito: F
python convertir_temperatura.py 36.6 --de C --decimales 1
```

Notas:

- Si no se indica `--a`, se convierte a la escala contraria a la de origen.
- Se rechazan valores por debajo del cero absoluto (-273.15 °C / -459.67 °F) y valores no finitos.
- Código de salida: `0` si todo va bien, `1` si la temperatura no es válida y `2` si los argumentos son incorrectos.

## Tests

```bash
python -m unittest -v
```
