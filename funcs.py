# ALL FUNCTIONS USED IN GUI.py

def checkName(name=""):
    if len(name) < 2:
        return False
    for char in name:
        if not name.isalpha():
            return False
    return True

def checkBirthDay(date=""): #01/01/2022
    if len(date.split("/")) != 3:
        return False
    day, month, year = date.split("/")
    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        return False
    date = day+month+year
    for digit in date:
        if not digit.isdigit():
            return False
    return True

def checkPhoneNumber(number=""):
    if len(number) != 10:
        return False
    for digit in number:
        if not digit.isdigit():
            return False
    return True

def checkemailAddress(email=""):
    if len(email.split("@")) != 2:
        return False
    name = email.split("@")[0]
    domain = email.split("@")[1]

    if len(domain.split(".")) < 1:
        return False
    return True

def capitalName(name=""):
    return name[0].upper()+name[1:]


