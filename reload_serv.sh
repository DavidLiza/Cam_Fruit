#!/usr/bin/env bash

# This Script is used to manage the Eye service,
# in order to check status , enable it 
# or take differnent actions and decisions about it


while :
do
    echo "***** SELECT THE OPTION ****"
    echo "1. Start Service "
    echo "2. Stop Service"
    echo "3. Check status"
    echo "4. Restart (Stop it and Start it)"
    echo "5. Reload Configuration File"
    echo "6. Conf Service to start on Boot"
    echo "7. Avoid Service to start on Boot"
    echo "8. Deamon Reload"
    echo "9. Exit"

    seleccion=0
    read seleccion

    case $seleccion in
    1)
        echo "$seleccion Seleccionado (sudo systemctl start frubana.service) "
        sudo systemctl start frubana.service
        echo "Process Done"
        ;;
    2)
        echo "$seleccion Seleccionado (sudo systemctl stop frubana.service)"
        sudo systemctl stop frubana.service
        echo "Process Done"
        ;;
    3)
        echo "$seleccion Seleccionado (sudo systemctl status frubana.service)"
        sudo systemctl status frubana.service
        ;;
    4)
        echo "$seleccion Seleccionado (sudo systemctl restart frubana.service)"
        sudo systemctl restart frubana.service
        ;;
    5)
        echo "$seleccion Seleccionado (sudo systemctl reload frubana.service)"
        sudo systemctl reload frubana.service
        ;;
    6)
        echo "$seleccion Seleccionado (sudo systemctl enable frubana.service)"
        sudo systemctl enable frubana.service
        ;;
    7)
        echo "$seleccion Seleccionado (sudo systemctl disable frubana.service)"
        sudo systemctl disable frubana.service
        ;;
    8)
        echo "$seleccion Seleccionado DEAMON (sudo systemctl daemon-reload)"
        sudo systemctl daemon-reload
        ;;
    9)
        echo "$seleccion Exit"
        break
        ;;
    esac

    echo "Hit Enter to continue"
    read 
    clear
done 

echo "Exit Programm : Hit Enter to continue"
read 
clear 