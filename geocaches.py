from flask import Blueprint
from flask import Blueprint, Response, request
from db import *
from data import *
import json
from flask import request
import datetime
from pymongo import errors 
from datetime import datetime
from utils import create_geocaches_filter_criteria

geocaches_api = Blueprint('geocaches_api', __name__)

@geocaches_api.get("/geocache")
def find_geocache_by_cache_code():

    """
    Get 1 geocache by geocache code
    Path : /geocache?cache_code=X
    """

    try:
        geocache_code = request.args.get("cache_code")

        data = geocaches_collection.find_one({"cache_code": geocache_code})
        return Response(json.dumps(data, default=str),  status=200, mimetype='application/json')
    
    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Cache with the cache code is not found" }
        return Response(json.dumps(error_message),  status=500, mimetype='application/json')
    

@geocaches_api.get("/geocaches")
def find_geocaches_by_criteria():

    """
    Get all geocaches based on filter criteria provided 
    If no filter criteria is provided, return all caches
    Path : /geocaches?geocache_type=X
    """

    try:
        geocache_types = [x for x in request.args.getlist("geocache_type")]
        container_types = [x for x in request.args.getlist("container_type")]
        difficulty = float(request.args.get("difficulty")) if request.args.get("difficulty") != None else ""
        terrain =  float(request.args.get("terrain")) if request.args.get("terrain") != None else ""
        planning_areas = [x for x in request.args.getlist("planning_area")]
        geocache_code = request.args.get("cache_code")
        page = int(request.args.get("page"))

        criteria = create_geocaches_filter_criteria(
            geocache_types, 
            container_types, 
            difficulty, 
            terrain, 
            planning_areas,
            geocache_code
        )

        cols_to_exclude = {
            "cache_id": 0,
            "description": 0,
            "latitude": 0,
            "longitude": 0,
            "details_url": 0,
            "favorite_points": 0,
            "hint": 0,
            "owner_id": 0,
            "total_did_not_find": 0,
            "total_found": 0,
            "trackable_count": 0,
            "_id": 0,
        }

        if criteria != {}:
            result =  geocaches_collection.find(criteria, cols_to_exclude).limit(10).skip(page)
        else:
            result = geocaches_collection.find({}, cols_to_exclude).limit(10).skip(page)

        data = [doc for doc in result]
        return Response(json.dumps(data, default=str),  status=200, mimetype='application/json')
    
    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Geocaches created by these owner(s) cannot be found" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")  
    

@geocaches_api.get("/geocaches_map")
def find_all_geocaches_by_criteria():

    """
    Get all geocaches based on filter criteria provided 
    If no filter criteria is provided, return all caches
    Path : /geocaches?geocache_type=X
    """

    try:
        geocache_types = [x for x in request.args.getlist("geocache_type")]
        container_types = [x for x in request.args.getlist("container_type")]
        difficulty = float(request.args.get("difficulty")) if request.args.get("difficulty") != None else ""
        terrain =  float(request.args.get("terrain")) if request.args.get("terrain") != None else ""
        planning_areas = [x for x in request.args.getlist("planning_area")]
        geocache_code = request.args.get("cache_code")

        criteria = create_geocaches_filter_criteria(
            geocache_types, 
            container_types, 
            difficulty, 
            terrain, 
            planning_areas,
            geocache_code
        )

        cols_to_exclude = {
            "cache_id": 0,
            "description": 0,
            "details_url": 0,
            "favorite_points": 0,
            "hint": 0,
            "owner_id": 0,
            "total_did_not_find": 0,
            "total_found": 0,
            "trackable_count": 0,
            "_id": 0,
        }

        if criteria != {}:
            result =  geocaches_collection.find(criteria, cols_to_exclude)
        else:
            result = geocaches_collection.find({}, cols_to_exclude)

        data = [doc for doc in result]
        return Response(json.dumps(data, default=str),  status=200, mimetype='application/json')
    
    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Geocaches created by these owner(s) cannot be found" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")  
    
@geocaches_api.route("/seed")
def geocachesList():

    """
    Seed the database with geocache data from data.py file
    """

    try: 
        geocaches_collection.drop()  

        for doc in caches_data:
            doc['placed_date'] = datetime.strptime(doc['placed_date'], "%Y-%m-%d")
            doc['last_found_date'] = datetime.strptime(doc['last_found_date'], "%Y-%m-%d")

        geocaches_collection.insert_many(caches_data)
        print("success")
    except errors.OperationFailure:
        print("An authentication error was received. Are you sure your database user is authorized to perform write operations?")
    return "Done"
