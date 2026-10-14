# Troubleshooting

## The robot moves to the wrong side (left and right are swapped)

The Hailo GStreamer pipelines mirror the camera image by default (`videoflip video-direction=horiz`). With a mirrored image, a person on the robot's left appears on the right side of the frame.

Edit `gstreamer_helper_pipelines.py` inside the Hailo examples virtual environment:

```
venv_hailo_rpi_examples/lib/python3.11/site-packages/hailo_apps/hailo_app_python/core/gstreamer/gstreamer_helper_pipelines.py
```

Replace the three occurrences of

```
'videoflip name=videoflip video-direction=horiz ! '
```

with

```
'videoflip name=videoflip video-direction=identity ! '
```

Do not invert the commands in `zones.py` to compensate; fix the image instead, so the stream in the dashboard matches what the robot sees.

## The ESP32 does not connect to MQTT

- Check that `MQTT_HOSTNAME` in `secrets.h` matches the Raspberry Pi hostname (`hostname` on the Pi).
- The ESP32 resolves the broker with mDNS. If your network blocks mDNS, use the Pi's IP address instead.
- Mosquitto must listen on `1883` (TCP, for the ESP32) and `9001` (WebSockets, for the dashboard).

## The dashboard says "disconnected"

- Enter the Raspberry Pi IP in the dashboard (default `192.168.137.3`, the address Windows hotspot sharing assigns).
- Verify the WebSockets listener: `sudo ss -ltnp | grep 9001`.

## Detections are unstable in low light

`zonas.py` applies CLAHE to every frame before display, and the confidence threshold is `UMBRAL = 0.35`. Raise it if there are false positives; lower it if the person is lost often.
