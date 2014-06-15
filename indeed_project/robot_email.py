#add ability to send an email when the extraction is done from separate computer
# must be from a gmail account!!

import smtplib

def get_email_params():
    to_email = ""
    from_email = ""
    from_email_pswd = ""
    message = "Hey! I'm done with the extraction. Come get your data."
    confirm = ""
    while "y" not in confirm.lower():
        to_email = raw_input("Enter e-mail address to send to: ")
        from_email = raw_input("Enter e-mail address to send from: ")
        from_email_pswd = raw_input("Enter password of e-mail address sending from: ")
        print "Here's what I have: "
        print "Sending to email: "+to_email
        print "Sending from email: "+from_email
        print "Password: " + from_email_pswd
        confirm = raw_input("Is all this correct (y/n)?: ")
    return (message,to_email,from_email,from_email_pswd)


def send(message,to_email,from_email,from_email_pswd):
    try:
        server = smtplib.SMTP('smtp.gmail.com','587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_email,from_email_pswd)
        server.sendmail(from_email,to_email,message)
        server.close()
    except:
        print "Failed to send e-mail."


