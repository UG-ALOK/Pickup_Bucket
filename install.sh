
#!/data/data/com.termux/files/usr/bin/bash

set -e

RED='\033[1;31m'
GOLD='\033[1;33m'
WHITE='\033[1;37m'
GREEN='\033[1;32m'
RESET='\033[0m'

PROJECT_NAME="PICKUP BUCKET"
MAIN_FILE="pickup_bucket.py"

clear

echo -e "${GOLD}"
echo "=========================================="
echo "           PICKUP BUCKET"
echo "       Termux Project Installer"
echo "=========================================="
echo -e "${RESET}"
echo -e "${WHITE}Developer: Firewall-Crusher${RESET}"
echo

if [ -z "${PREFIX:-}" ] || [ ! -d "$PREFIX" ]; then
    echo -e "${RED}[ERROR] This installer is intended for Termux.${RESET}"
    echo "Open Termux and run this installer there."
    exit 1
fi

if [ ! -f "$MAIN_FILE" ]; then
    echo -e "${RED}[ERROR] $MAIN_FILE was not found.${RESET}"
    echo "Place install.sh beside $MAIN_FILE and run it again."
    exit 1
fi

echo -e "${GOLD}[1/4] Updating package information...${RESET}"
pkg update -y

echo -e "${GOLD}[2/4] Installing dependencies...${RESET}"
pkg install -y python nano

echo -e "${GOLD}[3/4] Installing Python package...${RESET}"
python -m pip install requests

echo -e "${GOLD}[4/4] Preparing project...${RESET}"
chmod +x "$MAIN_FILE"

mkdir -p pickup_bucket_reports

echo
echo -e "${GREEN}Installation completed successfully!${RESET}"
echo -e "${WHITE}Start the program with:${RESET}"
echo -e "${GOLD}python $MAIN_FILE${RESET}"
echo
echo -e "${WHITE}Reports directory:${RESET}"
echo "pickup_bucket_reports/"
echo
