import csv
"""with open("setting_codes_en_US.csv", newline="") as csvfile:
	spamreader=csv.reader(csvfile)
	for _ in spamreader:
		print(",".join(row))"""

fichier=open("error_codes_en_US.csv", "r", encoding="utf-8")
try:
	reader=csv.reader(fichier, delimiter=",")
	for row in reader:
		print(row[2])
finally:
	fichier.close()