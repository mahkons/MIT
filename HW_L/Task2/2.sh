#!/usr/bin/env bash

bash 1.sh > /etc/grub.d/40_custom

grub2-mkconfig -o /boot/grub2/grub.cfg