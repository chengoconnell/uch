from GPs.GPLogin import login
from GPs.Doctormenu import mainmenu

def gpStart():
    email = []
    login(email)
    if email:
        mainmenu(email[0])