#!/bin/bash

# Obtém o diretório atual do script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navega para o diretório atual
cd "$DIR"

# Executa o arquivo Python3
python3 mainDash.py
done
