
# Import required module/s
import socket
import ast
import colorama
colorama.init()


def connectToServer(HOST, PORT):
	"""Create a socket connection with the Server and connect to it.

	Parameters
	----------
	HOST : str
		IP address of Host or Server, the Client needs to connect to
	PORT : int
		Port address of Host or Server, the Client needs to connect to

	Returns
	-------
	socket
		Object of socket class for connecting and communication to Server
	"""

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.connect((HOST, PORT))

	return server_socket


def formatRecvdData(data_recvd):
	"""Format the data received from the Server as required for better representation.

	Parameters
	----------
	data_recvd : str
		Data received from the Server about scheduling of Vaccination Appointment
	"""
	

	if '{' in data_recvd:
		index = data_recvd.index('{')
		text = data_recvd[:index]
		dict_text = data_recvd[index:]
		dict_found = ast.literal_eval(dict_text)
		print(colorama.Fore.LIGHTCYAN_EX,text)
		print(colorama.Style.BRIGHT,colorama.Fore.BLUE,"Choice\t:\t", colorama.Fore.LIGHTCYAN_EX,"Options")
		print(colorama.Style.RESET_ALL)
		for ind, (key, value) in enumerate(dict_found.items()):
			print(colorama.Fore.LIGHTBLUE_EX, key,"\t\t:\t", colorama.Fore.LIGHTCYAN_EX, value)
	elif 'Invalid' in data_recvd:
		print(colorama.Fore.LIGHTRED_EX,data_recvd)
	elif 'You have been late in scheduling' in data_recvd:
		print(colorama.Fore.LIGHTRED_EX,data_recvd)
	elif "Your appointment is scheduled" in  data_recvd:
		print(colorama.Fore.LIGHTYELLOW_EX,data_recvd)
	elif "$$" in  data_recvd:
		print(colorama.Fore.LIGHTGREEN_EX,data_recvd)	
	else:
		print(colorama.Fore.LIGHTMAGENTA_EX,data_recvd)
	


if __name__ == '__main__':
	"""Main function, code begins here
	"""

	# Define constants for IP and Port address of the Server to connect to.
	HOST = '127.0.0.1'
	PORT = 24680

	# Start the connection to the Server
	server_socket = None
	try:
		server_socket = connectToServer(HOST, PORT)
	except ConnectionRefusedError:
		print("*** Start the server first! ***")
	
	# Receive the data sent by the Server and provide inputs when asked for.
	if server_socket != None:
		while True:
			data_recvd = server_socket.recv(1024).decode('utf-8')
			formatRecvdData(data_recvd)

			if '>>>' in data_recvd:
				data_to_send = input(" ==> ")
				server_socket.sendall(data_to_send.encode('utf-8'))
			
			if not data_recvd:
				server_socket.close()
				break
		
		server_socket.close()
