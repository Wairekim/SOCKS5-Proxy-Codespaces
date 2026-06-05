#!/bin/bash
set -e

sudo sed -i 's/^[[:space:]]*Port .*/Port 1080/' /etc/tinyproxy/tinyproxy.conf
sudo sed -i '/^[[:space:]]*Allow /d' /etc/tinyproxy/tinyproxy.conf
sudo sed -i '/^[[:space:]]*Deny /d' /etc/tinyproxy/tinyproxy.conf
sudo sed -i '/^[[:space:]]*ConnectPort /d' /etc/tinyproxy/tinyproxy.conf
echo 'Allow 0.0.0.0/0' | sudo tee -a /etc/tinyproxy/tinyproxy.conf
echo 'Allow ::/0' | sudo tee -a /etc/tinyproxy/tinyproxy.conf
echo 'DisableViaHeader Yes' | sudo tee -a /etc/tinyproxy/tinyproxy.conf

sudo tinyproxy
echo "Tinyproxy started on port 1080"
