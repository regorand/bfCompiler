import sys

def main():
	if(len(sys.argv) >= 2):
		exe = loadFile(sys.argv[1])
		if ',' in exe:
			inputBuffer = input()
		else:
			inputBuffer = ''
		fieldOutput = (len(sys.argv) > 2) and sys.argv[2] == 'fields'
		verbose = (len(sys.argv) > 2) and sys.argv[2] == 'true'
		execute(exe, inputBuffer, verbose, fieldOutput)
		
def execute(exe, inputBuffer, verbose, fieldOutput):
	fields = [0]
	
	outputBuffer = ''
	
	pointerOverflowLeft = False
	
	pointer = 0
	
	executePointer = 0
	while(executePointer < len(exe)):
		char = exe[executePointer]#
		if(verbose):
			print("executePointer: " + str(executePointer))
			print("pointer value: " + str(pointer))
			print("field value: " + str(fields[pointer]))
		if(char == '+'):
			if(verbose):
				print("executing +")
			fields[pointer]+=1
			if(fields[pointer] > 255):
				fields[pointer] = 0
		elif(char == '-'):
			if(verbose):
				print("executing -")
			fields[pointer]-=1
			if(fields[pointer] < 0):
				fields[pointer] = 255
		elif(char == '>'):
			if(verbose):
				print("executing >")
			pointer+=1
			if(pointerOverflowLeft):
				pointerOverflowLeft = False
			if(pointer > len(fields) - 1):
				fields.append(0)
		elif(char == '<'):
			if(verbose):
				print("executing <")
			if(pointer > 0):
				pointer-=1
			else:
				pointerOverflowLeft = True
		elif(char == ','):
			if(verbose):
				print("executing ,")
			newChar = chr(0)
			if(len(inputBuffer) > 0):
				newChar = inputBuffer[0]
				inputBuffer = inputBuffer[1:]
			fields[pointer] = ord(newChar)
		elif(char == '.'):
			if(verbose):
				print("executing .")
			outputBuffer += chr(fields[pointer])
		elif(char == '['):
			if(verbose):
				print("executing [")
			if(pointerOverflowLeft or fields[pointer] == 0):
				if(pointerOverflowLeft):
					pointerOverflowLeft = False
				bracketLevel = 1
				while(bracketLevel > 0 and executePointer < len(exe)):
					executePointer+=1
					if(exe[executePointer] == '['):
						bracketLevel+=1
					elif(exe[executePointer] == ']'):
						bracketLevel-=1	
		elif(char == ']'):
			if(verbose):
				print("executing ]")
			bracketLevel = 1
			while(bracketLevel > 0 and executePointer >= 0):
				executePointer-=1
				if(exe[executePointer] == '['):
					bracketLevel-=1
				elif(exe[executePointer] == ']'):
					bracketLevel+=1
			executePointer-=1
		executePointer+=1
	
	if(verbose or fieldOutput):
		print("pointer at: " + str(pointer))
		for index, field in enumerate(fields, start=0):
			print("Field " + str(index) + ": " + str(field))
		
	print(outputBuffer)
		
def loadFile(file):
	with open(file, 'r') as myfile:
		data=myfile.read().replace('\n', '')
		return data
	print("could not find the file")
	sys.exit(1)

main()