#!/bin/bash

# Check if an IP address is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <IP_ADDRESS>"
    exit 1
fi

# Ping the target and extract TTL value
TTL=$(ping -c 1 "$1" | grep -oP 'ttl=\K\d+')

# Determine OS based on TTL value
if [ -n "$TTL" ]; then
    if [ "$TTL" -ge 100 ] && [ "$TTL" -le 128 ]; then
        echo "Likely Windows OS (TTL: $TTL)"
    elif [ "$TTL" -ge 50 ] && [ "$TTL" -le 64 ]; then
        echo "Likely Linux OS (TTL: $TTL)"
    else
        echo "Unknown OS (TTL: $TTL)"
    fi
else
    echo "Failed to retrieve TTL. Target may be unreachable."
fi
