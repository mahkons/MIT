#!/usr/bin/env bash

echo "#!/bin/sh"
echo "exec tail -n +3 \$0"
echo "# This file provides an easy way to add custom menu entries.  Simply type the"
echo "# menu entries you want to add after this comment.  Be careful not to change"
echo "# the 'exec tail' line above."

echo "submenu 'Menu for openSUSE Leap 42.3 textmode' \$menuentry_id_option 'gnulinux-text' {"

for root in $(ls /boot | grep -E "^initrd-(.*)$" | sed -r 's/^initrd-(.*)$/\1/'); do
	name="openSUSE Leap 42.3 $root"
	cat /boot/grub2/grub.cfg | sed -rn '/### BEGIN \/etc\/grub.d\/10_linux ###/,/^}/p' | sed '1d' | sed 's/set gfxpayload=keep/set gfxpayload=text/' | 
	sed "s/openSUSE Leap 42.3/$name/" | sed '/echo/d' | sed -r "s|(/boot/vmlinuz-)([^ ]*)|\1$root|" | sed -r "s|(/boot/initrd-)([^\b]*)|\1$root|" | sed 's/ro .*/ro quiet 3/'
done 

echo "}"
echo ""