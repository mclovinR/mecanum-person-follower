"""Lógica pura de seguimiento por zonas (sin cámara, sin Hailo, sin MQTT).

Separada de zonas.py para poder probarla en cualquier computadora.
Las coordenadas del bounding box están normalizadas de 0.0 a 1.0.
"""

ZONA_IZQ = 0.25  # borde derecho de la zona izquierda
ZONA_DER = 0.75  # borde izquierdo de la zona derecha


def zona_dominante(x1, x2):
    """Devuelve la zona donde cae la mayor parte de la persona.

    Zonas: IZQ 0.00-0.25 | CENTRO 0.25-0.75 | DER 0.75-1.00
    Retorna (zona, pct_izq, pct_centro, pct_der).
    """
    bw = x2 - x1
    if bw <= 0:
        return "centro", 0.0, 0.0, 0.0

    pct_izq = max(0, min(x2, ZONA_IZQ) - x1) / bw
    pct_centro = max(0, min(x2, ZONA_DER) - max(x1, ZONA_IZQ)) / bw
    pct_der = max(0, x2 - max(x1, ZONA_DER)) / bw

    zona = max(
        ("izq", pct_izq),
        ("centro", pct_centro),
        ("der", pct_der),
        key=lambda z: z[1],
    )[0]
    return zona, pct_izq, pct_centro, pct_der


def comando_para_persona(zona, bbox_h, distancia_cerca):
    """Traduce la posición de la persona a un comando MQTT para el ESP32.

    Una persona cerca ocupa más alto del cuadro, así que la altura del
    bounding box sirve como estimación de distancia.
    """
    if bbox_h > distancia_cerca:
        return "persona_cerca"
    if zona == "izq":
        return "persona_izquierda"
    if zona == "der":
        return "persona_derecha"
    return "persona_frente"
