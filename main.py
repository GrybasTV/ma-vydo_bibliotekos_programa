# Nustatymai
MAX_VELAVIMAS = 365  # Maksimalus vėlavimas dienomis
DEBUGINIMAS = True

# Importuojame modulius
import json
import random
import string
from datetime import datetime

# Failų pavadinimai
KNYGOS_FAILAS = './knygos.json'
ASMENS_DUOMENYS_FAILAS = './asmensduomenys.json'
UTELEZUOTOS_FAILAS = './utelizuotos.json'

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Klaida")
        if DEBUGINIMAS:
            print(f"Failas '{file_path}' nerastas.")
    except json.JSONDecodeError as e:
        print("Klaida")
        if DEBUGINIMAS:
            print(f"JSON formatavimo klaida faile '{file_path}': {e}")
    except Exception as e:
        print("Nenumatyta klaida, kreipkitės į administratorių:")
        if DEBUGINIMAS:
            print(f"Nenumatyta klaida: {e}")
    return None

def save_json(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Klaida išsaugant duomenis į '{file_path}': {e}")

def generuoti_vartotojo_numeri(skaitytojai):
    while True:
        pirmoji_raide = random.choice(string.ascii_uppercase)
        trys_skaiciai = ''.join(random.choices(string.digits, k=3))
        vartotojo_numeris = pirmoji_raide + trys_skaiciai
        if vartotojo_numeris not in [s['vartotojo_numeris'] for s in skaitytojai]:
            return vartotojo_numeris
 

def autentifikuoti_darbuotoja(darbuotojai):
    while True:
        darbuotojo_kodas = input("Įveskite darbuotojo kodą: ")
        darbuotojas = next((d for d in darbuotojai if d['darbuotojo_kodas'] == darbuotojo_kodas), None)
        if darbuotojas:
            darbuotojo_slaptazodis = input("Įveskite darbuotojo slaptažodį: ")
            if darbuotojo_slaptazodis == darbuotojas['slaptazodis']:
                print("Sėkmingai prisijungta kaip darbuotojas.")
                print()
                return darbuotojas
            else:
                print("Neteisingas slaptažodis. Bandykite dar kartą.")
        else:
            print("Neteisingas darbuotojo kodas. Bandykite dar kartą.")

def prideti_nauja_knyga(knygos):
    kodas = input("Įveskite knygos kodą: ")
    pavadinimas = input("Įveskite knygos pavadinimą: ")
    try:
        leidimo_metai = int(input("Įveskite knygos leidimo metus: "))
        kiekis = int(input("Įveskite knygos kiekį: "))
    except ValueError:
        print("Prašome įvesti skaičius.")
        return
    zanras = input("Įveskite knygos žanrą: ")
    vietos = [{"tipas": "knygyne", "kiekis": kiekis}]
    
    knygos['knygos'].append({
        "knygos_kodas": kodas,
        "pavadinimas": pavadinimas,
        "leidimo_metai": leidimo_metai,
        "zanras": zanras,
        "vietos": vietos
    })
    save_json(KNYGOS_FAILAS, knygos)
    print("Nauja knyga pridėta sėkmingai.")

def perziureti_knygas(knygos):
    while True:
        print("\nPasirinkite peržiūros variantą:")
        print("1 - Visų knygų knygyne sąrašas")
        print("2 - Paieška")
        print("3 - Utelizuoti senas knygas")
        print("4 - Grįžti")
        try:
            pasirinkimas = int(input("Pasirinkimas: "))
        except ValueError:
            print("Įveskite galiojantį skaičių.")
            continue

        if pasirinkimas == 1:
            visos_knygos_sarasas_darbuotoju(knygos)
        elif pasirinkimas == 2:
            paieska_knygose_darbuotojui(knygos)
        elif pasirinkimas == 3:
            utelizuoti_knygas(knygos)
        elif pasirinkimas == 4:
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")

def visos_knygos_sarasas_darbuotoju(knygos):
    # su asmens duoemninimis
    for knyga in knygos['knygos']:
        print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, "
              f"Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
        knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta['tipas'] == 'knygyne')
        pas_skaitytoja = [v for v in knyga['vietos'] if v['tipas'] == 'pas_skaitytoja' and 'vartotojas' in v]
        
        print(f"  Knygyne: {knygyne_kiekis} vnt.")
        if pas_skaitytoja:
            print("  Pas skaitytojus:")
            for info in pas_skaitytoja:
                vartotojas = info['vartotojas']
                print(f"    Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
        else:
            print("  Pas skaitytojus: 0 vnt.")
    input("Paspauskite ENTER, kad grįžti atgal.")


def visos_knygos_sarasas_skaitytojui(knygos):
    # be asmens duomenų
    for knyga in knygos['knygos']:
        print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, "
              f"Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
        knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta['tipas'] == 'knygyne')
        pas_skaitytoja = [v for v in knyga['vietos'] if v['tipas'] == 'pas_skaitytoja' and 'vartotojas' in v]
        
        print(f"  Knygyne: {knygyne_kiekis} vnt.")
        if pas_skaitytoja:
            print("  Pas skaitytojus:")            
        else:
            print("  Pas skaitytojus: 0 vnt.")
    input("Paspauskite ENTER, kad grįžti atgal.")    

def paieska_knygose_darbuotojui(knygos):
    paieska = input("Įveskite knygos pavadinimo, žanro, kodo arba išleidimo metų frazę: ").lower()
    rasta = False

    for knyga in knygos['knygos']:
        try:
            if (paieska in knyga['pavadinimas'].lower() or 
                paieska in knyga['zanras'].lower() or 
                paieska in knyga['knygos_kodas'].lower() or 
                paieska in str(knyga['leidimo_metai']).lower()):
                
                rasta = True
                print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, "
                      f"Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta['tipas'] == 'knygyne')
                pas_skaitytoja = [v for v in knyga['vietos'] if v['tipas'] == 'pas_skaitytoja']
                
                print(f"  Knygyne: {knygyne_kiekis} vnt.")
                if pas_skaitytoja:
                    print("  Pas skaitytojus:")
                    for info in pas_skaitytoja:
                        vartotojas = info['vartotojas']
                        print(f"    Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
                else:
                    print("  Pas skaitytojus: 0 vnt.")
        except Exception as e:
            if DEBUGINIMAS:
                print(f"Klaida apdorojant įrašą: {e}")
            continue

    if not rasta:
        print("Nerasta jokia knyga pagal nurodytą frazę.")
    input("Paspauskite ENTER, kad grįžti atgal.")

def paieska_knygose_skaitytojui(knygos):
    paieska = input("Įveskite knygos pavadinimo, žanro, kodo arba išleidimo metų frazę: ").lower()
    rasta = False

    for knyga in knygos['knygos']:
        try:
            if (paieska in knyga['pavadinimas'].lower() or 
                paieska in knyga['zanras'].lower() or 
                paieska in knyga['knygos_kodas'].lower() or 
                paieska in str(knyga['leidimo_metai']).lower()):
                
                rasta = True
                print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, "
                      f"Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta['tipas'] == 'knygyne')
                pas_skaitytoja = [v for v in knyga['vietos'] if v['tipas'] == 'pas_skaitytoja']
                
                print(f"  Knygyne: {knygyne_kiekis} vnt.")
                if pas_skaitytoja:
                    print("  Pas skaitytojus:")
                    for info in pas_skaitytoja:
                        vartotojas = info['vartotojas']
                        print(f"    Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
                else:
                    print("  Pas skaitytojus: 0 vnt.")
        except Exception as e:
            if DEBUGINIMAS:
                print(f"Klaida apdorojant įrašą: {e}")
            continue

    if not rasta:
        print("Nerasta jokia knyga pagal nurodytą frazę.")
    input("Paspauskite ENTER, kad grįžti atgal.")


def utelizuoti_knygas(knygos):
    try:
        metai = int(input("Įveskite knygos senumą metais, kurias ištrinti: "))
    except ValueError:
        print("Įvesta netinkama reikšmė, prašome įvesti skaičių.")
        return

    siandiena = datetime.now().year

    # Įkelti arba sukurti utelizuotos knygos sąrašą
    utelizuotos = load_json(UTELEZUOTOS_FAILAS) or []

    knygos_utelizuoti = []

    for knyga in knygos['knygos']:
        if siandiena - knyga['leidimo_metai'] > metai:
            knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta.get('tipas') == 'knygyne')
            pas_skaitytoja = any(vieta.get('tipas') == 'pas_skaitytoja' for vieta in knyga['vietos'])

            if knygyne_kiekis > 0 and not pas_skaitytoja:
                knygos_utelizuoti.append(knyga)
            elif pas_skaitytoja:
                print(f"Knyga '{knyga['pavadinimas']}' yra pas skaitytoją ir negali būti utelizuota.")

    if knygos_utelizuoti:
        for knyga in knygos_utelizuoti:
            print(f"Utelizuojama knyga: {knyga['pavadinimas']} (kodas: {knyga['knygos_kodas']})")
            knygos['knygos'].remove(knyga)
            utelizuotos.append(knyga)
        
        save_json(KNYGOS_FAILAS, knygos)
        save_json(UTELEZUOTOS_FAILAS, utelizuotos)

        print("Knygos utelizuotos sėkmingai.")
    else:
        print("Nėra knygų, kurias galima utelizuoti pagal nurodytus metų senumą.")

def darbuotojo_menu(darbuotojas, knygos, skaitytojai, darbuotojai):
    while True:
        print("\nPasirinkite veiksmą:")
        print("1 - Įvesti naują knygą")
        print("2 - Esamos knygos")
        print("3 - Vėluojančios knygos")
        print("4 - Atsijungti")
        try:
            pasirinkimas = int(input("Pasirinkimas: "))
        except ValueError:
            print("Įveskite galiojantį skaičių.")
            continue

        if pasirinkimas == 1:
            prideti_nauja_knyga(knygos)
        elif pasirinkimas == 2:
            perziureti_knygas(knygos)
        elif pasirinkimas == 3:
            patikrinti_velavimus(knygos, skaitytojai)
        elif pasirinkimas == 4:
            print("Atsijungiama...")
            print("Viso gero..")
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")

def registruotis_skaitytojas(skaitytojai, asmensduomenys):
    # strip() - pašalina tarpus pradžioje ir pabaigoje
    while True:
        vardas = input("Įveskite savo vardą: ").strip()
        if vardas:
            break
        print("Vardas negali būti tuščias. Bandykite dar kartą.")

    while True:
        pavarde = input("Įveskite savo pavardę: ").strip()
        if pavarde:
            break
        print("Pavardė negali būti tuščia. Bandykite dar kartą.")    

    while True:
        asmens_kodas_lt = input("Įveskite savo asmens kodą: ").strip()
        if asmens_kodas_lt in [s['asmens_kodas_lt'] for s in skaitytojai]:
            print("Toks asmens kodas jau egzistuoja. Pabandykite prisijungti..")
            return
        if asmens_kodas_lt:
            break
        print("Asmens kodas negali būti tuščias. Bandykite dar kartą.")

    while True:
        kontaktinis_telefonas = input("Įveskite savo kontaktinį telefoną: ").strip()
        if kontaktinis_telefonas in [s['kontaktinis_telefonas'] for s in skaitytojai]:
            print("Toks kontaktinis telefonas jau egzistuoja. Pabandykite prisijungti..")
            return
        if kontaktinis_telefonas:
            break
        print("Kontaktinis telefonas negali būti tuščias. Bandykite dar kartą.")

    while True:
        el_pastas = input("Įveskite savo el. paštą: ").strip()
        if el_pastas in [s['el_pastas'] for s in skaitytojai]:
            print("Toks el. paštas jau egzistuoja. Pabandykite prisijungti..")
            return
        if el_pastas:
            break  
        print("El. paštas negali būti tuščias. Bandykite dar kartą.")

    vartotojo_numeris = generuoti_vartotojo_numeri()    
    
    if vartotojo_numeris in [s['vartotojo_numeris'] for s in skaitytojai]:
        print("Toks vartotojo numeris jau egzistuoja. Pabandykite prisijungti..")
        return

    naujas_skaitytojas = {
        "vardas": vardas,
        "pavarde": pavarde,
        "vartotojo_numeris": vartotojo_numeris,
        "asmens_kodas_lt": asmens_kodas_lt,
        "kontaktinis_telefonas": kontaktinis_telefonas,
        "el_pastas": el_pastas
    }
    skaitytojai.append(naujas_skaitytojas)
    asmensduomenys['skaitytojai'] = skaitytojai
    save_json(ASMENS_DUOMENYS_FAILAS, asmensduomenys)
    print("Registracija sėkminga!")
    print(f"Jūsų vartotojo numeris: {vartotojo_numeris}. Prašome išsisaugoti šį numerį.")

def grazinti_knyga(knygos, skaitytojai, vartotojo_numeris):
    knygos_kodas = input("Įveskite grąžinamos knygos kodą: ")
    rasta_knyga = False
    for knyga in knygos['knygos']:
        if knyga['knygos_kodas'] == knygos_kodas:
            for vieta in knyga['vietos']:
                if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                    knyga['vietos'].remove(vieta)
                    # Atnaujinti knygyno kiekį
                    knygyne = next((v for v in knyga['vietos'] if v['tipas'] == 'knygyne'), None)
                    if knygyne:
                        knygyne['kiekis'] += 1
                    else:
                        knyga['vietos'].append({"tipas": "knygyne", "kiekis": 1})
                    rasta_knyga = True
                    break
            if rasta_knyga:
                break

    if rasta_knyga:
        save_json(KNYGOS_FAILAS, knygos)
        print("Knyga sėkmingai grąžinta.")
    else:
        print("Nerasta knyga su nurodytu kodu arba ji nėra pas jus.")

def pasiimti_knyga(knygos, skaitytojai, vartotojo_numeris): 
    if ispejimas_skaitytojui(knygos, skaitytojai, vartotojo_numeris):
        tikrai_veluoja = []
        for knyga in knygos['knygos']:
            for vieta in knyga['vietos']:
                if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                    vartotojas = vieta['vartotojas']
                    paemimo_data = datetime.strptime(vartotojas['paemimo_data'], '%Y-%m-%d')
                    if (datetime.now() - paemimo_data).days > MAX_VELAVIMAS:
                        tikrai_veluoja.append(vartotojas)   
        for skaitytojas in tikrai_veluoja:
            print(f"  - Vartotojo numeris: {skaitytojas['vartotojo_numeris']}, Paėmimo data: {skaitytojas['paemimo_data']}")
    else:
        knygos_kodas = input("Įveskite pasiimamos knygos kodą: ")
        rasta_knyga = False
        for knyga in knygos['knygos']:
            if knyga['knygos_kodas'] == knygos_kodas:
                for vieta in knyga['vietos']:
                    if vieta['tipas'] == 'knygyne' and vieta['kiekis'] > 0:
                        vieta['kiekis'] -= 1
                        if vieta['kiekis'] == 0:
                            knyga['vietos'].remove(vieta)
                        knyga['vietos'].append({
                            "tipas": "pas_skaitytoja",
                            "vartotojas": {
                                "vartotojo_numeris": vartotojo_numeris,
                                "paemimo_data": datetime.now().strftime('%Y-%m-%d')
                            }
                        })
                        rasta_knyga = True
                        break
                if rasta_knyga:
                    break

        if rasta_knyga:
            save_json(KNYGOS_FAILAS, knygos)
            print("Knyga sėkmingai pasiimta.")
        else:
            print("Nerasta knyga su nurodytu kodu arba nėra laisvų egzempliorių.")

def skaitytojo_menu(knygos, skaitytojai, asmensduomenys):
    while True:
        print("\nPasirinkite veiksmą:")
        print("1 - Grąžinti knygą")
        print("2 - Knygyno Knygos")
        print("3 - Mano Knygos")
        print("4 - Atgal")
        try:
            veiksmas = int(input("Pasirinkimas: "))
        except ValueError:
            print("Įveskite galiojantį skaičių.")
            continue

        if veiksmas == 1:
            grazinti_knyga(knygos, skaitytojai, vartotojo_numeris)
        elif veiksmas == 2:
            perziureti_knygos_skaitytojas(knygos, skaitytojai)
        elif veiksmas == 3:
            perziureti_mano_knygos(knygos, vartotojo_numeris)
        elif veiksmas == 4:
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")

def perziureti_knygos_skaitytojas(knygos, skaitytojai):
    while True:
        print("\nPasirinkite peržiūros variantą:")
        print("1 - Visų knygų knygyne sąrašas")
        print("2 - Paieška")
        print("3 - Pasiimti knygą")
        print("4 - Grįžti atgal")
        try:
            pasirinkimas = int(input("Pasirinkimas: "))
        except ValueError:
            print("Įveskite galiojantį skaičių.")
            continue

        if pasirinkimas == 1:
            visos_knygos_sarasas_skaitytojui(knygos)
        elif pasirinkimas == 2:
            paieska_knygose_skaitytojui(knygos)
        elif pasirinkimas == 3:
            pasiimti_knyga(knygos, skaitytojai, vartotojo_numeris)
        elif pasirinkimas == 4:
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")

def perziureti_mano_knygos(knygos, vartotojo_numeris):
    """
    Rodo skaitytojo paimtas knygas.
    """
    print("Jūsų paimtos knygos:")
    rasta_knyga = False
    for knyga in knygos['knygos']:
        for vieta in knyga['vietos']:
            if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                print(f"  - {knyga['pavadinimas']} (kodas: {knyga['knygos_kodas']})")
                rasta_knyga = True
    if not rasta_knyga:
        print("Jūs neturite jokių knygų.")
    input("Paspauskite ENTER, kad grįžti atgal.")

def autentifikuoti_skaitytoja(skaitytojai):
    """
    Autentifikuoja skaitytoją pagal vartotojo numerį.
    """
    vartotojo_numeris = input("Įveskite savo vartotojo numerį: ")
    skaitytojas = next((s for s in skaitytojai if s['vartotojo_numeris'] == vartotojo_numeris), None)
    if skaitytojas:
        print("Sėkmingai prisijungta kaip skaitytojas.")
        print()
        return skaitytojas
    else:
        print("Neteisingas vartotojo numeris. Bandykite dar kartą.")
        return None

def registracija_menu(skaitytojai, asmensduomenys):
    print("\n--- Naujo skaitytojo registracija ---")
    registruotis_skaitytojas(skaitytojai, asmensduomenys)

def skaitytojo_apdorojimas(knygos, skaitytojai, asmensduomenys):
    """
    Apdorojama skaitytojo veikla, įskaitant registraciją ir prisijungimą.
    """
    while True:
        print("\nPasirinkite veiksmą:")
        print("1 - Naujo skaitytojo registracija")
        print("2 - Esamas skaitytojas")
        print("3 - Grįžti atgal")
        try:
            pasirinkimas = int(input("Pasirinkimas: "))
        except ValueError:
            print("Įveskite galiojantį skaičių.")
            continue

        if pasirinkimas == 1:
            registracija_menu(skaitytojai, asmensduomenys)
        elif pasirinkimas == 2:
            skaitytojas = autentifikuoti_skaitytoja(skaitytojai)
            if skaitytojas:
                ispejimas_skaitytojui(knygos, skaitytojai, skaitytojas['vartotojo_numeris'])
                global vartotojo_numeris
                vartotojo_numeris = skaitytojas['vartotojo_numeris']
                skaitytojo_menu(knygos, skaitytojai, asmensduomenys)
        elif pasirinkimas == 3:
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")


# Pagrindinis meniu 
def pagrindine_menu(knygos, skaitytojai, darbuotojai, asmensduomenys):
    while True:
        print("\nSveiki atvykę į biblioteką!")
        print("1 - Darbuotojas")
        print("2 - Skaitytojas")
        print("3 - Viso Gero")
        role = input("Pasirinkimas: ")

        if role == '1':
            darbuotojas = autentifikuoti_darbuotoja(darbuotojai)
            if darbuotojas:
                darbuotojo_menu(darbuotojas, knygos, skaitytojai, darbuotojai)
        elif role == '2':
            skaitytojo_apdorojimas(knygos, skaitytojai, asmensduomenys)
        elif role == '3':
            print("Lauksime sugrįžtant")
            break
        else:
            print("Neteisingas pasirinkimas. Bandykite dar kartą.")

def patikrinti_velavimus(knygos, skaitytojai):
    visi_veluojantys_skaitytojai = []
    for knyga in knygos['knygos']:
        for vieta in knyga['vietos']:
            if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta:
                vartotojas = vieta['vartotojas']
                paemimo_data = datetime.strptime(vartotojas['paemimo_data'], '%Y-%m-%d')
                if (datetime.now() - paemimo_data).days > MAX_VELAVIMAS:
                    visi_veluojantys_skaitytojai.append(vartotojas)
    
    if visi_veluojantys_skaitytojai:
        print("Vėluojantys skaitytojai:")
        for skaitytojas in visi_veluojantys_skaitytojai:
            print(f"  - Vartotojo numeris: {skaitytojas['vartotojo_numeris']}, Paėmimo data: {skaitytojas['paemimo_data']}")
            # Rasti veluojančia knyga
            knyga = next((k for k in knygos['knygos'] for v in k['vietos'] if v['tipas'] == 'pas_skaitytoja' and 'vartotojas' in v and v['vartotojas']['vartotojo_numeris'] == skaitytojas['vartotojo_numeris']), None)
            if knyga:
                print(f"    Knygos pavadinimas: {knyga['pavadinimas']}, Knygos kodas: {knyga['knygos_kodas']}")
            # Rasti asmens duomenis
            asmuo = next((a for a in skaitytojai if a['vartotojo_numeris'] == skaitytojas['vartotojo_numeris']), None)
            if asmuo:
                print(f"    Vardas: {asmuo['vardas']}, Pavardė: {asmuo['pavarde']}, "
                      f"Kontaktinis telefonas: {asmuo['kontaktinis_telefonas']}, El. paštas: {asmuo['el_pastas']}")
    else:
        print("Daugiau nėra vėluojančių skaitytojų.")

# ispejimas_skaitytojui jei veluoja daugiau nei MAX_VELAVIMAS ir neleidžia paiimti naujų knygų kol senos negrąžiniotos:
def ispejimas_skaitytojui(knygos, skaitytojai, vartotojo_numeris):
    tikrai_veluoja = []
    for knyga in knygos['knygos']:
        for vieta in knyga['vietos']:
            if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                vartotojas = vieta['vartotojas']
                paemimo_data = datetime.strptime(vartotojas['paemimo_data'], '%Y-%m-%d')
                if (datetime.now() - paemimo_data).days > MAX_VELAVIMAS:
                    tikrai_veluoja.append(vartotojas)
    
    if tikrai_veluoja:
        print(f"Jūs vėluojate grąžinti šias knygas:")
        for skaitytojas in tikrai_veluoja:
            print(f"  - Vartotojo numeris: {skaitytojas['vartotojo_numeris']}, Paėmimo data: {skaitytojas['paemimo_data']}")
        print("Jūs negalite pasiimti naujų knygų kol nebus grąžintos senos.")
        # negražintos knygos pavadinimas ir kodas:
        for knyga in knygos['knygos']:
            for vieta in knyga['vietos']:
                if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                    print(f"  - {knyga['pavadinimas']} (kodas: {knyga['knygos_kodas']})")
        return True
    else:
        return False    



def main():
    # Pagrindinė programos funkcija.
    # Įkelti duomenis
    knygos = load_json(KNYGOS_FAILAS)
    asmensduomenys = load_json(ASMENS_DUOMENYS_FAILAS)
    if not knygos or not asmensduomenys:
        print("Nepavyko įkelti būtinos informacijos. Programa uždaroma.")
        return    

    skaitytojai = asmensduomenys.get('skaitytojai', [])
    darbuotojai = asmensduomenys.get('darbuotojai', [])

    # Pagrindinis meniu
    pagrindine_menu(knygos, skaitytojai, darbuotojai, asmensduomenys)

if __name__ == "__main__":
    main()
