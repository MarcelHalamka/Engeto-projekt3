"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Marcel Halamka
email: maacek1@seznam.cz
discord: Kronos#8011
"""
import requests
from bs4 import BeautifulSoup
import csv
import sys

def get_valid_url_and_csv() -> str:
    """
    Tato funkce zkontroluje zda-li byly zadány správné argumenty
    pro spuštění kodu a pokud ano tak vrací url se kterým budu
    dále pracovat
    """
    if len(sys.argv) != 3:
        print("Zadejte prosím dva argumenty")
        sys.exit(1)
    url = sys.argv[1]
    csv_file = sys.argv[2]
    if url != "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105" or csv_file != "vysledky_volby.csv":
        print("Zadali jste neplatné argumenty. Správná URL je: 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=10&xnumnuts=6105' a správný \
              název CSV souboru je: 'vysledky_volby.csv'.")
        sys.exit(1)
    return url

def get_soup(url: str) -> BeautifulSoup:
    """
    Vytvořím url adresy soup, kterou pak použiju při
    scrapování dat
    """
    odpoved_serveru = requests.get(url)
    soup = BeautifulSoup(odpoved_serveru.text, "html.parser")
    return soup

def main_data(soup: BeautifulSoup) -> list:
    """
    Tato obrovská funkce vyhledá a scrapuje data z mé url stránky.Hlavičku
    jsem psal ručně, ale pokud by byla delší, vyscrapoval bych ji.Poté se ukládá
    každý element do listu my_list který až se na konci každého cyklu naplní, provede se
    pomocí .append uložení do main_listu a list se vyprázdní aby se mohl v dalším
    cyklu opět znovu plnit. A main_list se nakonec použije na převod do CSV
    souboru. List hlavicka už jsem uložil na první místo main_listu.
    """
    numbers = soup.find_all(class_="cislo")
    okrsky = soup.find_all(class_="overflow_name")
    links = soup.find_all("a")
    cislo = 0

    hlavicka = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy", "Občanská demokratická strana",
                "Řád národa - Vlastenecká unie", "CESTA ODPOVĚDNÉ SPOLEČNOSTI", "Česká str.sociálně demokrat.", "Radostné Česko",
                "STAROSTOVÉ A NEZÁVISLÍ", "Komunistická str.Čech a Moravy", "Strana zelených",
                "ROZUMNÍ-stop migraci,diktát.EU", "Strana svobodných občanů",
                "Blok proti islam.-Obran.domova", "Občanská demokratická aliance", "Česká pirátská strana",
                "Referendum o Evropské unii",
                "TOP 09", "ANO 2011", "SPR-Republ.str.Čsl. M.Sládka", "Křesť.demokr.unie-Čs.str.lid.",
                "Česká strana národně sociální",
                "REALISTÉ", "SPORTOVCI", "Dělnic.str.sociální spravedl.", "Svob.a př.dem.-T.Okamura (SPD)",
                "Strana Práv Občanů"]
    main_list = [hlavicka]
    for link in links[5:-2:2]:
        my_list = []
        href = "https://volby.cz/pls/ps2017nss/" + link.get("href")
        odpoved_serveru2 = requests.get(href)
        soup2 = BeautifulSoup(odpoved_serveru2.text, "html.parser")
        my_list.append(numbers[cislo].getText())
        my_list.append(okrsky[cislo].getText())
        registred = soup2.find(class_="cislo", headers="sa2")
        my_list.append(registred.get_text().replace('\xa0', ' '))
        envelopes = soup2.find("td", headers="sa3").getText()
        my_list.append(envelopes.replace('\xa0', ' '))
        valid = soup2.find(class_="cislo", headers="sa6").getText()
        my_list.append(valid.replace('\xa0', ' '))
        all_tr = soup2.find_all(class_="cislo", headers="t1sa2 t1sb3")
        all_tr2 = soup2.find_all(class_="cislo", headers="t2sa2 t2sb3")
        for one_tr in all_tr:
            soucet_strany = one_tr.getText().replace('\xa0', ' ')
            my_list.append(soucet_strany)

        for one_tr2 in all_tr2:
            soucet_strany2 = one_tr2.getText().replace('\xa0', ' ')
            my_list.append(soucet_strany2)
        cislo += 1
        main_list.append(my_list)

    return main_list

def save_to_csv(data: list, csv_file: str) ->str:
    """
    Tato funkce ukládá data do tabulky csv souboru kdy díky delimiter(",")
    se odděluje vše čárkou
    """
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(data[0])
        for row in data[1:]:
            writer.writerow(row)
    print("Data byla úspěšně zapsána do CSV souboru.")

def main():
    """
    Hlavní funkce která spouští postupně všechny funkce výše uvedené
    """
    url = get_valid_url_and_csv()
    soup = get_soup(url)
    data = main_data(soup)
    csv_file = "vysledky_volby.csv"
    save_to_csv(data, csv_file)

if __name__ == "__main__":
    main()