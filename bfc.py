from macros import commands
import math
import sys
import shlex

ifStack = []

def main():
	if(len(sys.argv) >= 1):
		codeString = loadFile(sys.argv[1])
		
		code = codeString.split('\n')
		
		result = resolveCommands(code)
		
		#random
		
		#>[-]+<[[-]>-<]>[]
		#runs loop only if first cell is 0
		
		result = optimize(result)
		
		print(result)
		
		saveToFile(result)

def resolveCommands(code):
	output = ''
	
	for index, line in enumerate(code):
		params = shlex.split(line, posix=False)
		cmd = getMatchingCommand(params[0])
		output += cmd.get('code')
		paramCount = cmd.get('params')
		if(paramCount != None):
			if(paramCount + 1 > len(params)):
				compileError('not enough parameters in line: ' + str(index))
		output = resolveParams(params, code, output, index)
	
	return output
	
def getMatchingCommand(cmd):
	for command in commands:
		cmdString = command.get('cmd')
		if(cmdString == cmd):
			return command
	compileError("no matching command found")
	
def resolveParams(params, code, output, lineIndex):
	global ifStack
	if(params[0] == 'set'):
		if('\'' in params[1]):
			output += buildNumber(ord(params[1][1]))
		else:
			output += buildNumber(int(params[1]))
			
	elif(params[0] == 'nat'):
		indices = list(find_all(params[1], '\''))
		if(len(indices) != 2):
			compileError("not enough \"'\" for native code in line. " + str(lineIndex))
		output += params[1][indices[0] + 1:indices[1]]
	elif(params[0] == 'str'):
		output + resolveStringLiterals(params[1], lineIndex)
	elif(params[0] == 'left' or params[0] == 'right'):
		for i in range(0, int(params[1])):
			output += '<' if params[0] == 'left' else '>'
	elif(params[0] == 'mov' or params[0] == 'copy'):
		if(params[1] != 'left' and params[1] != 'right'):
			compileError('no directional parameter for command: ' + params[0] + ' in line: ' + str(lineIndex))
		
		left = ''
		right = ''
		for i in range (0, int(params[2])):
			left += '<'
			right += '>'
		if(params[1] == 'left'):
			output = output.replace('*', left, 1)
		output = output.replace('*', right, 1)
		output = output.replace('*', left, 1)
		output = output.replace('*', right, 1)
		if(params[0] == 'copy'):
			output = output.replace('*', left, 1)
			output = output.replace('*', right, 1)
			output = output.replace('*', left, 1)
			if(params[1] == 'right'):
				output = output.replace('*', right, 1)
		else:
			if(params[1] == 'right'):
				output = output.replace('*', left, 1)
	elif(params[0] == 'if'):
		if(len(params) > 1 and params[1] == 'not'):
			output += '>[-]+<[>-<[-]]>[-<+>]<['
		else:
			output += '['
	return output	
		
def getNumberStringFromIndex(code, index):
	intlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	numString = ''
	if(code[index] in intlist):
		numString += code[index]
		if(index+1 < len(code) and code[index+1] in intlist):
			numString += code[index+1]
			if(index+2 < len(code) and code[index+2] in intlist):
				numString += code[index+2]
		return numString
	return ''
	
def resolveStringLiterals(code, lineIndex):
	string_literals = list(find_all(code, '"'))
	if(len(string_literals) != 2):
		compileError("non matching amount of \" in line. " + str(lineIndex))

	word = code[string_literals[0] + 1:string_literals[1]] 
	wordCode = ''
	for chr in word:
		wordCode += buildNumber(ord(chr)) + '>'
	return wordCode[:-1]
	
def buildNumber(value, isBase = True):
	result = ''
	if(value < 10):
		for i in range(0, value):
			result+='+'
	else:
		floorRoot = int(math.sqrt(value))
		remainder = value - (floorRoot * floorRoot)
		for i in range(0, floorRoot):
			result += '+'
		result += '[->'
		for i in range(0, floorRoot):
			result += '+'
		result += '<]'
		if(remainder != 0):
			result += buildNumber(remainder, False)
		if(isBase):
			result += '>[-<+>]<'
	return result
	
def optimize(output):
	uselessStrings = ['<>', '><', '+-', '-+', ',,']
	for s in uselessStrings:
		index = output.find(s)
		while(index != -1):
			output = output[:index] + output[index + len(s):]
			index = output.find(s)
	return output
			
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)
	
def compileError(message):
	print('could not compile:\n' + message)
	sys.exit(1)
	
def saveToFile(code):
	file = open("code.bf", "w")
	file.write(str(code))
	file.close()
	
def loadFile(file):
	with open(file, 'r') as myfile:
		data=myfile.read()
		return data
	return '++.'
	
main()