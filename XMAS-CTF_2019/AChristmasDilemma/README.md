# A Christmas Dilemma
This challenge was divided into two seperate steps were the first on was a CAPTCHA challenge as in several others of the XMAS-CTF challenges.
The CAPTCHA challenge can be seen in the image below. 
![alt text](ChristmasDIlemma_captcha.png "CAPTCHA")
This challenge was solved by iterating through a wordlist (in this case "rockyou.txt") and generating the corresponding MD5-sum for each word. If the MD5-sum matches the requested CAPTCHA, the correct word is found and sent to the server.
The second part of the challenge was a mathematical problem shown in the image below.
![alt text](ChristmasDilemma_task.png "MathematicalChallenge")


