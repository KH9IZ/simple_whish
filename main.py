from authlib.integrations.flask_client import OAuth
from flask import (
    Flask,
    abort,
    redirect,
    request,
    session,
    url_for,
)

from forms import WhishForm
from models import (
    Whish,
    close_db,
    connect_db,
    create_tables,
)

app = Flask(__name__)
# with open('/run/secrets/FLASK_SECRET_KEY') as f:
#     app.config["SECRET_KEY"] = f.read()
app.config["SECRET_KEY"] = 'the random string'

create_tables()

oauth = OAuth(app)
oauth.register(
    name="yandex",
    client_id="9f6516d5a74148f2b509ef4370a03170",
    client_secret="aa686babf09f415abc0505624d6a6a8c",
    authorize_url="https://oauth.yandex.ru/authorize",
    access_token_url="https://oauth.yandex.ru/token",
    api_base_url="https://login.yandex.ru",
)


@app.before_request
def before_request():
    connect_db()


@app.after_request
def after_request(resp):
    close_db()
    return resp


@app.route("/login/")
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth.yandex.authorize_redirect(redirect_uri)


@app.route("/auth/")
def auth():
    token = oauth.yandex.authorize_access_token()
    resp = oauth.yandex.get("/info", token=token)
    resp.raise_for_status()
    userinfo = resp.json()

    uid = userinfo.get("id")

    session["uid"] = uid
    return redirect(url_for("get_whish"))


@app.route("/whish/", methods=["POST"])
def post_whish():
    if not (uid := session.get("uid")):
        abort(403)
    form = WhishForm(request.form)
    if not form.validate():
        abort(400)
    whish = Whish.create(uid=uid, title=form.title.data, description=form.description.data)
    print(f"Saving {form.title.data=} {form.description.data=} {uid=}.")
    return {"status": "ok"}


@app.route("/whishes/", methods=["GET"])
def get_whish():
    if not (uid := session.get("uid")):
        abort(403)
    print(f"{uid=}")
    whishes = Whish.select().where(Whish.uid == uid)
    return [
        {
            'id': w.id,
            'titile': w.title,
            'description': w.description,
        }
        for w in whishes
    ]


if __name__ == "__main__":
    app.run()
