from cryptography.fernet import Fernet
import os,gnupg,getch

def imposter():
	return open('auth/token', 'r').read()

def getPass():
	password = ''
	while True:
		x = getch.getch()
		# x = msvcrt.getch().decode("utf-8")
		if x == '\r' or x == '\n':
			break
		print('*', end='', flush=True)
		password +=x
	return password

def gnu_encrypt():
	exists = os.path.exists('auth/tokenkey.asc') and os.path.exists('auth/token')
	if exists == False:
		gpg = gnupg.GPG(gnupghome='auth/')
		#Takes a email and password as input, password is textfield anonimzed
		name_email = input('Email: ')
		print('Password: ', end='')
		passphrase = getPass()
		#generate keys and wrtie to <filename>.asc
		input_data = gpg.gen_key_input(name_email=name_email, passphrase=passphrase)
		key = gpg.gen_key(input_data)
		print(key)
		ascii_armored_public_keys = gpg.export_keys(str(key), passphrase=passphrase)
		ascii_armored_private_keys = gpg.export_keys(str(key), True, passphrase=passphrase)
		with open('auth/tokenkey.asc', 'w') as stream:
			stream.write(ascii_armored_public_keys)
			stream.write(ascii_armored_private_keys)
		#Load key data and proceed with encryption
		key_data = open('auth/tokenkey.asc').read()
		import_result = gpg.import_keys(key_data)
		public_keys = gpg.list_keys()
		fingerprint = public_keys[0]['fingerprint']
		with open('auth/token', 'rb') as stream:
			status = gpg.encrypt_file(stream, fingerprint, output='auth/encrypted_token.gpg')
	else:
		print('Key and Token already exist, starting')

def gnu_decrypt():
	print('Password: ', end='')
	passphrase = getPass()
	gpg = gnupg.GPG(gnupghome='auth/')
	key_data = open('auth/tokenkey.asc').read()
	import_result = gpg.import_keys(key_data)
	public_keys = gpg.list_keys()
	fingerprint = public_keys[0]['fingerprint']
	with open('auth/encrypted_token.gpg', 'rb') as stream:
		decrypted_data = gpg.decrypt_file(stream, fingerprint, passphrase=passphrase)
	return decrypted_data

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
