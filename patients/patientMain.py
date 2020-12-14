import sqlite3 as sql
import datetime
from datetime import date
from patients.patient import Patient
from patients.PatientRiskProfile import PatientMedical
from patients.lifeStyleQuestionnaire import RiskProfile
from patients.appointment import Appointment
import re
import string
import pandas as pd
import usefulfunctions as uf

""" This is the main menu when the patient is selected in the first menu"""

connection = sql.connect('UCH.db')
c = connection.cursor()

# class notRegistered(Exception):
#     def __init__(self, message = "A GP needs to confirm your registration before you can access our services. Please try logging in tomorrow."):
#         self.message = message
#         super().__init__(self.message)

def options(nhsNumber):
    c.execute("SELECT * FROM PatientDetail WHERE nhsNumber =?", [nhsNumber])
    results = c.fetchall()
    uf.banner('Patient')
    if results[0][11] == 0:
        # raise notRegistered()
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
        action = input("Choice: ")
        if action == '1':
            x = Appointment()
            x.bookAppointment(nhsNumber)
            options(nhsNumber)
        elif action == '2':
            x = Appointment()
            x.viewAppConfirmations(nhsNumber)
            options(nhsNumber)
        elif action == '3':
            x = Appointment()
            x.cancelAppointment(nhsNumber)
            options(nhsNumber)
        elif action == '4':
            print("Choose [1] to see your medical profile")
            print("Choose [2] to take the lifestyle risk questionnaire")
            print("Choose [3] to update your medical history")
            qchoice = input("Choice: ")
            if qaction == '1':
                name = PatientMedical()
                name.show_profile(nhsNumber)
                options(nhsNumber)
            elif qaction == '2':
                print("Please fill out the following risk profile")
                x = RiskProfile()  # need to pass patientEmail into the functions
                x.questions()
                x.BMI_calculator()
                x.diet()
                x.smoking()
                x.drugs()
                x.alcohol()
                x.insert_to_table(nhsNumber)
                options(nhsNumber)
            elif qaction == '3':
                x = PatientMedical()
                x.vaccination(nhsNumber)
                x.cancer(nhsNumber)
                options(nhsNumber)
        elif action == '5':
            # Put this in the patientFunctions.py?
            hash = ""
            for i in results[0][11]:
                hash += "*"
            print("Your NHS number is: ")
            x = str(results[0][0])
            one = x[0:3]
            two = x[3:6]
            three = x[6:10]
            print(one, two, three)
            print("First Name: " + str(results[0][2]))
            print("Last Name: " + str(results[0][3]))
            print("Email: " + str(results[0][1]))
            print("Date of Birth: " + str(results[0][4]))
            print("Age: " + str(results[0][5]))
            print("Gender: " + str(results[0][6]))
            print("Address: ")
            print(str(results[0][7]))
            print(str(results[0][8]))
            print(str(results[0][9]))
            print("Telephone Number: +" + str(results[0][10]))
            print("Password: " + hash)
            # print(pd.Series(results[0]))
            options(nhsNumber)
        elif action == '6':
            options(nhsNumber)
        elif action == '0':
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()


def task():
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=input("Choice: ")
    if action == '0':
        return 0
    if action != '1' and action != '2':
        print("I'm sorry, '" + str(action) + "' is an invalid option. ")
        task()
    elif action == '1':
        # First Name
        firstName=input("Please enter your first name. ")
        firstName = string.capwords(firstName.strip())
        # print(firstName)
        # Last Name
        lastName=input("Please enter your last name. ")
        lastName = string.capwords(lastName.strip())
        # print(lastName)
        # Date of Birth
        dateOfBirth = input('Please enter your birthday in DD-MM-YYYY format. ')
        day, month, year = map(int, dateOfBirth.split('-'))
        dateOfBirth = datetime.date(year, month, day)
        # print(dateOfBirth)
        # Age
        today = date.today()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
        # print(age)
        # Gender
        print("Gender")
        print("Choose [1] for female")
        print("Choose [2] for male")
        print("Choose [3] for non-binary")
        gender=input("Choice: ")
        while gender != '1' and gender != '2' and gender != '3':
            print("I'm sorry, '" + gender + "' is an invalid option. ")
            print("Gender")
            print("Choose [1] for female")
            print("Choose [2] for male")
            print("Choose [3] for non-binary")
            gender=input("Choice: ")
        if gender == '1':
            gender = "Female"
        elif gender == '2':
            gender = "Male"
        elif gender == '3':
            gender = "Non-Binary"
        # print(gender)
        # Address Line 1
        addressLine1 = input("Address Line 1: ")
        addressLine1 = string.capwords(addressLine1.strip())
        # print(addressLine1)
        # Address Line 2
        addressLine2 = input("Address Line 2: ")
        addressLine2 = string.capwords(addressLine2.strip())
        # print(addressLine2)
        # City
        city = input("City: ")
        city = string.capwords(city.strip())
        addressLine2 = (addressLine2 + " " + city).strip()
        # print(addressLine2)
        # Postcode
        postcode = input("Postcode: ")
        postcode = postcode.strip().upper()
        # print(postcode)
        # Telephone Number
        telephoneNumber = input("Telephone number, including country code (i.e. +447123456789): ")
        telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        while len(telephoneNumber) > 12 or len(telephoneNumber) < 11:
            print("I'm sorry, that is not a valid telephone. Please try again. ")
            telephoneNumber = input("Telephone number, including country code (i.e. +447123456789): ")
            telephoneNumber = re.sub("[^0-9]", "", telephoneNumber)
        telephoneNumber = int(telephoneNumber)
        # print(telephoneNumber)
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
    elif action == '2':
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
        if password != patientEmails[0][10]:
            while password != patientEmails[0][10]:
                print("I'm sorry, that password is not correct. ")
                password=input("Please enter your password. ")
            # print("Wonderful! Hi, " + patientEmails[0][2] + " you are now logged in.")
            options(patientEmails[0][0])
        else:
            # print("Wonderful! Hi, " + patientEmails[0][2] + " you are now logged in.")
            options(patientEmails[0][0])
