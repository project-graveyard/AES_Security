# package to encrypt file with AES standard
import pyAesCrypt

# glob is a filename globbing utility, needed to change the file names with regex
# FUNCTIONS
# escape(pathname) - escape all special characters
# glob(pathname, *, recursive=False) - returns a list of path matching a pathname pattern
import glob

# os - runs os routines (depends on the system you are on)
# sys - provides access to some objects used or maintained by the interpreter and to functions that interact strongly with the interpreter.
import os
import sys


# Clear function
clf = 'clear' if os.name == 'posix' else 'cls'
def clear(): return os.system(clf)


# List directory function
listdir_val = 'ls' if os.name == 'posix' else 'dir'
def listdir(): return os.system(listdir_val)


# Main screen for script control
def mainScreen():
    action = 1
    while action:
        clear()

        # get current directory
        curDir = os.getcwd()

        # Print welcome message
        print('Welcome To The AES Security Manager\nEncrypt and/or decrypt your files...')
        print('-'*50)
        print('[1] Change Current Directory')
        print('[2] Encrypt / Decrypt Single File')
        print('[3] Encrypt / Decrypt Recursively')
        print('[0] Exit')
        print('-'*50)
        print(' >> Current directory: ' + curDir + '\n')
        try:
            action = int(input(' >> Enter option: '))
        except ValueError:
            print('\n[E] Error: Type option between 0 - 3.\n')
            input(' >> Press enter to continue...')
            mainScreen()

        # ------------------- Begin actions ----------------------
        if action == 1:
            mainShell() 	# change directory
        if action == 2:
            print(cryptOne(''))			# Encrypt single file
            input(' >> Press enter to continue...')
        if action == 3:
            re = cryptAll('')
            if re and re != None:
                print(re)		# Encrypt recursively
            input(' >> Press enter to continue...')
        if action == 0:
            sys.exit()			# Exit pyRED


# Open a shell for directory change
def mainShell():
    '''
    Creates a shell environment to change current directory, encrypt or decrypt files
    '''
    clear()
    curDir = os.getcwd()
    # display instructions
    print('[!] Shell open.\n')
    print('(i) Instructions:')
    print('		*  "cd <directory name>" to change to new directory')
    print('		*  "cd .." to go one level up the directory')
    print('		*  Use "ls" or "dir" to list directory.')
    print('		*  Enter "encrypt" to encrypt a file in the current directory')
    print('		*  Enter "decrypt" to encrypt a file in the current directory')
    print('		*  Enter "encrypt all" to encrypt all files in the current directory')
    print('		*  Enter "decrypt all" to decrypt all files in the current directory')
    print('[0] Go Back\n')
    print(' >> Current directory: ' + curDir + '\n')
    action = 1
    while action:
        action = input(' >> ')

        # if action == '0' break else convert to lower case
        if action == '0':
            break

        if action == 'encrypt' or action == 'decrypt':
            print(cryptOne(action))
            input(' >> Press enter to continue...')
            mainScreen()
        elif action == 'encrypt all':
            action = 'encrypt'
            re = cryptAll(action)
            if re and re != None:
                print(re)
            input(' >> Press enter to continue...')
            mainScreen()
        elif action == 'decrypt all':
            action = 'decrypt'
            re = cryptAll(action)
            if re and re != None:
                print(re)
            input(' >> Press enter to continue...')
            mainScreen()
        elif action[:2] == 'cd':
            try:
                print(action[3:])
                os.chdir(action[3:])
                curDir = os.getcwd()
                print('\n >> Current directory: ' + curDir + '\n')
            except:
                print('\nError: Unable to enter directory.\n')
		# add command to list directory
        elif action[:2] == 'ls' or action[:3] == 'dir':
            listdir()
        else:
            print("\nInvalid command, try again!\n")
    mainScreen()


# Encrypt / Decrypt individual file
def cryptOne(action, password="", file=""):
    if not action:
        action = input('\n >> Would you like to Encrypt (1) or Decrypt (2)? ')

    if action == '1' or action == 'encrypt':
        action = 'encrypt'
    elif action == '2' or action == 'decrypt':
        action = 'decrypt'
    else:
        return '\nInvalid input: Type 1 for Encryption or 2 for Decryption.\n'

    print('\n >> Beginning ' + action + ' process.')

    # check if password is entered
    if not password:
        # Get the password
        try:
            password = input(
                '\n >> Enter password for encryption/decryption:\n ')
        except:
            return '\nError: Did you enter a password at all?\n'
    if not file:
        listdir()
        try:
            file = str(input('\n >> Enter filename to encrypt/decrypt: '))
        except:
            return '\nError: File not found. Try again.\n'

    # check if file name is correct | if password is entered | the file is in the current path
    if len(file) < 1 or len(password) < 1 or not os.path.isfile(file):
        return '\nError: Enter correct file/password.\n'

    if action == 'encrypt':
        # add '.aes' to filename
        newfile = file + '.aes'
    if action == 'decrypt':
        # remove '.aes' from filename
        newfile = os.path.splitext(file)[0]
    bufferSize = 64 * 1024
    try:
        if action == 'encrypt':
            pyAesCrypt.encryptFile(file, newfile, password, bufferSize)
            os.remove(file)
        if action == 'decrypt':
            try:
                pyAesCrypt.decryptFile(file, newfile, password, bufferSize)
                os.remove(file)
            except ValueError:
                return ' >> Error: Wrong password!\n'
        return '\n[!] Success - ' + action + ': ' + newfile + '\n'
    except:
        return '\nError: Encryption/decryption failed, try again.\n'


# Encrypt | Decrypt recursively
def cryptAll(action, password="", folder=""):
    if not action:
        action = input('\n >> Would you like to Encrypt (1) or Decrypt (2)? ')

    if action == '1' or action == 'encrypt':
        action = 'encrypt'
    elif action == '2' or action == 'decrypt':
        action = 'decrypt'
    else:
        return '\nError: Type 1 for Encryption or 2 for Decryption.\n'

    print('\n  >> Beginning recursive ' + action + ' process.')
    if not password:
        try:
            password = str(
                input('\n >> Enter password for encryption/decryption:\n '))
        except:
            return '\nError: Did you enter a password at all?\n'
    if not folder:
        listdir()
        try:
            print('\n >> Enter folder to recursively encrypt/decrypt ')
            folder = str(
                input('    or * for current directory (including all files): '))
        except:
            return '\nError: Folder not found. Try again.\n'

    if len(password) < 1 or len(folder) < 1:
        return '\nError: Enter correct folder/password.\n'

    if folder == '*':
        folder = os.getcwd()
    else:
        folder = os.path.join(os.getcwd(), folder)
    if not os.path.isdir(folder):
        return '\nError: Location is not a directory.\n'
    else:
        print('\n >> Begin ' + action + ' of directory: ' + folder + '\n')

    # Begin recursive encryption/decryption

    # set buffer size to 64KB
    bufferSize = 64 * 1024
    fd = folder + '/**/*' if os.name == 'posix' else folder + '\\**\*'

    # get the paths of each file in the folder
    for x in glob.glob(fd, recursive=True):
        fullpath = os.path.join(folder, x)
        if action == 'encrypt':
            newfile = os.path.join(folder, x + '.aes')

        if action == 'decrypt':
            try:
                newfile = os.path.join(folder, os.path.splitext(x)[0])
            except:
                newfile = 'decrypted.' + x

        if os.path.isfile(fullpath):
            # Encrypt / Decrypt
            print(' >> Original: \t' + fullpath + '')
            if action == 'encrypt':
                try:
                    pyAesCrypt.encryptFile(
                        fullpath, newfile, password, bufferSize)
                    print('\nEncrypted: \t' + newfile + '\n')
                    os.remove(fullpath)
                except:
                    print('\nError: Unable to encrypt.\n')
            if action == 'decrypt':
                try:
                    pyAesCrypt.decryptFile(
                        fullpath, newfile, password, bufferSize)
                    print('\nDecrypted: \t' + newfile + '\n')
                    os.remove(fullpath)
                except ValueError:
                    return '\nError: Wrong password!\n'


if __name__ == '__main__':
    mainScreen()
