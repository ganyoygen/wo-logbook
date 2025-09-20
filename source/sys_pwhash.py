import hashlib
import random
import string
import base64

def get_random_string(length):
    '''
    ascii_lowercase	Contain all lowercase letters
    ascii_uppercase	Contain all uppercase letters
    ascii_letters	Contain both lowercase and uppercase letters
    digits	        Contain digits ‘0123456789’.
    punctuation	    All special symbols !”#$%&'()*+,-./:;<=>?@[\]^_`{|}~.
    whitespace	    Includes the characters space, tab, linefeed, return, formfeed, and vertical tab [^ \t\n\x0b\r\f]
    printable	    characters that are considered printable. This is a combination of constants digits, letters, punctuation, and whitespace.
    '''
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str

def generate_hash(password):   
    m = hashlib.sha256(password.encode())
    return m.hexdigest()

def verify_password(password,password_hash):
    if generate_hash(password) == password_hash:
        return True
    return False

def encode(original_string):
    try: 
        string_bytes = original_string.encode('utf-8')
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string
    except: return ""

def decode(encoded_string):
    try: 
        encoded_bytes = encoded_string.encode('utf-8')
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except: return ""

if __name__ == "__main__":
    password = 'password'
    password_hash = generate_hash(password)
    print('pw_hash:',password_hash)
    print('pw_salah:',verify_password('piton',password_hash)) # coba dengan password salah
    print('pw_benar:',verify_password('password',password_hash)) # coba dengan password yang benar
    print('ran_string:',get_random_string(8))
    print("")
    pwd_encode = encode(password)
    print('pwd_encode:',pwd_encode)
    print('pwd_string:',decode(pwd_encode))
