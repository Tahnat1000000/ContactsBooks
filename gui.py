import os, PySimpleGUI as sg, funcs

contacts = []
window, lastTheme = None, "Classic"
contactBookName = "Contact Book" # THE CURRENT CONTACT BOOK NAME
contactInformation = "" # THE INFORMATION ABOUT LAST CONTACT SELECTED

def createMainWindow(theme="SystemDefault"):
    global window, lastTheme, contacts

    if window is not None:
        window.close()

    screenNames = {"SystemDefault": "Light", "DarkBlue": "Dark", "Topanga": "Gold"}

    usersDirPath = os.path.join(os.getcwd(), "ContactsBooks")
    existContactBooks = [fileName.split(".")[0] for fileName in os.listdir(usersDirPath)]
    lastTheme = screenNames.get(theme)

    sg.theme(theme)
    layout = [
        [sg.Text("Contact Book:"), sg.Combo(existContactBooks, key="-NAME-", size=(17), default_value=contactBookName, enable_events=True), sg.Stretch(), sg.Text("Theme:"), sg.Combo(["Light", "Dark", "Gold"], key="-THEMELIST-", default_value=screenNames.get(theme), enable_events=True)],
        [sg.Button("New Contact Book", key="-NEWUSERBUTTON-", size=(28))],
        [sg.HSeparator()],
        [sg.Listbox([(str(index+1) + ". " + contact.split(",")[0] + " " + contact.split(",")[1]) for index, contact in enumerate(contacts)], key="-CONTACTLIST-", expand_y=True, size=(30,10), disabled=(not contactBookName != "Contact Book"), enable_events=True), sg.VSeparator(), sg.Text("", key="-CONTACTINFORMATION-", size=(50), expand_y=True, justification="left")],
        [sg.Button("Add Contact", key="-NEWCONTACT-", size=(28), disabled=(contactBookName == "Contact Book")), sg.Text("  ") ,sg.Button("Update Contact", key="-UPDATECONTACT-", size=(17), disabled=True), sg.Button("Delete Contact", key="-DELETECONTACT-", size=(17), disabled=True)],
    ]
    window = sg.Window("Contact Book - Main", layout, size=(600,400), finalize=True)

def createNewContactBookWindow():
    global window

    screenNames = {"Light": "SystemDefault", "Dark": "DarkBlue", "Gold": "Topanga"}
    layout = [[sg.Text("NEW CONTACT BOOK")],
              [sg.Text("Full Name : "), sg.Input(key="-CONTACTBOOKNAME-")],
              [sg.Text("", key="-MESSAGE-")],
              [sg.Submit(), sg.Cancel()]]

    win = sg.Window("Contact Book - Create New Contact Book", layout)
    while True:
        event, values = win.read()
        if event == "Submit":
            contactBookName = values["-CONTACTBOOKNAME-"].split(" ")

            name = ""
            for index, val in enumerate(contactBookName):
                if index == 0:
                    name += funcs.capitalName(val)
                else:
                    name += " "+funcs.capitalName(val)

            CBPath = os.path.join(os.getcwd(), "ContactsBooks", name + ".txt")
            if len(contactBookName) == 0:  # IF NAME INPUT IS EMPTY
                win["-MESSAGE-"].update("Contact book name is empty.")
            elif os.path.exists(CBPath) == False:  # IF USER NOT EXISTS
                with open(CBPath, "a") as f:
                    f.close()
                win["-MESSAGE-"].update("New contact book created - " + name)
                win.close()
                window.close()
                createMainWindow(screenNames.get(lastTheme))
            else:  # IF USER EXISTS
                win["-MESSAGE-"].update("Contact book on this name allready exist.")

        if event in ["Cancel", sg.WIN_CLOSED]:
            win.close()
            break

def createNewContactWindow(contactIndex = -1):
    global contacts, window, contactInformation
    if contactIndex > -1:
        firstname, lastname, birthday, phone, email = contacts[contactIndex].split(",")
        layout = [[sg.Text("ADD NEW CONTACT")],
                  [sg.Text("First Name: ", size=(20,1)), sg.Input(default_text=firstname.strip(), key="-CONTACTNAME-")],
                  [sg.Text("Last Name: ", size=(20,1)), sg.Input(default_text=lastname.strip(), key="-CONTACTLASTNAME-")],
                  [sg.Text("Birth Day: ", size=(20,1)), sg.Input(default_text=birthday.strip(), key="-CONTACTBIRTHDAY-")],
                  [sg.Text("Phone Number: ", size=(20,1)), sg.Input(default_text=phone.strip(), key="-CONTACTNUMBER-")],
                  [sg.Text("Email Address: ", size=(20,1)), sg.Input(default_text=email.strip(), key="-CONTACTEMAIL-")],
                  [sg.Text("", key="-MESSAGE-")],
                  [sg.Submit(), sg.Cancel()]]
    else:
        layout = [[sg.Text("ADD NEW CONTACT")],
                  [sg.Text("First Name: ", size=(20,1)), sg.Input(key="-CONTACTNAME-")],
                  [sg.Text("Last Name: ", size=(20,1)), sg.Input(key="-CONTACTLASTNAME-")],
                  [sg.Text("Birth Day: ", size=(20,1)), sg.Input(key="-CONTACTBIRTHDAY-")],
                  [sg.Text("Phone Number: ", size=(20,1)), sg.Input(key="-CONTACTNUMBER-")],
                  [sg.Text("Email Address: ", size=(20,1)), sg.Input(key="-CONTACTEMAIL-")],
                  [sg.Text("", key="-MESSAGE-")],
                  [sg.Submit(), sg.Cancel()]]

    win = sg.Window("Contact Book - Add New Contact", layout)
    while True:
        event, values = win.read()

        if event == "Submit":
            firstname, lastname, birthday, phone, email = values["-CONTACTNAME-"], values["-CONTACTLASTNAME-"], values["-CONTACTBIRTHDAY-"], values["-CONTACTNUMBER-"], values["-CONTACTEMAIL-"]
            if funcs.checkName(firstname) is False or funcs.checkName(lastname) is False:
                win["-MESSAGE-"].update("Invaild first name or last name")
            elif funcs.checkBirthDay(birthday) is False:
                win["-MESSAGE-"].update("Example: 01/01/2022")
            elif funcs.checkPhoneNumber(phone) is False:
                win["-MESSAGE-"].update("Phone number should be 10 digits")
            elif funcs.checkemailAddress(email) is False:
                win["-MESSAGE-"].update("Invaild email address")
            else:
                contacts.append(f"{funcs.capitalName(firstname)}, {funcs.capitalName(lastname)}, {birthday}, {phone}, {email}")
                if contactIndex > -1:
                    contacts.remove(contacts[contactIndex])
                    with open(os.path.join(os.getcwd(), "ContactsBooks", contactBookName + ".txt"), "w") as file:
                        for contact in contacts:
                            file.write(contact)
                        file.close()
                else:
                    with open(os.path.join(os.getcwd(), "ContactsBooks", contactBookName + ".txt"), "a") as file:
                        file.write(f"{funcs.capitalName(firstname)}, {funcs.capitalName(lastname)}, {birthday}, {phone}, {email}\n")
                        file.close()
                win.close()
                contactInformation = ""
                window["-CONTACTINFORMATION-"].update("")
                window["-UPDATECONTACT-"].update(disabled=True)
                window["-DELETECONTACT-"].update(disabled=True)
                window["-CONTACTLIST-"].update([(str(index + 1) + ". " + contact.split(",")[0] + " " + contact.split(",")[1]) for index, contact in enumerate(contacts)])

        if event in ["Cancel", sg.WIN_CLOSED]:
            win.close()
            break

def main():
    global window, lastTheme, contacts, contactBookName, contactInformation
    createMainWindow("SystemDefault")
    while True:
        event,values = window.read()

        ### THEME COMBO CHOOSE OPTION
        if event == "-THEMELIST-" and values["-THEMELIST-"] != lastTheme:
            if values["-THEMELIST-"] == "Light":
                createMainWindow("SystemDefault")
            elif values["-THEMELIST-"] == "Dark":
                createMainWindow("DarkBlue")
            elif values["-THEMELIST-"] == "Gold":
                createMainWindow("Topanga")

        ### ADD NEW CONTACT BOOK - IF BUTTON PRESSED
        if event == "-NEWUSERBUTTON-":
            window.hide()
            createNewContactBookWindow()
            window.UnHide()

        ### IMPORT USER CONTACTS
        if event == "-NAME-" and values["-NAME-"] != "Contact Book" and values["-NAME-"] != contactBookName: # CONTACT BOOK WAS SELECTED
            contactBookName = values["-NAME-"]

            with open(os.path.join(os.getcwd(), "ContactsBooks", contactBookName + ".txt"), "r") as file:
                contacts = [contact for contact in file.readlines()]
                file.close()

            window["-CONTACTLIST-"].update(disabled=False)
            window["-CONTACTLIST-"].update([(str(index+1) + ". " + contact.split(",")[0] + " " + contact.split(",")[1]) for index, contact in enumerate(contacts)])
            window["-NEWCONTACT-"].update(disabled=False)
            contactInformation = ""
            window["-CONTACTINFORMATION-"].update(contactInformation)
            window["-UPDATECONTACT-"].update(disabled=True)
            window["-DELETECONTACT-"].update(disabled=True)

        ### ADD MEW CONTACT
        if event == "-NEWCONTACT-":
            window.hide()
            createNewContactWindow()
            window.UnHide()

        ### CLICKING ON CONTACT FOR INFORMATION
        if event == "-CONTACTLIST-" and len(contacts) > 0:
            contactIndex = int(values["-CONTACTLIST-"][0][0])-1
            firstname, lastname, birthday, phone, email = (contacts.__getitem__(contactIndex)).split(",")
            contactInformation = f"FIRST NAME:                 {firstname}\n" \
                                 f"LAST NAME:                 {lastname}\n" \
                                 f"BIRTH DAY:                   {birthday.strip()}\n" \
                                 f"PHONE NUMBER:         {phone}\n" \
                                 f"EMAIL ADDRESS:         {email}\n"
            window["-CONTACTINFORMATION-"].update(contactInformation)
            if contactInformation != "":
                window["-UPDATECONTACT-"].update(disabled=False)
                window["-DELETECONTACT-"].update(disabled=False)

        ### DELETE CONTACT FROM CONTACT BOOK
        if event == "-DELETECONTACT-" and contactInformation != "" and values["-CONTACTLIST-"] != []:
            contactIndex = int(values["-CONTACTLIST-"][0][0]) - 1
            contactInformation = ""
            contacts.remove(contacts[contactIndex])
            window["-CONTACTLIST-"].update([(str(index+1) + ". " + contact.split(",")[0] + " " + contact.split(",")[1]) for index, contact in enumerate(contacts)])
            window["-CONTACTINFORMATION-"].update(contactInformation)
            window["-UPDATECONTACT-"].update(disabled=True)
            window["-DELETECONTACT-"].update(disabled=True)
            with open(os.path.join(os.getcwd(), "ContactsBooks", contactBookName + ".txt"), "w") as file:
                for contact in contacts:
                    firstname, lastname, birthday, phone, email = contact.split(",")
                    file.write(f"{firstname}, {lastname}, {birthday}, {phone}, {email}")
                file.close()

        ### UPDATE CONTACT FROM CONTACT BOOK
        if event == "-UPDATECONTACT-" and contactInformation != "" and values["-CONTACTLIST-"] != []:
            contactIndex = int(values["-CONTACTLIST-"][0][0]) - 1
            window.hide()
            createNewContactWindow(contactIndex)
            window.UnHide()
            pass

        if event in [sg.WIN_CLOSED]:
            break

    window.close()
