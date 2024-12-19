# What is this?
_uknowit.py_ is a software that i have created for testing how secure a password is by brute-forcing combinations of characters.

# Setup
```sh
$ git clone https://github.com/iwansal64/uknowit-py.git
$ cd uknowit-py
$ sudo ./install.sh
$ uknowit
```
here's the one line installation
```sh
git clone https://github.com/iwansal64/uknowit-py.git && cd uknowit-py && sudo ./install.sh && uknowit
```

and that's pretty much it..
Now your computer should can run the program now by typing `uknowit`

## First Look
When you run `uknowit` it will output something like this :

![image](https://github.com/user-attachments/assets/19ca9c6f-cadd-4dd6-80f8-c85f3758e470)

## Usage 
Format: `uknowit <hash_type> {hash} {max_length} [-c {characters}] [-p {percent}] [-e {end}] [-m {cores}]`

Prompt: `uknowit plain 12345678 8 -c d -m 4`

Output: 

![image](https://github.com/user-attachments/assets/37b1706e-ba0d-4683-a53e-125958bbfb2c)

Multiprocessing makes it faster!! Here's the difference between using only 1 core and using 4 cores at the same time! :

![image](https://github.com/user-attachments/assets/ef54f283-6d6a-4099-b6cf-79d5f2844080)


