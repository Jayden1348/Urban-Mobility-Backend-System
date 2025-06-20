import csv
from io import StringIO
from Models.DataModels import User, Traveller, Scooter, Log
from cryptography.fernet import Fernet
import os

# Load the key once at module level
with open("logkey.key", "rb") as keyfile:
    key = keyfile.read()
fernet = Fernet(key)
logs_dir = "Logs"
os.makedirs(logs_dir, exist_ok=True)


def write_encrypted_log_csv(row, logfile=os.path.join(logs_dir, "logs.enc")):
    """
    row: list or tuple of values to log (e.g. [date, time, username, description, additionalinfo, suspicious])
    """
    # Convert row to CSV string
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(row)
    csv_line = output.getvalue().strip()  # Remove newline at end

    encrypted = fernet.encrypt(csv_line.encode())
    with open(logfile, "ab") as f:
        f.write(encrypted + b"\n")


def read_encrypted_logs_csv(logfile=os.path.join("Logs", "logs.enc")):
    """
    Yields each decrypted CSV row as a list.
    """
    if not os.path.exists(logfile):
        return  # Or: yield from () for an empty generator
    with open(logfile, "rb") as f:
        for line in f:
            decrypted = fernet.decrypt(line.strip()).decode()
            reader = csv.reader([decrypted])
            for row in reader:
                yield row
