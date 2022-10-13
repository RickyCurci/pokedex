from flask import *
from random import *
import time 
import json 


def genWallet(owner, nickname, password):
	idp = ""; alphabet = "abcdefghilmnopqrstuvzxyjkw1234567890[#=)";
	for i in range(0,17): 
		idp += alphabet[randint(0,len(alphabet)-1)]
	
	contract = { "owner": owner, 
		"nickname": nickname, 
		"password": password, 
		"id": idp, 
		"timestamp": time.strftime("%d/%m/%y"), 
		"counter": "1 "+time.strftime("%d/%m/%y"), 
		"pokedex": []

	}

	f = open("wallet.json", "r"); c = json.load(f); c["contracts"][str(len(c["contracts"])+1)] = contract
	f = open("wallet.json", "w"); json.dump(c,f,indent = len(c["contracts"]))


def genRandomSentece(): 
	alphabet = "abcdefghilmnopqrstuvzxyjkw1234567890[#=)"; s = ""
	f = open("pokedex.json","r"); j = json.load(f);
	for i in range(0,21): 
		s += alphabet[randint(0,len(alphabet))] 

	s = list(s); s[randint(0,len(s))] = " "+j["pokemon"][randint(0,len(j["pokemon"]))]["name"]+" "
	s = "".join(s); print(s)

	f = open("code.json","r"); j = json.load(f); j["code"].append(s)
	f = open("code.json","w"); json.dump(j,f,indent = len(j["code"]))

def RequestCode(idp,password): 
	fx = open("wallet.json", "r"); jc = json.load(fx);
 	

	for i in jc["contracts"]:

		if jc["contracts"][str(i)]["id"] == idp and jc["contracts"][str(i)]["password"] == password: 
			counter = jc["contracts"][str(i)]["counter"].split(" ")
			counter[1] = counter[1].split("/")
			
			data = jc["contracts"][str(i)]["timestamp"].split("/"); 
			actual_data = time.strftime("%d/%m/%y"); actual_data = actual_data.split("/")
			
			if actual_data[0] == counter[1][0] and int(actual_data[1]) - int(counter[1][1]) == 1 and actual_data[2] == counter[1][2] and int(counter[0]) == int(actual_data[1]) - int(data[1]): 
				genRandomSentece()

				counter[0] = str(int(counter[0])+1); counter[1] = time.strftime("%d/%m/%y"); jc["contracts"][str(i)]["counter"] = " ".join(counter)
				fx = open("wallet.json", "w"); json.dump(jc,fx,indent = len(jc["contracts"]))
			else: 

				print("> invalid time. WAIT 1 MONTH")

def collectPokemon(idp,psw, code): 
	f = open("pokedex.json","r"); pokedex = json.load(f)
	fx = open("wallet.json","r"); wallet = json.load(fx)
	fy = open("code.json","r"); sentece = json.load(fy)

	code = code.split(" "); code.remove(code[0]); code.remove(code[1])

	for i in pokedex["pokemon"]: 
		if code[0] == i["name"]: 
			for j in wallet["contracts"]:
				if wallet["contracts"][j]["id"] == idp and wallet["contracts"][j]["password"] == psw: 
					for y in sentece["code"]: 
						y = y.split(" "); y.remove(y[0]); y.remove(y[1])
						if code[0] == y[0]:
							if len(wallet["contracts"][j]["pokedex"]) != 0: 
								for l in wallet["contracts"][j]["pokedex"]: 

									if l["name"] == code[0]: 
										print("> already collect"); break

									wallet["contracts"][j]["pokedex"].append(i); 
									fx = open("wallet.json","w"); json.dump(wallet,fx,indent = len(wallet)); break
							else: 
								wallet["contracts"][j]["pokedex"].append(i); 
								fx = open("wallet.json","w"); json.dump(wallet,fx,indent= len(wallet))
	





def searchByName(name):
	name = name.lower(); name = list(name); name[0] = name[0].upper(); name = "".join(name); print(name)
	f = open("pokedex.json","r"); j = json.load(f);

	for i in j["pokemon"]: 
		if i["name"] == name: 
			print(i)


app = Flask(__name__)
@app.route("/")
def home(): 
	#return render_template('index.html')
	return """

		<!DOCTYPE html>
		<html>
		<head>
			
			<link rel="preconnect" href="https://fonts.googleapis.com"> 
			<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> 
			<link href="https://fonts.googleapis.com/css2?family=M+PLUS+1+Code&display=swap" rel="stylesheet">
					
			<meta charset="utf-8">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<title>pokedex</title>
		</head>
		<style type="text/css">
			button {height:10%;width:40%;border-radius:10px 10px;}
			a {font-size:40px;font-family:'M PLUS 1 Code',sans-serif;text-decoration:none;color:white;}
		</style>
		<body>
			<button style="position:absolute;top:20%;left:30%;background:#1a0853;"><a href="http://127.0.0.1:5001/genWallet"> genWallet </a></button>
			<button style="position:absolute;top:30%;left:30%;background:#385c6a;"><a href="http://127.0.0.1:5001/requestCode"> requestCode </a></button>

		</body>
		</html>





	"""
@app.route("/genWallet")
def index(): 

	return """
	<html>
		<style> 
			input {position:absolute;left:35%;width:30%;height:5%;font-size:20px}
		</style>
		<form action="http://127.0.0.1:5001/genWallet" method="post">

			<input style="top:20%" type="text" name="owner"><br>
			<input style="top:30%" type="text" name="nickname"><br>
			<input style="top:40%" type="text" name="password"><br>
			
			<input style="top:50%" type="submit" value="singup">

		</form>
	</html>
	"""

@app.route("/genWallet",methods=["POST"])
def singup():

	if request.method == "POST": 
		result = request.form
		genWallet(result["owner"],result["nickname"],result["password"])

		f = open("wallet.json", "r"); c = json.load(f); 
		k = list(c["contracts"].keys()); p = c["contracts"][k[-1]]
		return """
		<html> 
			<link rel="preconnect" href="https://fonts.googleapis.com"> 
			<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> 
			<link href="https://fonts.googleapis.com/css2?family=M+PLUS+1+Code&display=swap" rel="stylesheet">
			<style>

				.response-msg { position:relative;top:20%;font-family: 'M PLUS 1 Code', sans-serif; font-size:20px;}

			</style>
			<body>
				<p class="response-msg" align="center"> the id for """+p["nickname"]+"""' is """+p["id"]+"""</p>
			</body>
		</html>
		"""

app.run(port=5001)
#genRandomSentece()
#collectPokemon("r=a41nasy7e51v8v8","27Cinque2005","nmhj3wkb49[zv10g Wartortle 5s9j")
#RequestCode("r=a41nasy7e51v8v8","27Cinque2005")
#genWallet("Riccardo Curci","RickyCurci","27Cinque2005")

