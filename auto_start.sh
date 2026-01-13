#!/bin/bash

# Экспорт переменных из .env
source .env

# Разрешаем редактирование файла настроек
sudo chmod 666 "$SETTINGS_FILE_PATH"

cd "$RC_API_PATH"
set -e
source "./remoteenv/bin/activate"
python -u main.py > main.log &

RC_API_PID=$!
echo "Remote Control API запущен, PID: $RC_API_PID"