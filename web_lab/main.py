# Programul principal: main.py
# Student: Ruxanda Cujbă

import csv
import argparse
from datetime import datetime

#exercitiu 44 si 45
print("\nExercitiu 44 & 45")
import webtools
from webtools import get_title, security_headers, DEFAULT_HEADERS, check_paths, site_report

#exercitiu 48
print("\nExercitiu 48")
parser = argparse.ArgumentParser(description="Instrument de analiză și raportare site-uri web.")
parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul site-ului țintă")
args = parser.parse_args()

target_url = args.url

print(f"--- Rulare main.py pentru ținta: {target_url} ---")

# Demonstrație Exercițiul 44 & 47
print("User-Agent folosit (DEFAULT_HEADERS):", DEFAULT_HEADERS)
page_res = webtools.fetch(target_url)
print("Titlul paginii prin webtools:", get_title(page_res.text))

#exercitiu 49
print("\nExercitiu 49")
print("\n--- Generare raport CSV (Exercițiul 49) ---")
paths_to_check = ["/", "/robots.txt", "/sitemap.xml", "/admin"]
check_results = check_paths(target_url, paths_to_check)

with open("report.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["path", "status", "checked_at"])
    
    now_iso = datetime.now().isoformat()
    for path, status in check_results.items():
        writer.writerow([path, status, now_iso])

print("Rezultatele verificării căilor au fost salvate în 'report.csv'.")

#exercitiu 50
print("\nExercitiu 50")
print("\n--- Rulare proiect final (Exercițiul 50) ---")
site_report(target_url)