import json

from authlib.client import AssertionSession
from mastodon import Mastodon
import tweepy

import settings


def masto_auth():
    return Mastodon(
        access_token=settings.mastodon_key,
        api_base_url="https://botsin.space"
    )


def twitter_auth():
    auth = tweepy.OAuthHandler(
        settings.consumer_key,
        settings.consumer_secret
    )
    auth.set_access_token(
        settings.access_token,
        settings.access_token_secret
    )
    return tweepy.API(auth)


def google_api_auth(arqv_json="credenciais/colaborabot-gAPI.json", subject=None):
    with open(arqv_json, "r") as f:
        conf = json.load(f)

    header = {"alg": "RS256"}
    scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    key_id = conf.get("private_key_id")
    if key_id:
        header["kid"] = key_id

    # Google puts scope in payload
    claims = {"scope": " ".join(scopes)}
    return AssertionSession(
        grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
        token_url=conf["token_uri"],
        issuer=conf["client_email"],
        audience=conf["token_uri"],
        claims=claims,
        subject=subject,
        key=conf["private_key"],
        header=header,
    )


def id_mastodon():
    id_perfil = settings.mastodon_profile_id
    return id_perfil
