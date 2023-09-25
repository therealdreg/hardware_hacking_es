# Hardware Hacking ES Comunidad

- Discord: https://discord.gg/wkWr6Dj46D 
- Telegram: https://t.me/hardwarehackinges

---

# Hacking EEPROM AT24C256 I2C 5V

### Material Requerido:

- [BusPiratev3](https://www.adafruit.com/product/237)
- [EEPROM AT24C256 I2C 5V](https://es.aliexpress.com/item/4000099529430.html?spm=a2g0o.productlist.main.1.2bd56c2cd7dFX0&algo_pvid=a2da1f90-95d1-4099-8463-9e25238687ec)
- [Pinzas BusPirate](https://www.adafruit.com/product/238)

## Paso 1: Conectar pinzas a EEPROM

Usamos este esquema para conectarnos:

![](Pasted%20image%2020230921184311.png)
schema by David Sánchez 

Tiene que quedar asi:

![](photo_5793917552844455218_y.jpg)

---
## Paso 2: Conectarse al I2C con BusPirate

Ahora nos conectaremos usando algun software como TeraTerm o Putty, en mi caso usare TeraTerm.

1. Lo abrimos y seleccionamos la interfaz COM correspondiente del BusPirate

![](assets/Pasted-image-20230916160959.png)

2. Ahora configuramos la interfaz serial dentro de Setup->Serial Port

![](assets/Pasted-image-20230916161256.png)

3. Y lo dejamos con esta configuracion de 115200 baudios de velocidad, 8 bits de datos, ninguno de paridad y uno de stop. 

![](assets/Pasted-image-20230916161412.png)

4. Ahora para no quedarnos ciegos vamos a la configuración de fuente y aumentamos el tamaño y lo dejamos en 14.

![](assets/Pasted-image-20230916161528.png)

![](assets/Pasted-image-20230916161613.png)

5. Abrimos el menu del buspirate presionando m+enter

![](Pasted%20image%2020230921191417.png)
6. Presionamos el 4 y damos enter, dos veces

![](Pasted%20image%2020230921191520.png)

Presionamos W mayúscula y P mayúscula y ya podriamos leer la memoria y escribir

![](Pasted%20image%2020230921191747.png)

---

## Paso 3:  Localizar direcciones I2C

Usamos la macro de búsqueda de direcciones de 7bit para obtener la dirección de escritura y de lectura.

Escribimos (1) y damos a enter

![](Pasted%20image%2020230923185623.png)

## Paso 4:  Como leer y escribir con I2C

#### Como escribir I2C

Con los corchetes indicamos el principio y el final de cada comando I2C.

![](i2c-escribir.png)

El primer byte en hexadecimal es la dirección que indica si escribimos o leemos.

Los dos siguientes bytes son la direccion donde se va a escribir. 

Los bytes 0x41 0x41 0x41 son el contenido que se escribira en la dirección selecionada de manera consecutiva.

#### Como leer I2C

Para leer una dirección tenemos que usar la direccion de escritura de la eeprom.

Hay que escribir la direccion para luego poder leer el contenido aunque no sobreescribamos nada.

Se sigue el mismo patrón que escribiendo pero sin Bytes de contenido.

```i2c
[0xA0 0x00 0x69]
```

Después de seleccionar la direccion 0x69 escribimos el byte de lectura y una r para leer un byte, en el caso que queramos leer varios bytes escribimos 'r:(numero de veces)' para que sea una lectura secuencial.

```i2c
[0xa1 r:20]
```

---

Tenemos flasheado el CTF de Dreg, para leer la flag de la EEPROM introducimos estos comandos:

```bash
[0xA0 0x00 0x69]

[0xa1 r:20]
```

![](Pasted%20image%2020230921193046.png)

Para saber mas sobre el protocolo I2C con el bus pirate lee [esto.](http://dangerousprototypes.com/blog/bus-pirate-manual/i2c-guide/)

Usamos un conversor de [hexadecimal](https://gchq.github.io/CyberChef/) y obtenemos este resultado.

![](Pasted%20image%2020230921193712.png)

---
# Hacking Router TP-Link TL-WR841N

### Material Requerido:

- TP-Link TL-WR841N 
- Soldador Estaño
- FLux 
- USB a TTL o Buspirate
- Multimetro
- Cable Ethernet o Wifi
- Pines para UART
- Ordenador

## Paso 1: Comprar el router.

El modelo que vamos a analizar es el [TP-Link TL-WR841N V14 ](https://www.amazon.es/dp/B001FWYGJS?ref=ppx_yo2ov_dt_b_product_details&th=1)


---
## Paso 2: Abriendo el router.

Lo primero que debemos hacer es quitar los dos tornillos que hay en la parte inferior y después haremos palanca con algún trozo de plástico, yo he usado una púa de guitarra.

![](assets/photo_5775957412656824276_y.jpg)

![](assets/photo_5775957412656824277_y.jpg)


![](assets/photo_5775957412656824275_y.jpg)

Y ya tendríamos acceso directo a la PCB del router.

---

## Paso 3: Identificar componentes y UART.

Una vez abierto el router hay que identificar todos los componentes posibles.

![](assets/photo_5773698350053441531_y_1.jpg)

#### Cada circulo es una parte interesante de la pcb para nosotros:

- Circulo Rojo: Es la memoria RAM. Mirando la [ficha técnica](https://openwrt.org/toh/tp-link/tl-wr841nd) de la Versión 14 en OpenWRT podemos ver que tiene 32 MiB.   

![](assets/photo_5773698350053441532_y.jpg)

- Circulo Amarillo: Es el SOC (System-On-Chip) MT7628NN.

![](assets/photo_5773698350053441538_y.jpg)

- Circulo Azul: Es la memoria flash EN25Q32(A/B). Aquí es donde se guarda el bootloader y el sistema de archivos etc.

![](assets/photo_5773698350053441528_y.jpg)

- Circulo Rosa: Es la Interfaz UART que usaremos para obtener terminal de root y obtener el sistema de archivos. La resistencia **R18** bloquea la escritura UART, luego habrá que quitarla. 
 
![](assets/photo_5773698350053441535_y.jpg)

---
## Paso 4: Soldar pines a UART y ELIMINAR R18.

Soldar pines a UART no es complicado simplemente necesitaremos:

- [Soldador de estaño](https://www.amazon.es/Profesional-Temperatura-Ajustable-Desoldadora-Antiest%C3%A1ticas/dp/B09B3GRVTM/ref=sr_1_2_sspa?keywords=soldador+esta%C3%B1o&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)
- [Estaño](https://www.electronicaembajadores.com/es/Productos/Detalle/HRJ1121/herramienta/accesorios-y-consumibles-de-soldadura/mbo-soldadura-de-estano-60-sn-40-pb-0-5-mm-250-g-121103) a poder ser de calidad (se notan mucho los acabados.)
- [Pines](https://www.amazon.es/ANGEEK-Single-Breakable-Connector-Arduino/dp/B07XXXNH9V/ref=sr_1_5?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=Pines+pcb&sr=8-5)

![](assets/photo_5775957412656824287_y.jpg)

Aqui vemos como se ha eliminado la **R18** que impide la escritura a través de UART y los pines listos para conectarnos. En este caso hemos conectado el RX, el TX y el GND. El VCC no es necesario porque la alimentación la daremos usando el adaptador de corriente del router.

![](assets/Pasted-image-20230916142036.png)

---

## Paso 5: Conectarse al UART.

### Usando USB-to-TTL

![](assets/photo_5778209212470510367_y.jpg)

Aqui podemos ver como he conectado todos los pines desde el USB_UART-to-TTL, una cosa IMPORTANTE es que para que funcione la escritura necesitamos que el cable de datos TX vaya a 5V, porque si lo ponemos a 3,3V no funcionara correctamente.

Ahora para conectarnos correctamente lo primero es entender el protocolo [SERIAL](https://learn.sparkfun.com/tutorials/serial-communication) ,lo mas importante es que el pin RX del adaptador TTL-USB tiene que ir al TX del router y el TX del adaptador TTL-USB al RX del router además de conectar los dos GNDs. 

![](UART.png)

![](assets/photo_5778209212470510371_y.jpg)

Ahora nos conectaremos usando algun software como TeraTerm o Putty, en mi caso usare TeraTerm.

1. Lo abrimos y seleccionamos la interfaz COM correspondiente del TTL-USB

![](assets/Pasted-image-20230916160959.png)

2. Ahora configuramos la interfaz serial dentro de Setup->Serial Port

![](assets/Pasted-image-20230916161256.png)

3. Y lo dejamos con esta configuracion de 115200 baudios de velocidad, 8 bits de datos, ninguno de paridad y uno de stop. 

![](assets/Pasted-image-20230916161412.png)

4. Ahora para no quedarnos ciegos vamos a la configuración de fuente y aumentamos el tamaño y lo dejamos en 14.

![](assets/Pasted-image-20230916161528.png)

![](assets/Pasted-image-20230916161613.png)

5. Tras esto enchufamos el router a la corriente y veremos el bootloader cargando.

![](assets/Pasted-image-20230916162016.png)

![](assets/Pasted-image-20230916162303.png)

Tras esto ya podemos escribir comandos pero antes vamos a ver como se haría con el bus pirate.

### Usando Bus Pirate

Ahora explicaremos paso a paso con el bus pirate:

![](assets/photo_5778209212470510384_y.jpg)

La configuración del emulador de terminal es la misma que en el USB-to-TTL ahora lo importante es como conectemos los cables, aqui tenemos un esquema de que es cada color:

![](assets/Pasted-image-20230916163947.png)

1.  Ahora debemos conectar el MOSI(GRIS) al RX y el MISO(NEGRO) al TX, el GND(MARRON) al GND del router además de conectar el VPU(VERDE) al 5V(NARANJA) del propio bus pirate

![](assets/photo_5778209212470510399_y.jpg)
   
2. Lo siguiente es conectarse usando TeraTerm y con la misma configuración de antes e interactuar con el menu del bus pirate.


Escribimos 'm' y pulsamos intro

![](assets/Pasted-image-20230916172055.png)

Elegimos el modo 3 (UART)

![](assets/Pasted-image-20230916172117.png)

Pulsamos enter 4 veces para elegir todo por defecto es decir: Sin bit de paridad, 1 bit de parada , y con el colector abierto (Open Drain) para meterle por VPU esos 5V que necesita.

![](assets/Pasted-image-20230916172153.png)

Pulsamos 'W' mayúscula para dar corriente, pulsamos 'P' mayúscula para activar las resistencias pull-up y solo nos falta activar el live monitor para recibir la shell de UART. 

![](assets/Pasted-image-20230916172445.png)

Esto lo haremos usando la macro (1) que es el Transparent bridge aunque si ponemos (0) nos saldra la lista de macros.

![](assets/Pasted-image-20230916172600.png)

Ahora conectamos el router a la corriente y obtendremos shell.

![](assets/Pasted-image-20230916172742.png)

--- 

## Paso 6: Extraer Sistema de archivos y Firmware

Lo primero que haremos para extraer el sistema de archivos es instalar un servidor [TFTP](https://bitbucket.org/phjounin/tftpd64/downloads/) (Trivial FIle Transfer Protocol), en mi caso instale la version [Tftpd64-4.62-setup.exe](https://bitbucket.org/phjounin/tftpd64/downloads/Tftpd64-4.62-setup.exe) una vez instalada hay que abrirlo y dejar la configuración de esta manera:

![](assets/Pasted-image-20230916173638.png)

![](assets/Pasted-image-20230916173656.png)

![](assets/Pasted-image-20230916174518.png)

Tras configurarlo nos conectamos al router por wifi o por cable y revisamos que ip nos ha dado:

![](assets/Pasted-image-20230916174805.png)

Con esto ya sabemos que desde el terminal del router tenemos transferir por TFTP a 192.168.0.100 

Para comprobar que estamos conectados al router por red introducimos la puerta de enlace en el navegador:

![](assets/Pasted-image-20230916175017.png)

Una vez conectados es el momento de extraer el sistema de archivos y el firmware completo.

Tenemos una terminal muy limitada, para tener mas herramientas  hay que subir una copia de [busybox-mipsel.](https://busybox.net/downloads/binaries/1.21.1/busybox-mipsel)
### Obtención de la flash via MTD

Este router utiliza el subsistema MTD, que se divide en bloques. Concatenamos todos los bloques en orden para obtener el contenido de la flash, para más información de [MTD.](http://linux-mtd.infradead.org/doc/general.html) 

Los bloques se encuentran en el directorio /dev y empiezan por la palabra mtd:

![](assets/Pasted-image-20230916181059.png)

Copiamos todos los archivos de mtd con el script [transfer.sh](assets/transfer.sh).

--- 

## Paso 7: Extraccion del Firmware

Metemos los archivos en kali y los concatenamos siguiendo estos comandos:

```bash
cat mtdblock0 > firmware

cat mtdblock1 >> firmware

cat mtdblock2 >> firmware

cat mtdblock3 >> firmware

cat mtdblock4 >> firmware
```

Descomprimimos y extraemos con binwalk para después poder analizarlo:

```bash
binwalk -eM firmware
```

![](assets/Pasted-image-20230919180023.png)
![](assets/Pasted-image-20230919180039.png)


### U-boot

![](Pasted%20image%2020230922230512.png)

![](Pasted%20image%2020230923011106.png)

![](Pasted%20image%2020230923011114.png)


![](Pasted%20image%2020230923011301.png)

