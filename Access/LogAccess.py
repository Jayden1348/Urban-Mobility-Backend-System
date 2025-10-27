import csv
from io import StringIO
from Utils.encryption import encryptor
import os

logs_dir = "Logs"
os.makedirs(logs_dir, exist_ok=True)


def write_encrypted_log_csv(row, logfile=os.path.join(logs_dir, "logs.enc")):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(row)
    csv_line = output.getvalue().strip()
    encrypted_data = encryptor.encrypt_data(csv_line)
    
    with open(logfile, "a", encoding='utf-8') as f:
        f.write(encrypted_data + "\n")


def read_encrypted_logs_csv(logfile=os.path.join("Logs", "logs.enc")):
    if not os.path.exists(logfile):
        return []

    logs = []
    with open(logfile, "r", encoding='utf-8') as f:
        for line in f:
            try:
                encrypted_line = line.strip()
                if encrypted_line: 
                    decrypted = encryptor.decrypt_data(encrypted_line)

                    if decrypted == encrypted_line:
                        raise ValueError("Decryption failed or data corrupted")

                    reader = csv.reader([decrypted])
                    for row in reader:
                        if row:
                            logs.append(row)
            except Exception as e:
                logs.append(["-", "-", "-", "CORRUPTED LOG", f"This log is corrupted and cannot be decrypted: {str(e)}", "-"])
    
    return logs