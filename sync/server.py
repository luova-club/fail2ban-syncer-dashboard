from flask import Flask, request, abort

import json

app = Flask(__name__)

whitelist = []

@app.before_request()
def before_request(request):
    if not request.ip in whitelist:
        abort(402)


def add_ban(request, ban):
    try:
        with open("bans.json", "r") as f:
            data = json.load(f)
        request = request.json()
        data[request["ip"]] = ban
        with open("bans.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        return json.dumps({"status": 500, "error": e}), 500
    finally:
        return json.dumps({"status": 400}), 400

def get_bans():
    with open("bans.json", "r") as f:
        data = json.load(f)
    return data

@app.route("/ban", methods=["POST", "GET"])
def ban():
    add_ban(request, True)
    return ""
@app.route("/unban", methods=["POST"])
def unban():
    add_ban(request, False)
    return ""
@app.route("/get_bans")
def route_get_bans():
    return get_bans()

@app.route("/is_banned/<ip>")
def is_banned(ip):
    if request.method == "GET":
        if ip in get_bans():
            return json.dumps({"is_banned": True})
        else:
            return json.dumps({"is_banned": False})     


app.run()