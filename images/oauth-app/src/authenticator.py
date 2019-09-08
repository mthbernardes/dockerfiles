#!/usr/bin/env python3

import os
import yaml 
import requests

from requests_oauth2.services import GoogleClient
from requests_oauth2 import OAuth2BearerToken
from flask import Flask, request, redirect, session, Response


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(20)

config = yaml.load(open("conf.yaml"),Loader=yaml.FullLoader)
client_id = config["google-oauth"][0]["client_id"]
client_secret = config["google-oauth"][0]["client_secret"]
redirect_uri = config["google-oauth"][0]["redirect_uri"]
domains = config["google-oauth"][0]["domains"]
emails = config["google-oauth"][0]["emails"]

google_auth = GoogleClient(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

def checkpermissions(email):
    if email.split("@")[1] in domains or email in emails:
        return True
    return False

@app.route("/google-login")
def login():
    url = google_auth.authorize_url(scope=["profile", "email"],response_type="code",)
    html = "<a href=\"{}\">Login</a>".format(url)
    return html

@app.route("/google-auth")
def google_index():
    if not session.get("access_token"):
        code = request.args.get("code")
        error = request.args.get("error")
        if error:
            return "error :( {!r}".format(error)
        if not code:
            login()
        data = google_auth.get_token(
            code=code,
            grant_type="authorization_code",
        )
        session["access_token"] = data.get("access_token")

    if session["access_token"]:
        with requests.Session() as s:
            s.auth = OAuth2BearerToken(session["access_token"])
            r = s.get("https://www.googleapis.com/plus/v1/people/me")
        r.raise_for_status()
        data = r.json()

        for email in data["emails"]:
            if not checkpermissions(email["value"]):
                return Response("<script>window.location.href=\"/login\"</script>",status=401)
        return Response("<script>window.location.href=\"/\"</script>",status=200)
    return Response("<script>window.location.href=\"/login\"</script>",status=401)

if __name__ == "__main__":
    app.run(debug=False)

