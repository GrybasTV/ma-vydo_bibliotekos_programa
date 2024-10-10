

# importuojame modulius
import os 
import json 
from datetime import datetime 


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


# knygos.json faile esančių duomenų payzdys:
# {
#     "knygos": [
#         {
#             "knygos_kodas": "001",
#             "pavadinimas": "Modernūs laikai",
#             "leidimo_metai": 1900,
#             "zanras": "Fantastika",                              
#             "vietos": [
#                 {
#                     "tipas": "knygyne",
#                     "kiekis": 3
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "vartotojas": {
#                         "vartotojo_numeris": "A123",
#                         "paemimo_data": "2023-09-01"                        
#                     }
#                 }
#             ]
#         },
#         {
#             "knygos_kodas": "002",
#             "pavadinimas": "Peilis Rankoje",
#             "leidimo_metai": 2018,
#             "zanras": "Detektyvas",                                 
#             "vietos": [
#                 {
#                     "tipas": "knygyne",
#                     "kiekis": 2
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "user": {
#                         "vartotojo_numeris": "B456",
#                         "paemimo_data": "2023-08-15"                        
#                     }
#                 }
#             ]
#         },
#         {
#             "knygos_kodas": "003",
#             "pavadinimas": "Paslaptingas Miškas",
#             "leidimo_metai": 2021,
#             "zanras": "Nuotykių",
#             "vietos": [
#                 {
#                     "tipas": "knygyne",
#                     "kiekis": 5
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "vartotojas": {
#                         "vartotojo_numeris": "C789",
#                         "paemimo_data": "2023-07-20"
#                     }
#                 }
#             ]
#         },
#         {
#             "knygos_kodas": "004",
#             "pavadinimas": "Žvaigždžių Karai",
#             "leidimo_metai": 2019,
#             "zanras": "Mokslinė Fantastika",
#             "vietos": [
#                 {
#                     "tipas": "knygyne",
#                     "kiekis": 4
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "vartotojas": {
#                         "vartotojo_numeris": "D012",
#                         "paemimo_data": "2023-06-10"
#                     }
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "vartotojas": {
#                         "vartotojo_numeris": "E345",
#                         "paemimo_data": "2023-06-15"
#                     }
#                 },
#                 {
#                     "tipas": "pas_skaitytoja",
#                     "vartotojas": {
#                         "vartotojo_numeris": "F678",
#                         "paemimo_data": "2023-06-20"
#                     }
#                 }
#             ]
#         }
#     ]
# }
    

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
                    pasirinkimas = int(input("Pasirinkite: \n1 - Įvesti naują knygą\n2 - Esamos knygos\n3 - Uždaryti programą\n"))
                    
                    # Įvesti naują knygą
                    if pasirinkimas == 1:
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
                    elif pasirinkimas == 2:
                        while True:
                            perziura_pasirinkimas = int(input("Pasirinkite: \n1 - Visų knygų knygyne sąrašas\n2 - Paieška\n3 - Utelizuoti senas knygas\n4 - Uždaryti Programą\n"))
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
                                    
                            # Uždaryti programą
                            elif perziura_pasirinkimas == 4:
                                exit()                               
                    elif pasirinkimas == 3:
                        exit()           
                    
            else: 
                print("Neteisingas darbuotojo kodas. Bandykite dar kartą.")
                break
    
    # Jei vartotojas yra skaitytojas
    elif role == '2':
        # Paprašome skaitytojo vartotojo numerio
        skaitytojo_numeris = input("Įveskite savo vartotojo numerį: ")

        # Patikriname, ar skaitytojo numeris yra teisingas
        if skaitytojo_numeris in [skaitytojas['vartotojo_numeris'] for skaitytojas in skaitytojai]:
            # Peržiūrėti visas knygas
            for knyga in knygos['knygos']:
                print(f"Knygos kodas: {knyga['knygos_kodas']}, Pavadinimas: {knyga['pavadinimas']}, Leidimo metai: {knyga['leidimo_metai']}, Žanras: {knyga['zanras']}")
                for vieta in knyga['vietos']:
                    if vieta['tipas'] == 'knygyne':
                        print(f"  Vieta: {vieta['tipas']}, Kiekis: {vieta['kiekis']}")
                    elif vieta['tipas'] == 'pas_skaitytoja':
                        vartotojas = vieta['vartotojas']
                        print(f"  Vieta: {vieta['tipas']}, Vartotojo numeris: {vartotojas['vartotojo_numeris']}, Paėmimo data: {vartotojas['paemimo_data']}")
        else:
            print("Neteisingas vartotojo numeris. Bandykite dar kartą.")
    
    # Jei vartotojas nori išeiti iš programos
    elif role == '3':
        print("Lauksime sugrįžtant")
        break

    # Jei vartotojas įveda neteisingą pasirinkimą
    else:
        continue

