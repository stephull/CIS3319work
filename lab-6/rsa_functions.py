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

# use RSA encryption, similar to Lab 3 with RSA
def rsa_signature(e):
    pass
def rsacrypt(mod, k, e):    # more info here: https://www.pythonpool.com/rsa-encryption-python/
    assert mod==ENC or mod==DEC
    if (mod == ENC):
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
        public_key = (n, e)
        write_key(RSA_PUB_KEY, str(public_key))
        
        def find_mod_inv(a, m):
            for i in range(1, m):
                temp_a = a % m
                temp_b = i % m
                if ((temp_a * temp_b) % m == 1): return i
            return -1
        d = find_mod_inv(e, phi)
        if (d == -1): 
            write_key(RSA_PUB_KEY, "---REDACTED---")
            raise Exception("\nNo modular inverse calculated, sorry. Try again.\n")
        
        secret_key = (d, n)
                
        # ENCRYPTION: C = P^e mod n /// DECRYPTION: P = C^d mod n
        return
    else:
        return