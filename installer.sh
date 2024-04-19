#!/usr/bin/bash

chmod 777 /opt/mlpc4/log/
echo $'\nuser ALL=(ALL) NOPASSWD: /bin/systemctl restart mplc4' >> /etc/sudoers
cp cleaner.py /opt/mlpc4/log/cleaner.py
chmod +x /opt/mlpc4/log/cleaner.py
echo $'[Unit]\nDescription=mplclogscleaner\n\n[Service]\nExecStart=/opt/mplc4/log/cleaner.py\n\n[Install]\nWantedBy=multi-user.target' >> /lib/systemd/system/mplclogscleaner.service
systemctl daemon-reload
systemctl enable mplclogscleaner.service
systemctl start mplclogscleaner.service
