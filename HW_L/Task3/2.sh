#!/usr/bin/env bash

echo "bash /var/mycronscript.sh
bash /var/mycrontmp.sh
exit 0
" >> /etc/rc.d/after.local