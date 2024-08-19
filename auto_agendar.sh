#!/bin/bash

if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
fi

PYTHON_SCRIPT="./agendar.py"
DATA_AMANHA=$(date -d "tomorrow" +"%d/%m/%Y")
LOG_FILE="./output.log"

{
    echo -n "[$(date +'%d/%m/%Y %H:%M:%S')] (Almoço) "
    python3 "$PYTHON_SCRIPT" "$USERNAME" "$PASSWORD" "$DATA_AMANHA" "2" >> "$LOG_FILE" 2>&1
    echo >> "$LOG_FILE"
    echo -n "[$(date +'%d/%m/%Y %H:%M:%S')] (Jantar) "
    python3 "$PYTHON_SCRIPT" "$USERNAME" "$PASSWORD" "$DATA_AMANHA" "3" >> "$LOG_FILE" 2>&1
} >> "$LOG_FILE" 2>&1

echo >> "$LOG_FILE"

