#Implementation of the RSA encryption algorithm with random key generation in Python
# without using ready-made libraries (cryptography or PyCrypto)
#-----------------------------------------------------------------------------------

from random import randint, choice


#Search for prime numbers using the "Sieve of Eratosthenes"
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def generate_primes(end):
    if end < 3:
        return [1, 1, 1]

    #filling an array with prime numbers
    tmp = [num for num in range(2, end + 1) if is_prime(num)]
    
    #selection of variables for key generation
    p, q = tmp.pop(randint(0, len(tmp) - 1)), tmp.pop(randint(0, len(tmp) - 1))
    return p, q, [num for num in range(2, end + 1) if is_prime(num)]

def exponent_generate(array, phi):
    try:
        tmp_ar = [num for num in array if num < phi and phi % num != 0]
        return choice(tmp_ar)
    except:
        print("Oops no matching exponent numbers")
        return None

def d_generate(limit, e, phi):
    try:
        tmp_ar = [num for num in range(limit**2) if (num * e) % phi == 1]
        return choice(tmp_ar)
    except:
        print("Oops no matching d numbers")
        return None


def generate_keys(limit=1024):

    #Check whether invalid values ​​were received at the input of the function
    try:
        if limit is None or type(limit) is str or limit < 15:
            raise

    except:
        print("There was an error in key generation!\n"
              "Generation will be done with default values")
        return generate_keys()
    
    p, q, primes = generate_primes(limit)
    n_mod = p * q
    phi = (p - 1) * (q - 1)
    e = exponent_generate(primes, phi)
    d = d_generate(limit, e, phi)

    try:
        if all([e, d, n_mod]):
            return (e, n_mod), (d, n_mod)
        
        raise

    except:
        print("There was an error in key generation!\n"
              "Generation will be done with default values")
        
        return generate_keys()


public_key, private_key = generate_keys() #Generation of keys on the set numerical boundary. Default: 1024
print(f"Public key: {public_key} \nPrivate key: {private_key}") #Print keys

# Text encryption
def encrypt(message, public_key):
    e, n_mod = public_key
    ciphertext = [pow(ord(char), e, n_mod) for char in message]
    return ciphertext

# Message decryption
def decrypt(ciphertext, private_key):
    d, n_mod = private_key
    plaintext = [chr(pow(char, d, n_mod)) for char in ciphertext]
    return ''.join(plaintext)

#Tests
message = "The five boxing wizards jump quickly.?!@№$%&^(\|/){+-_=}[<`~>] 1234567890"

chiphertext = encrypt(message, public_key)
print(f'Chiphertext: {chiphertext}\n')

plaintext = decrypt(chiphertext, private_key)
print(f'Plaintext: {plaintext}')