## Удаленное управление настройками [krakensdr_doa](https://github.com/krakenrf/krakensdr_doa)
В связи с тем, что встроенная функция удаленного управления не работает корректно, было написано это простое API.

API принимает и возвращает json-словарь с настройками kraken `_share/settings.json` - [пример файла]((https://gist.github.com/farsett/ee28254da45d572ae60d525ae4e26a8e)).

### Установка
Предполагается, что уже установлен [krakensdr_doa](https://github.com/krakenrf/krakensdr_doa)

1. Перейдите в рабочую директорию и склонируйте репозиторий
    ```
    git clone https://github.com/farsett/kraken_remote.git
    ```
2. Создайте виртуальное окружение `remoteenv`
   ```
   cd kraken_remote
   python3 -m venv remoteenv
   ```
3. Установите необходимые библиотеки
   ```
   source /remoteenv/bin/activate
   pip install fastapi uvicorn
   ```
4. На основе файла `.envexample` создайте файл `.env`
   - SETTINGS_FILE_PATH - путь к файлу настроек krakensdr_doa
   - RC_API_PATH - путь к файлам в директории API
   - RC_HOST - адрес хоста API (по умолчанию доступен на всех адресах)
   - RC_PORT - порт (по умолчанию `8833`)
5. Сделайте `auto_start.sh` исполняемым и проверьте работоспособность
   ```
   sudo chmod +x auto_start.sh
   ./auto_start.sh
   ```
6. Добавьте cron-задачу на автозапуск
   ```
   sudo crontab -e
   ```
   добавив в конце
    ```
   @reboot /путь/к/auto_start.sh
   ```
   
    ...либо создайте сервис