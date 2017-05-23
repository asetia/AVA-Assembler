def convert(inFile, outFile1, outFile2):
	assembly_file = open(inFile, 'r')
	machine_file = open(outFile1, 'w')
	lut_file = open(outFile2, 'w')
	assembly = list(assembly_file.read().split('\n'))

	lineNum = 0;
	labelsNum = 0;

	#dictionaries to ease conversion of opcodes/operands to binary
	opcodes = {'ADR' : '000', 'ADI' : '001', 'STR' : '010', 'LDR' : '011',
	'MOV' : '100', 'CMP' : '101', 'BR' : '110', 'HT' : '111'}
	registers = {'r0' : '000', 'r1' : '001', 'r2' : '010', 'r3' : '011',
	'r4' : '100', 'r5' : '101', 'r6' : '110', 'r7' : '111'}
	lut = {}

	for line in assembly:
		instr = line.split();
		lineNum += 1
		if instr[0] not in opcodes:
			lut[instr[0].replace(':', '')] = labelsNum
			lut_file.write(str(lineNum) + '\n')
			labelsNum += 1
	for line in assembly:
		output = ""
		instr = line.split();
		print(instr)
		if instr[0] in opcodes:
			output += opcodes[instr[0]]
			del instr[0]
			if output is '111':
				output += '000000'
			elif output is '100':
				#MOV
				imm = bin(int(instr[0]))[2:]
				#pad to 6
				for i in range(0, 6-len(imm)):
					imm = '0'+imm
				output += imm
			else:
				instr[0] = instr[0].replace(',', '');
				if instr[0] in registers:
					#ADR OR ADI
					output += registers[instr[0]]
					if instr[1] in registers:
						#ADR
						output += registers[instr[1]]
					else:
						#ADI
						imm = bin(int(instr[1]))[2:]
						#pad to 3
						for i in range(0, 3-len(imm)):
							imm = '0'+imm
						output += imm
				else:
					#BR
					output += instr[0]
					imm = bin(int(lut[instr[1]]))[2:]
					for i in range(0, 5-len(imm)):
						imm = '0'+imm
					output += imm
			machine_file.write(str(output) + '\t// ' + line + '\n')
		print(output)

	assembly_file.close()
	machine_file.close()

#convert("assembly.txt", "machine.txt", "lut.txt")
convert("stringmatch.txt", "sm_machine.txt", "sm_lut.txt")
convert("cordic.txt", "c_machine.txt", "c_lut.txt")
convert("division.txt", "d_machine.txt", "d_lut.txt")