import hashlib
from flask import request, Response, Blueprint
import json
from flask_cors import cross_origin
from db import *
from flask_jwt_extended import create_access_token
import hashlib
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

auth_api = Blueprint('auth_api', __name__)

@auth_api.post("/create_account")
def create_account():
    
	"""
	Create a new account with a unique username
	Input : { username : "xxx",  password : "xxx" }
	"""

	try:
		new_user_data = request.get_json()
		
		# hash password
		new_user_data["password"] = hashlib.sha256(new_user_data["password"].encode("utf-8")).hexdigest() 
		
		# check if user already exists
		doc = users_collection.find_one({"username": new_user_data["username"]})    

		# create a new account only if user does not exist yet
		if not doc:
			users_collection.insert_one(new_user_data)
			success_message = { "msg" : "New account is created" }
			return Response(json.dumps(success_message), status=201, mimetype="application/json")
		else:
			error_message = { "msg" : "Cannot create a new account. Username already exists" }
			return Response(json.dumps(error_message), status=401, mimetype="application/json")
	
	except Exception as ex:
		print(ex)
		error_message = { "msg" : "Cannot create a new account. Please try again" }
		return Response(json.dumps(error_message), status=500, mimetype="application/json")


@auth_api.post("/login")
def login():

	"""
	Log in to existing account
	Input : { username : "xxx", password : "xxx" }
	"""

	try:
		login_data = request.get_json() 

		# obtain user data corresponding to input login credentials provided
		doc = users_collection.find_one({'username': login_data['username']})  

		# if username exists and input password matches user password,
		# create and return an access token (identity=username) 
		if doc:
			hashed_input_password = hashlib.sha256(login_data['password'].encode("utf-8")).hexdigest()
			if hashed_input_password == doc['password']:
				access_token = create_access_token(identity=doc['username'])
				result = { "accessToken" : access_token }
				return Response(json.dumps(result), status=201, mimetype="application/json")
			
			# input password does not match user password
			else:
				error_message =  { "msg" : "Username or password is incorrect" }
				return Response(json.dumps(error_message), status=401, mimetype="application/json")
		
		# input username is not found in users collection
		else:
			error_message =  { "msg" : "Username or password is incorrect" }
			return Response(json.dumps(error_message), status=401, mimetype="application/json")
	
	except Exception as ex:
		print(ex)
		error_message =  { "msg" : "Cannot log in to account. Please try again" }
		return Response(json.dumps(error_message), status=500, mimetype="application/json")


@auth_api.get("/profile")
@jwt_required(optional=False)
def profile():

	"""
	Obtain profile data
	"""
	
	try:
		# obtain current user's username (identity=username)
		current_user = get_jwt_identity() 
		doc = users_collection.find_one({'username' : current_user})
		if doc:
			return Response(json.dumps(doc, default=str), status=200, mimetype="application/json")
		else:
			error_message = { "msg" : "Failed to fetch user credentials" }
			return Response(json.dumps(error_message), status=401, mimetype="application/json")
		
	except Exception as ex:
		print(ex)
		error_message =  { "msg" : "Cannot load profile details. Please try to log in again" }
		return Response(json.dumps(error_message), status=500, mimetype="application/json")

@auth_api.post("/logout")
def logout():
	logout_message =  { "msg" : "Successfully logged out" }
	response = Response(json.dumps(logout_message), status=200, mimetype="application/json")
	unset_jwt_cookies(response)
	return response
