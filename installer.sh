#!/usr/bin/bash

chmod 777 /opt/mplc4/log/
echo $'\nroot ALL=(ALL) ALL\nuser ALL=(ALL) NOPASSWD: /bin/systemctl restart mplc4\n' >> /etc/sudoers
cp cleaner.py /opt/mplc4/log/cleaner.py
chmod +x /opt/mplc4/log/cleaner.py
echo $'[Unit]\nDescription=mplclogscleaner\n\n[Service]\nExecStart=/opt/mplc4/log/cleaner.py\n\n[Install]\nWantedBy=multi-user.target' >> /lib/systemd/system/mplclogscleaner.service
systemctl daemon-reload
systemctl enable mplclogscleaner.service
systemctl start mplclogscleaner.service
