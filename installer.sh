#!/usr/bin/bash

chmod 777 /opt/mplc4/log/
echo $'# For CLEANER_SERVICE_NAME\nroot ALL=(ALL) ALL\nuser ALL=(ALL) NOPASSWD: /bin/systemctl daemon-reload\nuser ALL=(ALL) NOPASSWD: /bin/systemctl * mplc4\nuser ALL=(ALL) NOPASSWD: /bin/systemctl * CLEANER_SERVICE_NAME' >> /etc/sudoers
# cp cleaner.py /opt/mplc4/log/cleaner.py
chmod +x /opt/mplc4/log/cleaner.py
echo $'[Unit]\nDescription=CLEANER_SERVICE_NAME\n\n[Service]\nExecStart=/opt/mplc4/log/cleaner.py\n\n[Install]\nWantedBy=multi-user.target' >> /lib/systemd/system/CLEANER_SERVICE_NAME.service
systemctl daemon-reload
systemctl enable CLEANER_SERVICE_NAME.service
systemctl start CLEANER_SERVICE_NAME.service
