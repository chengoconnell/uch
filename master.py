import pandas as pd
import sqlite3 as sql

class Menus:
   def MasterMenu(self):
       print("Welcome, please login")
       print("choose [1] for Admin")
       print("choose [2] for Patient")
       print("choose [3] for GP")

   def adminmenu(self):
       print("Welcome admin")
       print("choose [1] to add a new GP/Physician")
       print("choose [2] to deactivate or delete a profile")
       print("choose [3] to confirm patient registration")
       print("choose [4] to check patient details")
       print("choose [0] when finished navigating menu")
   # add more options yadayada you get the point
def addGP():
    print("registering new physician")
    create = int(input("choose [1] to input physician or [2] to exit: "))
    if create == 1:
        a = input("first name ")
        b = input("last name ")
        c = input("email ")
        d = int(input("enter date of birth as ddmmyy "))
        f = input("specialty ")
        gp = physician(a, b, c, d, f)
        gp.add_physician()
    elif create == 2:
        pass  # add code to abort registration
    else:
        print("did not enter Y or N")
        raise NameError

#yadayada add more functions for selections

class physician():
    def __init__(self, first, last, email, date_birth, specialty):
        self.first = first
        self.last = last
        self.email = email
        self.date_birth = date_birth
        self.specialty = specialty

    def add_physician(self):
        connection = sql.connect('UCH.db')
        c = connection.cursor()
        input = [self.email, self.first, self.last, self.date_birth, self.specialty]
        c.execute("""INSERT INTO doctors VALUES(?, ?, ?, ?, ?)""", input)
        connection.commit()
        # The following allows you to check the doctors table: 
        # c.execute("SELECT * FROM doctors")
        # items = c.fetchall()
        # for i in items:
        #     print(i)
        # connection.commit()
        

masterlogin = Menus()
masterlogin.MasterMenu()

selection1 = int(input("choice: "))
while selection1 != 0:
   if selection1 == 2:
       #call code for patient
       pass
   elif selection1 == 3:
       #call code for GP
       pass

   elif selection1 == 1:
       # add code for...
       pass
   # yadayada add more elif statements

       username = input('Username: ')
       password = input('Password: ')

       admin_df = pd.read_excel("Admins Data.xlsx", index_col= 0)
       user_series = pd.Series([password], index = [username])
       system_series = admin_df.loc[username]

       if str(system_series['Password']) == user_series[username]:
           print('logged in')


           AdminM = Menus()
           AdminM.adminmenu()
           selection = int(input("please select an option: "))

           while selection != 0:
               if selection == 1:
                   addGP()

               elif selection == 2:
               #add code for...
                   pass

               elif selection == 3:
               #add code for...
                   pass
           # yadayada add more elif statements

               else:
                   print("not a valid selection")

               AdminM.adminmenu()
               selection = int(input("please select an option: "))

           print("exiting menu")

   else:
       print("not a valid selection")