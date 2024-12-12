import time
from matplotlib import pyplot as plt
N = 6459327652408515587
E = 65537
private_key_size = 64

def get_omega(N):
    base = pow(2,64)
    om_1 = -(N % base)
    omega = 1
    for i in range(64):
        omega = (omega * omega * om_1) % base
    return omega

def montmul(x,y,N,omega):
    base = pow(2,64)
    r = 0
    w = base.bit_length()  # w = 64 for base = 2^64
    mods = (N.bit_length() + w - 1) // w  # Equivalent to ceil(log_base(n))
    for i in range(mods):
        y_l = y % base
        y = y // base
        u = (omega * (y_l * (x % base) + (r % base))) % base
        temp = x * y_l
        temp2 = N * u
        r = r + temp + temp2
        r = r // base
    if r >= N:
        r = r - N
    return r

def MontgomeryRSA(N,d,c):
    R = pow(2,64)
    start = time.time()
    R2 = pow(R,2,N) # R^2 mod N
    om = get_omega(N)
    x = montmul(c,R2, N, om)
    a = montmul(1,R2, N, om)
    for bit in d:
        a = montmul(a,a,N,om)
        if bit == '1':
            a = montmul(a,x,N,om)
    end = time.time()
    m = montmul(a,1,N,om)
    m = hex(m)[2:]
    return (m,end-start)
"""
decryption_trial = 100

# check the Montgomenry algorithm doing well.
d = "0x1537f000ca50a81"
d = int(d,16)
ciphertext = "ac123"
correct = hex(pow(int(ciphertext,16),d,N))[2:]
#m = rsa_decrypt(int(ciphertext,16),N,d,pow(2,64))
m = MontgomeryRSA(N,bin(d)[2:],int(ciphertext,16))
print(f"My result: {m}")
print(f"Correct ans: {correct}")
if correct == m:
    print("Good job!")"""

# 실행시간이 긴 ciphertext (1< 50 중에서 24000넘는것)
ciphertext_list = ['2','7','a','15','16','19','1c','1d','1e','1f','23','27']

decryption_trial = 10000
duration = []
int_ciphertext = int("ac123",16)

for power in range(0,63):
    decryption_key = pow(2,power,N)
    bin_decryption_key = bin(decryption_key)[2:].zfill(64)
    dur = 0
    for i in range(decryption_trial):
        _, dur_per_one = MontgomeryRSA(N,bin_decryption_key,int_ciphertext)
        dur += dur_per_one
    print(f"For D: {hex(decryption_key).upper()}")
    print(f"Time : {dur*1000:.5f}")
    duration.append(dur*10)


index = range(0,63)
plt.plot(index,duration,'bs-')
plt.savefig("montgomery.png")

print(f"suspicious bit: {duration.index(max(duration))}")

avg = sum(duration) / 63
duration = [ x - avg for x in duration]
infer = ['1' if x > 0 else '0' for x in duration]
infer = ''.join(infer)
hex_infer = hex(int(infer,2))[2:].upper()
print(hex_infer)