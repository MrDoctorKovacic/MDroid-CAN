##
## Handlers.py
## Small functions to parse a frame's data into usable information
##

def hex2dec(integer): return int(str(integer), 16)

# Handles ID 339
def parseASC1(data):
	# Speed is MSB+LSB
	# Bit length of 12, discard last 4 bits of LSB
	# Gain of 1/8, so 0x0008 is 1kmph
	speed = (.125 * int(str(format(data[2], 'x')) + str(format(data[1], 'x'))[0], 16))

	# speed is weird, in that it's only valid above 0.5kmph.
	if speed <= 0.5:
		speed = 0

	return {"Speed": speed}

# Handles ID 790
def parseDME1(data):
	rpm = round ( int(str(format(data[3], 'x')) + str(format(data[2], 'x')), 16)/6.4, 2) 

	# Randomly jumps down to < 120-300 RPM for some reason, I suspect different data is being sent
	if rpm > 500:
		return {"RPM": rpm}
	else:
		return None

# Handles ID 809
def parseDME2(data):
	parsed = {
		"Temp C": ( (0.75) * hex2dec(data[1]) )-48.373,
		"Cruise Control": bin(data[3])[-1] == 1, # 1 or 0 in bit 7 of byte 3
		"Throttle Position": data[5],
		"Kickdown Switch": data[6] == 4,
		"Brake Pedal Pressed": data[6] == 1,
	}
	return parsed

# Handles ID 824
def parseDME3(data):
	parsed = {
		"Sport On": data[2] == 0 or data[2] == 2,
		"Sport Error": data[2] == 3,
	}
	return parsed

# Handles ID 1349
# TODO
def parseDME4(data):
	parsed = {
		"Oil Temp": round(hex2dec(data[4])-48.373, 2)
	}
	return parsed

# Handles ID 1555
def parseIC(data):
	# Convert int to hex and back again
	fuelData = hex2dec(data[2])

	# Fuel level will parse to be a float between 0 and 1
	if fuelData == 128: #hex 80 is empty
		fuelLevel = 0
	elif fuelData <= 135 and fuelData > 128:
		fuelLevel = (fuelData-128)/64
	else: # between 0 and 57, add another 7 to account for rollover
		fuelLevel = (fuelData+7)/64
	
	parsed = {
		"Odometer": (int(str(format(data[1], 'x')) + str(format(data[0], 'x')), 16)*10) / 1.609,
		"Fuel Level": round(fuelLevel, 2),
		"Running Clock": int(str(format(data[4], 'x')) + str(format(data[3], 'x')), 16)
	}
	return parsed

# Handles ID 1557
# TODO
def parseAC(data):
	# x being temperature in Deg C,
	#(x>=0 deg C,DEC2HEX(x),DEC2HEX(-x)+128) x range min -40 C max 50 C
	#if format(data[3], 'x') > 50:
	#	temp = format(data[3], 'x')+(128)
	#else:
	#	temp = format(data[3], 'x')
	
	parsed = {
		"Air Conditioning On": data[0] == 80,
		#"Outside Temp (C)": temp
	}
	return parsed

# Handles ID 504
def parseBrakePressure(data):
	parsed = {
		"Brake Pressure": data[2]
	}
	return parsed