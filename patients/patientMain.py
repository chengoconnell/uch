import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import re
import string

connection = sql.connect('UCH.db')
c = connection.cursor()


def options(nhsNumber):
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
    results = c.fetchall()
    if results[0][12] == 0:
        print("A GP needs to confirm your registration before you can access our services. Please try logging in tomorrow.")
        exit()
    else:
        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to view your confirmed appointments")
        print("Choose [3] to cancel an appointment")
        print("Choose [4] to see your medical profile")
        print("Choose [5] to see your contact details")
        print("Choose [6] to update your contact details")
        print("Choose [0] to exit")
        choice = int(input("Choice: "))
        if choice == 1:
            x = Appointment()
            x.bookAppointment(nhsNumber)
            options(nhsNumber)
        elif choice == 2:
            x = Appointment()
            x.viewAppConfirmations(nhsNumber)
            options(nhsNumber)
        elif choice == 3:
            x = Appointment()
            x.cancelAppointment(nhsNumber)
            options(nhsNumber)
        elif choice == 4:
            print("Choose [1] to see your medical profile")
            print("Choose [2] to take the lifestyle risk questionnaire")
            print("Choose [3] to update your medical history")
            qchoice = int(input("Choice: "))
            if qchoice == 1:
                name = PatientMedical()
                name.show_profile(nhsNumber)
            elif qchoice == 2:
                print("Please fill out the following risk profile")
                x = RiskProfile()  # need to pass patientEmail into the functions
                x.questions()
                x.BMI_calculator()
                x.diet()
                x.smoking()
                x.drugs()
                x.alcohol()
                x.insert_to_table(nhsNumber)
            elif qchoice == 3:
                x = PatientMedical()
                x.vaccination(nhsNumber)
                x.cancer(nhsNumber)
        elif choice == 5:
            print(results[0])
        elif choice == 6:
            pass
        elif choice == 0:
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()


def task():
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=int(input("Choice: "))
    if action != 1 and action != 2:
        print("I'm sorry, '" + str(action) + "' is an invalid option. ")
        task()
    elif action == 1:
        # First Name
        firstName=input("Please enter your first name. ")
        firstName = string.capwords(firstName.strip())
        print(firstName)
        # Last Name
        lastName=input("Please enter your last name. ")
        lastName = string.capwords(lastName.strip())
        print(lastName)
        # Date of Birth
        dateOfBirth = input('Please enter your birthday in DD-MM-YYYY format. ')
        day, month, year = map(int, dateOfBirth.split('-'))
        dateOfBirth = datetime.date(year, month, day)
        print(dateOfBirth)
        # Age
        today = date.today()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        print(age)
        # Gender
        print("Gender")
        print("Choose [1] for female")
        print("Choose [2] for male")
        print("Choose [3] for non-binary")
        gender=int(input("Choice: "))
        while gender != 1 and gender != 2 and gender != 3:
            print("I'm sorry, '" + gender + "' is an invalid option. ")
            print("Gender")
            print("Choose [1] for female")
            print("Choose [2] for male")
            print("Choose [3] for non-binary")
            gender=int(input("Choice: "))
        if gender == 1:
            gender = "Female"
        elif gender == 2:
            gender = "Male"
        elif gender == 3:
            gender = "Non-Binary"
        print(gender)
        # Address Line 1
        addressLine1 = input("Address Line 1: ")
        addressLine1 = string.capwords(addressLine1.strip())
        print(addressLine1)
        # Address Line 2
        addressLine2 = input("Address Line 2: ")
        addressLine2 = string.capwords(addressLine2.strip())
        print(addressLine2)
        # City
        city = input("City: ")
        city = string.capwords(city.strip())
        addressLine2 = (addressLine2 + " " + city).strip()
        print(addressLine2)
        # Postcode
        postcode = input("Postcode: ")
        postcode = postcode.strip().upper()
        print(postcode)
        # Telephone Number
        telephoneNumber = input("Telephone number, including country code (i.e. +447123456789): ")
        telephoneNumber = int(re.sub("[^0-9]", "", telephoneNumber))
        print(telephoneNumber)
        # Email
        patientEmail=input("Please enter your email. ")
        goodEmail = True
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            goodEmail = True
        else:
            goodEmail = False
        while goodEmail == False:
            print("I'm sorry, that is not a valid email. Please try again. ")
            patientEmail=input("Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
                goodEmail = True
            else:
                goodEmail = False
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            while patientEmails != []:
                print("I'm sorry, that email is already in use. Please use another email.")
                patientEmail=input("Please enter your email. ")
                c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
                patientEmails = c.fetchall()
        # Password
        password=input("Please enter your password. ")
        x=Patient(patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2, postcode, telephoneNumber, password)
        x.register()
        x.registrationSummary()
        options(x.nhsNumber)
    elif action == 2:
        patientEmail=input("Please enter your email. ")
        goodEmail = True
        if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
            goodEmail = True
        else:
            goodEmail = False
        while goodEmail == False:
            print("I'm sorry, that is not a valid email. Please try again. ")
            patientEmail=input("Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", patientEmail):
                goodEmail = True
            else:
                goodEmail = False
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails == []:
            while patientEmails == []:
                print("I'm sorry, that email is not in our system. Please try again. ")
                patientEmail=input("Email: ")
                c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
                patientEmails = c.fetchall()
        password=input("Please enter your password. ")
        if password != patientEmails[0][11]:
            while password != patientEmails[0][11]:
                print("I'm sorry, that password is not correct. ")
                password=input("Please enter your password. ")
            print("Wonderful! Hi, " + patientEmails[0][2] + " you are now logged in.")
            options(patientEmails[0][0])
        else:
            print("Wonderful! Hi, " + patientEmails[0][2] + " you are now logged in.")
            options(patientEmails[0][0])
