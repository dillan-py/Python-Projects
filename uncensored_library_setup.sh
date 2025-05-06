#!/bin/bash
set -e

echo "=== Uncensored Library Setup for Raspberry Pi 5 ==="

# Update system
sudo apt update && sudo apt full-upgrade -y

# Install dependencies
sudo apt install -y cmake git build-essential openjdk-17-jdk flatpak wget unzip

# Install Box64
echo "=== Installing Box64 ==="
git clone https://github.com/ptitSeb/box64.git
cd box64
mkdir -p build && cd build
cmake .. -DRPI4=1 -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j$(nproc)
sudo make install
cd ../..
rm -rf box64

# Install Prism Launcher via Flatpak
echo "=== Installing Prism Launcher ==="
flatpak install -y flathub org.prismlauncher.PrismLauncher

# Run Prism Launcher (first time setup)
echo "You can now launch Prism Launcher with:"
echo "  flatpak run org.prismlauncher.PrismLauncher"

# Create Minecraft saves folder if not exist
mkdir -p ~/.minecraft/saves

# Download the Uncensored Library
echo "=== Downloading The Uncensored Library Map ==="
wget https://uncensoredlibrary.com/download/library-map.zip -O ~/library-map.zip
unzip ~/library-map.zip -d ~/.minecraft/saves/
rm ~/library-map.zip

echo "=== Setup Complete ==="
echo "1. Launch Prism Launcher: flatpak run org.prismlauncher.PrismLauncher"
echo "2. Log in, install Minecraft 1.14.4, and launch the map from Singleplayer."
echo "3. Enjoy The Uncensored Library!"









How to Use

    Save the script:

nano uncensored_library_setup.sh

Paste the script and save (CTRL+O, ENTER, CTRL+X)

Make it executable:

chmod +x uncensored_library_setup.sh

Run it:

./uncensored_library_setup.sh
