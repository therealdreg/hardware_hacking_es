#!/usr/bin/env python3

import serial
import time

# Aquí es importante establecer un timeout, ya que las lecturas del puerto serie las haremos con la función
# read_until. La gracia de usar este comando es que si le decimos read_until("AAA"), bloquerá la ejecución
# hasta que en el buffer aparezca "AAA". Como esto es peligroso (por magia divina, puede que nunca aparezca AAA),
# tenemos que establecer aquí un timeout para que, si no recibimos nada en 5 segundos, nos devuelva el control a
# nosotros y podamos tratarlo.
s = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, timeout=5)

# Cambiar modo
s.write(b"m\n") 
time.sleep(0.1)

# SPI
s.write(b"5\n")
time.sleep(0.1)

# 125kHz
s.write(b"2\n")
time.sleep(0.1)

# Clock: Idle low
s.write(b"1\n")
time.sleep(0.1)

# Clock: Active to idle
s.write(b"2\n")
time.sleep(0.1)

# Input sample phase: Middle
s.write(b"1\n")
time.sleep(0.1)

# CS: /CS
s.write(b"2\n")
time.sleep(0.1)

# Select output type: Normal
s.write(b"1\n")
time.sleep(0.1)

# Power supplies on
s.write(b"W\n")
time.sleep(0.1)

# Inicialización del modo SPI
s.write(b"]r:10[0x40 0x00 0x00 0x00 0x00 0x95 r:8]\n")
time.sleep(0.1)
s.write(b"[0x41 0x00 0x00 0x00 0x00 0xFF r:8]\n")
time.sleep(0.1)
s.write(b"[0x41 0x00 0x00 0x00 0x00 0xFF r:8]\n")
time.sleep(0.1)
s.write(b"[0x50 0x00 0x00 0x02 0x00 0xFF r:8]\n")
time.sleep(0.1)
s.reset_input_buffer()
s.reset_output_buffer()
# Archivo para volcar los bloques pares
f1 = open("even.bin", "wb")
# Archivo para volcar los bloques impares
f2 = open("odd.bin", "wb")
# Variables para ir controlando si es un bloque par o impar de manera intuitiva. Podríamos hacerlo dividiendo directamente
# i / 512, pero creo que así es más fácil de entender.
n = 0
# Aquí recorreríamos todas las direcciones de memoria del 0 a los 2GB.
# No obstante, sabemos (os lo digo yo) que la información se encuentra en los primeros 16MB, por lo que para que no sea infinito,
# no vamos a seguir leyendo.
# Como ya hemos visto, hemos establecido el tamaño de bloque en 512 bytes, por lo que las direcciones de memoria también las vamos
# recorriendo de 512 en 512.
for i in range(0, 16 * 1024 * 1024, 512):
    # Como los comandos reciben la direccion como argumento en 4 bytes diferentes, tenemos que trocear la dirección en 4. Es decir, para la dirección 0x01020304
    # Aqui obtenemos 0x01
    a4 = i >> 24 & 0xff
    # Aqui obtenemos 0x02
    a3 = i >> 16 & 0xff
    # Aqui obtenemos 0x03
    a2 = i >> 8 & 0xff
    # Y aqui obtenemos 0x04
    a1 = i & 0xff
    print(f"Reading {hex(a4)} {hex(a3)} {hex(a2)} {hex(a1)}...")
    # El bus pirate nos abstrae del formato en el que les pasamos los bytes. Es decir, le da igual que le pasemos 0x0F o 15, así que nos ahorramos usar la función hex()
    s.write(f"[0x51 {a4} {a3} {a2} {a1} 0xFF r:520]\n".encode())
    # Esperamos hasta que en el buffer aparezca SPI>, o lo que es lo mismo, que la tarjeta SD nos haya respondido y el bus pirate esté esperando a que le enviemos otro comando.
    response = s.read_until(b"SPI>")
    # Nos quedamos unicamente con la linea donde aparece los bytes que están escritos en el bloque, quitándole el READ: del principio.
    sector_bytes_str = response.decode().split("\n")[8].lstrip("READ: ").split()
    # Primero obtenemos la cabecera, desde el principio hasta que leemos 0xFE (los primeros 4 bytes siempre acaban en 0xFE)
    header_bytes = bytes([ int(x, 16) for x in sector_bytes_str[:sector_bytes_str.index("0xFE")+1] ])
    # Luego obtenemos la información del bloque, desde ese primer 0xFE que mencionamos antes, hasta los siguientes 512 bytes (recordemos que es el tamaño de bloque establecido).
    sector_bytes = bytes([ int(x, 16) for x in sector_bytes_str[sector_bytes_str.index("0xFE")+1:sector_bytes_str.index("0xFE")+512+1] ])
    # Si n es par, escribimos el bloque en el archivo even.bin
    if n % 2 == 0:
        f1.write(sector_bytes)
    # Si n es impar, escribimos el bloque en el archivo odd.bin
    else:
        f2.write(sector_bytes)
    # Por último, incrementamos n antes de vovler a iniciar el bucle.
    n += 1

