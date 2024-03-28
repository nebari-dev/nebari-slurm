#!/bin/bash

IFS=$'\n' # Split output into lines based on newline

# Use `ip address show` instead of `ip -br -4 address show` for broader compatibility
readarray -t lines <<< "$(ip -br -4 address show | grep UP)"
for line in "${lines[@]}"; do
  if [[ $line =~ (eth[0-9]|ens[0-9]+|enp[0-9].*) ]]; then
    INTERFACE=$(echo $line | awk '{print $1}')
    IP_RANGE=$(echo $line | awk '{print $3}')
    break
  fi
done

# Write variables into network_info.txt
echo "Interface: $INTERFACE" > network_info.txt
echo "IP Range: $IP_RANGE" >> network_info.txt
