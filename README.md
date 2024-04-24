# Описание
Служба для автоматической очистки логов исполнительной среды MasterSCADA 4D *(на Linux)* **при проблеме отсутствия подключения к АРМ** среды исполнения MS4D из-за быстрого переполнения носителя с небольшим объёмом памяти.
> Для запуска необходим **Python 3.7+**


# Быстрая установка
1. **Скопируйте репозиторий** любым удобным для вас способом. Например:
    ```sh
    sudo git clone 'https://github.com/ss3nclam/mplc4_logs_cleaner.git' /tmp
    ```

2. *(необязательно)* **Настройте параметры в скрипте `cleaner.py` по своему усмотрению**:
    - ***MAX_LOGS_COUNT*** - максимальное количество логов в директории ***(по-умолчанию - 10)***
    - ***SLEEP_TIME*** - периодичность проверки директории в сек. ***(по-умолчанию - 3600)***

3. **Запустите установщик** из загруженного репозитория:
    ```sh
    sudo bash /tmp/mplc4_logs_cleaner/installer.sh
    ```

4. **Убедитесь в исправной работе службы**:
    - В директории `/opt/mplc4/log` должны появиться два новых файла `cleaner.py` и `cleaner_logs.txt`
    - В выводе команды `systemctl status mplclogscleaner` статус службы должен быть `activated`
    - Файл `cleaner_logs.txt` не должен быть пустым или содержать ошибок

5. **Убетитесь, что служба `mplc4` запущена и работает исправно**:
    ```sh
    systemctl status mplc4
    ```
    *Так же:*
    ```sh
    ps -e | grep mplc
    ```

6. *(необязательно)* **Удалите загруженный репозиторий**


# Ручная установка
1. **Измените права доступа для директории с логами**:
    ```sh
    sudo chmod 777 /opt/mplc4/log/
    ```

2. **Разрешите перезапуск службы без ввода пароля**, добавив строку `user ALL=(ALL) NOPASSWD: /bin/systemctl restart mplc4` в файл `/etc/sudoers`

3. **Загрузите репозиторий и скопируйте скрипт** `cleaner.py` в папку `/opt/mplc4/log`

4. **Настройте права доступа для скрипта**:
    ```sh
    sudo chmod +x /opt/mplc4/log/cleaner.py
    ```

5. **Создайте конфиг новой службы**:
    ```sh
    sudo touch /lib/systemd/system/mplclogscleaner.service
    ```

    Содержимое конфига должно иметь след. вид:
    ```ini
    [Unit]
    Description=mplclogscleaner

    [Service]
    ExecStart=/opt/mplc4/log/cleaner.py

    [Install]
    WantedBy=multi-user.target
    ```

6. **Перезагрузите демона служб**:
    ```sh
    sudo systemctl daemon-reload
    ```

8. **Разрешите старт службы при запуске системы**:
    ```sh
    sudo systemctl enable mplclogscleaner.service
    ```

9. **Запустите службу**:
    ```sh
    sudo systemctl start mplclogscleaner.service
    ```

10. **См. пункты 4-6** из раздела ***Быстрая установка***