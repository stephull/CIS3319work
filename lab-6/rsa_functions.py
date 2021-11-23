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
def digitize_text(m, e):
    assert m==ENC or m==DEC
    if (m == ENC):
        assert type(e) == str, "To encrypt RSA plaintext into numbers, you need a string value"
        num = 0
        for i in range(len(e)):
            temp = ord(e[i])
            num += int(temp * pow(ABC_LEN, i))
        return num
    else:
        assert type(e) == int, "To decrypt received RSA plaintext, you need an integer"
        t = ""; i = e
        while (i != 0):
            t += chr(int(i % ABC_LEN))
            i /= ABC_LEN
        return t

# use RSA signature
#def rsa_signature(e) : pass

# encrypt and decrypt RSA, similar to Lab 3 with RSA
# 'x' = e in encryption, d in decryption 
# AND 'var' = P in encryption, C in decryption
def rsacrypt(mod, n, x, var):
    assert mod==ENC or mod==DEC
    return int(pow(var, x) % n)

# get private key D for RSA
def find_mod_inv(a, m):
    for i in range(1, m):
        temp_a = a % m
        temp_b = i % m
        if ((temp_a * temp_b) % m == 1): return i
    return -1

# finally, start gathering essential components of RSA every time program begins anew
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
        e = r.randint(2, math.floor(math.sqrt(phi)))
        # square root reduces time compexity and unnecessary waiting for 'e'
    write_key(RSA_PUB_KEY, str(n), str(e))
    d = find_mod_inv(e, phi)
    if (d == -1) : begin_rsa()  # very unlikely to go into infinite loop thereafter
    return [d, n]