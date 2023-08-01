import hashlib
from flask import request, Response, Blueprint
import json
from flask_cors import cross_origin
from db import *
from flask_jwt_extended import create_access_token
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from db import *
from datetime import date

user_analytics_api = Blueprint('user_analytics_api', __name__)

@user_analytics_api.post("/log_geocache")
@jwt_required(optional=False)
def log_geocache():
    try:
        current_user = get_jwt_identity() 
        geocache_data = request.get_json()

        user_analytics_record = {
            "username" : current_user,
            "date": date.today().strftime("%Y-%m-%d"),
            "cache_code" : geocache_data["cache_code"],
            "name" : geocache_data["name"],
            "geocache_type" : geocache_data["geocache_type"],
            "container_type" : geocache_data["container_type"],
            "difficulty": geocache_data["difficulty"],
            "terrain": geocache_data["terrain"],
            "planning_area": geocache_data["planning_area"],
            "owner_name": geocache_data["owner_name"],
            "found_rate": geocache_data["found_rate"]
        }
        
        users_analytics_collection.insert_one(user_analytics_record)
        success_message = { "msg" : "Geocache is logged to user %s" % current_user }
        return Response(json.dumps(success_message), status=201, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")


@user_analytics_api.get("/geocaches_records")
@jwt_required(optional=False)
def get_all_found_geocaches():
    try:
        current_user = get_jwt_identity() 
   
        date = request.args.get("date")

        filter_criteria = {
            "username" : current_user
        }

        result = users_analytics_collection.find(filter_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    


@user_analytics_api.get("/geocaches_records_by_date")
@jwt_required(optional=False)
def count_geocaches_found_by_date():
    try:
        current_user = get_jwt_identity() 
   
        date = request.args.get("date")

        filter_criteria = {
            "date" : date,
            "username" : current_user
        }

        result = users_analytics_collection.find(filter_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    
    
@user_analytics_api.get("/geocaches_records_agg_date")
@jwt_required(optional=False)
def count_geocaches_agg_by_date():
    try:
        current_user = get_jwt_identity() 
   
        agg_criteria = [
            {
                "$match" : {
                    "username" : current_user 
                }
            },
            {
                "$group" : {
                    "_id" : "$date",
                    "total_caches" : {"$sum": 1}
                }
            }
        ]

        result = users_analytics_collection.aggregate(agg_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    

@user_analytics_api.get("/geocaches_records_agg_geocache_type")
@jwt_required(optional=False)
def count_geocaches_agg_by_geocache_type():
    try:
        current_user = get_jwt_identity() 
   
        agg_criteria = [
            {
                "$match" : {
                    "username" : current_user 
                }
            },
            {
                "$group" : {
                    "_id" : "$geocache_type",
                    "total_caches" : {"$sum": 1}
                }
            }
        ]

        result = users_analytics_collection.aggregate(agg_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    


@user_analytics_api.get("/geocaches_records_agg_container_type")
@jwt_required(optional=False)
def count_geocaches_agg_by_container_type():
    try:
        current_user = get_jwt_identity() 
   
        agg_criteria = [
            {
                "$match" : {
                    "username" : current_user 
                }
            },
            {
                "$group" : {
                    "_id" : "$container_type",
                    "total_caches" : {"$sum": 1}
                }
            }
        ]

        result = users_analytics_collection.aggregate(agg_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    
@user_analytics_api.get("/geocaches_records_agg_planning_area")
@jwt_required(optional=False)
def count_geocaches_agg_by_planning_area():
    try:
        current_user = get_jwt_identity() 
   
        agg_criteria = [
            {
                "$match" : {
                    "username" : current_user 
                }
            },
            {
                "$group" : {
                    "_id" : "$planning_area",
                    "total_caches" : {"$sum": 1}
                }
            },
            {
                "$sort" : {"total_caches" : -1}
            }
        ]

        result = users_analytics_collection.aggregate(agg_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    
@user_analytics_api.get("/geocaches_records_agg_cache_owner")
@jwt_required(optional=False)
def count_geocaches_agg_by_cache_owner():
    try:
        current_user = get_jwt_identity() 
   
        agg_criteria = [
            {
                "$match" : {
                    "username" : current_user 
                }
            },
            {
                "$group" : {
                    "_id" : "$owner_name",
                    "total_caches" : {"$sum": 1}
                }
            },
            {
                "$sort" : {"total_caches" : -1}
            }
        ]

        result = users_analytics_collection.aggregate(agg_criteria)

        if result:
            data = [doc for doc in result]
            return Response(json.dumps(data, default=str), status=200, mimetype="application/json")
        else:
            error_message = { "msg" : "Failed to fetch user credentials" }
            return Response(json.dumps(error_message), status=401, mimetype="application/json")
        
    except Exception as ex:
        print(ex)
        error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    
