port=8888
display_title = 'Network Display'
example_curl_cmd = 'curl -X PUT -d "Hello World" http://{0}:{1}/message'
display_content = '''<p>You network display is running and ready to
                   receive messages.</p><p>Try:</p><p>{0}</p>
                   <p>to see the message on this screen.</p>'''.format(example_curl_cmd)
