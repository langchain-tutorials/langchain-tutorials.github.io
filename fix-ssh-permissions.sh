#!/bin/bash

echo "🔒 Fixing SSH permissions..."

# Fix .ssh directory
chmod 700 ~/.ssh
echo "✅ Fixed .ssh directory permissions (700)"

# Fix all private keys
chmod 600 ~/.ssh/id_ed25519_* 2>/dev/null
echo "✅ Fixed private key permissions (600)"

# Fix all public keys
chmod 644 ~/.ssh/id_ed25519_*.pub 2>/dev/null
echo "✅ Fixed public key permissions (644)"

# Fix SSH config
if [ -f ~/.ssh/config ]; then
    chmod 600 ~/.ssh/config
    echo "✅ Fixed config file permissions (600)"
fi

# Fix known_hosts
if [ -f ~/.ssh/known_hosts ]; then
    chmod 644 ~/.ssh/known_hosts
    echo "✅ Fixed known_hosts permissions (644)"
fi

echo ""
echo "📋 Current SSH permissions:"
ls -la ~/.ssh/

echo ""
echo "✅ All SSH permissions fixed!"