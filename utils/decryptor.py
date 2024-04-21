from cryptography.fernet import Fernet
import json,sys

defaults=json.load(open('defaults.json', 'r'))

def imposter():
	token_file = 'auth/token_'+defaults['ego']
	try: 
		f = open(token_file, 'r')
		return f.read()
	except IOError or OSError:
		print("Token file related to ego does not exist")
		print("Select a proper ego or fix / create the token file")
		sys.exit()

#These methods are unmaintained / unsupported
#I support full on file encryption either by being built in
#Or external systems, could not care less lol.
def decrypted_token():
	keyfile = 'auth/tokenkey.key'
	token_file_encrypted = 'auth/encrypted-token'
	with open(keyfile, 'rb')as tokenkeys:
		tokenkeys = tokenkeys.read()
	fernet = Fernet(tokenkeys)

	with open(token_file_encrypted, 'rb')as encrypted:
		encrypted = encrypted.read()
	decrypted = fernet.decrypt(encrypted)

	return decrypted.decode()

def decrypted_web_token():
	keyfile = 'auth/webtokenkey.key'
	token_file_encrypted = 'auth/encrypted-web-server-token'
	with open(keyfile, 'rb')as tokenkeys:
		tokenkeys = tokenkeys.read()
	fernet = Fernet(tokenkeys)

	with open(token_file_encrypted, 'rb')as encrypted:
		encrypted = encrypted.read()
	decrypted = fernet.decrypt(encrypted)

	return decrypted.decode()

def decrypted_client_id():
	keyfile = 'auth/clientkey.key'
	token_file_encrypted = 'auth/encrypted-client-id'
	with open(keyfile, 'rb')as tokenkeys:
		tokenkeys = tokenkeys.read()
	fernet = Fernet(tokenkeys)

	with open(token_file_encrypted, 'rb')as encrypted:
		encrypted = encrypted.read()
	decrypted = fernet.decrypt(encrypted)

	return decrypted.decode()
