import string
import sys
from os import system
import hashlib
import math
import multiprocessing

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
	print("| uknowit sha256 81253bddb35f92a6fcd 5                                                            |")
	print("| uknowit md5 12b6a0f1cf3aa53af35701 7 -c ul -p 50                                                |")
	print("| uknowit blake2 66155be9b92e0d666b7 0 -c ulsd -m 4                                               |")
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
def start_brute_force(start_percent: int, end_percent: int, do_print: bool=True, print_percent: bool=True) -> [bool, str]:
	current_index = 0
	current_characters_index = [0 for i in range(max_length)]

	end_iteration = len(checked_characters)**max_length
	iteration = end_iteration * (start_percent / 100)
	progress_percentage = (iteration/end_iteration) * 10
  
	left_combinations = end_iteration - words_combinations
	for index in range(len(current_characters_index)-1, -1, -1):
		# <- 36^0,36^1,36^2
		# -> 1, 36, 1296
		power_number = len(checked_characters)**index

		if left_combinations > power_number:
			current_characters_index[index] += math.floor(left_combinations / power_number)
			left_combinations = left_combinations % power_number
 
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
		progress_percentage = (iteration/end_iteration) * 100
		for index in current_characters_index:
			current_password_guess += checked_characters[index]

		hash_function = get_hash_function()
		if hash_type != "plain":
			hash_function.update(str(current_password_guess).encode("utf-8"))

		guessed_password_hashed = (hash_function.hexdigest()) if hash_type != "plain" else (current_password_guess)


		if guessed_password_hashed == hashed_password:
			if do_print:
				print(f"PASSWORD : {current_password_guess}                                                         ")

			return [True, current_password_guess]
		
		if progress_percentage > end_percent:
			if do_print:
				print("REACH ENDS PERCENTAGE!                       ")

			return [False, str(progress_percentage)]

		if do_print or print_percent:
			print(f'|{"="*(int(progress_percentage/10)):<10}|{round(progress_percentage, 3)}%' + (f' - |{current_password_guess}|' if do_print else ''), end="\r")
			# print(current_password_guess)
	
	if do_print:
		print(f'|{"="*10:<10}|DONE')
  
	return [False, ""]
 
if input("continue? (y/n)") == "y":
	if multiprocesses > 1:
		with multiprocessing.Pool(processes=multiprocesses) as p:
			processes = []
			for i in range(multiprocesses):
				processes.append(p.apply_async(start_brute_force, (((i/multiprocesses)*(end_percent-start_percent))+start_percent, (((i+1)/multiprocesses)*(end_percent-start_percent))+start_percent, False, i == multiprocesses-1)))

			
			index = 1
			while True:
				try:
					res = processes[index].get(timeout=2)
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
