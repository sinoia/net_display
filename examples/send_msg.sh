hostname=$(hostname)
curl -X PUT -d "$*" http://${hostname}:8888/msg
