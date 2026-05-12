#!/bin/bash
set -e

LAB_NAME="ac-midband-extract"

ensure_student_home() {
    install -d -m 0755 -o student -g student /home/student/.local /home/student/.local/bin /home/student/.local/result
    chown -R student:student "/home/student/${LAB_NAME}" /home/student/.local 2>/dev/null || true
    chmod +x "/home/student/${LAB_NAME}"/tools/*.py 2>/dev/null || true
}

if [ "$(id -u)" -eq 0 ]; then
    ensure_student_home
    exec /bin/su - student -c "cd /home/student/${LAB_NAME} && exec /bin/bash"
fi

mkdir -p /home/student/.local/bin /home/student/.local/result
chmod +x "/home/student/${LAB_NAME}"/tools/*.py 2>/dev/null || true
cd "/home/student/${LAB_NAME}" || exit 1
exec /bin/bash
