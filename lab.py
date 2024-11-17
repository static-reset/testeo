import threading
import time
import random

# Lista para almacenar los registros de validación
registros_validacion = []
# Lista para almacenar las hebras que pasan la validación
hebras_validadas = []

# Definir la función de validación
def validar_jugador(id_jugador, semaforo, zona_validacion):
    tiempo_inicio = time.time()
    with semaforo:
        print(f"Jugador {id_jugador} entrando a la zona de validación {zona_validacion}")
        time.sleep(15)  # Simula la duración de la validación
        tiempo_fin = time.time()
        duracion = tiempo_fin - tiempo_inicio
        print(f"Jugador {id_jugador} completó la validación en la zona {zona_validacion}")
        # Agregar registro de validación
        registros_validacion.append((id_jugador, zona_validacion, duracion))
        # Agregar hebra validada a la lista
        hebras_validadas.append(id_jugador)

# Crear semáforos para las zonas de validación (capacidad de 32 jugadores cada una)
semaforo_zona1 = threading.Semaphore(32)
semaforo_zona2 = threading.Semaphore(32)

# Lista para almacenar las hebras
hebras = []

# Crear y arrancar las hebras
for i in range(256):
    zona_validacion = random.choice([1, 2])  # Asignar aleatoriamente una zona de validación
    semaforo = semaforo_zona1 if zona_validacion == 1 else semaforo_zona2
    hebra = threading.Thread(target=validar_jugador, args=(i, semaforo, zona_validacion))
    hebras.append(hebra)
    hebra.start()

# Esperar a que todas las hebras terminen
for hebra in hebras:
    hebra.join()

# Crear archivo de texto con los registros de validación
with open('Validacion.txt', 'w') as f:
    for registro in registros_validacion:
        f.write(f"Jugador {registro[0]} en zona {registro[1]}: {registro[2]:.2f} segundos\n")

print("Archivo Validacion.txt creado con éxito.")

# Fase de Eliminación Directa
def enfrentamiento(jugador1, jugador2, ronda, tipo):
    tiempo_inicio = time.time()
    print(f"Enfrentamiento: Jugador {jugador1} vs Jugador {jugador2}")
    time.sleep(10)  # Simula la duración del enfrentamiento
    ganador = random.choice([jugador1, jugador2])
    tiempo_fin = time.time()
    duracion = tiempo_fin - tiempo_inicio
    print(f"Ganador: Jugador {ganador}")
    # Crear archivo de texto para el enfrentamiento
    with open(f'{tipo}_Ronda{ronda}.txt', 'a') as f:
        f.write(f"Jugador {jugador1} vs Jugador {jugador2}: Ganador Jugador {ganador}, Tiempo {duracion:.2f} segundos\n")
    return ganador

# Listas para almacenar los ganadores y perdedores de cada ronda
ganadores = hebras_validadas
perdedores = []

ronda = 1
while len(ganadores) > 1:
    nuevos_ganadores = []
    nuevos_perdedores = []
    for i in range(0, len(ganadores), 2):
        if i + 1 < len(ganadores):
            ganador = enfrentamiento(ganadores[i], ganadores[i + 1], ronda, 'Ganadores')
            nuevos_ganadores.append(ganador)
            perdedor = ganadores[i] if ganador == ganadores[i + 1] else ganadores[i + 1]
            nuevos_perdedores.append(perdedor)
    ganadores = nuevos_ganadores
    perdedores.extend(nuevos_perdedores)
    ronda += 1

print("Fase de Eliminación Directa completada.")

# Fase de Repechaje
ronda_repechaje = 1
while len(perdedores) > 1:
    nuevos_ganadores_repechaje = []
    for i in range(0, len(perdedores), 2):
        if i + 1 < len(perdedores):
            ganador = enfrentamiento(perdedores[i], perdedores[i + 1], ronda_repechaje, 'Repechaje')
            nuevos_ganadores_repechaje.append(ganador)
    perdedores = nuevos_ganadores_repechaje
    ronda_repechaje += 1

print("Fase de Repechaje completada.")

# Enfrentamiento Final
ganador_eliminacion_directa = ganadores[0]
ganador_repechaje = perdedores[0]

def enfrentamiento_final(jugador1, jugador2):
    tiempo_inicio = time.time()
    print(f"Enfrentamiento Final: Jugador {jugador1} (Eliminación Directa) vs Jugador {jugador2} (Repechaje)")
    time.sleep(10)  # Simula la duración del enfrentamiento
    ganador = random.choice([jugador1, jugador2])
    tiempo_fin = time.time()
    duracion = tiempo_fin - tiempo_inicio
    print(f"Ganador Final: Jugador {ganador}")
    # Crear archivo de texto para el enfrentamiento final
    with open('Enfrentamiento_Final.txt', 'w') as f:
        f.write(f"Enfrentamiento Final: Jugador {jugador1} (Eliminación Directa) vs Jugador {jugador2} (Repechaje)\n")
        f.write(f"Ganador: Jugador {ganador}\n")
        f.write(f"Tiempo de finalización: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tiempo_fin))}\n")
    return ganador

ganador_final = enfrentamiento_final(ganador_eliminacion_directa, ganador_repechaje)

print("Torneo completado. Ganador final:", ganador_final)
