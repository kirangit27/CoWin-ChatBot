# Import required module/s
import socket
from bs4 import BeautifulSoup
import requests
import datetime


# Define constants for IP and Port address of Server
# NOTE: DO NOT modify the values of these two constants
HOST = '127.0.0.1'
PORT = 24680


def fetchWebsiteData(url_website):
	"""Fetches rows of tabular data from given URL of a website with data excluding table headers.

	Parameters
	----------
	url_website : str
		URL of a website

	Returns
	-------
	bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""
	
	web_page_data = ''

	page = requests.get(url_website)

	soup = BeautifulSoup(page.content, 'html.parser')

	tb = soup.find('tbody')
	for i in tb.find_all('tr', class_='row1'):
		web_page_data = i.find_all('td', class_='hospital_name"')

	for j in tb.find_all('tr'):
		name = j.find_all('td')
		web_page_data.append(name)		

	return web_page_data

############################################################################################################################

def fetchVaccineDoses(web_page_data):
	"""Fetch the Vaccine Doses available from the Web-page data and provide Options to select the respective Dose.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers

	Returns
	-------
	dict
		Dictionary with the Doses available and Options to select, with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineDoses(web_page_data))
	{'1': 'Dose 1', '2': 'Dose 2'}
	"""

	vaccine_doses_dict = {}
	
	dose_list = []
	for k in web_page_data:
		soup2 = BeautifulSoup(str(k), 'html.parser')
		dose = soup2.find('td', class_='dose_num')
		dose_list.append(dose.get_text())
		
	unique_list = []

	for x in dose_list:
		if x not in unique_list:
			unique_list.append(x) 

	temp_dict = {}
	for z in unique_list:
		dose_num = 'Dose '+z
		mydict = {z:dose_num}
		vaccine_doses_dict = {**temp_dict,**mydict}
		temp_dict = vaccine_doses_dict		

	return vaccine_doses_dict

############################################################################################################################

def fetchAgeGroup(web_page_data, dose):
	"""Fetch the Age Groups for whom Vaccination is available from the Web-page data for a given Dose
	and provide Options to select the respective Age Group.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Age Groups (for whom Vaccination is available for a given Dose) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchAgeGroup(web_page_data, '1'))
	{'1': '18+', '2': '45+'}
	>>> print(fetchAgeGroup(web_page_data, '2'))
	{'1': '18+', '2': '45+'}
	"""

	age_group_dict = {}
	
	age_list = []
	for k in web_page_data:
		soup3 = BeautifulSoup(str(k), 'html.parser')
		dose_find = soup3.find('td', class_='dose_num')
		if(dose_find.get_text() == dose):
			age = soup3.find('td', class_='age')
			age_list.append(age.get_text())	
	unique_list = []
	for x in age_list:
		if x not in unique_list:
			unique_list.append(x)

	unique_list.sort()

	temp_dict = {}
	num = 1
	for q in unique_list:
		sr_num = str(num)
		mydict = {sr_num:q}
		age_group_dict = {**temp_dict,**mydict}
		temp_dict = age_group_dict
		num+=1		

	return age_group_dict

############################################################################################################################

def fetchStates(web_page_data, age_group, dose):
	"""Fetch the States where Vaccination is available from the Web-page data for a given Dose and Age Group
	and provide Options to select the respective State.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the States (where the Vaccination is available for a given Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchStates(web_page_data, '18+', '1'))
	{
		'1': 'Andhra Pradesh', '2': 'Arunachal Pradesh', '3': 'Bihar', '4': 'Chandigarh', '5': 'Delhi', '6': 'Goa',
		'7': 'Gujarat', '8': 'Harayana', '9': 'Himachal Pradesh', '10': 'Jammu and Kashmir', '11': 'Kerala', '12': 'Telangana'
	}
	"""

	states_dict = {}
	
	states_list = []
	for k in web_page_data:
		soup4 = BeautifulSoup(str(k), 'html.parser')
		dose_find = soup4.find('td', class_='dose_num')
		if(dose_find.get_text() == dose):
			age_find = soup4.find('td', class_='age')
			if(age_find.get_text() == age_group):
				state_find = soup4.find('td', class_='state_name')
				states_list.append(state_find.get_text())	
	unique_list = []
	for x in states_list:
		if x not in unique_list:
			unique_list.append(x)

	unique_list.sort()

	temp_dict = {}
	num = 1
	for q in unique_list:
		sr_num = str(num)
		mydict = {sr_num:q}
		states_dict = {**temp_dict,**mydict}
		temp_dict = states_dict
		num+=1	

	return states_dict

############################################################################################################################

def fetchDistricts(web_page_data, state, age_group, dose):
	"""Fetch the District where Vaccination is available from the Web-page data for a given State, Dose and Age Group
	and provide Options to select the respective District.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Districts (where the Vaccination is available for a given State, Dose, Age Group) and Options to select,
		with Key as 'Option' and Value as 'Command'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchDistricts(web_page_data, 'Ladakh', '18+', '2'))
	{
		'1': 'Kargil', '2': 'Leh'
	}
	"""

	districts_dict = {}
	
	dist_list = []
	for k in web_page_data:
		soup5 = BeautifulSoup(str(k), 'html.parser')
		dose_find = soup5.find('td', class_='dose_num')
		if(dose_find.get_text() == dose):
			age_find = soup5.find('td', class_='age')
			if(age_find.get_text() == age_group):
				state_find = soup5.find('td', class_='state_name')
				if(state_find.get_text() == state):
					dist_find = soup5.find('td', class_='district_name')
					dist_list.append(dist_find.get_text())	
	unique_list = []
	for x in dist_list:
		if x not in unique_list:
			unique_list.append(x)

	unique_list.sort()

	temp_dict = {}
	num = 1
	for q in unique_list:
		sr_num = str(num)
		mydict = {sr_num:q}
		districts_dict = {**temp_dict,**mydict}
		temp_dict = districts_dict
		num+=1		

	return districts_dict

############################################################################################################################

def fetchHospitalVaccineNames(web_page_data, district, state, age_group, dose):
	"""Fetch the Hospital and the Vaccine Names from the Web-page data available for a given District, State, Dose and Age Group
	and provide Options to select the respective Hospital and Vaccine Name.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Hosptial and Vaccine Names (where the Vaccination is available for a given District, State, Dose, Age Group)
		and Options to select, with Key as 'Option' and Value as another dictionary having Key as 'Hospital Name' and Value as 'Vaccine Name'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchHospitalVaccineNames(web_page_data, 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {
				'MedStar Hospital Center': 'Covaxin'
			}
	}
	>>> print(fetchHospitalVaccineNames(web_page_data, 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {
				'Eden Clinic': 'Covishield'
			}
	}
	"""
	
	hospital_vaccine_names_dict = {}
	
	hospital_list = []
	for k in web_page_data:
		soup6 = BeautifulSoup(str(k), 'html.parser')
		dose_find = soup6.find('td', class_='dose_num')
		if(dose_find.get_text() == dose):
			age_find = soup6.find('td', class_='age')
			if(age_find.get_text() == age_group):
				state_find = soup6.find('td', class_='state_name')
				if(state_find.get_text() == state):
					dist_find = soup6.find('td', class_='district_name')
					if(dist_find.get_text() == district):
						hospital_find = soup6.find('td', class_='hospital_name')
						vaccine_find = soup6.find('td', class_='vaccine_name')
						hos_dict = {hospital_find.get_text() : vaccine_find.get_text()}
						hospital_list.append(hos_dict)	

	unique_list = []
	for x in hospital_list:
		if x not in unique_list:
			unique_list.append(x)

	unique_list.sort()

	temp_dict = {}
	num = 1
	for q in unique_list:
		sr_num = str(num)
		mydict = {sr_num:q}
		hospital_vaccine_names_dict = {**temp_dict,**mydict}
		temp_dict = hospital_vaccine_names_dict
		num+=1								

	return hospital_vaccine_names_dict

############################################################################################################################

def fetchVaccineSlots(web_page_data, hospital_name, district, state, age_group, dose):
	"""Fetch the Dates and Slots available on those dates from the Web-page data available for a given Hospital Name, District, State, Dose and Age Group
	and provide Options to select the respective Date and available Slots.

	Parameters
	----------
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	hospital_name : str
		Name of Hospital where Vaccination is available for given District, State, Dose and Age Group
	district : str
		District where Vaccination is available for a given State, Dose and Age Group
	state : str
		State where Vaccination is available for a given Dose and Age Group
	age_group : str
		Age Group available for Vaccination and its availability in the States
	dose : str
		Dose available for Vaccination and its availability for the Age Groups

	Returns
	-------
	dict
		Dictionary with the Dates and Slots available on those dates (where the Vaccination is available for a given Hospital Name,
		District, State, Dose, Age Group) and Options to select, with Key as 'Option' and Value as another dictionary having
		Key as 'Date' and Value as 'Available Slots'
	
	Example
	-------
	>>> url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	>>> web_page_data = fetchWebsiteData(url_website)
	>>> print(fetchVaccineSlots(web_page_data, 'MedStar Hospital Center', 'Kargil', 'Ladakh', '18+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '81'}, '3': {'May 17': '109'}, '4': {'May 18': '78'},
		'5': {'May 19': '89'}, '6': {'May 20': '57'}, '7': {'May 21': '77'}
	}
	>>> print(fetchVaccineSlots(web_page_data, 'Eden Clinic', 'South Goa', 'Goa', '45+', '2'))
	{
		'1': {'May 15': '0'}, '2': {'May 16': '137'}, '3': {'May 17': '50'}, '4': {'May 18': '78'},
		'5': {'May 19': '145'}, '6': {'May 20': '64'}, '7': {'May 21': '57'}
	}
	"""

	vaccine_slots = {}
	
	slot_list = []
	for k in web_page_data:
		soup7 = BeautifulSoup(str(k), 'html.parser')
		dose_find = soup7.find('td', class_='dose_num')
		if(dose_find.get_text() == dose):
			age_find = soup7.find('td', class_='age')
			if(age_find.get_text() == age_group):
				state_find = soup7.find('td', class_='state_name')
				if(state_find.get_text() == state):
					dist_find = soup7.find('td', class_='district_name')
					if(dist_find.get_text() == district):
						hospital_find = soup7.find('td', class_='hospital_name')
						if(hospital_find.get_text() == hospital_name):
							may_15_find = soup7.find('td', class_='may_15')
							slot_dict = {'May 15' : may_15_find.get_text()}
							slot_list.append(slot_dict)
							may_16_find = soup7.find('td', class_='may_16')
							slot_dict = {'May 16' : may_16_find.get_text()}
							slot_list.append(slot_dict)
							may_17_find = soup7.find('td', class_='may_17')
							slot_dict = {'May 17' : may_17_find.get_text()}
							slot_list.append(slot_dict)
							may_18_find = soup7.find('td', class_='may_18')
							slot_dict = {'May 18' : may_18_find.get_text()}
							slot_list.append(slot_dict)
							may_19_find = soup7.find('td', class_='may_19')
							slot_dict = {'May 19' : may_19_find.get_text()}
							slot_list.append(slot_dict)
							may_20_find = soup7.find('td', class_='may_20')
							slot_dict = {'May 20' : may_20_find.get_text()}
							slot_list.append(slot_dict)
							may_21_find = soup7.find('td', class_='may_21')
							slot_dict = {'May 21' : may_21_find.get_text()}
							slot_list.append(slot_dict)	

	unique_list = []
	for x in slot_list:
		if x not in unique_list:
			unique_list.append(x)

	temp_dict = {}
	num = 1
	for q in unique_list:
		sr_num = str(num)
		mydict = {sr_num:q}
		vaccine_slots = {**temp_dict,**mydict}
		temp_dict = vaccine_slots
		num+=1	

	return vaccine_slots

############################################################################################################################

def openConnection():
	"""Opens a socket connection on the HOST with the PORT address.

	Returns
	-------
	socket
		Object of socket class for the Client connected to Server and communicate further with it
	tuple
		IP and Port address of the Client connected to Server
	"""

	client_socket = None
	client_addr = None

	
	ADDR =(HOST,PORT)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(ADDR)
	server.listen()

	client_socket, client_addr = server.accept()
	print("Client is connected at: ",ADDR)	
	
	return client_socket, client_addr

############################################################################################################################

def startCommunication(client_conn, client_addr, web_page_data):
	"""Starts the communication channel with the connected Client for scheduling an Appointment for Vaccination.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	client_addr : tuple
		IP and Port address of the Client connected to Server
	web_page_data : bs4.element.ResultSet
		All rows of Tabular data fetched from a website excluding the table headers
	"""

	invalid_count = 0
	while True:
		client_conn.send(bytes('''$$$$$$\            $$\      $$\ $$\                  $$$$$$\  $$\                  $$\     $$$$$$$\             $$\     
$$  __$$\           $$ | $\  $$ |\__|                $$  __$$\ $$ |                 $$ |    $$  __$$\            $$ |    
$$ /  \__| $$$$$$\  $$ |$$$\ $$ |$$\ $$$$$$$\        $$ /  \__|$$$$$$$\   $$$$$$\ $$$$$$\   $$ |  $$ | $$$$$$\ $$$$$$\   
$$ |      $$  __$$\ $$ $$ $$\$$ |$$ |$$  __$$\       $$ |      $$  __$$\  \____$$\\_$$  _|  $$$$$$$\ |$$  __$$\\_$$  _|  
$$ |      $$ /  $$ |$$$$  _$$$$ |$$ |$$ |  $$ |      $$ |      $$ |  $$ | $$$$$$$ | $$ |    $$  __$$\ $$ /  $$ | $$ |    
$$ |  $$\ $$ |  $$ |$$$  / \$$$ |$$ |$$ |  $$ |      $$ |  $$\ $$ |  $$ |$$  __$$ | $$ |$$\ $$ |  $$ |$$ |  $$ | $$ |$$\ 
\$$$$$$  |\$$$$$$  |$$  /   \$$ |$$ |$$ |  $$ |      \$$$$$$  |$$ |  $$ |\$$$$$$$ | \$$$$  |$$$$$$$  |\$$$$$$  | \$$$$  |
 \______/  \______/ \__/     \__|\__|\__|  \__|       \______/ \__|  \__| \_______|  \____/ \_______/  \______/   \____/         ''','utf-8'))
		while True:
			client_conn.send(bytes("\n>>> Select the Dose of Vaccination:\n"+str(fetchVaccineDoses(web_page_data))+"\n",'utf-8'))
			data = client_conn.recv(1024)
			if(data.decode('utf-8') == '2'):
				print("Dose selected: ", data.decode('utf-8'))
				client_conn.send(bytes("\n<<< Dose selected: 2\n",'utf-8'))
				while True:
					client_conn.sendall(bytes("\n>>> Provide the date of First Vaccination Dose (DD/MM/YYYY), for e.g. 12/5/2021",'utf-8'))
					data = client_conn.recv(1024)
					if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
						print("Client wants to quit!\nSaying Bye to client and closing the connection!")
						stopCommunication(client_conn)
					elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
						break
					elif(checkdate(data.decode('utf-8'))):
						no_of_weeks = calc_weeks(data.decode('utf-8')) 
						if(no_of_weeks < 0):
							while True:
								client_conn.send(bytes("\n<<<< Invalid Date provided of First Vaccination Dose: ",'utf-8'))
								break
						else:
							client_conn.send(bytes("\n<<< Date of First Vaccination Dose provided: "+str(data.decode('utf-8'))+"\n<<< Number of weeks from today: "+str(no_of_weeks),'utf-8'))
							if(no_of_weeks >= 0 and no_of_weeks < 4):
								client_conn.send(bytes("\n<<< You are not eligible right now for 2nd Vaccination Dose! Try after "+str(4 - no_of_weeks)+" weeks.",'utf-8'))
								stopCommunication(client_conn)
							elif(no_of_weeks > 8):
								client_conn.send(bytes("\n<<< You have been late in scheduling your 2nd Vaccination Dose by "+str(no_of_weeks - 8)+" weeks.\n",'utf-8'))
							elif(no_of_weeks >= 4 and no_of_weeks <= 8):
								client_conn.send(bytes("\n<<< You are eligible for 2nd Vaccination Dose and are in the right time-frame to take it.\n",'utf-8'))
							key_dose = '2'
							while True:
								client_conn.send(bytes("\n>>> Select the Age Group:\n"+str(fetchAgeGroup(web_page_data, key_dose))+"\n",'utf-8'))
								data = client_conn.recv(1024)
								if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
									print("Client wants to quit!\nSaying Bye to client and closing the connection!")
									stopCommunication(client_conn)
								elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
									break
								elif((data.decode('utf-8')).isdigit()):
									if(int(data.decode('utf-8')) <= len(fetchAgeGroup(web_page_data, key_dose)) and int(data.decode('utf-8')) != 0):
										for index, (key_age, value_age) in enumerate(fetchAgeGroup(web_page_data, key_dose).items()):
											if (data.decode('utf-8') == key_age):
												print("Age Group selected: ",str(value_age))
												client_conn.send(bytes("\n<<< Selected Age Group: "+str(value_age),'utf-8'))
												while True:
													client_conn.send(bytes("\n>>> Select the State:\n"+str(fetchStates(web_page_data,  value_age, key_dose))+"\n",'utf-8'))
													data = client_conn.recv(1024)
													if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
														print("Client wants to quit!\nSaying Bye to client and closing the connection!")
														stopCommunication(client_conn)
													elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
														break
													elif((data.decode('utf-8')).isdigit()):
														if(int(data.decode('utf-8')) <= len(fetchStates(web_page_data,  value_age, key_dose)) and int(data.decode('utf-8')) != 0):
															for index, (key_state, value_state) in enumerate(fetchStates(web_page_data, value_age, key_dose).items()):
																if(data.decode('utf-8') == key_state):
																	print("State selected: ",str(value_state))
																	client_conn.send(bytes("\n<<< Selected State: "+str(value_state),'utf-8'))
																	while True:
																		client_conn.send(bytes("\n>>> Select the District:\n"+str(fetchDistricts(web_page_data, value_state, value_age, key_dose))+"\n",'utf-8'))
																		data = client_conn.recv(1024)
																		if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																			print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																			stopCommunication(client_conn)
																		elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																			break
																		elif((data.decode('utf-8')).isdigit()):
																			if(int(data.decode('utf-8')) <= len(fetchDistricts(web_page_data, value_state, value_age, key_dose)) and int(data.decode('utf-8')) != 0):
																				for index, (key_dist, value_dist) in enumerate(fetchDistricts(web_page_data, value_state, value_age, key_dose).items()):
																					if(data.decode('utf-8') == key_dist):
																						print("District selected: ",str(value_dist))
																						client_conn.send(bytes("\n<<< Selected District: "+str(value_dist),'utf-8'))
																						while True:
																							client_conn.send(bytes(	"\n>>> Select the Vaccination Center Name:\n"+str(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose))+"\n",'utf-8'))
																							data = client_conn.recv(1024)
																							if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																								print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																								stopCommunication(client_conn)
																							elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																								break
																							elif((data.decode('utf-8')).isdigit()):
																								if(int(data.decode('utf-8')) <= len(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose)) and int(data.decode('utf-8')) != 0):
																									for index, (key_hos, value_hos) in enumerate(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose).items()):
																										if(data.decode('utf-8') == key_hos):
																											hos_dict = value_hos
																											for index, (key_hos_dict, value_hos_dict) in enumerate(hos_dict.items()):
																												print("Hospital selected: ",str(key_hos_dict))
																												client_conn.send(bytes("\n<<< Selected Vaccination Center: "+str(key_hos_dict),'utf-8'))
																												while True:
																													client_conn.send(bytes("\n>>> Select one of the available slots to schedule the Appointment:\n"+str(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose))+"\n",'utf-8'))
																													data = client_conn.recv(1024)
																													if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																														print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																														stopCommunication(client_conn)
																													elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																														break
																													elif((data.decode('utf-8')).isdigit()):
																														if(int(data.decode('utf-8')) <= len(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose)) and int(data.decode('utf-8')) != 0):
																															for index, (key_slot, value_slot) in enumerate(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose).items()):
																																if(data.decode('utf-8') == key_slot):
																																	slot_dict = value_slot
																																	for index, (key_slot_dict, value_slot_dict) in enumerate(slot_dict.items()):
																																		print("Vaccination Date selected: ", str(key_slot_dict))
																																		print("Available Slots on that date: ", str(value_slot_dict))
																																		client_conn.send(bytes("\n<<< Selected Vaccination Appointment Date: "+str(key_slot_dict)+"\n<<< Available Slots on the selected Date: "+str(value_slot_dict),'utf-8'))
																																		if(int(value_slot_dict) > 0):
																																			client_conn.send(bytes("<<< Your appointment is scheduled. Make sure to carry ID Proof while you visit Vaccination Center!",'utf-8'))
																																			stopCommunication(client_conn)
																																		else:
																																			client_conn.send(bytes("<<< Selected Appointment Date has no available slots, select another date!",'utf-8'))
																																			continue
																														else:
																															invalid_count+=1
																															print("Invalid input detected "+str(invalid_count)+" time(s)!")
																															client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																															if(invalid_count < 3):
																																continue
																															elif(invalid_count == 3):
																																print("Notifying the client and closing the connection!")
																																stopCommunication(client_conn)
																													else:
																														invalid_count+=1
																														print("Invalid input detected "+str(invalid_count)+" time(s)!")
																														client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																														if(invalid_count < 3):
																															continue
																														elif(invalid_count == 3):
																															print("Notifying the client and closing the connection!")
																															stopCommunication(client_conn)
																								else:
																									invalid_count+=1
																									print("Invalid input detected "+str(invalid_count)+" time(s)!")
																									client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																									if(invalid_count < 3):
																										continue
																									elif(invalid_count == 3):
																										print("Notifying the client and closing the connection!")
																										stopCommunication(client_conn)							
																							else:
																								invalid_count+=1
																								print("Invalid input detected "+str(invalid_count)+" time(s)!")
																								client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																								if(invalid_count < 3):
																									continue
																								elif(invalid_count == 3):
																									print("Notifying the client and closing the connection!")
																									stopCommunication(client_conn)
																			else:
																				invalid_count+=1
																				print("Invalid input detected "+str(invalid_count)+" time(s)!")
																				client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																				if(invalid_count < 3):
																					continue
																				elif(invalid_count == 3):
																					print("Notifying the client and closing the connection!")
																					stopCommunication(client_conn)						
																		else:
																			invalid_count+=1
																			print("Invalid input detected "+str(invalid_count)+" time(s)!")
																			client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																			if(invalid_count < 3):
																				continue
																			elif(invalid_count == 3):
																				print("Notifying the client and closing the connection!")
																				stopCommunication(client_conn)
														else:
															invalid_count+=1
															print("Invalid input detected "+str(invalid_count)+" time(s)!")
															client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
															if(invalid_count < 3):
																continue
															elif(invalid_count == 3):
																print("Notifying the client and closing the connection!")
																stopCommunication(client_conn)														
													else:
														invalid_count+=1
														print("Invalid input detected "+str(invalid_count)+" time(s)!")
														client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
														if(invalid_count < 3):
															continue
														elif(invalid_count == 3):
															print("Notifying the client and closing the connection!")
															stopCommunication(client_conn)
									else:
										invalid_count+=1
										print("Invalid input detected "+str(invalid_count)+" time(s)!")
										client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
										if(invalid_count < 3):
											continue
										elif(invalid_count == 3):
											print("Notifying the client and closing the connection!")
											stopCommunication(client_conn)						
								else:
									invalid_count+=1
									print("Invalid input detected "+str(invalid_count)+" time(s)!")
									client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
									if(invalid_count < 3):
										continue
									elif(invalid_count == 3):
										print("Notifying the client and closing the connection!")
										stopCommunication(client_conn)
					else:
						continue

			elif(data.decode('utf-8') == '1'):
				for index, (key_dose, value_dose) in enumerate(fetchVaccineDoses(web_page_data).items()):
					if (data.decode('utf-8') == key_dose):
						print("Dose selected: ", data.decode('utf-8'))
						client_conn.send(bytes("\n<<< Dose selected: "+str(key_dose),'utf-8'))
						while True:
							client_conn.send(bytes("\n>>> Select the Age Group:\n"+str(fetchAgeGroup(web_page_data, key_dose))+"\n",'utf-8'))
							data = client_conn.recv(1024)
							if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
								print("Client wants to quit!\nSaying Bye to client and closing the connection!")
								stopCommunication(client_conn)
							elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
								break
							elif((data.decode('utf-8')).isdigit()):
								if(int(data.decode('utf-8')) <= len(fetchAgeGroup(web_page_data, key_dose)) and int(data.decode('utf-8')) != 0):
									for index, (key_age, value_age) in enumerate(fetchAgeGroup(web_page_data, key_dose).items()):
										if (data.decode('utf-8') == key_age):
											print("Age Group selected: ",str(value_age))
											client_conn.send(bytes("\n<<< Selected Age Group: "+str(value_age),'utf-8'))
											while True:
												client_conn.send(bytes("\n>>> Select the State:\n"+str(fetchStates(web_page_data,  value_age, key_dose))+"\n",'utf-8'))
												data = client_conn.recv(1024)
												if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
													print("Client wants to quit!\nSaying Bye to client and closing the connection!")
													stopCommunication(client_conn)
												elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
													break
												elif((data.decode('utf-8')).isdigit()):
													if(int(data.decode('utf-8')) <= len(fetchStates(web_page_data,  value_age, key_dose)) and int(data.decode('utf-8')) != 0):
														for index, (key_state, value_state) in enumerate(fetchStates(web_page_data, value_age, key_dose).items()):
															if(data.decode('utf-8') == key_state):
																print("State selected: ",str(value_state))
																client_conn.send(bytes("\n<<< Selected State: "+str(value_state),'utf-8'))
																while True:
																	client_conn.send(bytes("\n>>> Select the District:\n"+str(fetchDistricts(web_page_data, value_state, value_age, key_dose))+"\n",'utf-8'))
																	data = client_conn.recv(1024)
																	if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																		print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																		stopCommunication(client_conn)
																	elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																		break
																	elif((data.decode('utf-8')).isdigit()):
																		if(int(data.decode('utf-8')) <= len(fetchDistricts(web_page_data, value_state, value_age, key_dose)) and int(data.decode('utf-8')) != 0):
																			for index, (key_dist, value_dist) in enumerate(fetchDistricts(web_page_data, value_state, value_age, key_dose).items()):
																				if(data.decode('utf-8') == key_dist):
																					print("District selected: ",str(value_dist))
																					client_conn.send(bytes("\n<<< Selected District: "+str(value_dist),'utf-8'))
																					while True:
																						client_conn.send(bytes(	"\n>>> Select the Vaccination Center Name:\n"+str(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose))+"\n",'utf-8'))
																						data = client_conn.recv(1024)
																						if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																							print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																							stopCommunication(client_conn)
																						elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																							break
																						elif((data.decode('utf-8')).isdigit()):
																							if(int(data.decode('utf-8')) <= len(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose)) and int(data.decode('utf-8')) != 0):
																								for index, (key_hos, value_hos) in enumerate(fetchHospitalVaccineNames(web_page_data, value_dist, value_state, value_age, key_dose).items()):
																									if(data.decode('utf-8') == key_hos):
																										hos_dict = value_hos
																										for index, (key_hos_dict, value_hos_dict) in enumerate(hos_dict.items()):
																											print("Hospital selected: ",str(key_hos_dict))
																											client_conn.send(bytes("\n<<< Selected Vaccination Center: "+str(key_hos_dict),'utf-8'))
																											while True:
																												client_conn.send(bytes("\n>>> Select one of the available slots to schedule the Appointment:\n"+str(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose))+"\n",'utf-8'))
																												data = client_conn.recv(1024)
																												if(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
																													print("Client wants to quit!\nSaying Bye to client and closing the connection!")
																													stopCommunication(client_conn)
																												elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
																													break
																												elif((data.decode('utf-8')).isdigit()):
																													if(int(data.decode('utf-8')) <= len(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose)) and int(data.decode('utf-8')) != 0):
																														for index, (key_slot, value_slot) in enumerate(fetchVaccineSlots(web_page_data, key_hos_dict, value_dist, value_state,value_age,key_dose).items()):
																															if(data.decode('utf-8') == key_slot):
																																slot_dict = value_slot
																																for index, (key_slot_dict, value_slot_dict) in enumerate(slot_dict.items()):
																																	print("Vaccination Date selected: ", str(key_slot_dict))
																																	print("Available Slots on that date: ", str(value_slot_dict))
																																	client_conn.send(bytes("\n<<< Selected Vaccination Appointment Date: "+str(key_slot_dict)+"\n<<< Available Slots on the selected Date: "+str(value_slot_dict),'utf-8'))
																																	if(int(value_slot_dict) > 0):
																																		client_conn.send(bytes("<<< Your appointment is scheduled. Make sure to carry ID Proof while you visit Vaccination Center!",'utf-8'))
																																		stopCommunication(client_conn)
																																	else:
																																		client_conn.send(bytes("<<< Selected Appointment Date has no available slots, select another date!",'utf-8'))
																																		continue
																													else:
																														invalid_count+=1
																														print("Invalid input detected "+str(invalid_count)+" time(s)!")
																														client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																														if(invalid_count < 3):
																															continue
																														elif(invalid_count == 3):
																															print("Notifying the client and closing the connection!")
																															stopCommunication(client_conn)
																												else:
																													invalid_count+=1
																													print("Invalid input detected "+str(invalid_count)+" time(s)!")
																													client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																													if(invalid_count < 3):
																														continue
																													elif(invalid_count == 3):
																														print("Notifying the client and closing the connection!")
																														stopCommunication(client_conn)
																							else:
																								invalid_count+=1
																								print("Invalid input detected "+str(invalid_count)+" time(s)!")
																								client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																								if(invalid_count < 3):
																									continue
																								elif(invalid_count == 3):
																									print("Notifying the client and closing the connection!")
																									stopCommunication(client_conn)							
																						else:
																							invalid_count+=1
																							print("Invalid input detected "+str(invalid_count)+" time(s)!")
																							client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																							if(invalid_count < 3):
																								continue
																							elif(invalid_count == 3):
																								print("Notifying the client and closing the connection!")
																								stopCommunication(client_conn)
																		else:
																			invalid_count+=1
																			print("Invalid input detected "+str(invalid_count)+" time(s)!")
																			client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																			if(invalid_count < 3):
																				continue
																			elif(invalid_count == 3):
																				print("Notifying the client and closing the connection!")
																				stopCommunication(client_conn)						
																	else:
																		invalid_count+=1
																		print("Invalid input detected "+str(invalid_count)+" time(s)!")
																		client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
																		if(invalid_count < 3):
																			continue
																		elif(invalid_count == 3):
																			print("Notifying the client and closing the connection!")
																			stopCommunication(client_conn)
													else:
														invalid_count+=1
														print("Invalid input detected "+str(invalid_count)+" time(s)!")
														client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
														if(invalid_count < 3):
															continue
														elif(invalid_count == 3):
															print("Notifying the client and closing the connection!")
															stopCommunication(client_conn)														
												else:
													invalid_count+=1
													print("Invalid input detected "+str(invalid_count)+" time(s)!")
													client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
													if(invalid_count < 3):
														continue
													elif(invalid_count == 3):
														print("Notifying the client and closing the connection!")
														stopCommunication(client_conn)
								else:
									invalid_count+=1
									print("Invalid input detected "+str(invalid_count)+" time(s)!")
									client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
									if(invalid_count < 3):
										continue
									elif(invalid_count == 3):
										print("Notifying the client and closing the connection!")
										stopCommunication(client_conn)						
							else:
								invalid_count+=1
								print("Invalid input detected "+str(invalid_count)+" time(s)!")
								client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
								if(invalid_count < 3):
									continue
								elif(invalid_count == 3):
									print("Notifying the client and closing the connection!")
									stopCommunication(client_conn)

			elif(data.decode('utf-8') == 'q' or data.decode('utf-8') == 'Q'):
				print("Client wants to quit!\nSaying Bye to client and closing the connection!")
				stopCommunication(client_conn)
			elif(data.decode('utf-8') == 'b' or data.decode('utf-8') == 'B'):
				continue
			else:
				invalid_count+=1
				print("Invalid input detected "+str(invalid_count)+" time(s)!")
				client_conn.send(bytes("\n<<< Invalid input provided "+str(invalid_count)+" time(s)! Try again.",'utf-8'))
				if(invalid_count == 3):
					print("Notifying the client and closing the connection!")
					stopCommunication(client_conn)

############################################################################################################################

def stopCommunication(client_conn):
	"""Stops or Closes the communication channel of the Client with a message.

	Parameters
	----------
	client_conn : socket
		Object of socket class for the Client connected to Server and communicate further with it
	"""
	
	client_conn.send(bytes("\n<<< See ya! Visit again :)",'utf-8'))
	client_conn.close()
	exit()

############################################################################################################################

def checkdate(date_given):
	"""
	Checks if the given date is valid or not
	
	Parameters
	----------
	date_given : str
		Date provided for the first dose
	"""
	try:
		datetime.datetime.strptime(date_given,"%d/%m/%Y")
		return True
	except:
		client_conn.send(bytes("\n<<<< Invalid Date provided of First Vaccination Dose: ",'utf-8'))
		return False

############################################################################################################################

def calc_weeks(first_date):
	"""
	Calculates number of weeks between first does and today
	
	Parameters
	----------
	first_date : str
		Date provided for the first dose
	"""
	Today = datetime.date.today()
	date_object = datetime.datetime.strptime(first_date, "%d/%m/%Y")
	span = Today - date_object.date()
	no_of_week = int(span.days/7)
	
	return no_of_week

############################################################################################################################


if __name__ == '__main__':
	"""Main function, code begins here
	"""
	url_website = "https://www.mooc.e-yantra.org/task-spec/fetch-mock-covidpage"
	web_page_data = fetchWebsiteData(url_website)
	client_conn, client_addr = openConnection()
	startCommunication(client_conn, client_addr, web_page_data)
