import argparse
import json
import os


GTFO = {
    "find",
    "vim.basic",
    "vim",
    "nmap",
    "cp",
    "bash",
    "less",
    "awk",
    "python3",
    "perl",
}


# A1: Citirea liniilor curate din fișier
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        linii = [linie.strip() for linie in f]
        return [linie for linie in linii if linie and not linie.startswith("#")]


# A2: Extragerea numelui binarului din cale
def nume(cale):
    return cale.rsplit("/", 1)[-1]


# A3: Construirea constatărilor SUID (listă de dicționare)
def suid_constatari(cale):
    cai = citeste_linii(cale)
    cai_unice = sorted(set(cai))
    return [
        {
            "cale": c,
            "nume": nume(c),
            "risc": "mare" if nume(c) in GTFO else "normal",
        }
        for c in cai_unice
    ]


# A4: Procesarea drepturilor sudo (tuplu și dicționar)
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
        u_clean = user.strip()
        d_clean = drept.strip()
        out.append(
            {
                "user": u_clean,
                "drept": d_clean,
                "risc": "mare" if "NOPASSWD" in d_clean else "normal",
            }
        )
    return out


# Procesarea sarcinilor cron
def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        out.append({"user": user, "comanda": comanda, "risc": "normal"})
    return out


# Gruparea tuturor constatărilor într-un singur dicționar
def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


# A5: Funcția principală și generarea raportului
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    # PASUL A1
    cai_suid_raw = citeste_linii(os.path.join(a.capturi, "suid.txt"))
    print("A1. linii SUID:", len(cai_suid_raw))

    # PASUL A2
    nume_unice = {nume(c) for c in cai_suid_raw}
    print("A2. SUID distincte:", len(nume_unice))

    # PASUL A3
    mari_suid = [c for c in raport["suid"] if c["risc"] == "mare"]
    print(f"A3. {len(raport['suid'])} SUID, {len(mari_suid)} cu risc mare")
    print("   ", sorted(c["nume"] for c in mari_suid))

    # ASUL A4
    mari_sudo = [c for c in raport["sudo"] if c["risc"] == "mare"]
    mari_cron = [c for c in raport["cron"] if c["risc"] == "mare"]
    print(f"A4. sudo gasite: {len(raport['sudo'])} ({len(mari_sudo)} cu risc mare)")
    print(f"    cron gasite: {len(raport['cron'])} ({len(mari_cron)} cu risc mare)")

    print("-" * 40)

    # PASUL A5
    print("A5. Rezumat pe categorii (Raport final):")
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"   {categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    useri_sudo = {item["user"] for item in raport["sudo"]}
    useri_cron = {item["user"] for item in raport["cron"]}
    utilizatori = sorted(useri_sudo | useri_cron)

    print(f"   utilizatori implicati: {', '.join(utilizatori)}")

    with open("enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("   Raport salvat in enum.json")


if __name__ == "__main__":
    main()
