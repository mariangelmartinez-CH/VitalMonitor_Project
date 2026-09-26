import numpy as np
import matplotlib.pyplot as plt

# Parametros de la simulacion
frecuencia_muestreo = 100      # muestras por segundo (Hz)
duracion_segundos = 10         # cuanto tiempo de senal generamos
frecuencia_cardiaca_bpm = 75   # pulsaciones por minuto

# Vector de tiempo: un punto cada 1/frecuencia_muestreo segundos
t = np.linspace(0, duracion_segundos, duracion_segundos * frecuencia_muestreo)

# Frecuencia cardiaca en Hz (latidos por segundo)
frecuencia_cardiaca_hz = frecuencia_cardiaca_bpm / 60

# Una onda PPG real no es una senoidal simple: sube rapido y baja lento.
# Se aproxima sumando el armonico principal con uno secundario mas debil.
onda_principal = np.sin(2 * np.pi * frecuencia_cardiaca_hz * t)
segundo_armonico = 0.3 * np.sin(2 * np.pi * frecuencia_cardiaca_hz * 2 * t + 0.5)
senal_limpia = onda_principal + segundo_armonico

# Ruido: ningun sensor real da una senal perfecta
ruido = np.random.normal(0, 0.05, size=t.shape)

# Deriva de la linea base, como si el dedo se moviera un poco
deriva = 0.1 * np.sin(2 * np.pi * 0.05 * t)

senal_ppg = senal_limpia + ruido + deriva

# Graficamos
plt.figure(figsize=(10, 4))
plt.plot(t, senal_ppg)
plt.title("Senal PPG simulada")
plt.xlabel("Tiempo (segundos)")
plt.ylabel("Amplitud")
plt.tight_layout()
plt.show()