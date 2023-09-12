import hashlib
import random
import string

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

if __name__ == "__main__":
    password = 'password'
    password_hash = generate_hash(password)
    print(verify_password('piton',password_hash)) # coba dengan password salah
    print(verify_password('password',password_hash)) # coba dengan password yang benar
    print(get_random_string(8))
