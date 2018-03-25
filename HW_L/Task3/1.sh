#!/usr/bin/env bash

echo '
#!/usr/bin/env bash

time=$(cat /etc/mycron.cfg | sed -r '1!d' | sed  -r "s/#(.*)//" | sed -r "s/ //g")
time=$(( $time * 60 ))

command=$(cat /etc/mycron.cfg | sed -r "1d" | sed  -r "s/#(.*)//")

echo "#!/usr/bin/env bash

while true; do

$command

sleep $time

done
" > /var/mycrontmp.sh
' > /var/mycronscript.sh