from GPs.gp_login_function import gp_login
from GPs.gp_main_menu import gp_main_menu

def gp_start():
    email,doctorname = gp_login()
    if email == "exitGPLogin":
        return "exitGPLogin"
    if email:
        gp_main_menu(email, doctorname)
    return "exitGPLogin"