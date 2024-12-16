import string
import sys
from os import system
import hashlib
from time import time

arguments = sys.argv

system("clear")
print("\33[1;36m", end="")
print(r"""
.-. .-..-..-..-. .-. .---. .-.  .-..-..-----. 
| } { || ' / |  \{ |/ {-. \| {  } |{ |`-' '-' 
\ `-' /| . \ | }\  {\ '-} /{  /\  }| }  } {   
 `---' `-'`-``-' `-' `---' `-'  `-'`-'  `-' 
""")

if len(arguments) == 1:
	print("Welcome to UKNOWIT! - A password cracker")
	print("How to use?")
	print("+-------------------------------------------------------+")
	print("|                         FORMAT                        |")
	print("+-------------------------------------------------------+")
	print("| uknowit <hash_type> {hash} {max_length} [{characters}]|")
	print("+-------------------------------------------------------+")
	print()
	print("+-------------------------------------------------------+")
	print("|                       HASH TYPE                       |")
	print("+---------------------------+---------------------------+")
	for index, hash_type in enumerate(list(hashlib.algorithms_available)+["plain"]):
		if index % 2 == 0:
			print(f'{f"| - {hash_type}":<28}', end="")
		else:
			print(f'{f"| - {hash_type}":<28}', end="|\n")
	if len(hashlib.algorithms_available) % 2 != 0:
		print(f'{f"|":<28}', end="|\n")
		
	print("+---------------------------+---------------------------+")
	print()
	print("+-------------------------------------------------------+")
	print("|                       CHARACTERS                      |")
	print("+---------------------------+---------------------------+")
	print("| - l (lower_case)          | - d (digits)              |")
	print("| - u (upper_case)          | - s (symbols)             |")
	print("+---------------------------+---------------------------+")
	print()
	print("+-------------------------------------------------------+")
	print("|                        EXAMPLES                       |")
	print("+-------------------------------------------------------+")
	print("| uknowit sha256 81253bddb35f92a6fcd 5                  |")
	print("| uknowit md5 12b6a0f1cf3aa53af35701 7 uld              |")
	print("| uknowit blake2 66155be9b92e0d666b7 0 ulsd             |")
	print("+-------------------------------------------------------+")
	exit(0)


characters = arguments[4] if len(arguments) > 4 else "ul"
hash_type = arguments[1]
hashed_password = arguments[2]
max_length = int(arguments[3])
checked_characters = ["", " "] + (list(string.ascii_lowercase) if "l" in characters else []) + (list(string.ascii_uppercase) if "u" in characters else []) + (list(string.digits) if "d" in characters else []) + (list(string.punctuation) if "s" in characters else [])


try:
	get_hash_function = ((lambda x: x) if hash_type == "plain" else (lambda : hashlib.new(hash_type)))
except ValueError:
	print(f"\33[1;31mHash Type '{hash_type}' is not recognized!")
	exit(1)

print(f"Just to make sure..")
print(f"+----------------------->")
print(f"\33[1;33mHashed Password : {hashed_password}")
print(f"Hash Type : {hash_type}")
print(f"Maximal Length : {max_length} characters")
print(f"+----------------------->")
print(f"Characters :")
for character in characters:
	if character == "l":
		print("\t- Lower Case")
	elif character == "u":
		print("\t- Upper Case")
	elif character == "s":
		print("\t- Symbols")
	elif character == "d":
		print("\t- Digits")
print(f"Character Total : {len(checked_characters)} characters")
print(f"Possible Words Total : {len(checked_characters)**max_length}")
print("\33[1;37m", end="")
print(f"+---------------------->")

if input("continue? (y/n)") == "y":
	current_password_guess = ""
	current_characters_index = [0 for i in range(max_length)]
	current_index = 0

	iteration = 0
	end_iteration = len(checked_characters)**max_length
	progress_percentage = (iteration/end_iteration) * 10
	# est = ""
	# last_time = time()
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
		for i in current_characters_index:
			current_password_guess += checked_characters[i]

		hash_function = get_hash_function()
		if hash_type != "plain":
			hash_function.update(str(current_password_guess).encode("utf-8"))

		guessed_password_hashed = (hash_function.hexdigest()) if hash_type != "plain" else (current_password_guess)


		guessed_password_hashed2 = (hash_function.hexdigest()) if hash_type != "plain" else (current_password_guess)

		if guessed_password_hashed == hashed_password:
			print(f"PASSWORD : {current_password_guess}                                                         ")
			break

		# if iteration % 1000 == 0:
		# 	speed = time() - last_time / 10

		# 	seconds_time_left = (end_iteration - iteration) * speed
		# 	minutes_time_left = 0
		# 	hours_time_left = 0
   
		# 	minutes_time_left += seconds_time_left % 60
		# 	seconds_time_left = seconds_time_left % 60

		# 	hours_time_left += minutes_time_left % 60
		# 	minutes_time_left = minutes_time_left % 60

		# 	seconds_time_left = int(seconds_time_left)
		# 	minutes_time_left = int(minutes_time_left)
		# 	hours_time_left = int(hours_time_left)

		# 	est = f"{f'{hours_time_left} hours ' if hours_time_left > 0 else f'{minutes_time_left} minutes ' if minutes_time_left > 0 else f'{seconds_time_left} seconds'}"

		# 	last_time = time()

		print(f'|{"="*(int(progress_percentage/10)):<10}|{round(progress_percentage, 3)}% - |{current_password_guess}|', end="\r")
	
	print(f'|{"="*10:<10}|DONE')
