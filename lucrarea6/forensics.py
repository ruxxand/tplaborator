import re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def tip_real(cale):
    """B1. Identifică tipul real al fișierului după magic bytes."""
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    
    return f"Necunoscut (hex: {cap.hex()})"

def extrage_strings(cale, min_len=4):
    """B2. Extrage secvențele de text imprimabil dintr-un fișier binar."""
    with open(cale, "rb") as f:
        date = f.read()
    
    # Caută caractere ASCII imprimabile (de la spațiu la ~) de lungime min_len
    rezultate = re.findall(rb"[ -~]{" + str(min_len).encode() + rb",}", date)
    return [m.decode('latin-1') for m in rezultate]

def dms_in_grade_zecimale(dms, ref):
    """Convertește coordonatele GPS (grade, minute, secunde) în grade zecimale."""
    grade = float(dms[0])
    minute = float(dms[1])
    secunde = float(dms[2])
    
    zecimal = grade + (minute / 60.0) + (secunde / 3600.0)
    if ref in ['S', 'W']:
        zecimal = -zecimal
    return zecimal

def citește_exif_gps(cale):
    """B3. Extrage metadatele EXIF și coordonatele GPS din imagine."""
    try:
        img = Image.open(cale)
        exif = img._getexif() or {}
    except Exception as e:
        print(f"Eroare la citirea EXIF: {e}")
        return

    print("--- Metadate EXIF ---")
    gps_data = {}
    for tag_id, val in exif.items():
        tag_nume = TAGS.get(tag_id, tag_id)
        if tag_nume == "GPSInfo":
            for gps_tag_id in val:
                sub_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                gps_data[sub_tag] = val[gps_tag_id]
        else:
            print(f"{tag_nume} = {val}")

    if gps_data:
        print("\n--- Date GPS ---")
        lat = dms_in_grade_zecimale(gps_data['GPSLatitude'], gps_data['GPSLatitudeRef'])
        lon = dms_in_grade_zecimale(gps_data['GPSLongitude'], gps_data['GPSLongitudeRef'])
        print(f"Latitudine:  {lat:.6f}")
        print(f"Longitudine: {lon:.6f}")
        print(f"Google Maps Link: https://maps.google.com/?q={lat},{lon}")

def extrage_arhiva_ascunsa(cale_in, cale_out="gasit.zip"):
    """B4. File carving: caută o arhivă ZIP lipită la finalul imaginii și o salvează."""
    with open(cale_in, "rb") as f:
        date = f.read()

    i = date.find(b"PK\x03\x04")
    if i != -1:
        with open(cale_out, "wb") as f_out:
            f_out.write(date[i:])
        print(f"[+] Arhivă ZIP extrasă cu succes de la octetul {i} în '{cale_out}'")
    else:
        print("[-] Nu s-a găsit nicio semnătură de arhivă ZIP.")

if __name__ == "__main__":
    print("=== B1. Tip Real ===")
    print("probe/foto.jpg:", tip_real("probe/foto.jpg"))
    print("probe/ascuns.png:", tip_real("probe/ascuns.png"))

    print("\n=== B2. Strings in ascuns.png ===")
    strings_gasiți = extrage_strings("probe/ascuns.png")
    for s in strings_gasiți[:10]: # afișează primele 10
        print(" >", s)

    print("\n=== B3. EXIF & GPS ===")
    citește_exif_gps("probe/foto.jpg")

    print("\n=== B4. File Carving ===")
    extrage_arhiva_ascunsa("probe/ascuns.png")