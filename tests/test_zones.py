import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vision"))

from zones import comando_para_persona, zona_dominante  # noqa: E402


class ZonaDominanteTest(unittest.TestCase):
    def test_persona_completamente_a_la_izquierda(self):
        self.assertEqual(zona_dominante(0.0, 0.2)[0], "izq")

    def test_persona_en_el_centro(self):
        self.assertEqual(zona_dominante(0.4, 0.6)[0], "centro")

    def test_persona_completamente_a_la_derecha(self):
        self.assertEqual(zona_dominante(0.8, 1.0)[0], "der")

    def test_persona_entre_dos_zonas_gana_la_mayor_parte(self):
        # 0.10-0.35: 0.15 en IZQ y 0.10 en CENTRO -> IZQ
        self.assertEqual(zona_dominante(0.10, 0.35)[0], "izq")
        # 0.20-0.50: 0.05 en IZQ y 0.25 en CENTRO -> CENTRO
        self.assertEqual(zona_dominante(0.20, 0.50)[0], "centro")

    def test_los_porcentajes_suman_uno(self):
        _, izq, centro, der = zona_dominante(0.1, 0.9)
        self.assertAlmostEqual(izq + centro + der, 1.0)

    def test_bbox_invalido_devuelve_centro(self):
        self.assertEqual(zona_dominante(0.5, 0.5), ("centro", 0.0, 0.0, 0.0))


class ComandoTest(unittest.TestCase):
    def test_persona_cerca_tiene_prioridad_sobre_la_zona(self):
        self.assertEqual(comando_para_persona("izq", 0.9, 0.72), "persona_cerca")

    def test_comandos_por_zona(self):
        self.assertEqual(comando_para_persona("izq", 0.5, 0.72), "persona_izquierda")
        self.assertEqual(comando_para_persona("der", 0.5, 0.72), "persona_derecha")
        self.assertEqual(comando_para_persona("centro", 0.5, 0.72), "persona_frente")

    def test_altura_igual_al_limite_no_es_cerca(self):
        self.assertEqual(comando_para_persona("centro", 0.72, 0.72), "persona_frente")


if __name__ == "__main__":
    unittest.main()
