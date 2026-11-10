from dataclasses import dataclass, asdict
import json

# Definirea constantelor de verificare
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}

# A1 & A2. Clasa Proces
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        # TODO completat: Întoarce True dacă oricare din CAI_SUSPECTE se află în self.cale
        return any(cale_suspecta in self.cale for cale_suspecta in CAI_SUSPECTE)

# A3. Clasa Eveniment
@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self):
        # TODO completat: Întoarce True dacă self.id e în SUSPECTE_ID SAU self.nivel == "critical"
        return self.id in SUSPECTE_ID or self.nivel.lower() == "critical"

# A4. Încarcă procesele din JSON
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        # TODO completat: despachetează fiecarui dicționar în obiect Proces
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]


# --- Testare / Rulare conform etapelor A1 - A4 ---
if __name__ == "__main__":
    # Test A1 & A2
    p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
    print(p.pid, p.nume)
    print(p)
    print(p.e_suspect())
    
    print("-" * 50)

    # Test A4 - Încărcare din JSON
    cale_procese = "arsenal/windows/start/procese.json"
    procese = procese_din_json(cale_procese)
    print("procese:", len(procese))
    print("suspecte:", sum(1 for p in procese if p.e_suspect()))
    
    
    
from dataclasses import dataclass, asdict
import json
import sys

# Definirea constantelor de verificare
CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")
SUSPECTE_ID = {4625, 1102, 7045}

# A1 & A2. Clasa Proces
@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self) -> bool:
        return any(cale_suspecta in self.cale for cale_suspecta in CAI_SUSPECTE)

# A3. Clasa Eveniment
@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self) -> bool:
        return self.id in SUSPECTE_ID or self.nivel.lower() == "critical"

    def explica(self) -> str:
        """Opțional (Ex. 2): oferă o explicație scurtă pentru ID-urile cunoscute."""
        explicatii = {
            4625: "Brute force / Logon eșuat",
            1102: "Jurnal de securitate șters",
            7045: "Serviciu nou instalat"
        }
        return explicatii.get(self.id, "Eveniment critic/suspect")

# A4. Funcții ajutătoare pentru JSON
def procese_din_json(cale: str) -> list[Proces]:
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

def evenimente_din_json(cale: str) -> list[Eveniment]:
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]

# B1 & B2. Clasa Inventar
@dataclass
class Inventar:
    procese: list[Proces]

    @classmethod
    def din_json(cls, cale: str):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])

    def __len__(self) -> int:
        return len(self.procese)

    def suspecte(self) -> list[Proces]:
        return [p for p in self.procese if p.e_suspect()]

    def pe_user(self) -> dict[str, list[str]]:
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat

    def scor(self, evenimente: list[Eveniment] = None) -> int:
        """Opțional (Ex. 3): dă un număr total de risc."""
        evenimente_suspecte = sum(1 for e in (evenimente or []) if e.e_suspect())
        return len(self.suspecte()) + evenimente_suspecte


# B3. Raportul din terminal / CLI
def main():
    import argparse
    p = argparse.ArgumentParser(description="Inventar procese și evenimente Windows")
    p.add_argument("capturi", help="Folderul cu fișierele JSON de start")
    p.add_argument("--json", action="store_true", help="Afișează raportul în format JSON")
    a = p.parse_args()

    cale_proc = a.capturi.rstrip("/\\") + "/procese.json"
    cale_ev = a.capturi.rstrip("/\\") + "/evenimente.json"

    inv = Inventar.din_json(cale_proc)
    ev = evenimente_din_json(cale_ev)
    alarma = [e for e in ev if e.e_suspect()]

    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in inv.suspecte()],
            "evenimente_alarma": [asdict(e) for e in alarma]
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(inv.suspecte())}")
        for p in inv.suspecte():
            print(f"  [{p.pid}] {p.nume:<12} ({p.user})  {p.cale}")
        
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()