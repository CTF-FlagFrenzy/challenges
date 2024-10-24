import subprocess
import shutil  # Zum Kopieren von Dateien unter Windows

# Originaldatei mit eingebetteter Original-Flag
original_file = "nice_holiday.JPG"

# Globale Flag für das jeweilige Team
global_flag = "ABCD"

# Kopierte Datei, in die die kombinierte Flag geschrieben wird
output_file = "nice_holiday_copy.JPG"

# Funktion zum Auslesen der Original-Flag aus den EXIF-Daten
def extract_original_flag(file):
    # Verwende den vollständigen Pfad zu exiftool.exe
    result = subprocess.run([r"C:\Users\ilaria\Downloads\exiftool-12.99_64\exiftool.exe", "-Comment", file], stdout=subprocess.PIPE, text=True)
    
    # Ausgabe sieht typischerweise so aus: "Comment: CTF{original_flag}"
    exif_data = result.stdout
    
    # Extrahiere den Wert hinter "Comment:"
    for line in exif_data.splitlines():
        if "Comment" in line:
            # Spalte an "Comment:" und entferne Leerzeichen
            return line.split(":")[1].strip()
    
    return None

# Funktion zum Einbetten der kombinierten Flag in die EXIF-Daten
def embed_combined_flag(file, flag):
    # Verwende exiftool, um die EXIF-Daten des Bildes zu modifizieren und die kombinierte Flag einzubetten
    result = subprocess.run([r"C:\Users\ilaria\Downloads\exiftool-12.99_64\exiftool.exe", f"-Comment={flag}", file], stdout=subprocess.PIPE, text=True)
    print(result.stdout)

# Kopiere das Originalbild zu einer neuen Datei
def copy_file(source, destination):
    shutil.copy(source, destination)  # Verwende shutil.copy für das Kopieren unter Windows

# Original-Flag aus der Datei extrahieren
original_flag = extract_original_flag(original_file)

# Überprüfen, ob die Original-Flag erfolgreich extrahiert wurde
if original_flag:
    print(f"Original-Flag gefunden: {original_flag}")
    
    # Kombiniere die globale Flag mit der Original-Flag
    combined_flag = global_flag + original_flag
    print(f"Kombinierte Flag: {combined_flag}")
    
    # Kopiere die Originaldatei
    copy_file(original_file, output_file)
    
    # Kombinierte Flag in die EXIF-Daten der Kopie einbetten
    embed_combined_flag(output_file, combined_flag)
    
    print(f"Kombinierte Flag in {output_file} eingebettet.")
else:
    print("Keine Original-Flag gefunden!")
