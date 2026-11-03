import sys
import re
from collections import Counter


# LUCRAREA A (nucleu). parse_auth.py: scoate si numara esecurile

# Expresie regulata furnizata pentru identificarea liniilor de esec SSH
TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")



# A1. Scheletul si functia care intoarce o fisa (20 min)
def esec(linie):
    """
    Caută dacă o linie din log reprezintă un eșec de autentificare.
    
    :param linie: str - O linie de text din fisierul auth.log
    :return: tuple (user, ip) daca linia contine un esec, altfel None
    """
    m = TIPAR.search(linie)
    
    # Daca m este None (linia nu contine un esec), intoarce None
    if m is None:
        return None
    
    # Altfel, intoarce un tuplu format din utilizator si IP (m.group(1), m.group(2))
    return (m.group(1), m.group(2))



# A2. Lista de esecuri, robusta la randuri stricate (20 min)
def citeste_esecuri(cale):
    """
    Parcurge fisierul de jurnal si strange fisele (user, ip) intr-o lista de dictionare.
    Ignora liniile invalide si trateaza situatia in care fisierul nu exista.
    
    :param cale: str - Calea catre fisierul auth.log
    :return: list - Lista de dictionare de forma [{"user": ..., "ip": ...}]
    """
    esecuri = []
    
    # Tratarea exceptiei pentru fisier lipsa
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    
    # Bloc with pentru inchiderea automata a fisierului
    with f:
        for linie in f:
            r = esec(linie)
            # Daca r nu este None (exista un esec valid), adauga un dictionar in lista
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
                
    return esecuri



# A3. Numararea pe IP: o functie cu return (18 min)
def pe_ip(esecuri):
    """
    Calculeaza frecventa esecurilor grupate dupa adresa IP.
    
    :param esecuri: list - Lista de dictionare obtinuta de la citeste_esecuri
    :return: Counter - Un obiect Counter cu numarul de esecuri per IP
    """
    # Intoarce un Counter al adreselor din esecuri
    return Counter(e["ip"] for e in esecuri)



# A4. Rezumatul (12 min)
def main():
    """
    Functia principala care leaga intreaga conducta de date (pipeline):
    citeste log-ul, numara esecurile si tipareste rezumatul.
    """
    # Preia calea din argumentele CLI daca exista, altfel foloseste calea implicita din laborator
    cale_fisier = sys.argv[1] if len(sys.argv) > 1 else "arsenal/aparare/start/auth.log"
    
    # Pasul 1: Citirea esecurilor
    esecuri = citeste_esecuri(cale_fisier)
    
    # Pasul 2: Numararea pe IP-uri
    counts = pe_ip(esecuri)
    
    # Pasul 3: Afisarea rezultatelor
    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


# Punctul de intrare in script
if __name__ == "__main__":
    main()
