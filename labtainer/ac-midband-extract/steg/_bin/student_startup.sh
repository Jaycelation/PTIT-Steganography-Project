#!/bin/bash
LAB_NAME="ac-midband-extract"

if [ "$(id -u)" -eq 0 ]; then
    exec /bin/su - student -c "cd /home/student/${LAB_NAME} && exec /bin/bash"
fi

cd "/home/student/${LAB_NAME}" || exit 1
exec /bin/bash
