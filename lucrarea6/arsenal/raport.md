## Lucrarea B - Forensics pe fișiere și Steganografie

### B1. Magic Bytes (Tipul Real)
- `probe/foto.jpg`: JPEG (`ff d8`)
- `probe/ascuns.png`: PNG (`89 50 4e 47`)

### B2. Strings
Rularea căutării de secvențe text imprimabile în `probe/ascuns.png` a extras următoarele indicii utile:
- `IHDR`, `IDATx`, `IEND`
- `secret.txtFLAG{ascuns_prin_carving}`
- `secret.txtPK`

### B3. Metadate EXIF și GPS
- Imaginea `probe/foto.jpg` conține bloc EXIF.
- Coordonate GPS extrase:
  - Latitudine: **47.016667**
  - Longitudine: **28.857500**

### B4. File Carving
- Arhiva ZIP a fost detectată la octetul `782` din `probe/ascuns.png` prin căutarea semnăturii `PK\x03\x04`.
- Arhiva extrasă `gasit.zip` conține fișierul `secret.txt`, cu mesajul `FLAG{ascuns_prin_carving}`.

### B5 & B6. Steganografie LSB
- Mesajul a fost ascuns pe canalele RGB din `probe/foto.jpg` și salvat în `stego.png`.
- Mesajul extras cu succes din `stego.png`: `FLAG{ascuns_in_pixeli}`