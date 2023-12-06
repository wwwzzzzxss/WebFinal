####################################################
#  Network Programming - Unit 7 Remote Procedure Call          
#  Program Name: 7-RESTClient.py                                      			
#  This program is a simple REST API client.           		
# Install requests: pip3 install requests
#  2021.08.14                                             									
####################################################
import sys
import requests
import json

def main():
	URL = 'http://127.0.0.1:8888/user/' + str(sys.argv[1])
	if(len(sys.argv) < 1):
		print("Usage: python capi.py (signin or signup)")
		exit(1)
	elif((sys.argv[1]) == "signup"):
		new_user = input('User: ')
		new_password = input('Password: ')
		new_dict = {}
		new_dict["user"] = new_user
		new_dict["password"] = new_password
		response = requests.post(URL, json=new_dict)
		response_data = json.loads(response.text)
		if(response.status_code == 200):
			print("signup sucess")
			print("welcome new user: ",response_data['user'])
		elif(response.status_code == 409):
			print("signup fail")
			print(response_data['error'])
		elif(response.status_code == 415):
			print("signup fail")
			print(response_data['error'])
	elif(sys.argv[1] == "signin"):
		check_user = input('User: ')
		check_password = input('Password: ')
		new_dict = {}
		new_dict["user"] = check_user
		new_dict["password"] = check_password
		response = requests.post(URL, json=new_dict)
		response_data = json.loads(response.text)
		#print(response.headers)	
		if(response.status_code == 200):
			print("signin sucess")
			print("welcome user: ",response_data['user'])
		elif(response.status_code == 401):
			print(response_data['error'])
		elif(response.status_code == 415):
			print(response_data['error'])
	else:
		print("Usage: python capi.py (signin or signup)")

if __name__ == '__main__':
	main()