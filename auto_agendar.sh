#!/bin/bash

# Edite esses campos
USERNAME="username_sigaa"
PASSWORD="password_sigaa"

PYTHON_SCRIPT="/home/pedro/git-workspace/agendar_ru/agendar.py"
DATA_AMANHA=$(date -d "tomorrow" +"%d/%m/%Y")
LOG_FILE="/home/pedro/git-workspace/agendar_ru/output.log"

echo -n "[$(date +'%d/%m/%Y %H:%M:%S')] " >> "$LOG_FILE"
python3 "$PYTHON_SCRIPT" "$USERNAME" "$PASSWORD" "$DATA_AMANHA" "2" >> "$LOG_FILE" 2>&1
echo -n "[$(date +'%d/%m/%Y %H:%M:%S')] " >> "$LOG_FILE"
python3 "$PYTHON_SCRIPT" "$USERNAME" "$PASSWORD" "$DATA_AMANHA" "3" >> "$LOG_FILE" 2>&1
