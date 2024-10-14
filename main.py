# Nustatymai

max_velavimas = 365 # maksimalus vėlavimas dienomis




# importuojame modulius
import json 
from datetime import datetime 
import random # reikalingas sugeneruoti vartotojo numerį
import string #  reikalingas sugeneruoti vartotojo numerį





# Atidarome knygos.json failą kuriame saugoma bibliotekos duomenys ir nuskaitome duomenis

try:
    with open('./knygos.json', 'r', encoding='utf-8') as file:
        knygos = json.load(file)
except FileNotFoundError:
    print("Failas 'knygos.json' nerastas.")
except json.JSONDecodeError as e:
    print(f"JSON formatavimo klaida faile 'knygos.json': {e}")
except Exception as e:
    print(f"Nenumatyta klaida, kreipkitės į adminsitratorių: {e}")

# atidarome asmensduomenys.json failą kuriame saugoma skaitytojų ir darbuotojų duomenis, nuskaitome juos:
try:
    with open('./asmensduomenys.json', 'r', encoding='utf-8') as file:
        asmensduomenys = json.load(file)
        skaitytojai = asmensduomenys.get('skaitytojai', [])
        darbuotojai = asmensduomenys.get('darbuotojai', [])

except FileNotFoundError:
    print("Failas 'asmensduomenys.json' nerastas.")
except json.JSONDecodeError as e:
    print(f"JSON formatavimo klaida faile 'asmensduomenys.json': {e}")
except Exception as e:
    print(f"Nenumatyta klaida, kreipkitės į adminsitratorių: {e}")    

while True:
    # Paklausiame vartotojo, kas jis yra
    role = input("Sveiki atvykę į biblioteką! \n1 - Darbuotojas\n2 - Skaitytojas\n3 - Viso Gero\n")
    
    # Jei vartotojas yra darbuotojas
    if role == '1':
        while True:
            # Paprašome darbuotojo kodo
            darbuotojo_kodas = input("Įveskite darbuotojo kodą: ")
            
            # Patikriname, ar darbuotojo kodas yra teisingas
            if darbuotojo_kodas in [darbuotojas['darbuotojo_kodas'] for darbuotojas in darbuotojai]:
                while True:
                    # Darbuotojo pasirinkimai
                    darbuotojo_pasirinkimas = int(input("Pasirinkite: \n1 - Įvesti naują knygą\n2 - Esamos knygos\n3 - Atsijungti\n"))
                    
                    # Įvesti naują knygą
                    if darbuotojo_pasirinkimas == 1:
                        kodas = input("Įveskite knygos kodą: ")
                        pavadinimas = input("Įveskite knygos pavadinimą: ")
                        leidimo_metai = int(input("Įveskite knygos leidimo metus: "))
                        zanras = input("Įveskite knygos žanrą: ")
                        kiekis = int(input("Įveskite knygos kiekį: "))
                        vietos = [{"tipas": "knygyne", "kiekis": kiekis}]  # Pagal nutylėjimą tipas yra knygyne su kiekiu                        
                        
                        # Pridedame naują knygą į knygos.json
                        knygos['knygos'].append({
                            "knygos_kodas": kodas,
                            "pavadinimas": pavadinimas,
                            "leidimo_metai": leidimo_metai,
                            "zanras": zanras,
                            "vietos": vietos
                        })
                        with open('knygos.json', 'w', encoding='utf-8') as file:
                            json.dump(knygos, file, ensure_ascii=False, indent=4)
                    
                    # Peržiūrėti knygas
                    elif darbuotojo_pasirinkimas == 2:
                        while True:
                            perziura_pasirinkimas = int(input("Pasirinkite: \n1 - Visų knygų knygyne sąrašas\n2 - Paieška\n3 - Utelizuoti senas knygas\n4 - Grįžti\n"))
                            # Visų knygų knygyne sąrašas ir tipas kur yra ir kiek
                            if perziura_pasirinkimas == 1:
                                for knyga in knygos['knygos']:
                                    print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                                    knygyne_kiekis = 0
                                    pas_skaitytoja = []
                                    for vieta in knyga['vietos']:
                                        if vieta['tipas'] == 'knygyne':
                                            knygyne_kiekis += vieta['kiekis']
                                        elif vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta:
                                            vartotojas = vieta['vartotojas']
                                            pas_skaitytoja.append(f"Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
                                    
                                    print(f"  Knygyne: {knygyne_kiekis} vnt.")
                                    if pas_skaitytoja:
                                        print("  Pas skaitytojus:")
                                        for info in pas_skaitytoja:
                                            print(f"    {info}")
                                    else:
                                        print("  Pas skaitytojus: 0 vnt.")
                                input("Paspauskite ENTER, kad grįžti atgal")

                            elif perziura_pasirinkimas == 2:
                                paieska = input("Įveskite knygos pavadinimo, žanro, kodo arba išleidimo metų frazę: ")
                                rasta_knyga = False  

                                for knyga in knygos['knygos']:
                                    try:
                                        if (paieska.lower() in knyga['pavadinimas'].lower() or 
                                            paieska.lower() in knyga['zanras'].lower() or 
                                            paieska.lower() in knyga['knygos_kodas'].lower() or 
                                            paieska.lower() in str(knyga['leidimo_metai']).lower()):
                                            
                                            rasta_knyga = True  
                                            print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                                            knygyne_kiekis = 0
                                            pas_skaitytoja = []
                                            for vieta in knyga['vietos']:
                                                if vieta['tipas'] == 'knygyne':
                                                    knygyne_kiekis += vieta['kiekis']
                                                elif vieta['tipas'] == 'pas_skaitytoja':
                                                    vartotojas = vieta['vartotojas']
                                                    pas_skaitytoja.append(f"Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
                                            
                                            print(f"  Knygyne: {knygyne_kiekis} vnt.")
                                            if pas_skaitytoja:
                                                print("  Pas skaitytojus:")
                                                for info in pas_skaitytoja:
                                                    print(f"    {info}")
                                            else:
                                                print("  Pas skaitytojus: 0 vnt.")
                                    except Exception as e:
                                        print(f"Klaida apdorojant įrašą: {e}")

                                if not rasta_knyga:
                                    print("Nerasta jokia knyga pagal nurodytą frazę.")                                

                                input("Paspauskite ENTER, kad grįžti atgal")

                            # Ištrinti knygas pagal išleidimo metus įvedus metų skaičių. Ištrintos knygos perkeliamos į utelizuotos.json failą
                            elif perziura_pasirinkimas == 3:
                                try:
                                    metai = int(input("Įveskite knygos senumą metais, kurias ištrinti: "))
                                    siandiena = datetime.now().year

                                    # Atidarome arba sukuriame 'utelizuotos.json' failą
                                    try:
                                        with open('utelizuotos.json', 'r', encoding='utf-8') as file:
                                            utelizuotos = json.load(file)
                                    except FileNotFoundError:
                                        utelizuotos = []
                                    except json.JSONDecodeError as e:
                                        print(f"JSON formatavimo klaida faile 'utelizuotos.json': {e}")
                                        utelizuotos = []

                                    knygos_utelizuoti = []

                                    # Tikriname, kurios knygos turi būti utelizuotos
                                    for knyga in knygos['knygos']:
                                        if siandiena - knyga['leidimo_metai'] > metai:
                                            knygyne_kiekis = sum(vieta['kiekis'] for vieta in knyga['vietos'] if vieta.get('tipas') == 'knygyne')
                                            pas_skaitytoja = any(vieta.get('tipas') == 'pas_skaitytoja' for vieta in knyga['vietos'])

                                            if knygyne_kiekis > 0 and not pas_skaitytoja:
                                                knygos_utelizuoti.append(knyga)
                                            elif pas_skaitytoja:
                                                print(f"Knyga '{knyga['pavadinimas']}' yra pas skaitytoją ir negali būti utelizuota.")

                                    # Jei yra knygų, kurios turi būti utelizuotos
                                    if knygos_utelizuoti:
                                        for knyga in knygos_utelizuoti:
                                            print(f"Utelizuojama knyga: {knyga['pavadinimas']} (kodas: {knyga['knygos_kodas']})")
                                            knygos['knygos'].remove(knyga)
                                            utelizuotos.append(knyga)

                                        # Atnaujiname failą 'knygos.json'
                                        with open('knygos.json', 'w', encoding='utf-8') as file:
                                            json.dump(knygos, file, ensure_ascii=False, indent=4)

                                        # Atnaujiname failą 'utelizuotos.json'
                                        with open('utelizuotos.json', 'w', encoding='utf-8') as file:
                                            json.dump(utelizuotos, file, ensure_ascii=False, indent=4)

                                        print(f"Knygos utelizuotos sėkmingai.")
                                    else:
                                        print("Nėra knygų, kurias galima utelizuoti pagal nurodytus metų senumą.")

                                except ValueError:
                                    print("Įvesta netinkama reikšmė, prašome įvesti skaičių.")
                                except Exception as e:
                                    print(f"Nenumatyta klaida, kreipkitės į administratorių: {e}")
                            elif    perziura_pasirinkimas == 4:
                                break  
                    elif darbuotojo_pasirinkimas == 3:
                        break  # Reikia pataisyti į double break                                                          
                    else:
                        print("Neteisingas pasirinkimas. Bandykite dar kartą.")
                        break  
            else: 
                print("Neteisingas darbuotojo kodas. Bandykite dar kartą.")
                break
    
    # Jei vartotojas yra skaitytojas
    elif role == '2':
            while True:
                skaitytojo_pasirinkimas = int(input("Pasirinkite: \n1 - Naujo skaitytojo registracija\n2 - Esamas skaitytojas\n3 - Grįžti atgal\n"))
                
                # Registruotis
                if skaitytojo_pasirinkimas == 1:
                    vardas = input("Įveskite savo vardą: ")
                    pavarde = input("Įveskite savo pavardę: ")                    
                    def generuoti_vartotojo_numeri():
                        pirmoji_raide = random.choice(string.ascii_uppercase)
                        trys_skaiciai = ''.join(random.choices(string.digits, k=3))
                        return pirmoji_raide + trys_skaiciai
                    vartotojo_numeris = generuoti_vartotojo_numeri()
                    asmens_kodas_lt = input("Įveskite savo asmens kodą: ")
                    kontaktinis_telefonas = input("Įveskite savo kontaktinį telefoną: ")
                    el_pastas = input("Įveskite savo el. paštą: ")

                    # Patikriname, ar vartotojo numeris jau egzistuoja
                    if vartotojo_numeris in [skaitytojas['vartotojo_numeris'] for skaitytojas in skaitytojai]:
                        print("Toks vartotojo numeris jau egzistuoja. Bandykite dar kartą.")
                    else:
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
                        with open('asmensduomenys.json', 'w', encoding='utf-8') as file:
                            json.dump(asmensduomenys, file, ensure_ascii=False, indent=4)
                        print("Registracija sėkminga!")
                        print("Jūsų vartotojo numeris: ", vartotojo_numeris, "Prašome išsisaugoti šį numerį.")
                        skaitytojai.append(naujas_skaitytojas)
                # Esamas skaitytojas
                elif skaitytojo_pasirinkimas == 2:
                    vartotojo_numeris = input("Įveskite savo vartotojo numerį: ")

                    # Patikriname, ar skaitytojo numeris yra teisingas
                    if vartotojo_numeris in [skaitytojas['vartotojo_numeris'] for skaitytojas in skaitytojai]:
                        # Surandame skaitytoją pagal numerį
                        skaitytojas = next(skaitytojas for skaitytojas in skaitytojai if skaitytojas['vartotojo_numeris'] == vartotojo_numeris)
                        
                        # Patikriname, ar skaitytojas turi vėluojančių knygų
                        veluojancios_knygos = []
                        for knyga in knygos['knygos']:
                            for vieta in knyga['vietos']:
                                if vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                                    paemimo_data = datetime.strptime(vieta['vartotojas']['paemimo_data'], '%Y-%m-%d')
                                    if (datetime.now() - paemimo_data).days > max_velavimas:
                                        veluojancios_knygos.append(knyga['pavadinimas'])
                        
                        if veluojancios_knygos:
                            print("Jūs turite vėluojančių knygų ir negalite pasiimti naujų knygų, kol jų negrąžinsite.")
                            print("Vėluojančios knygos:")
                            for knyga in veluojancios_knygos:
                                print(f"  - {knyga}")
                                ar_grazinti = input("Ar norite grąžinti knygą? (taip/ne): ")
                                if ar_grazinti.lower() == 'taip':
                                    knygos_kodas = input("Įveskite grąžinamos knygos kodą: ")
                                else:
                                    print("Lauksime sugrįžtant ir grąžintant knygą.")
                                    break
                                rasta_knyga = False
                                for knyga in knygos['knygos']:
                                        if knyga['knygos_kodas'] == knygos_kodas:
                                            for vieta in knyga['vietos']:
                                                if vieta['tipas'] == 'pas_skaitytoja' and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                                                    knyga['vietos'].remove(vieta)
                                                    # Patikriname, ar jau yra įrašas su tipu "knygyne"
                                                    knygyne_rastas = False
                                                    for vieta in knyga['vietos']:
                                                        if vieta['tipas'] == 'knygyne':
                                                            vieta['kiekis'] += 1
                                                            knygyne_rastas = True
                                                            break
                                                    if not knygyne_rastas:
                                                        knyga['vietos'].append({"tipas": "knygyne", "kiekis": 1})
                                                    rasta_knyga = True
                                                    break
                                        if rasta_knyga:
                                            break
                                if rasta_knyga:
                                        with open('knygos.json', 'w', encoding='utf-8') as file:
                                            json.dump(knygos, file, ensure_ascii=False, indent=4)
                                        print("Knyga sėkmingai grąžinta.")
                                        continue
                                else:
                                        print("Nerasta knyga su nurodytu kodu arba ji nėra pas jus.")

                        else:
                            while True:
                                veiksmas = int(input("Pasirinkite: \n1 - Grąžinti knygą\n2 - Knygyno Knygos\n3 - Mano Knygos\n4 - Atgal\n"))
                                
                                # Grąžinti knygą
                                if veiksmas == 1:
                                    knygos_kodas = input("Įveskite grąžinamos knygos kodą: ")
                                    rasta_knyga = False
                                    for knyga in knygos['knygos']:
                                        if knyga['knygos_kodas'] == knygos_kodas:
                                            for vieta in knyga['vietos']:
                                                if vieta['tipas'] == 'pas_skaitytoja' and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                                                    knyga['vietos'].remove(vieta)
                                                    # Patikriname, ar jau yra įrašas su tipu "knygyne"
                                                    knygyne_rastas = False
                                                    for vieta in knyga['vietos']:
                                                        if vieta['tipas'] == 'knygyne':
                                                            vieta['kiekis'] += 1
                                                            knygyne_rastas = True
                                                            break
                                                    if not knygyne_rastas:
                                                        knyga['vietos'].append({"tipas": "knygyne", "kiekis": 1})
                                                    rasta_knyga = True
                                                    break
                                        if rasta_knyga:
                                            break
                                    if rasta_knyga:
                                        with open('knygos.json', 'w', encoding='utf-8') as file:
                                            json.dump(knygos, file, ensure_ascii=False, indent=4)
                                        print("Knyga sėkmingai grąžinta.")
                                        continue
                                    else:
                                        print("Nerasta knyga su nurodytu kodu arba ji nėra pas jus.")  
                                # Grįžti atgal
                                elif veiksmas == 2:
                                     # Peržiūrėti knygas                    
                                    while True:
                                        perziura_pasirinkimas = int(input("Pasirinkite: \n1 - Visų knygų knygyne sąrašas\n2 - Paieška\n3 - Pasimti knyga\n4 - Grįžti atgal\n"))
                                        # Visų knygų knygyne sąrašas ir tipas kur yra ir kiek
                                        if perziura_pasirinkimas == 1:
                                            for knyga in knygos['knygos']:
                                                print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                                                knygyne_kiekis = 0
                                                for vieta in knyga['vietos']:
                                                    if vieta['tipas'] == 'knygyne':
                                                        knygyne_kiekis += vieta['kiekis']
                                                    elif vieta['tipas'] == 'pas_skaitytoja' and 'vartotojas' in vieta:
                                                        vartotojas = vieta['vartotojas']           
                                                print(f"  Knygyne: {knygyne_kiekis} vnt.")
                                            input("Paspauskite ENTER, kad grįžti atgal")

                                        elif perziura_pasirinkimas == 2:
                                            paieska = input("Įveskite knygos pavadinimo, žanro, kodo arba išleidimo metų frazę: ")
                                            rasta_knyga = False  

                                            for knyga in knygos['knygos']:
                                                try:
                                                    if (paieska.lower() in knyga['pavadinimas'].lower() or 
                                                        paieska.lower() in knyga['zanras'].lower() or 
                                                        paieska.lower() in knyga['knygos_kodas'].lower() or 
                                                        paieska.lower() in str(knyga['leidimo_metai']).lower()):
                                                        
                                                        rasta_knyga = True  
                                                        print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                                                        knygyne_kiekis = 0
                                                        for vieta in knyga['vietos']:
                                                            if vieta['tipas'] == 'knygyne':
                                                                knygyne_kiekis += vieta['kiekis']
                                                        print(f"  Knygyne: {knygyne_kiekis} vnt.")
                                                except Exception as e:
                                                    print(f"Klaida apdorojant įrašą: {e}")

                                            if not rasta_knyga:
                                                print("Nerasta jokia knyga pagal nurodytą frazę.")                                

                                            input("Paspauskite ENTER, kad grįžti atgal")

                                         # Pasiimti knygą
                                        elif perziura_pasirinkimas == 3:
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
                                                # Atnaujiname knygos.json failą
                                                with open('knygos.json', 'w', encoding='utf-8') as file:
                                                    json.dump(knygos, file, ensure_ascii=False, indent=4)                                                
                                                # Atnaujiname asmensduomenys.json failą
                                                asmensduomenys['skaitytojai'] = skaitytojai
                                                with open('asmensduomenys.json', 'w', encoding='utf-8') as file:
                                                    json.dump(asmensduomenys, file, ensure_ascii=False, indent=4)
                                                
                                                print("Knyga sėkmingai pasiimta.")
                                            else:
                                                print("Nerasta knyga su nurodytu kodu arba nėra laisvų egzempliorių.")
                                        elif perziura_pasirinkimas == 4:
                                            break
                                        else:
                                            print("Neteisingas pasirinkimas. Bandykite dar kartą.")
                                            continue                                                
                                    # Skaitytojo turimos knygos                
                                elif veiksmas == 3:                                    
                                    print("Jūsų paimtos knygos:")
                                    rasta_knyga = False
                                    for knyga in knygos['knygos']:
                                        for vieta in knyga['vietos']:
                                            if vieta['tipas'] == 'pas_skaitytoja' and vieta['vartotojas']['vartotojo_numeris'] == vartotojo_numeris:
                                                print(f"  - {knyga['pavadinimas']} (kodas: {knyga['knygos_kodas']})")
                                                rasta_knyga = True
                                    if not rasta_knyga:
                                        print("Jūs neturite jokių knygų.")
                                    input("Paspauskite ENTER, kad grįžti atgal")
                                elif veiksmas == 4:
                                    break        
                    else:
                        print("Neteisingas vartotojo numeris. Bandykite dar kartą.")
                        break
                elif skaitytojo_pasirinkimas == 3:
                    continue
                else:
                    print("Neteisingas pasirinkimas. Bandykite dar kartą.")
                    continue

    # Jei vartotojas nori išeiti iš programos
    elif role == '3':
        print("Lauksime sugrįžtant")
        break

    # Jei vartotojas įveda neteisingą pasirinkimą
    else:
        continue

