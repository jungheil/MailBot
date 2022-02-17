from flask import Flask
from flask import request
from MailBot import MailBot
import os

app = Flask(__name__)

smtp_host = os.environ["SMTP_HOST"]
smtp_port = os.environ["SMTP_PORT"]
smtp_user = os.environ["SMTP_USER"]
smtp_pass = os.environ["SMTP_PASS"]
access_path = os.environ['ACCESS_PATH']
server_host = os.environ['SERVER_HOST']


@app.route(access_path)
def send():
    mb = MailBot(smtp_host, smtp_port, smtp_user, smtp_pass)
    subj = request.args.get('subj', '')
    body = request.args.get('body', '')
    body_type = request.args.get('type', 'plain')
    dst = request.args.get('dst', '')
    try:
        info = mb.Send(smtp_user, dst, subj, body, body_type=body_type)
    except Exception as e:
        info = {'status': False, 'error': str(e)}
    finally:
        return info


if __name__ == '__main__':
    app.run(host=server_host, debug=False, port=7070, threaded=True)
