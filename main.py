#Psychiatrist consultation Reservation System src code

#library for opening csv file
import csv

#library for making passsword invisible
import getpass

#make file name as variable
FILE_NAME = "UserInfo.csv"
APPT_FILE = "Appointment.csv"

#id generator to automatically generate id for each patient
def generate_id():

	#initialize the first id
	last_id = 'P0'

	#open file as read
	with open(FILE_NAME, 'r') as file:
		id_reader = csv.reader(file)
		next(id_reader)

	
		for row in id_reader:
			#check for the last id in file
			if len(row)>=1:
				#make it the the last id
				last_id = row[0]

	changeNumber = int(last_id[1:]) + 1
	new_id = 'P' + str(changeNumber)
	#value is returned to be passed to other functions
	return new_id

#register function for users without an account
def register():

	name_exist = False
	print("\t\t====================")
	print("\t\tAccount Registration")
	print("\t\t====================")
	while True:
		NewName = input("\tEnter your name in capital letter: ")

		if NewName != NewName.upper() and NewName != NewName.isalpha():
			print("\tPlease enter your name in all capital letter and alphabet only! :-)\n")

		#check if the name is already registered
		with open(FILE_NAME, 'r') as file:
			reader = csv.reader(file)
			next(reader)

			for row in reader:
				if NewName==row[1]:
					name_exist = True
					break
		if name_exist:
			print("\tName already exist, please login!")
			login()
			return

	
	while True:
		NewPass = getpass.getpass("\tEnter new Passwordi: ")
		PassLen = len(NewPass)
		if PassLen < 8:
			print("\tPassword cannot less than 8 characters!\n ")
		else:
			break

	while True:
		ConfPass = getpass.getpass("\tConfirm Password: ")
		if ConfPass == NewPass:
			break
		else:
			print("\tPassword does not match!\n")
	while True:
		NewEmail = input("\tEmail: ")
		if '@' not in NewEmail:
			print("\tThat's not a correct email format!\n  ")
		else:
			break
	
	#take the generated id as patient's id
	NewID = generate_id()

	#open and append new data to csv file
	with open(FILE_NAME, 'a', newline='') as file:
		fieldnames = ['patient_ID', 'patient_Name', 'patient_Email', 'password']
		writer = csv.DictWriter(file, fieldnames=fieldnames)

		writer.writerow({'patient_ID':NewID, 'patient_Name': NewName, 'patient_Email': NewEmail, 'password':NewPass})
		
	print("\n\n\t\t==================================")
	print("\t\tRegistration Succesful! :) ")
	print("\t\tYour ID: ",NewID)
	print("\t\t====================================\n")

	login()

#menu function for navigation through the system
def menu():
	print("\t===============================================")
	print("\tPsychiatrist Consultation Reservation System")
	print("\t===============================================\n")
	print("\t\t1. Make Appointment")
	print("\t\t2. View Appointment")
	print("\t\t3. Search Appoinment")
	print("\t\t4. View Profile")
	print("\t\t5. Print this menu")
	print("\t\t6. Exit")


#login function for users with existing account
def login():
	check = False
	attempt = 3
	
	print("\t\t\t======")
	print("\t\t\tLog In")
	print("\t\t\t======")

	while attempt > 0:
		username = input("\tUsername: ")
		password = getpass.getpass("\tPassword: ")
		
		#check if the password matches the username
		with open(FILE_NAME, 'r') as file:
			login_reader = csv.reader(file)
			next(login_reader)

			for row in login_reader:
				if (username==row[1]) and password==row[3]:
					print("\t")
					print("\t\t===============================")
					print("\t\t\tLogin Succesful! ")
					print("\t\t===============================\n")
					#pass user details into other function
					user_session(row)
					return
				if username == row[1]:
					check = True
		attempt-=1
		if check:
			print("\tWrong Password! ")
		else:
			print("\tUsername not found! ")

		print("\tAttempts left: ",attempt)

#this fucntion is activated when user is inside the system
def user_session(user):
	menu()
	while True:

		#error handler if user enter anything other than integer
		try:
			choice = int(input("\tPick a number from the list to perform action: "))
		except:
			print("Please enter what's inside the menu.")

		else:
			match choice:
				case 1:
					book_appointment(user)
					menu()
				case 2:
					view_appointment(user)
					menu()
				case 4:
					view_profile(user)
					menu()
				case 5:
					menu()
				case 6:
					break
					
				case _:
					print("\n\tInvalid option!\n")
		
					
def reservation_id_generator(user):
	#id format
	last_id = 'R0'

	with open(APPT_FILE, 'r') as file:
		reader = csv.reader(file)
		next(reader)
		for row in reader:
			if len(row)>=1:
				last_id = row[0]

		changeNumber = int(last_id[1:]) + 1 
		new_id = 'R' + str(changeNumber)
		return new_id



#function to allow customer make a reservation	
def book_appointment(user):

	not_booked = True
	#open file to append data inside
	with open(APPT_FILE, 'a', newline='') as file:
		fieldnames = ['Reservation_ID', 'patient_ID', 'patient_name', 'Date', 'Time', 'Package']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
	
	#pass the generated reservation ID from generator function
	RevID = reservation_id_generator(user)

	print("\t\tPlease enter a date to book: ")
	#loop to get reservation date from user
	while True:
		Day = int(input("\t\tDD: "))
		Month = int(input("\t\tMM: "))
		Year = (input("\t\tYYYY: "))
		if (Day > 31 or Day < 0) or (Month > 12 or Month <=0) or (len(Year) != 4):
			print("\t\tInvalid date, please enter again!")
			continue

		#open file as read
		with open(APPT_FILE, 'r') as file:
			reader = csv.reader(file)
			next(reader)
			Date = str(Day) + '/' + str(Month) + '/' + str(Year)
			
			#check if the date is already booked
			for row in reader:
				if row[3] == Date:
					print("\t\tThe date is already booked, please enter another date!")
					not_booked = False
					break
			if not_booked:
				break

	#loop to get time from user
	while True:
		Time = round(float(input("\t\tEnter the time this date(24 hour system): ")),2)
		if Time < 0 and Time >=24:
			print("\t\tPlease enter the time in 24 hour system format.")
		if Time >= 0 and Time < 12:
			str_Time = f"{Time:.2f} .a.m"
			break
		elif Time > 11:
			str_Time = f"{Time:.2f} .p.m"
			break

	package_menu()
	#loop to get package from user
	while True:
		Package = input("\tPlease select a package: ")
		if Package != 'a' and Package != 'b':
			print("\t\tInvalid Input, please select again!")
		else:
			break
			

	print("\t\tBooking succesfull!")

	#open file to append data		
	with open(APPT_FILE, 'a', newline='') as file:
		fieldnames = ['Reservation_ID', 'patient_ID', 'patient_name', 'Date', 'Time', 'Package']
		writer = csv.DictWriter(file, fieldnames=fieldnames)
		#append the inserted data to file
		writer.writerow({'Reservation_ID':RevID , 'patient_ID':user[0], 'patient_name': user[1], 'Date': Date, 'Time':str_Time, 'Package': Package})



#Function to view reserved appointments
def view_appointment(user):
	Appt_number = 0
	Appointments = []

	#open file to read existing reservations
	with open(APPT_FILE, "r") as file:
		reader = csv.reader(file)
		#loop through every content to find reservations by user
		for row in reader:
			#read user's id
			if row[1] == user[0]:
				Appt_number += 1
				#append the info inside an empty list
				Appointments.append(row)
	#if no reservation
	if Appt_number == 0:
		print(f"\n\t\tYou have no booked Appointment.\n")
		return
	
	#print the result by iterating inside the appended list
	for Appt in Appointments:
		print("\t\tReservationID: ", Appt[0])
		print("\t\tDate         : ", Appt[3])
		print("\t\tTime         : ", Appt[4])
		print("\t\tType         : ", Appt[5])
		print("\n")

	delete = input("Do you want to cancel a reservation? [y/n]").lower()

	if delete == 'y' or delete == 'yes':
		cancel_appointment(user, Appointments)
	else:
		return
		

def cancel_appointment(user ,Appointments):

	updated_reservations = []
	available_ids = []
	#appends all reservations made by customer
	for Appt in Appointments:
		available_ids.append(Appt[0])

	while True:
		remover = input("\nEnter a reservation ID you want to remove: ")

		if remover not in available_ids:
			print("Please select available ID.")
			continue

		confirm = input("Are you sure? [y/n]: ").lower()
		if confirm == 'n':
			break

		with open (APPT_FILE, 'r') as file:
			reader = csv.reader(file)
			next(reader)
			for row in reader:
				#append every row accept the one user ask to delete
				if row[0] != remover:
					updated_reservations.append(row)
		#open file in write mode and rewite back everything accept deleted data
		with open (APPT_FILE, 'w', newline="") as file:
			writer = csv.writer(file)
			writer.writerow(['Reservation_ID', 'patient_ID', 'patient_name', 'Date', 'Time', 'Package'])
			writer.writerows(updated_reservations)

		break


		

#menu of available packages for user to choose from
def package_menu():
	print("\n\t\t\t========")
	print("\t\t\tPACKAGES")
	print("\t\t\t========\n")
	print("\ta) Initial Psychiatrist Consultation -(60 minutes)	   : RM 320")
	print("\tb) Follow-up Psychiatrist Consultation -(20 - 30 minutes) : RM 180")


#view profile function which display user's details
def view_profile(user):
	print("\n\t\t\t================")
	print("\t\t\tPatient Details")
	print("\t\t\t================")
	print("\t ID   : ", user[0])
	print("\t Name : ", user[1])
	print("\t Email: ", user[2])
	print("\n")
	

# The start of the program
exist = input("\tDo you have an existing account? [y/n]: " ).lower()


if exist == 'y':
	login()
else:
	register()
					
print("hi")
