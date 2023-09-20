#!/bin/ash 

# Directorio de origen
src_dir="/dev"

# Directorio de destino
dest_dir="/var"

# Dirección IP del servidor TFTP
tftp_server="192.168.0.100"

i=0

# Bucle para copiar y enviar los archivos
while [ "$i" -lt 7 ]; do
    src_file="$src_dir/mtdblock$i"
    dest_file="$dest_dir/mtdblock$i"
    
    # Copiar el archivo
    cp "$src_file" "$dest_file"
    
    # Enviar el archivo por TFTP
    tftp -p -r "mtdblock$i" -l "$dest_file" "$tftp_server"
    
    echo "Archivo mtdblock$i copiado y enviado por TFTP"

    rm "$dest_file"

    echo "Archivo mtdblock$i eliminado de /var"

    i=$((i+1))
done

i=0

while [ "$i" -lt 7 ]; do
    src_file="$src_dir/mtd$i"
    dest_file="$dest_dir/mtd$i"
    
    # Copiar el archivo
    cp "$src_file" "$dest_file"
    
    # Enviar el archivo por TFTP
    tftp -p -r "mtd$i" -l "$dest_file" "$tftp_server"
    
    echo "Archivo mtd$i copiado y enviado por TFTP"

    rm "$dest_file"

    echo "Archivo mtd$i eliminado de /var"

    i=$((i+1))
done

tftp -p -r "mtd" -l "/proc/mtd" "$tftp_server"

echo "Proceso completado"
