import json
import dns.resolver 
import smtplib
from passlib.context import CryptContext
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_error_code(name):
    error_codes=json.load(open('app/json/error_codes.json', 'r'))
    return error_codes.get(name)

# Check if the mail is valid
def is_valid_email(test_address):
    valid_address=getenv("VALID_EMAIL","")
    regex="^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[_a-z0-9-]+(\.[_a-z0-9-]+)*(\.[a-z]{2,})$"
    match=re.match(regex,test_address)
    if(match==None):
        return False
    splitadd=test_address.split("@")
    domain=str(splitadd[1])
    records=dns.resolver.query(domain,"MX")
    mx_records=records[0].exchange
    mx_records=str(mx_records)
    server=smtplib.SMTP()
    server.set_debuglevel(0)
    server.connect(mx_records)
    server.helo(server.local_hostname)
    server.mail(valid_address)
    code,message=server.rcpt(str(test_address))
    server.quit()
    if(code==250):
        return True
    else:
        return False
