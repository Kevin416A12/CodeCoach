#!/bin/bash

echo "Limpiando compilaciones anteriores..."
rm -rf build

echo "Creando carpeta de compilación..."
mkdir build && cd build

echo "Ejecutando CMake..."
cmake .. -DCMAKE_BUILD_TYPE=Debug

echo "Compilando con todos los núcleos disponibles..."
make -j$(nproc)

if [ $? -eq 0 ]; then
    echo " Compilación exitosa. Ejecutando servidor..."
    ./CodeCoachAPI
else
    echo " Error de compilación. Revisar los mensajes arriba."
fi
