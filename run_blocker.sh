echo "========================================"
echo "   Website Blocker (Mini Firewall)"
echo "========================================"
echo

if [ "$EUID" -eq 0 ]; then
    echo "[INFO] Running with root privileges"
    echo
    echo "Starting Website Blocker..."
    echo
    python3 website_blocker.py
else
    echo "[ERROR] This script requires root privileges!"
    echo
    echo "To run with root privileges:"
    echo "1. Open terminal"
    echo "2. Navigate to this directory"
    echo "3. Run: sudo ./run_blocker.sh"
    echo
    echo "OR"
    echo
    echo "1. Open terminal"
    echo "2. Navigate to this directory"
    echo "3. Run: sudo python3 website_blocker.py"
    echo
    read -p "Press Enter to exit..."
fi
