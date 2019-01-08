import hashlib
from pwn import *
import sys
context.log_level = 'error'

#Hashes words from the wordlist "rockyou.txt" until a hash matching the CAPTCHA-requirement is found.
def breakCaptcha(wanted):
    #Open wordlist in read-mode
    with open("/home/fredrik/Programs/JohnTheRipper/run/Wordlists/rockyou.txt", "r") as file:
        for line in file:
            #Test against CAPTCHA requirement, if first 5 characters of MD5 sum are correct, the word is valid as CAPTCHA
            hashed = hashlib.md5(line.rstrip()).hexdigest()[:5]
            if(hashed==wanted):
                    break
    return line


#Used to convert the number of stones in each pile into binary and thereafter pad each binary to the same length by adding zeros from the left.
def binConv(board):
    pileBinary = [bin(int(pile))[2:] for pile in board] #Convert piles to binary
    length = [len(binary) for binary in pileBinary] #Pad all binaries to same lenth
    maxLen = max(length)
    pileBinary = ["0"*(maxLen - len(pile))+pile for pile in pileBinary]
    return pileBinary, maxLen

#Calculate the Nim-sum of all piles
def nimSum(pileBinary, maxLen):
    result = ""
    for i in xrange(maxLen):
        res = 0
        for pile in pileBinary:
            res +=  int(pile[i])
            res %= 2
        result += str(res)
    return result

#Choose move based on the calculated Nim-Sum
def chooseMove(board):
    binaries, maxlen = binConv(board)
    calcedNim = nimSum(binaries, maxlen)
    first_one = calcedNim.find("1")
    first_index = len(calcedNim) - first_one -1
    mod = 2**(first_index+1)
    print board
    mod_piles = [pile % mod for pile in board]
    max_mod = -1
    max_index = -1
    for i, m_pile in enumerate(mod_piles):
        if m_pile > max_mod:
            max_mod = m_pile
            max_index = i
    max_bin = bin(board[max_index])[2:]
    max_bin = "0"*(len(calcedNim)-len(max_bin)) + max_bin
    new_bin = ""
    for i in xrange(len(calcedNim)):
        if calcedNim[i] == "1":
            new_bin += str((int(max_bin[i])+1)%2)
        else:
            new_bin += max_bin[i]
    quantity = board[max_index] - int(new_bin, base=2)
    return (max_index, quantity)

#Open connection to remote server
p = remote('199.247.6.180', 14002)
p.recvline()
#Parse md5sum for CAPTCHA-challenge
interesting = p.recvline()
a, b = interesting.split("=")
wanted = b[:-2]

line = breakCaptcha(wanted)
#Send CAPTCHA to remote server
p.sendline(line)

#Game starts, loops until an error occurs or the game is won
while True:
    p.recvuntil("Current state of the game: ")
    #Parse current status of piles
    board = p.recvline()
    board = board[1:-2]
    board = board.split(',')
    board = [int(element.strip(' ')) for element in board]
    #Choose move based on pile status
    pile, quantity = chooseMove(board)
    #Pass calculated move to server
    p.recvuntil("Input the pile:")
    p.sendline(str(pile))
    p.recvuntil("Input the quantity:")
    p.sendline(str(quantity))
    p.recvline()
    #Check if te game is finished
    checkFinish = p.recvline()
    if (checkFinish.find("Current state of the game:") == -1):
        print checkFinish #Prints flag
        break

p.interactive()


