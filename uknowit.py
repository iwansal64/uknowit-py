import string
import sys
from os import system
import hashlib
import math
import multiprocessing
import time
from typing import Tuple
import random

arguments = sys.argv

system("clear")
print("\33[1;36m\33[5;31m", end="")
print(r"""
.-. .-..-..-..-. .-. .---. .-.  .-..-..-----. 
| } { || ' / |  \{ |/ {-. \| {  } |{ |`-' '-' 
\ `-' /| . \ | }\  {\ '-} /{  /\  }| }  } {   
 `---' `-'`-``-' `-' `---' `-'  `-'`-'  `-' 
""")

hashfunctions = list(hashlib.algorithms_available)+["plain"]

print("\33[0m")

if len(arguments) < 4:
	print("\33[1;36mWelcome to UKNOWIT!-A password cracker")
	print("How to use?")
	print("+-------------------------------------------------------------------------------------------------+")
	print("|                                              FORMAT                                             |")
	print("+-------------------------------------------------------------------------------------------------+")
	print("| uknowit <hash_type> {hash} {max_length} [-c {characters}] [-p {percent}] [-e {end}] [-m {cores}]|")
	print("+-------------------------------------------------------------------------------------------------+", end="\n")
	print()
	print("+-------------------------------------------------------------------------------------------------+")
	print("|                                             HASH TYPE                                           |")
	print("+-------------------------------------------------+-----------------------------------------------+")
	for index, hash_type in enumerate(hashfunctions):
		if index % 4 == 0:
			print(f'{f"| - {hash_type}":<25}', end="")
		elif index % 4 == 1:
			print(f'{f"| - {hash_type}":<25}', end="")
		elif index % 4 == 2:
			print(f'{f"| - {hash_type}":<24}', end="")
		else:
			print(f'{f"| - {hash_type}":<24}', end="|\n")

	if (len(hashfunctions)) % 4 != 0:
		print(f'{f"|":<24}'*(4-(len(hashfunctions)) % 4), end="|\n")
		
	print("+-------------------------------------------------+-----------------------------------------------+")
	print()
	print("+-------------------------------------------------------------------------------------------------+")
	print("|                                           CHARACTERS                                            |")
	print("+-----------------------------------------------+-------------------------------------------------+")
	print("| - l (lower_case)                              | - d (digits)                                    |")
	print("| - u (upper_case)                              | - s (symbols)                                   |")
	print("+-----------------------------------------------+-------------------------------------------------+")
	print()
	print("+-------------------------------------------------------------------------------------------------+")
	print("|                                             EXAMPLES                                            |")
	print("+-------------------------------------------------------------------------------------------------+")
	print("| uknowit sha256 67cbfb2d71faddd4b79c5109f1021409f80cd030d4ab32f95be2e0683f2fc2f6 8 -c ul         |")
	print("| uknowit md5 0cbc6611f5540bd0809a388dc95a615b 7 -c l -p 50                                       |")
	print("| uknowit sha256 090e565b1557cdf3dc6c79a5295f1c19b0edab82c7fc867a41b3806ea53a8161 4 -c ulsd -m 4  |")
	print("+-------------------------------------------------------------------------------------------------+")
	exit(0)


characters: str = arguments[arguments.index("-c") + 1] if "-c" in arguments else "ul"
start_percent: int = int(arguments[arguments.index("-p") + 1]) if "-p" in arguments else 0
end_percent: int = int(arguments[arguments.index("-e") + 1]) if "-e" in arguments else 100
multiprocesses: int = int(arguments[arguments.index("-m") + 1]) if "-m" in arguments else 1
hash_type: str = arguments[1]
hashed_password: str = arguments[2]
max_length: int = int(arguments[3])
checked_characters: list[str] = ["", " "] + (list(string.ascii_lowercase) if "l" in characters else []) + (list(string.ascii_uppercase) if "u" in characters else []) + (list(string.digits) if "d" in characters else []) + (list(string.punctuation) if "s" in characters else [])
words_combinations = (len(checked_characters)**max_length) * (1 - (start_percent / 100))

try:
	get_hash_function = ((lambda : (lambda x:x)) if hash_type == "plain" else (lambda : hashlib.new(hash_type)))
except ValueError:
	print(f"\33[1;31mHash Type '{hash_type}' is not recognized!")
	exit(1)

print(f"Just to make sure..")
print(f"+----------------------->")
print(f"\33[1;33mHashed Password\t: {hashed_password}")
print(f"Hash Type\t: {hash_type}")
print(f"Maximal Length\t: {max_length} characters")
print(f"Cores\t\t: {multiprocesses}")
print(f"+----------------------->")
print(f"Characters:")
for character in characters:
	if character == "l":
		print("\t- Lower Case")
	elif character == "u":
		print("\t- Upper Case")
	elif character == "s":
		print("\t- Symbols")
	elif character == "d":
		print("\t- Digits")
print(f"Character Total\t: {len(checked_characters)} characters")
print(f"Possible Words Total\t: {words_combinations}")
print(f"Starting Percentage\t: {start_percent}")
print(f"End Percentage\t: {end_percent}")
print("\33[1;37m", end="")
print(f"+---------------------->")


current_password_guess = ""
def start_brute_force(start_percent: int, end_percent: int, do_print: bool=True, print_percent: bool=True, process_id: int=0) -> Tuple[bool, str]:
	# time.sleep(random.random() * 3)
	current_characters_index = [0 for i in range(max_length)]

	end_iteration = ((len(checked_characters)**max_length) * (end_percent / 100) - 1)
	starting_iteration = end_iteration * (start_percent / 100)
	iteration = starting_iteration
  
	left_combinations = starting_iteration
	for index in range(len(current_characters_index)-1, -1, -1):
		# <- 36^0,36^1,36^2
		# -> 1, 36, 1296
		power_number = len(checked_characters)**index

		if left_combinations > power_number:
			current_characters_index[index] += math.floor(left_combinations / power_number)
			left_combinations = left_combinations % power_number
 
	# print(process_id)
	# print(current_characters_index)
	# print(end_iteration)
	# return (False, "")

	i = 0
	while True:
		iteration += 1
		current_characters_index[0] += 1
		if current_characters_index[0] > len(checked_characters) - 1:
			increase_index = 0
			done = False
			while True:
				current_characters_index[increase_index] = 0

				if increase_index >= max_length - 1:
					done = True
					break
 
				current_characters_index[increase_index+1] += 1
				if current_characters_index[increase_index+1] > len(checked_characters) - 1:
					increase_index += 1
					continue
				
				
				break
				
			if done:
				break
		
		current_password_guess = ""
		progress_percentage = ((iteration/end_iteration) * 100)
		for index in current_characters_index:
			current_password_guess += checked_characters[index]

		hash_function = get_hash_function()
		if hash_type != "plain":
			hash_function.update(str(current_password_guess).encode("utf-8"))

		guessed_password_hashed = (hash_function.hexdigest()) if hash_type != "plain" else (current_password_guess)

		if guessed_password_hashed == hashed_password:
			if do_print:
				print(f"PASSWORD : {current_password_guess}                                                         ")

			return (True, current_password_guess)
	
		if iteration >= end_iteration:
			if do_print:
				print("REACH ENDS PERCENTAGE!                       ")

			return (False, "")

		if not do_print:
			progress_percentage = (((iteration-starting_iteration)/(end_iteration-starting_iteration)) * 100)

		if do_print or print_percent:
			i += 1
			if i > 3:
				i = 0
			print(f'|{"="*(int(progress_percentage/10)):<10}|{round(progress_percentage, 3)}%' + (f' - |{current_password_guess}|' if do_print else (' \\' if i % 4 == 0 else (' |' if i % 4 == 1 else (' /' if i % 4 == 3 else ' -')))), end="\r")
		
	
	if do_print:
		print(f'|{"="*10:<10}|DONE')
  
	return (False, "")
 
def second_to_time(sec: int|float) -> str:
	seconds = int(sec)
	minutes = 0 if seconds < 60 else math.floor(seconds / 60)
	hours = 0 if minutes < 60 else math.floor(minutes / 60)
	
	seconds = seconds % 60
	minutes = minutes % 60
 
	return f"{f'{hours} hours ' if hours > 0 else ''}{f'{minutes} minutes ' if minutes > 0 else ''}{f'{seconds} seconds'}"
	

if input("continue? (y/n)") == "y":
	before_time = time.time()
	if multiprocesses > 1:
		with multiprocessing.Pool(processes=multiprocesses) as p:
			processes = []
			for i in range(multiprocesses):
				processes.append(p.apply_async(start_brute_force, (((i/multiprocesses)*(end_percent-start_percent))+start_percent, (((i+1)/multiprocesses)*(end_percent-start_percent))+start_percent, False, i == multiprocesses-1, i)))

			
			index = 0
			while True:
				try:
					res = processes[index].get(timeout=2)
					# print(res)
					if res[0] == True:
						print(f"Password : {res[1]}             ")
						break
					else:
						del processes[index]
						if len(processes) == 0:
							print("No Matched Password :(")
							break
  
				except multiprocessing.TimeoutError:
					pass

				index += 1
				if index > len(processes)-1:
					index = 0	

				continue
				
			
	else:
		start_brute_force(start_percent, end_percent)

	print(f"Elapsed Time : {second_to_time(int(time.time()-before_time))}")
