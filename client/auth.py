import socket 
import json
import os
import hashlib
from datetime import datetime
# CONNECTING TO THE SERVER AND SENDING A MESSAGE

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "exit"
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)

def send(msg, client):
	message = msg.encode(FORMAT) 
	length = str(len(msg)).encode(FORMAT)
	length += b' ' * (HEADER - len(length))

	client.send(length)
	client.send(message)

def recv(client):
	length = client.recv(HEADER).decode(FORMAT)
	if length: 
		length = int(length)
		msg = client.recv(length).decode(FORMAT)
		
		return msg
	return None
	
# USER RELATED 

def parse(s): # gets a string and returns and array containing the words in it
	arr = []
	aux = ""
	for i in s:
		if i == "_":
			arr.append(aux)
			aux = ""
		else:
			aux += i
	return arr

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password, role="student"):
	try:
		password = hash_password(password)

		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)

		send(f"CREATEUSER_{username}_{password}_{role}_", client)

		msg = recv(client)

		if msg == "success":
			return True
		else: 
			raise Exception(msg)
	except Exception as e:
		print(f"Error creating user: {e}")
		return False

def authenticate_user(username, password):       
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)		

		send(f"AUTHUSER_{username}_", client)
		dbpassword = recv(client)

		password = hash_password(password)

		if dbpassword == "User not found": 
			raise Exception("User not found")

		if password == dbpassword: 
			send(f"GETUSER_{username}_", client) # get a dictonary containing information about the user
			user_string = recv(client)
			
			user_array = parse(user_string)

			user_data = {
					"username" : user_array[0],
					"password" : user_array[1],
					"role" : user_array[2],
					"created_date" : user_array[3],
					"stats" :   {
						"tests_taken": int(user_array[4]),
						"total_score": float(user_array[5]),
						"average_score": float(user_array[6])
					}
				 }

			return user_data
	except Exception as e:
		print(f"Error authenticating user: {e}")
		return None
    
def update_user_stats(username, score, max_score):
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)     
        
		send(f"UPDATEUSER_{username}_{score}_{max_score}_", client)		
 
		return True
	except Exception as e:
		print(f"Error updating user stats: {e}")
		return False
    
def get_all_users():
	users = []

	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)
		
		send("GETALLUSERS_", client)
		user_string = recv(client)
		while user_string != "done":
			user_array = []
			s = ""
			for i in user_string:
				if i == "_":
					user_array.append(s)
					s = ""
				else: 
					s+=str(i)

			user_data = {
				"username" : user_array[0],
				"role" : user_array[1],
				"created_date" : user_array[2],
				"stats" : {
					"tests_taken" : int(user_array[3]),
					"total_score" : float(user_array[4]),
					"average_score" : float(user_array[5])
					}
				} 
			users.append(user_data)

			user_string = recv(client)
		return users
	except Exception as e:
		print(f"Error getting users: {e}")
		return None    	
    
def save_analytics_data(data):
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)

		user, test_name, score, max_score, percentage, test_title, time = data["user"], data["test_name"], data["score"], data["max_score"], data["percentage"], data["test_title"], data["time"]

		s = f"{user}_{test_name}_{score}_{max_score}_{percentage}_{test_title}_{time}_"
		send(f"SAVEANALYTICS_{s}", client)

	except Exception as e:
		print(f"Error saving analytics: {e}")
		return False

def get_analytics_data():
    
	try:
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(ADDR)
		
		send("GETANALYTICS_", client)

		res = []
		analytics_string = recv(client) 

		while analytics_string != "done":
			analytics_array = [] 
			s = "" 
			for i in analytics_string:
				if i == "_":
					analytics_array.append(s)
					s = "" 
				else: 
					s+=i
			analytics_string = recv(client)

			analytics_data = {
					"user" : analytics_array[0], 
					"test_name" : analytics_array[1], 
					"score" : int(analytics_array[2]), 
					"max_score" : int(analytics_array[3]), 
					"percentage" : float(analytics_array[4]), 
					"test_title" : analytics_array[5],
					"time" : analytics_array[6]
					}	
			res.append(analytics_data)
		return {"records" : res}

	except Exception as e:
		print(f"Error getting analytics: {e}")
		return {"records": []}
