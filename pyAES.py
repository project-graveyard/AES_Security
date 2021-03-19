import pyAesCrypt
import glob
import os, sys
import subprocess

# Clear function
clf = 'clear'
if os.name == 'posix': clf = 'clear'
if os.name == 'nt': clf = 'cls'
clear = lambda: os.system(clf)

# List directory function
if os.name == 'posix': ldf = 'ls'
if os.name == 'nt': ldf = 'dir'
listdir = lambda: os.system(ldf)

# Main screen for script control
def mainScreen():
	action = 1
	while action:
		clear()
		curDir = os.getcwd()
		print('Welcome To The AES Security Manager\nEncrypt and/or decrypt your files...')
		print('-'*50)
		print('[1] Change directory (shell)')
		print('[2] Encrypt / Decrypt single file')
		print('[3] Encrypt / Decrypt recursively')
		print('[0] Exit')
		print('-'*50)
		print(' >> Current directory: ' + curDir + '\n')
		try: action = int(input(' >> Enter option: '))
		except ValueError:
			print('\n[E] Error: Type option between 0 - 3.\n')
			input(' >> Press enter to continue...')
			mainScreen()
		# ------------------- Begin actions ----------------------
		if action == 1: mainShell()					# Change directory
		if action == 2: 
			print(cryptOne('','',''))				# Encrypt single file
			input(' >> Press enter to continue...')
		if action == 3:
			re = cryptAll('','','')
			if re and re != None: print(re)			# Encrypt recursively
			input(' >> Press enter to continue...')
		if action == 0: sys.exit()					# Exit pyRED

# Open a shell for directory change
def mainShell():
	clear()
	curDir = os.getcwd()
	print(' - Recursive En/Decryption')
	print('-'*50 + '\n')
	print('[!] Shell open.\n')
	print('[i] Browse using following commands:')
	print('    cd <directory name>')
	print('    cd ..')
	print('[i] Use ls or dir to list directory.\n')
	print('[0] Go Back\n')
	print(' >> Current directory: ' + curDir + '\n')
	action = 1
	while action:
		action = input(' >> ')
		if action == '0': break
		if action == 'encrypt' or action == 'Encrypt' or action == 'decrypt' or action == 'Decrypt':
			print(cryptOne(action,'',''))
			input(' >> Press enter to continue...')
			mainScreen()
		if action == 'encryptall' or action == 'Encryptall':
			action = 'encrypt'
			re = cryptAll(action,'','')
			if re and re != None: print(re)
			input(' >> Press enter to continue...')
			mainScreen()
		if action == 'decryptall' or action == 'Decryptall':
			action = 'decrypt'
			re = cryptAll(action,'','')
			if re and re != None: print(re)
			input(' >> Press enter to continue...')
			mainScreen()
		if action[:2] == 'cd':
			try: 
				os.chdir(action[3:])
				curDir = os.getcwd()
				print('\n >> Current directory: ' + curDir + '\n')
			except:	print('\n[E] Error: Unable to enter directory.\n')
		else:
			proc = subprocess.Popen(action, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			stdoutput = proc.stdout.read() + proc.stderr.read()
			print('\n' + stdoutput.decode())
	mainScreen()

# Encrypt / Decrypt individual file
def cryptOne(act, password, file):
	if not act: act = input('\n >> Would you like to Encrypt (1) or Decrypt (2)? ')
	if (act == '1') or (isinstance(act, str) and (act == 'Encrypt' or act == 'encrypt')): act = str('encrypt')
	elif (act == '2') or (isinstance(act, str) and (act == 'Decrypt' or act == 'decrypt')): act = str('decrypt')
	else: return '[E] Error: Type 1 for Encryption or 2 for Decryption.'
	print('\n >> Beginning ' + act + ' process.')
	if not password:
		try: password = str(input('\n >> Enter password for encryption/decryption:\n '))
		except: return '[E] Error: Did you enter a password at all?'
	if not file:
		listdir()
		try: file = str(input('\n >> Enter filename to encrypt/decrypt: '))
		except: return '[E] Error: File not found. Try again.'
	if len(file) < 1 or len(password) < 1 or not os.path.isfile(file): return '[E] Error: Enter correct file/password.\n'
	if act == 'encrypt': newfile = file + '.aes'
	if act == 'decrypt': 
		try:
			newfile = os.path.splitext(file)[0]
		except: newfile = 'decrypted.' + file
	bufferSize = 64 * 1024
	try:
		if act == 'encrypt': 
			pyAesCrypt.encryptFile(file, newfile, password, bufferSize)
			os.remove(file)
		if act == 'decrypt':
			try:
				pyAesCrypt.decryptFile(file, newfile, password, bufferSize)
				os.remove(file)
			except ValueError:
				return ' >> Error: Wrong password!\n'
		return '\n[!] Success - ' + act + ': ' + newfile + '\n'
	except:
		return '[E] Error: Encryption/decryption failed, try again.\n'

# Encrypt / Decrypt recursively
def cryptAll(act, password, folder):
	if not act: act = input('\n >> Would you like to Encrypt (1) or Decrypt (2)? ')
	if (act == '1') or (isinstance(act, str) and (act == 'Encrypt' or act == 'encrypt')): act = str('encrypt')
	elif (act == '2') or (isinstance(act, str) and (act == 'Decrypt' or act == 'decrypt')): act = str('decrypt')
	else: return '[E] Error: Type 1 for Encryption or 2 for Decryption.'
	print('\n[!] Beginning recursive ' + act + ' process.')
	if not password:
		try: password = str(input('\n >> Enter password for encryption/decryption:\n '))
		except: return '[E] Error: Did you enter a password at all?'
	if not folder:
		listdir()
		try:
			print ('\n >> Enter folder to recursively encrypt/decrypt ') 
			folder = str(input('    or * for current directory (including all files): '))
		except: return '[E] Error: Folder not found. Try again.'
	if len(password) < 1 or len(folder) < 1: return '[E] Error: Enter correct folder/password.\n'
	if folder == '*': folder = os.getcwd()
	else: folder = os.path.join(os.getcwd(), folder) 
	if not os.path.isdir(folder): return '[E] Error: Location is not a directory.\n'
	else: print('\n >> Begin ' + act + ' of directory: ' + folder + '\n')
	# Begin recursive encryption/decryption
	bufferSize = 64 * 1024
	if os.name == 'posix': fd = folder + '/**/*'
	if os.name == 'nt': fd = folder + '\\**\*'
	for x in glob.glob(fd, recursive=True):
		fullpath = os.path.join(folder, x)
		if act == 'encrypt': fullnewf = os.path.join(folder, x + '.aes')
		if act == 'decrypt':
			try: fullnewf = os.path.join(folder, os.path.splitext(x)[0])
			except: fullnewf = 'decrypted.' + x
		if os.path.isfile(fullpath):
			# Encrypt / Decrypt
			print(' >> Original: \t' + fullpath + '')
			if act == 'encrypt':
				try:
					pyAesCrypt.encryptFile(fullpath, fullnewf, password, bufferSize)
					print('[!] Encrypted: \t' + fullnewf + '\n')
					os.remove(fullpath)
				except: print('[E] Error: Unable to encrypt.\n')
			if act == 'decrypt':
				try:
					pyAesCrypt.decryptFile(fullpath, fullnewf, password, bufferSize)
					print('[!] Decrypted: \t' + fullnewf + '\n')
					os.remove(fullpath)
				except ValueError:
					return '[E] Error: Wrong password!\n'

mainScreen()
