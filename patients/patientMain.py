import sqlite3 as sql
import datetime
from datetime import date
from patient import Patient
from PatientRiskProfile import PatientMedical
from lifeStyleQuestionnaire import RiskProfile
from appointment import Appointment

connection = sql.connect('patient.db')
c = connection.cursor()


def options(patientEmail):
    # if registration is not confirmed where patientEmail = patientEmail, try again later, end program
    # else, run program below:

        print("What would you like to do next?")
        print("Choose [1] to book an appointment")
        print("Choose [2] to view your confirmed appointments")
        print("Choose [3] to cancel an appointment")
        print("Choose [4] to see your medical profile")
        print("Choose [0] to exit")
        action = int(input("Choice: "))
        if action == 1:
            x = Appointment()
            x.bookAppointment(patientEmail)
            options(patientEmail)
        elif action == 2:
            x = Appointment()
            x.viewAppConfirmations(patientEmail)
            options(patientEmail)
        elif action == 3:
            x = Appointment()
            x.cancelAppointment(patientEmail)
            options(patientEmail)
        elif action == 4:
            print("Choose [1] to see your medical profile")
            print("Choose [2] to take the lifestyle risk questionnaire")
            print("Choose [3] to update your medical history")
            qaction = int(input("Choice: "))
            if qaction == 1:
                name = PatientMedical()
                name.show_profile(patientEmail)
            elif qaction == 2:
                print("Please fill out the following risk profile")
                x = RiskProfile()  # need to pass patientEmail into the functions
                x.questions()
                x.BMI_calculator()
                x.diet()
                x.smoking()
                x.drugs()
                x.alcohol()
                x.insert_to_table(patientEmail)
            elif qaction == 3:
                x = PatientMedical()
                x.vaccination(patientEmail)
                x.cancer(patientEmail)
        elif action == 0:
            print("Thank you for using the UCH e-health system! Goodbye for now!")
            exit()

def task():
    print("Choose [1] to register for a new account")
    print("Choose [2] to login")
    action=input("Choice: ")
    if action != '1' and action != '2':
        print("I'm sorry, '" + action + "' is an invalid option. ")
        task()
    elif action == '1':
        firstName=input("Please enter your first name. ")
        lastName=input("Please enter your last name. ")
        dateOfBirth = input('Please enter your birthday in YYYY-MM-DD format. ')
        year, month, day = map(int, dateOfBirth.split('-'))
        dateOfBirth = datetime.date(year, month, day)
        today = date.today()
        age = today.year - dateOfBirth.year - ((today.month, today.day) < (dateOfBirth.month, dateOfBirth.day))
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
        addressLine1 = input("Address Line 1: ")
        addressLine2 = input("Address Line 2 (including city): ")
        postcode = input("Postcode: ")
        telephoneNumber = input("Telephone in XXXXX-XXX-XXX format: ")
        patientEmail=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        if patientEmails != []:
            while patientEmails != []:
                print("I'm sorry, that email is already in use. Please use another email.")
                patientEmail=input("Please enter your email. ")
                c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
                patientEmails = c.fetchall()
        password=input("Please enter your password. ")
        x=Patient(patientEmail, firstName, lastName, dateOfBirth, age, gender, addressLine1, addressLine2, postcode, telephoneNumber, password)
        x.register()
        x.registrationSummary()
        options(x.patientEmail)
    elif action == '2':
        patientEmail=input("Please enter your email. ")
        c.execute("SELECT * FROM PatientDetail WHERE patientEmail =?", [patientEmail])
        patientEmails = c.fetchall()
        password=input("Please enter your password. ")
        if password != patientEmails[0][10]:
            while password != patientEmails[0][10]:
                print("I'm sorry, that password is not correct. ")
                password=input("Please enter your password. ")
            print("Wonderful! Hi, " + patientEmails[0][1] + " you are now logged in.")
            options(patientEmail)
        else:
            print("Wonderful! Hi, " + patientEmails[0][1] + " you are now logged in.")
            options(patientEmail)
    

print("Welcome!")
task()

