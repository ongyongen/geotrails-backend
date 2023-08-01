from flask import Blueprint, Response, request
from bson import ObjectId
from db import *
from data import *
import json
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

records_api = Blueprint('records_api', __name__)

@records_api.get("/records")
@jwt_required(optional=False)
def get_all_records_by_user():

    """
    Get all past logged caches records from a user
    """

    try:
        current_user = get_jwt_identity()

        # Get all logged cache records from the user (based on username)
        result = users_records_collection.find({"username" : current_user})
        data = [doc for doc in result]
        return Response(json.dumps(data, default=str), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Failed to fetch past logged cache records from this user" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
    
@records_api.post("/record")
@jwt_required(optional=False)
def create_logged_cache_record():

    """
    Create a new record under a user's logged caches records collection
    Input : new_record_data = {
        notes: "",
        cache_code : "",
        cache_name: "",
        geocache_type: "",
        container_type: "",
        difficulty: "", 
        terrain: "",
        latitude: "",
        longitude: "",
        planning_area: "", 
        owner_name: "",
        cache_url: "",
        found_rate: "",
        username: ""
    }
    """ 

    try:
        current_user = get_jwt_identity()
        new_record_data = request.get_json()
        new_record_data["username"] = current_user

        # Add new record for a logged cache (based on username)
        users_records_collection.insert_one(new_record_data)
        return Response(json.dumps(new_record_data, default=str), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Failed to log cache as found" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")

@records_api.put("/record")
@jwt_required(optional=False)
def update_logged_cache_record():

    """
    Update the notes field of an existing entry under a user's logged cache records
    Input : updated_record_data = {
        _id: "",
        notes: ""
    }
    """
    
    try:
        updated_record_data = request.get_json()
        records_id = updated_record_data["_id"]
        updated_records_notes = updated_record_data["notes"]

        update_record_identifier = {"_id": ObjectId(records_id)}
        update_record_field_logic = {"$set" : { "notes" : updated_records_notes }}
        users_records_collection.find_one_and_update(update_record_identifier, update_record_field_logic, new=True)

        success_message = { "msg" : "Successfully updated logged cache records" }
        return Response(json.dumps(success_message), status=200, mimetype="application/json")
    
    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Failed to update logged cache records" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")

@records_api.delete("/record")
@jwt_required(optional=False)
def delete_logged_cache_record():

    """
    Delete an existing logged cache record by ID 

    Input : delete_record_data = {
        _id : ""
    }
    """

    try:
        delete_record_data = request.get_json()
        record_id = delete_record_data["_id"]

        delete_record_identifier = { "_id": ObjectId(record_id) }
        users_records_collection.delete_one(delete_record_identifier)

        success_message = { "msg" : "Successfully deleted logged cache record" }
        return Response(json.dumps(success_message), status=200, mimetype="application/json")

    except Exception as ex:
        print(ex)
        error_message = { "msg" : "Failed to delete logged cache records" }
        return Response(json.dumps(error_message), status=500, mimetype="application/json")
