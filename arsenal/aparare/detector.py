import sys
import argparse
import json
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


# B1 & B2. suspecti() cu valoare implicita si validare prin raise
def suspecti(counts, prag=10):
    """
    Determina adresele IP care depasesc un anumit prag de esecuri.
    
    :param counts: Counter sau dict cu frecventa esecurilor per IP
    :param prag: int - Numarul minim de esecuri pentru ca o adresa sa fie suspecta
    :return: list - Tupluri (ip, count) sortate descrescator
    """
    # Validare: pragul trebuie sa fie cel putin 1
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    
    # Filtram si sortam descrescator dupa numarul de incercari (valoare)
    rezultate = [(ip, count) for ip, count in counts.items() if count >= prag]
    rezultate.sort(key=lambda x: x[1], reverse=True)
    return rezultate



# B3. argparse si raportul JSON
def main():
    p = argparse.ArgumentParser(description="Detector de atacuri brute force")
    p.add_argument("log", help="Calea catre fisierul auth.log")
    p.add_argument("--prag", type=int, default=10, help="Pragul de esecuri (implicit 10)")
    p.add_argument("--json", action="store_true", help="Format de iesire JSON")
    
    a = p.parse_args()
    
    # Procesarea datelor
    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)
    
    if a.json:
        # Constructia raportului JSON
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus]
        }
        print(json.dumps(raport, indent=2))
    else:
        # Afisarea rezumatului standard pe ecran
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
            
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
