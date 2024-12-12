# main python file for Inforamation Security project2 - problem 1.
# This file is run at the docker container with basic ubuntu image.

import time
import math
import os
import subprocess               # library to run the binary files via this python file.
from matplotlib import pyplot as plt # To visualize the result.

def value_store(time_per_bit,text):
    starting_index = text.find("Bit 0")
    target = text[starting_index:].split()
    target = [float(i) for i in target if '.' in i]
    time_per_bit = [x + y for x,y in zip(time_per_bit,target)]
    return time_per_bit

N = 139804740659022203
E = 65537
private_key_size = 64

binaries = ['./problem1','./problem2']
chosen_encrypted_message = "ac123"
correct_plaintext = "9E592BA19CC3E9"
decryption_trial = 100
time_per_bit = [0,] * 57
# because the N can be represented as 57bit, there will be 57 informations of decryption time.

for trial in range(decryption_trial):
    #start = time.time()
    process = subprocess.Popen([binaries[0]],stdin = subprocess.PIPE, stdout = subprocess.PIPE, text = True)
    result, _ = process.communicate(input = chosen_encrypted_message)
    #print("Printing result")
    #print(result)
    #print("-------------------------------------")
    #print(f"before:\n{time_per_bit}")
    time_per_bit = value_store(time_per_bit,result)
    #print(f"after:\n{time_per_bit}")
    #end = time.time()
    #print(f"Time for executing binary once: {end - start}")
    #breakpoint()

time_per_bit = [x / decryption_trial for x in time_per_bit]

index = range(1,58)
plt.plot(index,time_per_bit,'bs-')
plt.savefig("output1.png")

avg = sum(time_per_bit) / len(time_per_bit)
d_key = ['0' if x - avg < 0 else '1' for x in time_per_bit]

d_key = "".join(d_key)
res = hex(int(d_key,2))
print(f"founded decryption key: {res}")
print("Computing if it is correct - decrypting...")

plain_res = pow(int(chosen_encrypted_message,16),int(d_key,2),N)
print(f"founded plaintext: {hex(plain_res).upper()}")
print(f"Correct answer: 0x{correct_plaintext}")

if hex(plain_res).upper()[2:] == correct_plaintext:
    print("Good job")
else:
    print("Try again...")

# Basic RSA key generation
# get large enough prime number p,q
# then n = p x q
# ø(n) = (p-1) x (q-1)
# encrpytion key e: gcd(e,ø(n)) = 1 

# ciphertext = m^e mod n
# plaintext = c^d mod n
# The purpose of this problem is to find private key 'd'.

# This will be computed by Square-and-Multiply by high probability
# So, when the bit is zero, just square.
# but when the bit is one, both square and multiply

# That means, when the decryption time is longer, the probability that the bit is one gets bigger.