from pool_token.response import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from pool_token.settings import db
import secrets
from datetime import datetime, timedelta

@api_view(['GET'])
def index(request):
    return SuccessResponse(message="Demo Response")

@api_view(['GET'])
def generate_pool(request, pool_name,pool_size):
    data = []
    current_time = datetime.now()
    tokens = []
    #we will use JWT for token but this time suppose we are using random strings 
    for i in range(pool_size):
        temp = {}
        t = secrets.token_urlsafe(20)
        tokens.append(t)
        temp['token'] = t
        temp['status'] = 'available'
        temp['is_delete'] = False
        temp['pool_name'] = pool_name
        temp['created_at'] = current_time
        temp['updated_at'] = current_time
        data.append(temp)
    db.tokens.insert_many(data)
    return SuccessResponse(message="Token Generated Successfully", data=tokens)

@api_view(['GET'])
def get_pool(request, pool_name):
    pool_data = db.tokens.find({"pool_name": pool_name}, {"_id": 0})
    if not pool_data:
        return BadRequestResponse(message="Pool Not Found")
    return SuccessResponse(message="Tokens Found Successfully", data=list(pool_data))

@api_view(['GET'])
def assign_token(request, pool_name):
    get_token = db.tokens.find_one({"status": "available", "is_delete": False}, {"_id": 0})
    if not get_token:
        return BadRequestResponse(message="Token is Unavailable!")
    current_time = datetime.now()
    db.tokens.update_one({"token": get_token.get("token")}, {"$set": {"updated_at": current_time, "status": "blocked"}})
    return SuccessResponse(message="Assigned One Token", data = get_token.get("token"))

@api_view(['PUT'])
def unblocked_token(request, token_name):
    get_token = db.tokens.find_one({"token": token_name}, {"_id": 0})
    if not get_token:
        return BadRequestResponse(message="Token Not Found")
    current_time = datetime.now()
    db.tokens.update_one({"token": token_name}, {"$set": {"updated_at": current_time, "status": "available"}})
    return SuccessResponse(message="Token Unblocked Successfully", data=token_name)

@api_view(['DELETE'])
def delete_token(request, token_name):
    get_token = db.tokens.find_one({"token": token_name}, {"_id": 0})
    if not get_token:
        return BadRequestResponse(message="Token Not Found")
    current_time = datetime.now()
    db.tokens.update_one({"token": token_name}, {"$set": {"updated_at": current_time, "is_delete": True}})
    return SuccessResponse(message="Token Deleted Successfully", data=token_name)

@api_view(['PUT'])
def keep_alive_token(request):
    current_time = datetime.now()
    five_minute_before = current_time - timedelta(minutes=5)
    all_dead_tokens = db.tokens.find({"updated_at": {"$lte": five_minute_before}})
    if not all_dead_tokens:
        return BadRequestResponse(message="All Tokens are alive")
    token_list = [i.get("token") for i in all_dead_tokens]
    db.tokens.update({"token": {"$in": token_list}}, {"$set": {"is_delete": True}})
    return SuccessResponse(data=token_list, message='Deleted Tokens')


@api_view(['GET'])
def freed_or_released(request):
    current_time = datetime.now()
    one_minute_before = current_time - timedelta(minutes=1)
    all_dead_tokens = db.tokens.find({"updated_at": {"$lte": one_minute_before}})
    if not all_dead_tokens:
        return BadRequestResponse(message="All Tokens are alive")
    token_list = [i.get("token") for i in all_dead_tokens]
    db.tokens.update({"token": {"$in": token_list}}, {"$set": {"status": "available"}})
    return SuccessResponse(data=token_list, message='Marked Available Tokens')