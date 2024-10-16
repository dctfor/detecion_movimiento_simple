# Sistema de Detección de Movimiento con OpenCV

Sistema de vigilancia basado en Python que utiliza OpenCV para detectar movimiento a través de la webcam. El sistema guarda automáticamente imágenes cuando detecta movimiento, incluyendo marca de tiempo.

![Vista previa del sistema](https://via.placeholder.com/800x400?text=Sistema+de+Detección+de+Movimiento)

## Características Principales

- 🎥 Monitoreo en tiempo real a través de la webcam
- 🔍 Detección de movimiento mediante diferencia de frames
- 📸 Captura automática de imágenes al detectar movimiento
- ⏱️ Marca de tiempo en cada captura
- 🖥️ Visualización en tiempo real de:
  - Feed de video original
  - Umbral de detección
  - Diferencia entre frames
- 💾 Almacenamiento automático de capturas en carpeta dedicada

## Requisitos Previos

- Python 3.6 o superior
- Webcam funcional
- Bibliotecas de Python:
  - OpenCV (`opencv-python`)
  - NumPy

## Instalación

1. Clona este repositorio:
```bash
git clone [URL-del-repositorio]
cd deteccion-movimiento
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate.ps1 para powershell y venv\Scripts\activate.bat para cmd
```

3. Instala las dependencias:
```bash
pip install opencv-python
```
Lo anterior instala numpy, en caso contrario, instalarlo manualmente

## Uso

1. Ejecuta el script:
```bash
python detector_movimiento.py
```

2. El sistema mostrará tres ventanas:
   - "Feed de video": Muestra la imagen de la webcam con rectángulos verdes donde se detecta movimiento
   - "Umbral": Muestra la imagen binarizada usada para la detección
   - "Diferencia de frames": Muestra la diferencia entre frames consecutivos

3. Para salir del programa:
   - Presiona 'q' en cualquier momento

## Configuración

El script incluye varios parámetros ajustables:

```python
# Frecuencia de captura (frames por segundo)
frame_interval = 1/4  # 4 FPS por defecto

# Umbral de detección
cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

# Tamaño mínimo del área de movimiento (en píxeles)
if cv2.contourArea(contour) < 500:  # Ajustable según necesidades

# Calidad de la imagen guardada
cv2.imwrite(filename, frame2, [cv2.IMWRITE_JPEG_QUALITY, 30])  # 30% de calidad
```

### Ajustes Recomendados

- Para más detecciones: Reduce `frame_interval` (e.g., 1/30 para 30 FPS)
- Para menos falsas detecciones: Aumenta el umbral de área mínima
- Para mejor calidad de imagen: Aumenta el valor de JPEG_QUALITY (hasta 100)
- Para menor uso de disco: Reduce JPEG_QUALITY

## Estructura de Archivos

```
/
├── detector_movimiento.py     # Script principal
├── img/                      # Carpeta para imágenes capturadas
│   └── movimiento_detectado_[TIMESTAMP].jpg
└── README.md                 # Este archivo
```

## Funcionamiento Técnico

1. **Inicialización**
   - Verifica la disponibilidad de la webcam
   - Crea la carpeta 'img' si no existe o verifica si el script tiene permisos para crear la carpeta
   - Captura frame inicial de referencia

2. **Proceso de Detección**
   - Convierte frames a escala de grises
   - Aplica desenfoque gaussiano para reducir ruido
   - Calcula diferencia absoluta entre frames
   - Aplica umbral y dilatación
   - Identifica contornos de movimiento

3. **Almacenamiento**
   - Guarda imágenes automáticamente al detectar movimiento
   - Nombra archivos con timestamp
   - Comprime imágenes para optimizar espacio

## Solución de Problemas

1. **No se detecta la webcam:**
   - Verifica que la webcam esté conectada
   - Prueba cambiando el índice de la cámara (0, 1, 2, etc.)
   - Puedes usar la función comentada del código 'listar_webcams', para mostrar las cámaras detectadas

2. **Detecciones falsas:**
   - Aumenta el umbral de área mínima
   - Ajusta el valor de threshold
   - Reduce la sensibilidad del detector

3. **Alto uso de disco:**
   - Reduce la calidad de imagen (JPEG_QUALITY)
   - Aumenta el intervalo entre frames
   - Implementa un límite de capturas por segundo

## Contribución

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/NuevaCaracteristica`)
3. Commit a tus cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia Apache2.0 - ver el archivo [LICENSE](LICENSE) para más detalles.

## Reconocimientos

- OpenCV por proporcionar las herramientas de visión por computadora
- La comunidad de Python por sus contribuciones y documentación
