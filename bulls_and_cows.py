"""
projekt_2.py: druhý projekt do Engeto Online Python Akademie 
author: Diana Průšová
email: di.prusova@gmail.com
discord: Diana P. / Wild Diana#5386
"""
import random
import os
import time


def precti_ulozene_skore() -> dict:
    """
    Funkce načte skóre hráčů z daného souboru a uloží ho jako 
    slovník.
    """
    with open("skore.txt", mode="r", encoding="utf-8") as soubor:
        skore = eval(soubor.read())
        
    return skore


def vypis_skore():
    """
    Funkce vypíše skóre nejlepšího hráče a celkóvé skóre hráčů.
    """
    skore = precti_ulozene_skore()

    # VÝPIS NEJLEPŠÍHO HRÁČE
    nejlepsi = []
    for hodnota in skore["nejlepší"].values():
        nejlepsi.append(hodnota)

    print(
        f"NEJLEPŠÍ SKÓRE = čas hry: {nejlepsi[1]}, počet pokusů: {nejlepsi[2]}"
        f" - {nejlepsi[0]}"
    )

    # VÝPOČET A VÝPIS PRŮMĚRNÉHO SKÓRE
    prumerny_cas_float = skore["hráči"]["sum čas"] / skore["hráči"]["sum hráčů"]
    prumerny_cas = prevod_casu(prumerny_cas_float)

    prumerne_pokusy = skore["hráči"]["sum pokusů"] / skore["hráči"]["sum hráčů"]
    prumerne_pokusy = int(round(prumerne_pokusy, 0))

    print(
        f"PRŮMĚRNÉ SKÓRE = čas hry: {prumerny_cas}, počet pokusů: {prumerne_pokusy}"
    )


def uvitani():
    """
    Funkce uvítá hráče ve hře a představí pravidla hry.
    """
    os.system("cls")
    from obrazky import logo
    skore = precti_ulozene_skore()
    podtrzeni = "-" *55
    
    print(logo)

    vypis_skore()

    print("\nVítej hráči! Jsi připravený porovnat se mnou své síly?\n"
    f"{podtrzeni}\nZahrajeme si hru Bulls & Cows... Budeš hádat "
    "čtyřmístné číslo. Pokud trefíš číslici\na umístění, získáš 'BULL'"
    ", pokud trefíš jen číslo, ale ne umístění, získáš 'COW'.\n\nAle abych"
    " nebyl takový pes, prozdradím ti, že moje číslo nezačíná nulou "
    "a žádná\nčíslice se v řetězci nikdy neopakuje.")
 

def vygeneruji_hadane_cislo() -> list:
    """ 
    Funkce vygeneruje náhodné číslo, které bude hráč hádat.
    Retur: list se čtyřmi int
    """
    hadane_cislo = []
    hadane_cislo.append(random.randint(1, 9))

    while len(hadane_cislo) < 4:
        cislo = random.randint(0, 9)
        if cislo in hadane_cislo:
            continue
        else:
            hadane_cislo.append(cislo)

    return hadane_cislo


def ziskani_tipu_hrace() -> list:
    """
    Funkce si vyžádá tip číselné řady od hráče, zkonroluje, jestli 
    byl zadán ve správném formátu a převede jej na list integerů.
    """
    while True:
        tip_hrace = input("\nZadej čtyřmístné číslo (nebo 'exit'"
                        " pro ukončení hry): ").lower()

        # první KONTROLA OBSAHU  
        if tip_hrace == "exit":
            cislo_hrace = tip_hrace
            return cislo_hrace        
        elif not tip_hrace.isdigit():
            print("Můžeš zadat pouze číslice. Zkus to znovu...")
        elif len(tip_hrace) != 4:
            print("Je třeba zadat čtyři číslice. Zkus to znovu....")
        elif tip_hrace.startswith("0"):
            print("První číslice nemůže být nula. Zkus to znovu...")
        else: 
            # PŘEVOD NA LIST
            cislo_hrace = []
            for cislo in tip_hrace:
                cislo = int(cislo)
                cislo_hrace.append(cislo)  

            # druhá KONTROLA OBSAHU
            if len(set(cislo_hrace)) < 4:
                print("Jednu číslici jsi zadal vícekrát. Zkus to znovu...")
            else: 
                return cislo_hrace


def vyhodnoceni_typu_hrace(hadane_cislo: list):
    """Funkce získá přes funkci 'ziskani_tipu_hrace' tipy od hráče
    a následně je vyhodnocuje (počítá cow/bull a počet pokusu). 
    
    Return:
        - str: 'exit' - pokud chce hráč hru ukončit
        - int obsahující počet pokusů, pokud hráč číslo uhádne
    """
    pocet_pokusu = 0
    while True:
        cislo_hrace = ziskani_tipu_hrace()
        pocet_pokusu += 1
        bulls = 0
        cows = 0
        print(hadane_cislo)

        # VYHODNOCENÍ OBSAHU
        if cislo_hrace == "exit":
            return "exit"
        elif cislo_hrace == hadane_cislo:
            return pocet_pokusu
        else:
            for index, cislo in enumerate(cislo_hrace):
                cislo = int(cislo)
                if cislo == hadane_cislo[index]:
                    bulls += 1
                elif cislo in hadane_cislo:
                    cows += 1

            # POČÍNÁNÍ "SKÓRE"
            if bulls > 1:
                vypis_bulls = f"BULLS {bulls}x"
            else:
                vypis_bulls = f"BULL {bulls}x"

            if cows > 1:
                vypis_cows = f"COWS {cows}x"
            else:
                vypis_cows = f"COW {cows}x"

            # VÝPIS VÝSLEDKU
            print(f"| {vypis_bulls} | {vypis_cows} |")


def prevod_casu(cas: float) -> str:
    """
    Funkce získá počet vteřit (za který hráči trvalo uhodnout číslo) 
    a následně je převede na hodiny, minuty a vteřiny a uloží jako str. 
    
    PŘÍKLAD: 
        vstup: cas = 71.1254825
        výstup: 00:01:11
    """
    hodiny = int(round(cas / 3600, 0))
    minuty = int(round((cas % 3600) / 60, 0))
    vteriny = int(round(cas % 60, 0))

    prepocitany_cas = f"{hodiny:02}:{minuty:02}:{vteriny:02}"

    return prepocitany_cas


def predcasne_ukonceni():
    """
    Funkce vypíše rozloučení s hráčem v případě, že se rozhodne
    hru ukončit předčasně. 
    """
    from obrazky import loser
    print(f"\nUkončuji hru...\n{loser}")


def vyhra(cas_hry, pocet_pokusu):
    """
    Funkce oznámí hráči že vyhrál a vypíše celkový čas hry a počet
    pokusů, za které číslo uhádnul.
    """
    from obrazky import winner
    os.system("cls")
    cara = "-" *41
    cas = prevod_casu(cas_hry)

    print(f"{winner}\nNeuvěřitelné, ty jsi vyhrál! Gratuluji..."
        f"\n{cara}\n\nCELKOVÝ ČAS HRY: {cas}\n"
        f"CELKOVÝ POČET POKUSU: {pocet_pokusu}\n")


def aktualizace_skore(cas_hry: float, pocet_pokusu: int) -> dict:
    """
    Funkce načte uložené skóre z daného souboru a aktualizuje jeho
    hodnoty. Pokud je počet pokusů nižší než počet pokusů nejlepšího
    hráče, vyžádá si jméno hráče a upraví i tyto hodnoty. 
    """
    skore = precti_ulozene_skore()
    podtrzeni = "=" * 45

    # NEJLEPŠÍHO HRÁČE
    if skore["nejlepší"]["pokusy"] > pocet_pokusu:
        jmeno = input("Porazil jsi našeho nejlepšího hráče! Zadej své jméno: ").upper()
        if jmeno == "":
            jmeno = "ANONYM"

        print(f"\nGratuluju, byl jsi zapsán jako nejlepší hráč.\n{podtrzeni}")
        skore["nejlepší"]["jméno"] = jmeno
        skore["nejlepší"]["čas"] = prevod_casu(cas_hry)
        skore["nejlepší"]["pokusy"] = pocet_pokusu

    # CELKOVÉ SKÓRE
    skore["hráči"]["sum hráčů"] += 1
    skore["hráči"]["sum čas"] += cas_hry
    skore["hráči"]["sum pokusů"] += pocet_pokusu

    return skore
    

def ulozeni_noveho_skore(skore: dict):
    """
    Funkce zapíše aktualizované skóre do nového souboru, zkontroluje,
    jestli nedošlo při zápisu k chybě a pokud ne, skóre uloží. Pokud 
    dojde k chybě, funkce nechá původní soubor bezezměny a nové skóre 
    se neuloží.
    """

    # ZÁPIS SKÓRE DO SOUBORU
    with open("skore_kopie.txt", mode="w", encoding="utf-8") as soubor:
        soubor.write(str(skore))

    obsah = (open("skore_kopie.txt", mode="r", encoding="utf-8")).read()

    # KONTROLA ZÁPISU    
    if obsah == str(skore):
        os.remove("skore.txt")
        os.rename("skore_kopie.txt", "skore.txt")
    else:
        print("Došlo k chybě... Nové skóre bohužel nebylo uloženo.")
        os.remove("skore_kopie.txt")


def main():
    # HRA
    uvitani()
    score = precti_ulozene_skore()
    hadane_cislo = vygeneruji_hadane_cislo()
    t0 = time.time()
    vysstup_hrace = vyhodnoceni_typu_hrace(hadane_cislo)
    
    # VYHODNOCENÍ HRY
    if vysstup_hrace == "exit":
        predcasne_ukonceni()
    elif isinstance(vysstup_hrace, int) :
        t1 = time.time()
        cas_hry = t1 -t0
        vyhra(cas_hry, vysstup_hrace)

        # AKTUALIZACE SKÓRE
        skore = aktualizace_skore(cas_hry, vysstup_hrace)
        ulozeni_noveho_skore(skore)
      

if __name__ == "__main__":
    main()



