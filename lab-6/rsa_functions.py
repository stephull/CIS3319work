from configurations import *

'''
    rsa: For RSA configurations
'''
# AKS primality test for generating p and q in RSA
c = [0] * int(math.pow(10, PRIME_LIM))
def primality_test(n):
    c[0] = 1
    for i in range(n):
        c[i+1] = 1
        for j in range(i, 0, -1):
            c[j] = c[j-1] - c[j]
        c[0] = -c[0]
    c[0] += 1
    c[n] -= 1
    i = n
    while (i > -1 and c[i] % n == 0) : i -= 1
    return True if i < 0 else False

# convert all alphabetical or non-numerical contents into digits for encryption:
# method inspired by https://umaranis.com/rsa_calculator_demo.html 
def digitize_text(m, e):
    assert m==ENC or m==DEC
    if (m == ENC):
        # e must be a resource of type string, return list
        assert type(e) == str, "RSA encryption input invalid: needs string"
        return [ord(e[i]) for i in range(len(e))]
    else:
        # e must be a resource of type list, return string
        assert type(e) == list, "RSA decryption input invalid: needs list of numeric values"
        return "".join(chr(int(e[i])) for i in range(len(e)))

# encrypt and decrypt RSA, similar to Lab 3 with RSA
# 'x' = e in encryption, d in decryption 
# AND resource = P in encryption, C in decryption
def rsacrypt(n, x, resource) : return [pow(resource[i], x) % n for i in range(len(resource))]

# get private key D for RSA
def find_mod_inv(a, m):
    for i in range(1, m):
        temp_a = a % m
        temp_b = i % m
        if ((temp_a * temp_b) % m == 1): return i
    return -1

# start gathering essential components of RSA every time program begins anew
def begin_rsa():    
    # more info here: https://www.pythonpool.com/rsa-encryption-python/
    a = 0; b = 0; e = 4      #4 is the lowest non-prime number to start with.
    try:
        while (a == 0 or b == 0):
            x = r.randint(1, pow(10, PRIME_LOG))
            if (primality_test(x)):
                if (a > 0): b = x
                else: a = x
            time.sleep(SLEEP_LOG)
    except : print(ERROR_MSG_PRIME)
    n = a*b
    phi = (a-1)*(b-1)        
    while (not primality_test(e)):
        e = r.randint(2, math.floor(math.sqrt(phi)))    # square root reduces time compexity and unnecessary waiting for 'e'
    write_key(RSA_PUB_KEY, str(n), str(e))
    d = find_mod_inv(e, phi)
    return [d, n] if d != -1 else begin_rsa()

# RSA signature generation method (use same method to verify after)
def create_rsa_sign(k, n, x, contents):
    hash = hmac.new(str.encode(k), digestmod=hashlib.md5)
    hash.update(str.encode(contents))
    return hash.hexdigest()