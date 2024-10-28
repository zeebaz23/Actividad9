from typing import Tuple


class DatosMeteorologicos:
    direcciones = {
        'N': 0,
        'NNE': 22.5,
        'NE': 45,
        'ENE': 67.5,
        'E': 90,
        'ESE': 112.5,
        'SE': 135,
        'SSE': 157.5,
        'S': 180,
        'SSW': 202.5,
        'SW': 225,
        'WSW': 247.5,
        'W': 270,
        'WNW': 292.5,
        'NW': 315,
        'NNW': 337.5,
    }

    def __init__(self, nombre_archivo: str):
        self.nombre_archivo = nombre_archivo

    def procesar_datos(self) -> Tuple[float, float, float, float, str]:
        temperatura_total = 0
        humedad_total = 0
        presion_total = 0
        velocidad_viento_total = 0
        cantidad_registros = 0
        direcciones_viento = []

        with open(self.nombre_archivo, 'r') as archivo:
            for linea in archivo:
                if 'Estacion' in linea:
                    cantidad_registros += 1
                    for _ in range(8):
                        linea = next(archivo)
                        if 'Temperatura' in linea:
                            temperatura = float(linea.split(': ')[1].strip())
                            temperatura_total += temperatura
                        elif 'Humedad' in linea:
                            humedad = float(linea.split(': ')[1].strip())
                            humedad_total += humedad
                        elif 'Presion' in linea:
                            presion = float(linea.split(': ')[1].strip())
                            presion_total += presion
                        elif 'Viento' in linea:
                            viento_info = linea.split(': ')[1].strip().split(',')
                            velocidad_viento = float(viento_info[0])
                            direccion_viento = viento_info[1]
                            velocidad_viento_total += velocidad_viento
                            if direccion_viento in self.direcciones:
                                direcciones_viento.append(self.direcciones[direccion_viento])

        # Cálculo de promedios
        temperatura_promedio = temperatura_total / cantidad_registros
        humedad_promedio = humedad_total / cantidad_registros
        presion_promedio = presion_total / cantidad_registros
        velocidad_viento_promedio = velocidad_viento_total / cantidad_registros

        # Cálculo de dirección predominante
        if direcciones_viento:
            direccion_promedio_grados = sum(direcciones_viento) / len(direcciones_viento)
            direccion_promedio = self.convertir_a_direccion(direccion_promedio_grados)
        else:
            direccion_promedio = "Desconocida"

        return (temperatura_promedio, humedad_promedio, presion_promedio, velocidad_viento_promedio, direccion_promedio)

    def convertir_a_direccion(self, grados: float) -> str:
        grados = grados % 360
        direccion_mas_cercana = None
        diferencia_minima = float('inf')

        for direccion, grado in self.direcciones.items():
            diferencia = abs(grado - grados)
            # Asegura que la diferencia sea mínima
            if diferencia < diferencia_minima:
                diferencia_minima = diferencia
                direccion_mas_cercana = direccion

        return direccion_mas_cercana



datos = DatosMeteorologicos('datos.txt')
resultados = datos.procesar_datos()
print(f'Temperatura Promedio: {resultados[0]:.2f} °C')
print(f'Humedad Promedio: {resultados[1]:.2f} %')
print(f'Presión Promedio: {resultados[2]:.2f} hPa')
print(f'Velocidad Promedio del Viento: {resultados[3]:.2f} m/s')
print(f'Dirección Predominante del Viento: {resultados[4]}')
