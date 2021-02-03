A Simple server-client system using a reliable communication stream built on top of UDP. Application is used to make reservations for Specific University Rooms on specific days at Specific timeslots. They are saved on to a "database", a .txt file that writing and reading is happening on. Assignment 1 for SYSC 4502: Communications Software Programming, Carleton University 2021
	

	In this submission:
	README: for understanding the code
	
	server.py: the server side code
			When launching server.py using the command line, use the following command in the appropriate directive
			python server.py 2000
	
	client.py: the client side code
			When launching client.py using the command line, use the following command in the appropriate directive
			python client.py 127.0.0.1 2000



	1st argument of server.py must match second Argument on Client. First parameter of client.py is the IP of the machine that is
	running server.py. 127.0.0.1 can be used when running server.py on local machine. 


	This Program needs:
		days.txt - What days a reservation can be made
		rooms.txt - What rooms a reservation can be made on
		timeslots.txt - What timeslots a reservation can be made on
		reservations.txt - The reservations that have been made will be saved here, acts as the DataBase of the application



	The program was written using Windows 10 operating system, using Python 3.6 
	IDE used was PyCharm


	Written by Shaviyo Marasinghe (101019133)
	for SYSC 4502 Assignment 1
