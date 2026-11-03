import os
from arsenal.privesc.enum import GTFO, citeste_linii, nume


# B1. Funcție care întoarce MULȚIMEA căilor dintr-un fișier
def cai(fisier):
    return set(citeste_linii(fisier))


def main():
    # Căile către capturi
    cale_baza = os.path.join("arsenal", "privesc", "start", "baza_suid.txt")
    cale_acum = os.path.join("arsenal", "privesc", "start", "suid.txt")

    # B1. Încărcarc mulțimile
    baza = cai(cale_baza)
    acum = cai(cale_acum)

    print("B1. Modul comparare mulțimi:")
    print(f"baza: {len(baza)}  acum: {len(acum)}")
    print("-" * 40)

    # B2. Diferența de mulțimi (ce e în acum, dar NU în bază)
    noi = acum - baza
    print("B2. Diferența de mulțimi:")
    print(f"{len(noi)} SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)
    print("-" * 40)

    # B3. Dicționar de risc și filtrarea fișierelor periculoase
    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]

    print("B3. Filtrul final de risc:")
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
