#!/bin/bash
# Arranca broker MQTT, dashboard y visión. Ejecutar en la Raspberry Pi 5.
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
HAILO_DIR="${HAILO_DIR:-$HOME/Downloads/hailo-rpi5-examples}"
echo "==================================="
echo "  Arrancando sistema del robot..."
echo "==================================="

echo "[1/3] Verificando broker MQTT..."
sudo systemctl start mosquitto
sleep 1
if sudo systemctl is-active --quiet mosquitto; then
    echo "  Mosquitto OK"
else
    echo "  ERROR: Mosquitto no pudo arrancar"
    exit 1
fi

echo "[2/3] Verificando webcam..."
if [ -e /dev/video0 ]; then
    echo "  Webcam OK en /dev/video0"
else
    echo "  ERROR: No se encontró webcam en /dev/video0"
    exit 1
fi

echo "[2.5/3] Iniciando servidor web del dashboard..."
pkill -f "http.server 8888" 2>/dev/null
sleep 1
cd "$REPO_DIR/dashboard"
python3 -m http.server 8888 &
echo "  Dashboard disponible en: http://$(hostname -I | awk '{print $1}'):8888/dashboard_mecanum.html"

echo "[3/3] Iniciando seguimiento de personas..."
echo "  Stream disponible en: http://$(hostname -I | awk '{print $1}'):8080"
echo "  Ctrl+C para detener"
echo "==================================="

cd "$HAILO_DIR"
source setup_env.sh

echo "Python usado: $(which python)"
echo "Versión: $(python --version)"

PYTHONPATH="$REPO_DIR/vision" xvfb-run -a "$HAILO_DIR/venv_hailo_rpi_examples/bin/python" \
  "$REPO_DIR/vision/zonas.py" --input usb \
  --hef-path /usr/local/hailo/resources/models/hailo8l/yolov8s.hef \
  2>&1 | tee "$REPO_DIR/robot_log.txt"

echo "Script terminó con código: $?"
