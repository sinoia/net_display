hostname=$(hostname)
msg_text=${1}
curl http://${hostname}:8888/msg -XPUT -d '{"id": "message", "message": "'"${msg_text}"'"}'
