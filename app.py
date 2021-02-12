from flask import Flask, url_for, redirect, render_template, request, Markup, session
from functools import wraps
from DataStore.MySQL import MySQL
import sys, re, os, time, datetime, hashlib, base64, random, string

# 日付関数
dt_now = datetime.datetime.now()

'''
# 証明書のディレクトリ指定
dirname = os.getcwd()
if os.name == 'nt':
    print("on windows")
    ca_path = os.path.join(dirname, 'opt\\mysql\\ssl\\ca.pem')
    cert_path = os.path.join(dirname, 'opt\\mysql\\ssl\\client-cert.pem')
    key_path = os.path.join(dirname, 'opt\\mysql\\ssl\\client-key.pem')
elif os.name == 'posix':
    print("on mac or linux")
    ca_path = os.path.join(dirname, 'opt/mysql/ssl/ca.pem')
    cert_path = os.path.join(dirname, 'opt/mysql/ssl/client-cert.pem')
    key_path = os.path.join(dirname, 'opt/mysql/ssl/client-key.pem')
'''

# ログイン処理のリトライ回数上限
MAX_RETRY = 3

# ランダム文字列生成
def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

# Flaskインスタンスと暗号化キーの指定
app = Flask(__name__)
app.secret_key = randomname(16)

# saltの生成＆パスワードへの付与
def gen_password(pwd):
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac('sha256',
            pwd.encode('utf-8'), salt, 10000)
    return base64.b64encode(salt + digest).decode('ascii')

# パスワード検証
def verify_password(pwd, hash):
    b = base64.b64decode(hash)
    salt, digest_v = b[:16], b[16:]
    digest_n = hashlib.pbkdf2_hmac('sha256',
            pwd.encode('utf-8'), salt, 10000)
    return digest_n == digest_v

# ログイン画面
@app.route('/')
def main():
    props = {'title': 'login or sign up', 'msg': 'ユーザ登録＆ログイン'}
    return render_template('index.html', props=props)

# ユーザ登録画面に遷移
@app.route('/regist_user')
def regist_user():
    props = {'title': 'sign up', 'msg': 'ユーザ登録'}
    html = render_template('user_regist.html', props=props)
    return html

# ユーザー登録
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    pwd = request.form.get('pwd')
    # パスワードはハッシュ化する
    hash_pwd = gen_password(pwd)
    # ユーザーを追加
    add_result = add_user(name, age, gender, hash_pwd)
    if add_result:
        props = {'title': 'success sign up', 'msg': 'ユーザを登録しました！'}
        return render_template('msg.html', props=props)
    else:
        props = {'title': 'failed sign up', 'msg': 'ユーザの登録に失敗しました。'}
        return render_template('msg.html', props=props)


# DBにユーザ追加
def add_user(name, age, gender, pwd):
    # 別モジュールに渡すことに。
    stmt = 'INSERT INTO users (name, age, gender, password) VALUES (%s, %s, %s, %s)'
    reg = MySQL.ins_query(stmt, name, age, gender, pwd)
    if reg:
        return True
    else:
        return reg

# ログイン画面に遷移
@app.route('/login')
def login():
    props = {'title': 'try login', 'msg': 'ログイン試行'}
    return render_template('login_form.html', props=props)

# ログイントライ
@app.route('/login/try', methods=['POST'])
def login_try():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    result = check_user(name, str(pwd))
    if result:
        session['login'] = name
        return redirect('/user/home')
    else:
        props = {'title': 'login failed', 'msg': 'ログインに失敗しました。ユーザ名かパスワードが誤っています'}
        return render_template('msg.html', props=props)


# ログイン成功→ユーザーHOME画面
@app.route('/user/home')
def login_success():
    name = get_name()
    # ログイン先の画面(user_home.html)に遷移さす。
    props = {'title': 'user_home', 'msg':'あなたのマイページ'}
    return render_template('user_home.html', name=name, props=props)

# DBからログイン情報参照 レコードのCOUNT結果で存在有無を判断する！
def check_user(name, pwd):
    stmt = 'SELECT COUNT(*) FROM users WHERE name=%s'
    log = MySQL.query(stmt, name)
    if 1 in log[0]:
        stmt = 'SELECT password FROM users WHERE name=%s'
        hash_pwd = MySQL.query(stmt, name)
        return verify_password(str(pwd), str(hash_pwd[0]))
    else:
        return False


# セッション管理
def is_login():
    sys.stdout.write(str(session))
    return 'login' in session

# ログインリトライ処理
def retry_login():
    for i in range(MAX_RETRY + 1):
        result = is_login()
        sys.stdout.write(str(result), str(session))
        if result:
            return session['login']
        else:
            sleep_sec = 2 ** i
            time.sleep(sleep_sec)
            if i == MAX_RETRY:
                return 'None'

# ユーザ名の取得
def get_name():
    if is_login():
        return session['login']
    else:
        return retry_login()

# ログアウト処理
@app.route('/logout')
def logout():
    try_logout()
    props = {'title': 'logout', 'msg': 'お疲れ様でした(⌒,_ゝ⌒)'}
    return render_template('msg.html', props=props)

# ログアウトトライ
def try_logout():
    session.pop('login', None)

# ログイン必須を処理するデコレーターを定義
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        search_session = get_name()
        if search_session == 'None':
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


# 過去の記録確認
@app.route('/user/old_log')
@login_required
def check_old_log():
    name = get_name()
    dt = get_today()
    props = {'title': 'user old log', 'msg': '過去の記録確認'}
    stmt = 'SELECT memo, dt, tm FROM users_log\
            WHERE name = %s AND dt = cast(now() as date)'
    timeline = MySQL.query(stmt, name)
    return render_template('user_old_log.html',
            name=name, dt=dt,timeline=timeline, props=props)

# カレンダーに入力された日付を取得し、タイムラインを再表示する。
@app.route('/user/old_log', methods=['POST'])
@login_required
def check_calendar():
    name = get_name()
    dt = request.form.get('date')
    props = {'title': 'user old log', 'msg': '過去の記録確認'}
    stmt = 'SELECT memo, dt, tm FROM users_log\
            WHERE name = %s AND dt = %s'
    timeline = MySQL.query(stmt, name, dt)
    return render_template('user_old_log.html',
            name=name, dt=dt, timeline=timeline, props=props)


# 記録を作成する！
@app.route('/user/add_log')
@login_required
def add_log():
    props = {'title': 'write log', 'msg': '今この瞬間の出来事・気持ちなどを記録しよう'}
    return render_template('user_add_log.html',
            name=get_name(), props=props)

@app.route('/user/add_log', methods=['POST'])
@login_required
def write_log():
    name = get_name()
    memo = request.form.get('text')
    dt = get_today()
    tm = get_time()
    props = {'title': 'success write log', 'msg': '記録出来ました！この調子！'}
    stmt = 'INSERT INTO users_log values\
            (%s, %s, %s, %s);'
    write_log = MySQL.ins_query(stmt, name, memo, dt, tm)
    return render_template('user_add_log.html',
            name=name, memo=memo, dt=dt, tm=tm, props=props)


# 今日日付取得
def get_today():
    d = datetime.datetime.now()
    today = (d.strftime('%Y-%m-%d'))
    return today

# 現在時刻取得
def get_time():
    t = datetime.datetime.now()
    time = (t.strftime('%H:%M:%S'))
    return time

@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=False)
