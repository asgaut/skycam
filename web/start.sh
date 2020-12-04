#!/usr/bin/env bash

while [[ true ]]; do
  # wait 1 minute before checking for IP address
  sleep 60
  # do wlan0 have an IP?
  ip -f inet addr show wlan0 | grep "inet [0-9]*\.[0-9]*\.[0-9]*\.[0-9]*"
  if [ $? -eq 0 ]; then
    printf 'wlan0 have an IP address\n'
    # is it the wifi-connect address?
    ip -f inet addr show wlan0 | grep 192.168.42.1
    if [ $? -ne 0 ]; then
      printf 'wlan0 is not running wifi-connect\n'
      break
    fi
  fi
done
printf 'Starting nginx\n'
nginx -g "daemon off;"