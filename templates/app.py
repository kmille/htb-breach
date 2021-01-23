import os.path
import psutil
from flask import Flask, request, jsonify, redirect
from functools import wraps
from sshpubkeys import SSHKey
import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'api-user',
    'password': '{{ db_password_api }}',
    'host': '127.0.0.1',
    'database': 'api',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': '/etc/mysql/ca-cert.pem',
    'compress': True
}


app = Flask(__name__)


def log_user():
    x_forwarded_for = request.headers['X-Forwarded-For']
    db = mysql.connector.connect(**config)
    cursor = db.cursor(prepared=True)
    sql = "UPDATE user SET ip=%s WHERE role='public'"
    cursor.execute(sql, (x_forwarded_for, ))
    db.commit()
    db.close()


def check_auth(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kw):
            log_user()
            db = mysql.connector.connect(**config)
            cursor = db.cursor()
            cursor.execute("SELECT * from api.user")
            users = cursor.fetchall()
            db.close()
            for user in users:
                user_auth = user[3]
                auth_header, auth_secret = user_auth.split(";")
                if auth_header in request.headers and request.headers[auth_header] == auth_secret:
                    if user[2] == role:
                        # auth success
                        return f(*args, **kw)
            return jsonify({"error": "auth failed"}), 401
        return wrapper
    return decorator


@app.route("/api/v1/network", methods=['GET', 'POST'])
@check_auth("public")
def network():
    connections = psutil.net_connections()
    connections = list(filter(lambda x: x.status in ('LISTEN', 'ESTABLISHED'), connections))
    connections_nice = []
    for c in connections:
        connections_nice.append({'state': c.status, 'laddr': c.laddr, 'raddr': c.raddr})
    return jsonify(connections_nice)


@app.route("/api/v1/ssh", methods=['GET', 'POST'])
@check_auth("admin")
def ssh():
    if request.method == 'POST':
        ssh_key_request = request.get_json(force=True)['ssh_key']
        SSHKey(ssh_key_request).parse()
        with open(os.path.expanduser("~/.ssh/authorized_keys"), "a") as f:
            f.write(ssh_key_request.strip() + "\n")
    ssh_keys = []
    with open(os.path.expanduser("~/.ssh/authorized_keys")) as f:
        for line in f.readlines():
            pub_key = SSHKey(line)
            pub_key.parse()
            ssh_keys.append({'bits': pub_key.bits, 'md5': pub_key.hash_md5(), 'comment': pub_key.comment})
    return jsonify(ssh_keys)


@app.route("/PleaseSubscribe")
def subscribe():
    return redirect("https://www.youtube.com/channel/UCa6eh7gCkpPo5XXUDfygQQA")


if __name__ == '__main__':
    app.run()
