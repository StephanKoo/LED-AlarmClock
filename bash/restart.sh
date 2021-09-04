#!/bin/bash
pid=$(ps aux | grep 'LedAlarmClock.py' | grep python | awk '{print $2}')
if [ -z "$pid" ]; then 
    echo ""
else
    kill $pid
    sleep 2
fi

echo Wird jetzt Uhr starten
python3 /home/pi/LED-AlarmClock/python/src/LedAlarmClock.py & > /home/pi/LedAlarmClock.log
                                                              # Die Umleitung funktioniert nicht,
                                                              # vielleicht macht python das nicht
echo Uhr gestartet
