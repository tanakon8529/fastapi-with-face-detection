import jwt
from fastapi import APIRouter, HTTPException, Header, Depends
from loguru import logger
from datetime import datetime, timedelta
from typing import List, Optional

from app.settings.configs import JWT_PUBLIC_KEY, ACCESSTOKEN_FILE_PATH, \
                                FIRST_DEVUSER, FIRST_DEVUSER_PASSWORD

from app.core.base_model import UserInfo
from app.utils.json_util import json_controls

js_controls = json_controls()
router = APIRouter()

def decode_token_userinfo(token: str):
    try:
        payload = jwt.decode(token, JWT_PUBLIC_KEY, algorithms="HS256")
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail="secret key invalid : {}".format(e))

def verify_grant_type(type: str):
    try:
        if type == "client_credentials":
            return type
        elif type == "get_client_credentials":
            return type
        else:
            raise HTTPException(status_code=401, detail="Type invalid(01)")
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail="Type invalid(01) {}".format(e))

def check_expire_access_token(token):
    time_now = datetime.now()
    status_token = None
    pack_path = ACCESSTOKEN_FILE_PATH

    token_files = js_controls.read_json_file(pack_path)
    
    for data_token in token_files["data"]:
        if type(data_token) == dict:
            token_file_system = data_token["access_token"]
            if token_file_system == token:
                status_token = True
                break
    
    if token_file_system == token:
        date_time_obj = datetime.strptime(data_token["time_stamp"], '%Y-%m-%d %H:%M:%S')
        try:
            if date_time_obj < time_now:
                status_token = False
        
        except Exception as e:
            logger.error(f"{e}")
            raise HTTPException(status_code=401, detail="access_token invalid : {}".format(e))

    return status_token, data_token

def verify_token_user_info(auth: str = Header(...)):
    status_token, token_file = check_expire_access_token(auth)
    if status_token == True:
        return token_file
    elif status_token == False:
        raise HTTPException(status_code=401, detail="access_token expired")
    else:
        raise HTTPException(status_code=500, detail="access_token invalid")

def verify_user_info(token: str = Header(...)) -> UserInfo:
    username_info = UserInfo()
    payload = decode_token_userinfo(token)
    result_verify = False
    try:
        username_info.username = payload['username']
        username_info.password = payload['password']
        logger.info(username_info)

        username_pack = [FIRST_DEVUSER]
        password_pack = [FIRST_DEVUSER_PASSWORD]
                        
        if username_info.username in username_pack:
            if username_info.password in password_pack:
                result_verify = username_info.username
        
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail="Token invalid(01) {}".format(e))
    if result_verify == False:
        raise HTTPException(status_code=401, detail="username or password invalid(01)")

    return result_verify
