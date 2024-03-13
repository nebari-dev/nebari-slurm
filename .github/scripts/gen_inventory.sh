#!/bin/bash

# Check if the correct number of arguments was provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <hostname> <output_path>"
    exit 1
fi

# Get the hostname from the first argument
HOSTNAME=$1

# Get the output path from the second argument
OUTPUT_PATH=$2

# Ensure the directory exists
mkdir -p $(dirname "$OUTPUT_PATH")

# Create the inventory.ini file at the specified output path with dynamic content
cat <<EOF > "$OUTPUT_PATH"
${HOSTNAME} connection=local ansible_ssh_host=127.0.0.1

[hpc_master]
${HOSTNAME}

[hpc_worker]
${HOSTNAME}
EOF

echo "inventory.ini file has been created at $OUTPUT_PATH."
