import requests
import csv
import tkinter as tk

# Reads the indicated CSV file and grabs the email addresses from the 3rd column
def read_csv(file_name):
    emails = []
    with open(file_name, "r", newline='') as file:
        has_header = next(file, None)
        file.seek(0)
        email_data = csv.reader(file, delimiter=",")
        if has_header:
            next(email_data)
        for row in email_data:
            email = {"email": row[2]}
            print(email)
            emails.append(email)
    submit_emails(emails)

# Loops through emails list and submits each email to the CHPL newsletters webform
# Writes a log file to track if any emails did not get submitted properly    
def submit_emails(emails):
    log_file = open("email-submission-log.txt", "w")
    for email in emails:
        payload = email
        print(payload)
        r = requests.post("https://chapelhillpubliclibrary.org/library-newsletters/", data=payload)
        print(str(r)[11:14])
        logger = str(r)[11:14]
        if int(logger) != 200:
            log_file.write(email + " Did not submit successfully")

# Constructor to create GUI to increase ease of use
class App(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_title("Batch Email Submittal")
        self.label = tk.Label(self.root, text= "Enter the CSV file name")
        self.label.pack()


        self.entrytext = tk.StringVar()
        tk.Entry(self.root, textvariable=self.entrytext).pack()

        self.buttontext = tk.StringVar()
        self.buttontext.set("Submit")
        tk.Button(self.root, textvariable=self.buttontext, command=self.clicked1).pack()

        self.label = tk.Label(self.root, text="")
        self.label.pack()

        self.root.mainloop()

    # Grabs the input from the text box and adds .csv file extension
    # Handles click of submit button
    def clicked1(self):
        input = self.entrytext.get()
        file_name = str(input) + ".csv"
        self.label.configure(text=file_name)
        read_csv(file_name)

    # def button_click(self, e, file_name):
    #     read_csv(file_name)
        
App()
