import os
import webbrowser
import datetime
from dateutil.relativedelta import relativedelta
from pdfminer.high_level import extract_text
import ctypes

# Norādīta direktorija, kurā atrodas PDF faili
pdf_dir = "C:\\Users\\alans\\Desktop\\pdfstuff"

# Pārbauda, vai direktorijā atrodas pirmais PDF fails
if "1.pdf" in os.listdir(pdf_dir):
    # Teksts tiek izvilkts no PDF faila
    text1 = extract_text(os.path.join(pdf_dir, "1.pdf"))
    
    # Nepareizās rakstzīmes tiek aizstātas
    text1 = text1.replace('¢', 'ā')
    text1 = text1.replace('®', 'ē')
    text1 = text1.replace('²', 'ī')
    text1 = text1.replace('´', 'ņ')
    text1 = text1.replace('ō', 'š')
    text1 = text1.replace('°', 'ķ')
    text1 = text1.replace('¡', 'Ā')
    text1 = text1.replace('¼', 'Ū')
    text1 = text1.replace('¦', 'Ē')
    text1 = text1.replace('³', 'Ņ')
    text1 = text1.replace('ª', 'ģ')
    text1 = text1.replace('¯', 'Ķ')
    text1 = text1.replace('§', 'ē')
    text1 = text1.replace('º', 'š')

    # Izvelk skaitli pēc "Kopā apmaksai"
    pos1 = text1.find("Kopā apmaksai")
    pos2 = text1.find("EUR", pos1)
    summa = text1[pos2-2:pos2+18].strip()

    # No izvades tiek noņemts "EUR"
    summa = summa.replace("EUR", "").strip()

    # Izvelk datumu pēc "apmaksas termiņš"
    pos3 = text1.find("apmaksas termiņš")
    date = text1[pos3-2:pos3+26].strip()

    # No izvades tiek noņemts "apmaksas termiņš" un iekavas
    date = date.replace("apmaksas termiņš", "").replace("(", "").replace(")", "").strip()

    # Izveido ziņojumu uznirstošajam logam
    message = f"Jums ir jāmaksā par internetu {summa} EUR un jums ir laiks līdz {date} . Vai vēlaties maksāt tūlīt?"

    # Izveido uznirstošo logu ar pogām 'Jā' un 'Nē' un jautājuma ikonu
    result = ctypes.windll.user32.MessageBoxW(0, message, "Maksājuma atgādinājums", 36)

    # Ja tiek noklikšķināts 'Jā', tiek atvērta Swedbank tīmekļa vietne
    if result == 6:
        webbrowser.open("https://www.swedbank.lv/private")
    
    # Ja tiek noklikšķināts 'Nē', programma turpinās bez darbības
    elif result == 7:
        pass
