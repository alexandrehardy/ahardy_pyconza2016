#!/bin/sh

for i in `seq 1 100`; do
    curl http://127.0.0.1:8080 1>/dev/null 2>&1 &
done
