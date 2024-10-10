

#  Ikeliamas konfigas: config.json
import json
from datetime import datetime

try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print("Nustatymų failas nerastas.")
    config = {}
except json.JSONDecodeError:
    print("Klaida skaitant JSON failą.")
    config = {}

# Kofigu raktai
debug = config.get('debug') 
utelizavimo_terminas = config.get('utelizavimo_terminas')
# debug
if utelizavimo_terminas is None:
    print("Utelizavimo terminas nenustatytas konfigūracijoje.")
if debug is None:
    print("Debug raktas nenustatytas konfigūracijoje.")     

# Šiandienos data
dabartine_data = datetime.now()


# Knygų biblioteka. 
# Sąrašas saraše. Knygos biliotekoje: Knyga: autorius, išleidimo metai, žanras, kiekis, išduota, išduota iki, vėluoja.

# Importuoti knygų sąrašą iš knygos.json
try:
    with open('knygos.json', 'r') as knygos_file:
        knygos_bibliotekoje = json.load(knygos_file)
except FileNotFoundError:
    print("Failas knygos.json nerastas.")
    knygos_bibliotekoje = []
except json.JSONDecodeError:
    print("Klaida skaitant JSON failą knygos.json.")
    knygos_bibliotekoje = []

# Nustatyti knygos utelizavimo taisykles. Jei knygos išleidomo metai yra =< nei configo nusatymas, tada išmesti knygas iš sąrašo knygos_bibliotekoje ir sukuriant išmestų knygų restgistra: utelizuota

def utelizuoti_senas_knygas(knygos_bibliotekoje, utelizavimo_terminas):    
    utelizuota = []
    nauja_biblioteka = []
    for knyga in knygos_bibliotekoje:
        if dabartine_data.year - knyga["metai"] > utelizavimo_terminas:
            utelizuota.append(knyga)
        else:
            nauja_biblioteka.append(knyga)
    return nauja_biblioteka, utelizuota

# Inicijuojama knygų utelizavimo funkcija
knygos_bibliotekoje, utelizuota = utelizuoti_senas_knygas(knygos_bibliotekoje, utelizavimo_terminas)

# Išsaugoti naują knygų sąrašą į knygos.json
with open('knygos.json', 'w') as knygos_file:
    json.dump(knygos_bibliotekoje, knygos_file, ensure_ascii=False, indent=4)

# Išsaugoti utelizuotas knygas į utelizuotos.json
with open('utelizuotos.json', 'w') as utelizuotos_file:
    json.dump(utelizuota, utelizuotos_file, ensure_ascii=False, indent=4)

# Gauti utelizuotų knygų sąrašą.
def spausdinti_utelizuotas_knygas(utelizuota):
    if not utelizuota:
        print("Nėra utelizuojamų knygų.")
    else:
        print("Utelizuotos senos knygos:")
        for knyga in utelizuota:
            print(f"Pavadinimas: {knyga['pavadinimas']}, Autorius: {knyga['autorius']}, Metai: {knyga['metai']}, Žanras: {knyga['zanras']}")

# Spausdinti utelizuotas knygas jei debug režime
if debug == 1:
    spausdinti_utelizuotas_knygas(utelizuota)



# Funkcija gražinanti visas utelizuotas knygas iš utelizuotas.json į knygos.json
def grazinti_utelizuotas_knygas():
    try:
        with open('utelizuotos.json', 'r') as utelizuotos_file:
            utelizuota = json.load(utelizuotos_file)
    except FileNotFoundError:
        print("Nėra utelizuotų knygų.")
        utelizuota = []
    except json.JSONDecodeError:
        print("Klaida skaitant JSON failą.")
        utelizuota = []
    
    try:
        with open('knygos.json', 'r') as knygos_file:
            knygos_bibliotekoje = json.load(knygos_file)
    except FileNotFoundError:
        print("Knygų failas nerastas.")
        knygos_bibliotekoje = []
    except json.JSONDecodeError:
        print("Klaida skaitant JSON failą.")
        knygos_bibliotekoje = []

    knygos_bibliotekoje.extend(utelizuota)

    with open('knygos.json', 'w') as knygos_file:
        json.dump(knygos_bibliotekoje, knygos_file, ensure_ascii=False, indent=4)

    print("Utelizuotos knygos sėkmingai gražintos į biblioteką.")

if debug == 1:
    user_input = input("Ar norite gražinti utelizuotas knygas į biblioteką? (taip/ne): ")
    if user_input.lower() == 'taip':
        grazinti_utelizuotas_knygas()
    elif user_input.lower() == 'ne':
        print("Utelizuotos knygos nebus gražintos į biblioteką.")
    else:
        print("Neteisingas įvestis. Prašome įvesti 'taip' arba 'ne'.")



