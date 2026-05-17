#!/bin/bash

echo -e "\033[96m=================================================\033[0m"
echo -e "\033[92m  🚀 MENGINSTALL AUTONOMOUS AGENT (1-CLICK) 🚀\033[0m"
echo -e "\033[96m=================================================\033[0m"

echo -e "\n\033[93m[1/4] Mengupdate sistem dan menginstal dependensi dasar...\033[0m"
pkg update -y && pkg upgrade -y
pkg install python git nodejs termux-api -y

echo -e "\n\033[93m[2/4] Mengunduh Repositori dari GitHub...\033[0m"
rm -rf Autonomus-Agent
git clone https://github.com/keyfreshgmail-byte/Autonomus-Agent.git
cd Autonomus-Agent || exit

echo -e "\n\033[93m[3/4] Menginstal Library Python...\033[0m"
pip install --upgrade pip
pip install pyTelegramBotAPI requests beautifulsoup4

echo -e "\n\033[92m[4/4] Instalasi Selesai! Memulai Sistem...\033[0m"
sleep 2
clear

python bot.py