from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from app.utils.json_util import json_controls
from app.settings.configs import ACCESSTOKEN_FILE_PATH, \
                                FIRST_DEVUSER, SECOND_DEVUSER, STAGING_DEVUSER, SUPPORT_DEVUSER, \
                                PREREGISTER_DEVUSER, TRUEBUSINESS_DEVUSER, ASPENTREE_DEVUSER, ASPENTREE_DEVUSER_STAGING, \
                                ASPENTREE_DEVUSER_SUPPORT, ZENDESK_DEVUSER

js_controls = json_controls()

def generate_access_token(username):
    access_token = secrets.token_urlsafe(32)
    time_stamp = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    path_file = ACCESSTOKEN_FILE_PATH
    result = {
        "username" : username,
        "access_token" : access_token,
        "time_stamp" : time_stamp
    }
    username_pack = [FIRST_DEVUSER, SECOND_DEVUSER, STAGING_DEVUSER, SUPPORT_DEVUSER,
                     PREREGISTER_DEVUSER, TRUEBUSINESS_DEVUSER, ASPENTREE_DEVUSER, 
                     ASPENTREE_DEVUSER_STAGING, ASPENTREE_DEVUSER_SUPPORT, ZENDESK_DEVUSER
                    ]

    data_access_token = js_controls.read_json_file(path_file)
    if isinstance(data_access_token, UnboundLocalError):
        data_access_token = {"data":[]}
        data_access_token["data"].append(result)
        js_controls.write_json_file(path_file, data_access_token)

    if username in username_pack:
        username_in_file_pack = []
        for detail in data_access_token["data"]:
            if "username" in detail:
                username_in_file_pack.append(detail["username"])

    if username in username_in_file_pack:
        for detail in data_access_token["data"]:
            if detail["username"] == username:
                detail["access_token"] = access_token
                detail["time_stamp"] = time_stamp
                js_controls.write_json_file(path_file, data_access_token)
                break
    else:
        # Init Data
        data_access_token["data"].append(result)
        js_controls.write_json_file(path_file, data_access_token)
    
    return result

def get_access_token(username):
    result = None
    path_file = ACCESSTOKEN_FILE_PATH
    data_access_token = js_controls.read_json_file(path_file)
    for detail in data_access_token["data"]:
        if "username" in detail:
            if detail["username"] == username:
                result = detail
                break

    return result