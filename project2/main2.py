# main python file for Inforamation Security project2 - problem 2.
# This file is run at the docker container with basic ubuntu image.
import time
import math
import os
import subprocess                       # library to run the binary files via this python file.
from matplotlib import pyplot as plt    # To visualize the result.
import numpy as np

def time_update(time,text):
    starting_index = text.find("Decryption Time: ") + len("Decryption Time: ")
    time += float(text[starting_index:].split()[0])
    return time

# Montgomery algorithms to count how much r = r - N operation is runned. (when d_key bits are all '1')
def get_omega(N):
    base = pow(2,64)
    om_1 = -(N % base)
    omega = 1
    for i in range(64):
        omega = (omega * omega * om_1) % base
    return omega

def montmul(x,y,N,omega):
    target = 0 # To judge there was "r = r - N"
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
        target = 1
    return (r,target)

def MontgomeryRSA(N,d,c):
    R = pow(2,64)
    suspicious_bits = set()       # to get which bit occurs r = r - N
    R2 = pow(R,2,N) # R^2 mod N
    om = get_omega(N)
    x, _ = montmul(c,R2, N, om)
    a, _ = montmul(1,R2, N, om)
    index = 0
    for bit in d:
        a, was = montmul(a,a,N,om)
        if was == 1:
            suspicious_bits.add(index)
        if bit == '1':
            a, was = montmul(a,x,N,om)
            if was == 1:
                suspicious_bits.add(index)
        index += 1
    m, _ = montmul(a,1,N,om)
    m = hex(m)[2:]
    return (m,suspicious_bits)

N = 6459327652408515587
E = 65537
private_key_size = 64

binaries = ['./problem1','./problem2']

# Choosing ciphertexts (1000 per size low, middle, high)  total 3000 ciphertexts.
chosen_cipher_list = [x for x in range(1,1001)]                     # 1 ~ 1000
chosen_cipher_list_middle = [x for x in range(N//2, N//2 + 1000)]   # N//2 ~ N//2 + 999
chosen_cipher_list_high = [x  for x in range(N-1, N-1001, -1)]      # N-1000 ~ N-1
chosen_cipher_list_high.reverse()

#chosen_cipher_list = chosen_cipher_list + chosen_cipher_list_middle + chosen_cipher_list_high
chosen_cipher_list.extend(chosen_cipher_list_middle)
chosen_cipher_list.extend(chosen_cipher_list_high)
time_list = []

# Getting 10 data per cihpertext
decryption_trial = 10

# Popen out of for loop because the ./problem2 binary can utilize multiple io with same process.
process = subprocess.Popen([binaries[1]],stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)

# Total 30000 decryption.
# Leveraging Binary (./problem2)
for ciphertext in chosen_cipher_list:
    hex_ciphertext = hex(ciphertext)[2:]
    print(f"decryption for ciphertext: {hex_ciphertext}")
    duration = 0
    for trial in range(decryption_trial):
        process.stdin.write(hex_ciphertext + "\n")
        process.stdin.flush()
        process.stdout.readline().split()[1]
        result = process.stdout.readline()
        duration = time_update(duration, result)
    time_list.append(duration / 10)

process.terminate()

"""index = range(0,3000)
plt.plot(index,time_list,'bo')
plt.savefig("main2.png")"""

# Collecting short & long timed cihper
long_term = {}
short_term = {}
for i in range(len(time_list)):
    if time_list[i] < 12000:
        if 1000<= i < 2000:
            c = (i - 1000) + N//2 
        elif i >= 2000:
            c = (i - 2000) + N - 1000
        else:
            c = i
        print(f"{c}:\t\t{time_list[i]:.3f}")
        short_term[c] = time_list[i]
print('----------------------------------------')
for i in range(len(time_list)):
    if time_list[i] > 29000:
        if 1000<= i < 2000:
            c = (i - 1000) + N//2 
        elif i >= 2000:
            c = (i - 2000) + N - 1000
        else:
            c = i
        print(f"{c}:\t\t{time_list[i]:.3f}")
        long_term[c] = time_list[i]

short_num = len(short_term.keys())
long_num = len(long_term.keys())
# ---------------------------------------
print(f"Short # : {short_num}\nLong # : {long_num}")

key = [x for x in range(0,64)]
val = [0,] *64
points = dict(zip(key,val))

# Printing short & long term lists
print(f"Short time list")
for cipher in short_term.keys():
    print(f"{hex(cipher)[2:].upper()}:\t{short_term[cipher]:.3f}")
    m, suspicious_bits = MontgomeryRSA(N,"1"*64,cipher)
    for bit in suspicious_bits:
        points[bit] -= 1


print(f"Long time list")
for cipher in long_term.keys():
    print(f"{hex(cipher)[2:].upper()}:\t{long_term[cipher]:.3f}")
    m, suspicious_bits = MontgomeryRSA(N,"1"*64,cipher)
    for bit in suspicious_bits:
        points[bit] += 1

print(points)
"""plt.plot(points.keys(),points.values(),'bs-')
plt.savefig("dict.png")"""
plt.hist(points.values())
plt.savefig("hist.png")

avg = sum(points.values()) / len(points.values())
get_ones = ["1" if (x-avg) > 0 else "0" for x in points.values()]
get_ones[0] = "0"
get_ones[-1] = "1"
get_ones = "".join(get_ones)
print(f"Suscpicious bits: {get_ones}")



"""
# 12/7 start
for i in range(0,64):
    chosen_cipher = pow(2,i)
    hex_chosen_cipher = hex(chosen_cipher)[2:]
    print(f"decryption for ciphertext:2^{i}")
    time = 0
    for trial in range(decryption_trial):
        process.stdin.write(hex_chosen_cipher + "\n")
        process.stdin.flush()
        process.stdout.readline().split()[1]
        result = process.stdout.readline()
        time = time_update(time, result)
    time_list.append(time / decryption_trial)

avg = sum(time_list) / len(time_list)

for i in range(0,63):
    print("---------------------------------")
    print(f"{i}th bit")
    print(f"Time: {time_list[i]}")
    time_list[i] -= avg

d_key = ['1' if x > 0 else '0' for x in time_list]
d_key.reverse()
d_key = ''.join(d_key)
print(d_key)


ac123 = int('ac123',16)
plain_ac123 = 'DE8248B7254858C'
int_d_key = int(d_key,2)
hex_d_key = hex(int_d_key)[2:].upper()
or_d_key = int_d_key + 1
# because cipher를 1로 한경우는 항상 짧기 때문에 확신 불가능.
my_decrypt = hex(pow(ac123,int_d_key,N))[2:].upper()
my_decrypt2 = hex(pow(ac123,or_d_key,N))[2:].upper()
print(f"my decryption key: {hex_d_key}")
print(f"Correct plain : {plain_ac123}")
print(f"My result : {my_decrypt}")
print(f"My result2 : {my_decrypt2}")

# 12/7 end"""