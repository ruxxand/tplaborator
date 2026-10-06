import argparse
import base64
import hashlib
import json
import re
from urllib.parse import unquote

# A1. Exemplu demonstrativ Text vs Octeți
def demonstratie_a1():
    s = "Salut"
    b = s.encode()  # bytes
    print(f"Bytes: {b}, primul octet (ASCII): {b[0]}")
    
    # TODO A1: tipareste b.hex() si refa bytes din hex
    h = b.hex()
    print(f"Hex: {h}")
    b_refacut = bytes.fromhex(h)
    print(f"Bytes refacuti din hex: {b_refacut}")


# A2. Recunoaște stratul după formă
def ghici_strat(s):
    # Daca are %xx -> "url"
    if "%" in s:
        return "url"
    # Daca doar 0-9 a-f/A-F si lungime para -> "hex"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    # Daca doar A-Za-z0-9+/= -> "base64"
    if re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"
    return "necunoscut"


# A3. Desface stratul recunoscut
def desfa(s):
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        elif strat == "hex":
            return strat, bytes.fromhex(s)
        elif strat == "url":
            return strat, unquote(s).encode('latin1')
    except Exception:
        pass
    return "necunoscut", s.encode('latin1')


# A4. Verificare dacă un buchet de octeți e text citibil
def citibil(b):
    # True daca toti octetii sunt caractere ASCII imprimabile (32..126)
    return all(32 <= c < 127 for c in b)


def desfa_multistrat(val_initiala):
    val = val_initiala
    straturi_parcurse = []
    
    for _ in range(8):
        strat, b = desfa(val)
        if strat == "necunoscut":
            break
        straturi_parcurse.append(strat)
        if citibil(b):
            return straturi_parcurse, b.decode('latin1')
        try:
            val = b.decode('utf-8')
        except UnicodeDecodeError:
            try:
                val = b.decode('latin1')
            except Exception:
                break
    return straturi_parcurse, val


# A5. Spargi un XOR cu cheie de un octet
def sparge_xor(date_binare):
    for k in range(256):
        clar = bytes(b ^ k for b in date_binare)
        if citibil(clar):
            return k, clar.decode('utf-8', errors='ignore')
    return None, None


# A6. Spargi un hash prin dicționar
def sparge_hash(cale_hashuri="probe/hashuri.txt", cale_wordlist="probe/wordlist.txt"):
    try:
        tinta = open(cale_hashuri).readline().strip()
    except FileNotFoundError:
        return None, None

    lungime = len(tinta)
    algoritm = "md5" if lungime == 32 else ("sha1" if lungime == 40 else "sha256")

    try:
        with open(cale_wordlist, encoding="latin1") as f:
            for linie in f:
                cuv = linie.strip()
                h = getattr(hashlib, algoritm)(cuv.encode()).hexdigest()
                if h == tinta:
                    return tinta, cuv
    except FileNotFoundError:
        pass

    return tinta, None


# A7. argparse și fișa JSON
def main():
    p = argparse.ArgumentParser(description="Decoder universal forensics")
    p.add_argument("intrare", help="Sir de text sau cale catre fisier")
    p.add_argument("--fisier", action="store_true", help="Trateaza intrarea ca fisier binar pentru XOR")
    p.add_argument("--sparge-hash", action="store_true", help="Sparge hash-ul din probe/hashuri.txt")
    a = p.parse_args()

    rezultat_json = {}

    if a.sparge_hash:
        hash_tinta, parola = sparge_hash()
        print(f"[Hash] Tinta: {hash_tinta} -> Parola gasita: {parola}")
        rezultat_json = {"tip": "hash", "hash": hash_tinta, "rezultat": parola}

    elif a.fisier:
        # Citeste octetii din cale
        try:
            date = open(a.intrare, "rb").read()
            cheie, text_clar = sparge_xor(date)
            print(f"[XOR] Cheie gasita: {cheie} (0x{cheie:02x}) -> Text: {text_clar}")
            rezultat_json = {"tip": "xor", "cheie": cheie, "rezultat": text_clar}
        except FileNotFoundError:
            print(f"Eroare: Fisierul {a.intrare} nu exista.")
            return
    else:
        # Trateaza intrarea ca sir
        straturi, rezultat = desfa_multistrat(a.intrare)
        print(f"[Straturi] Decodat prin {straturi} -> Rezultat: {rezultat}")
        rezultat_json = {"strat": straturi, "rezultat": rezultat}

    # Salveaza fisa JSON
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(rezultat_json, f, indent=4, ensure_ascii=False)
    print("Fisa a fost salvata in arsenal/forensics/fisa.json")


if __name__ == "__main__":
    main()