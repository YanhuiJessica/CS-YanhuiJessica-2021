from flask import Flask, render_template
from flask.globals import request, session
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from datetime import timedelta
import numpy, json, random

app = Flask(__name__)
app.config['SECRET_KEY'] = '<change-if-you-want>'
csrf = CSRFProtect(app)
koalas_max = 4

# Server-side Session
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    session.modified = True

@app.route("/")
def index():
    if 'koalas' not in session:
        session['koalas'] = koalas_max
    session['pos'] = random.randint(1, 4)
    session['randkey'] = numpy.random.randint(0, 2, (128,128)).tolist()
    cnt = session['koalas']
    if cnt:
        msg = str(cnt) + ' koalas left.'
    else:
        msg = 'actf{test_flag}'
    return render_template("index.html", msg=msg, pos=session['pos'])

@app.route("/rescue", methods=['POST'])
def rescue():
    keys = eval(json.loads(json.dumps(request.form.get('keys').replace('null', 'None'))))
    check = numpy.zeros((128,128), int).tolist()
    pos = session['pos']
    for k in keys:
        check[(int(k['cx']) - 2) // 4][(int(k['cy']) - 2) // 4] = int(k['key'])
    diff = 0
    for i in range(0, len(check), 2):
        for j in range(0, len(check), 2):
            if check[i][j] == check[i + 1][j] == check[i][j + 1] == check[i + 1][j + 1]:
                continue
            else: diff += 1
    if diff > 1:
        session['koalas'] = koalas_max
        return 'finish'
    diff = 0
    if pos == 1:
        for i in range(0, len(check), 2):
            for j in range(0, len(check), 2):
                if check[i][j] != session['randkey'][i][j]:
                    diff += 1
    elif pos == 2:
        for i in range(0, len(check), 2):
            for j in range(1, len(check), 2):
                if check[i][j] != session['randkey'][i][j]:
                    diff += 1
    elif pos == 3:
        for i in range(1, len(check), 2):
            for j in range(0, len(check), 2):
                if check[i][j] != session['randkey'][i][j]:
                    diff += 1
    else:
        for i in range(1, len(check), 2):
            for j in range(1, len(check), 2):
                if check[i][j] != session['randkey'][i][j]:
                    diff += 1
    if diff <= 2:
        session['koalas'] -= 1
    else:
        session['koalas'] = koalas_max
    return 'finish'

@app.route("/randkey", methods=['POST'])
def get_randkey():
    try:
        cx = (int(request.form.get('cx')) - 2) // 4
        cy = (int(request.form.get('cy')) - 2) // 4
        return str(session['randkey'][cx][cy])
    except:
        return "PositionValueError"

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=8080)