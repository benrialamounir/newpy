#!/usr/bin/env bash
# newpy - Install script
# Run: curl -sSL https://raw.githubusercontent.com/benrialamounir/newpy/main/install.sh | bash
# Or:  chmod +x install.sh && ./install.sh

set -e

INSTALL_DIR="${HOME}/.local/bin"
SCRIPT_NAME="newpy"
REPO_URL="https://raw.githubusercontent.com/benrialamounir/newpy/main/newpy"

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download the script
echo "Downloading newpy..."
if command -v curl &> /dev/null; then
    curl -sSL "$REPO_URL" -o "${INSTALL_DIR}/${SCRIPT_NAME}"
elif command -v wget &> /dev/null; then
    wget -q "$REPO_URL" -O "${INSTALL_DIR}/${SCRIPT_NAME}"
else
    echo "Error: Neither curl nor wget found. Please install one of them."
    exit 1
fi

# Make it executable
chmod +x "${INSTALL_DIR}/${SCRIPT_NAME}"

echo ""
echo "newpy installed successfully!"
echo ""
echo "Make sure ${INSTALL_DIR} is in your PATH."
echo "You can add this to your ~/.bashrc or ~/.zshrc:"
echo ""
echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
echo ""
echo "Then run: newpy"