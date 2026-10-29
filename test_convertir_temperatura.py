import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from convertir_temperatura import convertir, main


class TestConvertir(unittest.TestCase):
    def test_c_a_f(self):
        self.assertAlmostEqual(convertir(100, "C", "F"), 212)
        self.assertAlmostEqual(convertir(0, "C", "F"), 32)

    def test_f_a_c(self):
        self.assertAlmostEqual(convertir(32, "F", "C"), 0)
        self.assertAlmostEqual(convertir(212, "F", "C"), 100)

    def test_punto_comun(self):
        self.assertAlmostEqual(convertir(-40, "C", "F"), -40)

    def test_misma_escala(self):
        self.assertEqual(convertir(25, "C", "C"), 25)

    def test_minusculas(self):
        self.assertAlmostEqual(convertir(100, "c", "f"), 212)

    def test_bajo_cero_absoluto(self):
        with self.assertRaises(ValueError):
            convertir(-300, "C", "F")
        with self.assertRaises(ValueError):
            convertir(-500, "F", "C")

    def test_valor_no_finito(self):
        with self.assertRaises(ValueError):
            convertir(float("nan"), "C", "F")
        with self.assertRaises(ValueError):
            convertir(float("inf"), "C", "F")

    def test_cero_absoluto_exacto(self):
        self.assertAlmostEqual(convertir(-273.15, "C", "F"), -459.67)
        self.assertAlmostEqual(convertir(-459.67, "F", "C"), -273.15)

    def test_escala_invalida(self):
        with self.assertRaises(ValueError):
            convertir(10, "K", "C")


def ejecutar(argv):
    """Ejecuta main capturando stdout y stderr."""
    salida, error = io.StringIO(), io.StringIO()
    with redirect_stdout(salida), redirect_stderr(error):
        try:
            codigo = main(argv)
        except SystemExit as e:  # argparse sale con SystemExit
            codigo = e.code
    return codigo, salida.getvalue().strip(), error.getvalue()


class TestCLI(unittest.TestCase):
    def test_main_ok(self):
        codigo, salida, _ = ejecutar(["100", "--de", "C", "--a", "F"])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida, "100 °C = 212.00 °F")

    def test_destino_por_defecto(self):
        codigo, salida, _ = ejecutar(["32", "--de", "f"])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida, "32 °F = 0.00 °C")

    def test_decimales(self):
        codigo, salida, _ = ejecutar(["36.6", "--de", "C", "--decimales", "1"])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida, "36.6 °C = 97.9 °F")

    def test_main_error(self):
        codigo, _, error = ejecutar(["-300", "--de", "C"])
        self.assertEqual(codigo, 1)
        self.assertIn("cero absoluto", error)

    def test_decimales_negativos(self):
        codigo, _, error = ejecutar(["10", "--de", "C", "--decimales", "-1"])
        self.assertEqual(codigo, 2)
        self.assertIn("--decimales", error)


if __name__ == "__main__":
    unittest.main()
