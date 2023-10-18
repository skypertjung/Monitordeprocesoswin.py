##Librerias
import os
import hashlib
import time
#Funciones
def calculate_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def monitor_directory(directory_path, log_file_path, recent_changes_file_path):
    while True:
        modified_files = []
        with open(log_file_path, "a") as log_file:
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_hash = calculate_hash(file_path)
                    log_file.write(f"{file_path}: {file_hash}\n")

                    # Comprobar si el archivo se ha modificado desde la última revisión
                    if file_hash != get_last_hash(file_path):
                        modified_files.append(file_path)

        # Guardar los archivos modificados recientemente en un archivo separado
        with open(recent_changes_file_path, "w") as recent_changes_file:
            for file_path in modified_files:
                recent_changes_file.write(f"{file_path}\n")

        time.sleep(3600)  # Espera 1 hora antes de la siguiente revisión

def get_last_hash(file_path):
    try:
        with open("hash_log.txt", "r") as log_file:
            lines = log_file.readlines()
            for line in reversed(lines):
                if line.startswith(file_path):
                    return line.split(":")[1].strip()
        return ""
    except FileNotFoundError:
        return ""

if __name__ == "__main__":
    directory_to_monitor = r"Introduce la ruta que quieres scanear"
    log_file_path = "hash_log.txt"
    recent_changes_file_path = "recent_changes.txt"
