import socket 
import threading 
from datetime import datetime 
import sqlite3

HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'exit'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050 
ADDR = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, conn):
	message = msg.encode(FORMAT) 
	length = str(len(msg)).encode(FORMAT)
	length += b' ' * (HEADER - len(length))
		
	conn.send(length)
	conn.send(message)

def parse(s):
	i=0
	while i+1 < len(s) and s[i] != '_':
		i+=1
	return s[:i], s[i+1:]

def create_user(param):
	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor()

	param1, param = parse(param) 
	param2, param = parse(param)
	param3, param = parse(param)
	
	
	cur.execute(f"SELECT username FROM users WHERE username = \"{param1}\";")
	if cur.fetchone():
		cur.close()
		dbconn.close()
		return "Username already exists" # user already exists  
	else:	 
		date = datetime.now().strftime("%Y-%m-%d")
		cur.execute(f"INSERT INTO users(username,password,role,created_date,tests_taken,total_score,average_score) VALUES(\"{param1}\",\"{param2}\",\"{param3}\",\"{date}\",0,0,0);")

		dbconn.commit()
		
	cur.close()
	dbconn.close()
	
	return "success" #user added 

def auth_user(comm):
    name, comm = parse(comm)
		
    dbconn = sqlite3.connect("database.db")
    cur = dbconn.cursor()

    cur.execute(f"SELECT password FROM users WHERE username = \"{name}\";")		

    res = cur.fetchone()
    if res:
        s = ""
        for i in res[0]:
            if i == ' ':
                s+="_"
            else:
                s+=str(i) 

        return s
    else:
        return "User not found"

def get_user(comm): 
	name, comm = parse(comm)	
	
	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor()

	cur.execute(f"SELECT username,password,role,created_date,tests_taken,total_score,average_score FROM users WHERE username = \"{name}\";")
	
	user_list = cur.fetchone()
	user_string = ""

	for i in user_list: 
		user_string += str(i) + '_' 
	return user_string 

def update_user(comm):
	username, comm = parse(comm)
	score, comm = parse(comm)
	max_score, comm = parse(comm)
	
	score, max_score = int(score), int(max_score)

	percentage = (score/max_score)*100

	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor()

	cur.execute(f"UPDATE users SET tests_taken = tests_taken+1 WHERE username = \"{username}\";")
	cur.execute(f"UPDATE users SET total_score = total_score+{percentage} WHERE username = \"{username}\";") 
	cur.execute(f"UPDATE users SET average_score = total_score/tests_taken WHERE username = \"{username}\";")

	dbconn.commit()

	cur.close()
	dbconn.close()

def get_all_users(conn):
	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor()

	cur.execute("SELECT username,role,created_date,tests_taken,total_score,average_score FROM users ORDER BY average_score DESC LIMIT 100;")

	user_array = cur.fetchone()

	while user_array:
		user_string = ""
		for i in user_array:
			user_string += str(i) + "_"

		send(user_string, conn)

		user_array = cur.fetchone() 

	return "done"

def save_analytics(comm):
	name, comm = parse(comm)
	test_name, comm = parse(comm)
	score, comm = parse(comm)
	max_score, comm = parse(comm)
	percentage, comm = parse(comm)
	test_title, comm = parse(comm)
	time, comm = parse(comm)

	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor()

	cur.execute(f"INSERT INTO records(user, test_name, score, max_score, percentage, test_title, timestamp) VALUES(\"{name}\",\"{test_name}\",\"{score}\",\"{max_score}\",\"{percentage}\",\"{test_title}\", \"{time}\");")

	dbconn.commit()		

	cur.close()
	dbconn.close()

def get_analytics(conn):

	dbconn = sqlite3.connect("database.db")
	cur = dbconn.cursor() 

	cur.execute("SELECT user, test_name, score, max_score, percentage, test_title, timestamp FROM records LIMIT 1000;") 
	
	record_array = cur.fetchone() 

	while record_array:
		record_string = "" 
		for i in record_array:
			record_string += str(i) + "_"
		 
		send(record_string, conn) 
		record_array = cur.fetchone() 
	
	cur.close()
	dbconn.close()

	return "done"

def get_tests_by_user(name, conn):
    dbconn = sqlite3.connect("database.db")
    cur = dbconn.cursor() 
    
    name = name[:-1]
    cur.execute(f"SELECT user, test_name, score, max_score, percentage, test_title, timestamp FROM records WHERE user = \"{name}\" LIMIT 1000;") 
	
    record_array = cur.fetchone() 

    while record_array:
        record_string = "" 
        for i in record_array:
            record_string += str(i) + "_"
		 
        send(record_string, conn) 
        record_array = cur.fetchone() 
	
    cur.close()
    dbconn.close()

    return "done"

def command(comm, conn):
	s, comm = parse(comm) 

	if s == "CREATEUSER":
		return create_user(comm)
	elif s == "AUTHUSER": 
		return auth_user(comm)
	elif s == "GETUSER":
		return get_user(comm)
	elif s == "UPDATEUSER":
		update_user(comm)
	elif s == "GETALLUSERS":
		return get_all_users(conn)
	elif s == "SAVEANALYTICS":
		save_analytics(comm)
	elif s == "GETANALYTICS":
		return get_analytics(conn)
	elif s == "GETTESTSBYUSER":
		return get_tests_by_user(comm, conn)
	
def handle_client(conn, addr):
	
	connected = True 

	while connected:
		msg_length = conn.recv(HEADER).decode(FORMAT)
		if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(HEADER).decode(FORMAT)		

			if msg==DISCONNECT_MESSAGE:
				connected = False 
			else:	
				exit_code = command(msg, conn)
				if exit_code:
					send(exit_code, conn)
	conn.close() 

def start():
	server.listen()

	print("SERVER STARTED")

	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target = handle_client, args = (conn, addr))
		thread.start()

start()
server.close()
