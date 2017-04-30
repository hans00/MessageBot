#!/bin/sh

case "${1}" in
  start)
    printf "Starting messagebot... "
    LOG='main.log' /usr/bin/env python app.py & echo $! > main.pid
    if [ $? ]; then
      echo "OK"
    else
      echo "Faild"
    fi
  ;;
  stop)
    printf "Starting messagebot... "
    kill -9 $(cat main.pid)
    if [ $? ]; then
      echo "OK"
    else
      echo "Faild"
    fi
    rm main.pid
  ;;
  restart)
    $0 stop
    $0 start
  ;;
  *)
    echo "Usage:  {start|stop|restart}"
    exit 1
  ;;
esac

exit 0