# forth.py

# https://skilldrick.github.io/easyforth/

import operator

stack = []

num_op = lambda op: lambda: stack.append(op(stack.pop(), stack.pop()))
bool_op = lambda op: lambda: stack.append(-1) if op(stack.pop(), stack.pop()) else stack.append(0)

def swap(): stack[-1], stack[-2] = stack[-2], stack[-1]
def rot(): stack[-1], stack[-2], stack[-3] = stack[-3], stack[-2], stack[-1]

builtins = {
	"+": num_op(operator.add),
	"-": num_op(operator.sub),
	"*": num_op(operator.mul),
	"/": num_op(operator.truediv),

	".": lambda: print(stack.pop()),

	"dup": lambda: stack.append(stack[-1]),
	"drop": stack.pop,
	"swap": swap,
	"over": lambda: stack.append(stack[-2]),
	"rot": rot,

	"emit": lambda: print(chr(stack.pop())),
	"cr": print,

	"=": bool_op(operator.eq),
	">": bool_op(operator.gt),
	"<": bool_op(operator.lt),
	">=": bool_op(operator.ge),
	"<=": bool_op(operator.le)
}

words = {}

def tokenize(chars):
	current_token = ""
	tokenizing_string = False
	amt_to_continue = 0

	for index, char in enumerate(chars):
		if amt_to_continue > 0:
			amt_to_continue -= 1
			continue

		elif index != len(chars) - 1 and char == "." and chars[index + 1] == "\"":
			tokenizing_string = True
			yield ".\""
			amt_to_continue = 2

		elif tokenizing_string:
			current_token += char
			if char == "\"":
				tokenizing_string = False
				yield current_token.rstrip("\"")
				current_token = ""

		elif char == " " and (no_spaces := current_token.strip()) != "":
			yield no_spaces
			current_token = ""

		else:
			current_token += char

		# print("Current token:", current_token)

	if (no_spaces := current_token.strip()) != "":
		yield no_spaces

def parse(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)

def main(expression):
	# print("Expression:", expression)
	global stack
	amt_to_continue = 0
	# print("Stack:", stack)
	for index, argument in enumerate(expression):
		if amt_to_continue > 0:
			amt_to_continue -= 1
			continue

		# print("argument:", argument)
		if argument == ":":
			name, body = expression[index + 1], expression[index + 2: (end_of_word := expression.index(";"))]
			# print("Name and body:", name, body)
			words[name] = body
			amt_to_continue = end_of_word

		elif argument == ".\"":
			print(expression[index + 1])
			amt_to_continue = 1

		else:
			try:
				builtins[argument]()
			except KeyError:
				if argument in words:
					main(words[argument])
				elif type(argument) in (int, float):
					stack.append(argument)
				else:
					print("Error: undefined word", argument)
			except IndexError:
				print("Error: stack underflow")

	# print("Stack:", stack)

if __name__ == "__main__":
	while True:
		main([parse(token) for token in tokenize(input("> "))])


"""
Words to implement:
- and
- or
- invert
- if then
- mod
- if else then
- do loop
- variable
- !
- @
- constant
- allot
- key
- begin until
"""
