from PIL import Image

def ascunde_mesaj_lsb(cale_img, mesaj, cale_out="stego.png"):
    """B5. Ascunde un mesaj prin LSB în pixelii imaginii."""
    img = Image.open(cale_img).convert("RGB")
    px = list(img.getdata())

    # Adăugăm un octet NULL (b'\x00') la final pentru a cunoaște oprirea la citire
    mesaj_complet = mesaj + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_complet)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul este prea lung pentru această imagine!")

    px_noi = []
    bit_idx = 0

    for r, g, b in px:
        canale = [r, g, b]
        for i in range(3):
            if bit_idx < len(biti):
                # Înlocuiește LSB-ul (ultimul bit) cu bitul din mesaj
                canale[i] = (canale[i] & ~1) | int(biti[bit_idx])
                bit_idx += 1
        px_noi.append(tuple(canale))

    img_stego = Image.new(img.mode, img.size)
    img_stego.putdata(px_noi)
    img_stego.save(cale_out)
    print(f"[+] Mesaj ascuns cu succes în '{cale_out}'")

def dezvaluie_mesaj_lsb(cale_stego):
    """B6. Extrage mesajul ascuns LSB din imagine."""
    img = Image.open(cale_stego).convert("RGB")
    px = list(img.getdata())

    biti = []
    for r, g, b in px:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))

    # Grupează biții câte 8
    octeti = bytearray()
    for i in range(0, len(biti), 8):
        grup_8 = "".join(biti[i:i+8])
        if len(grup_8) < 8:
            break
        val = int(grup_8, 2)
        if val == 0:  # Delimitatorul de final de mesaj
            break
        octeti.append(val)

    return octeti.decode("utf-8", errors="ignore")

if __name__ == "__main__":
    # B5: Ascundere
    mesaj_secret = b"FLAG{ascuns_in_pixeli}"
    ascunde_mesaj_lsb("probe/foto.jpg", mesaj_secret, "stego.png")

    # B6: Dezvăluire
    mesaj_gasit = dezvaluie_mesaj_lsb("stego.png")
    print(f"[+] Mesaj dezvăluit: {mesaj_gasit}")