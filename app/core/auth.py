import jwt
from fastapi import APIRouter, HTTPException, Header, Depends
from loguru import logger
from datetime import datetime, timedelta
from typing import List, Optional

from app.settings.configs import JWT_PUBLIC_KEY, ACCESSTOKEN_FILE_PATH, \
                                FIRST_DEVUSER, FIRST_DEVUSER_PASSWORD, \
                                SECOND_DEVUSER, SECOND_DEVUSER_PASSWORD, \
                                PREREGISTER_DEVUSER, PREREGISTER_DEVUSER_PASSWORD, \
                                SUPPORT_DEVUSER, SUPPORT_DEVUSER_PASSWORD, \
                                STAGING_DEVUSER, STAGING_DEVUSER_PASSWORD, \
                                TRUEBUSINESS_DEVUSER, TRUEBUSINESS_DEVUSER_PASSWORD, \
                                ASPENTREE_DEVUSER, ASPENTREE_DEVUSER_PASSWORD, \
                                ASPENTREE_DEVUSER_STAGING, ASPENTREE_DEVUSER_STAGING_PASSWORD, \
                                ASPENTREE_DEVUSER_SUPPORT, ASPENTREE_DEVUSER_SUPPORT_PASSWORD, \
                                ZENDESK_DEVUSER, ZENDESK_DEVUSER_PASSWORD

from app.core.base_model import UserInfo, CustomerVerify, PhoneNumber, LeadDetailBase
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

        username_pack = [FIRST_DEVUSER, SECOND_DEVUSER, SUPPORT_DEVUSER, PREREGISTER_DEVUSER,
                         STAGING_DEVUSER, TRUEBUSINESS_DEVUSER, ASPENTREE_DEVUSER, ASPENTREE_DEVUSER_STAGING,
                         ASPENTREE_DEVUSER_SUPPORT, ZENDESK_DEVUSER
                        ]
        password_pack = [FIRST_DEVUSER_PASSWORD, SECOND_DEVUSER_PASSWORD, SUPPORT_DEVUSER_PASSWORD, PREREGISTER_DEVUSER_PASSWORD,
                         STAGING_DEVUSER_PASSWORD, TRUEBUSINESS_DEVUSER_PASSWORD, ASPENTREE_DEVUSER_PASSWORD, ASPENTREE_DEVUSER_STAGING_PASSWORD,
                         ASPENTREE_DEVUSER_SUPPORT_PASSWORD, ZENDESK_DEVUSER_PASSWORD
                        ]
                        
        if username_info.username in username_pack:
            if username_info.password in password_pack:
                result_verify = username_info.username
        
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail="Token invalid(01) {}".format(e))
    if result_verify == False:
        raise HTTPException(status_code=401, detail="username or password invalid(01)")

    return result_verify

def verify_customer_detail(data: str = Header(...)) -> CustomerVerify:
    customer_info = CustomerVerify()
    payload = decode_token_userinfo(data)
    try:
        if "phone_number" in payload:
            customer_info.phone_number = payload["phone_number"]
        if "first_name_en" in payload:
            customer_info.first_name_en = payload["first_name_en"]
        if "last_name_en" in payload:
            customer_info.last_name_en = payload["last_name_en"]
        if "id_card" in payload:
            customer_info.id_card = payload["id_card"]
        if "passport_id" in payload:
            customer_info.passport_id = payload["passport_id"]
        if "uuid" in payload:
            customer_info.uuid = payload["uuid"]
        if "provider_source" in payload:
            customer_info.provider_source = payload["provider_source"]
        logger.info(customer_info)

        return customer_info
        
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail="data invalid(01) {}".format(e))

def verify_customer_detail_lead(data: str = Header(...)) -> LeadDetailBase:
    customer_info = LeadDetailBase()
    payload = decode_token_userinfo(data)
    try:
        if "first_name" in payload:
            customer_info.first_name = payload["first_name"]
        if "last_name" in payload:
            customer_info.last_name = payload["last_name"]
        if "email" in payload:
            customer_info.email = payload["email"]
        if "mobile_phone" in payload:
            customer_info.mobile_phone = payload["mobile_phone"]
        if "remark" in payload:
            customer_info.remark = payload["remark"]
        if "lead_source" in payload:
            customer_info.lead_source = payload["lead_source"]
        if "sub_lead_source" in payload:
            customer_info.sub_lead_source = payload["sub_lead_source"]
        if "interested_project" in payload:
            customer_info.interested_project = payload["interested_project"]
        if "owner_id" in payload:
            customer_info.owner_id = payload["owner_id"]
        if "source_system" in payload:
            customer_info.source_system = payload["source_system"]
        logger.info(customer_info)

        return customer_info
        
    except Exception as e:
        logger.error(f"{e}")
        raise HTTPException(status_code=401, detail="data invalid(01) {}".format(e))

def verify_mobile(data: str = Header(...)) -> PhoneNumber:
    customer_info = PhoneNumber()
    payload = decode_token_userinfo(data)
    try:
        customer_info.phone_number = payload["phone_number"]
        logger.info(customer_info)
        return customer_info
        
    except Exception as e:
        logger.error(f"verify_mobile : {e}")
        raise HTTPException(status_code=401, detail="data invalid(01) {}".format(e))
