from flask import Flask, json, request, jsonify

PORT = 8888
COMP_FILE = "user.json"
DICUS_FILE = 'discuss.json'
COMPANIES = []

def find_next_id():
    return max(comp["id"] for comp in COMPANIES) + 1
API = Flask(__name__)

@API.post("/user/signup")
def register():
    if request.is_json:
        global COMPANIES
        with open(COMP_FILE) as fp:
            COMPANIES = json.load(fp)
        new = request.get_json()
        new["id"] = find_next_id()
        for i in COMPANIES:
            if(i['user'] == new["user"]):
                return {"error": "user name already exists"}, 409
        COMPANIES.append(new)
        with open(COMP_FILE, 'w') as wfp:
            json.dump(COMPANIES, wfp)
        return new, 200
    else:
        return {"error": "Request must be JSON"}, 415

@API.post("/user/signin")
def check_user():
    if request.is_json:
        with open(COMP_FILE) as fp:
            COMPANIES = json.load(fp)
        new = request.get_json()
        for i in range(len(COMPANIES)):
            if(COMPANIES[i]['user'] == new['user']):
                if(COMPANIES[i]['password'] == new['password']):
                    new['id'] = COMPANIES[i]['id']
                    return new,200
                else:
                    return {"error":"review username and password again"},401 
        return {"error":"review username and password again"},401
    else:
    	return {"error": "Request must be JSON"}, 415

def main(): 
    API.run(host='0.0.0.0', port=PORT, debug=True)	

# end of main

if __name__ == '__main__':
	main()

