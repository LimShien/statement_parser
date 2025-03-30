import pytesseract
from PIL import Image
import csv
import re
from datetime import datetime

# Input file
context = "BOI"
image_path = ".data/bank-statement-2.jpg"
output_file = ".data/output_file.csv"

image = Image.open(image_path)
row_config = r'--oem 3 --psm 6'
# Perform OCR to extract text
extracted_text = pytesseract.image_to_string(image, config=row_config).strip()

# Display extracted text
#print(extracted_text)

lines = extracted_text.split("\n")
transactions = [["Date", "Transaction", "Value"]]

def format_date(date):
  if " " not in date:
     month = re.search(r"[a-zA-Z]{3}",date).group()
     day = re.search(r"\d+", date).group()
     date = day + " "+ month
  return date 

def get_date(line):
  date_pattern = re.compile(r"\b(?:0?[1-9]|[12][0-9]|3[01])\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b") # pattern for date formate 01Jan / 1 JAN
  if re.search(date_pattern,line):
    date = re.search(date_pattern,line).group()
    line = line.replace(date, " ")
    date = format_date(date)
    return date, line
  else:
    return None

def get_value(line):
  value_pattern = re.compile(r"\b([0-9]+.[0-9][0-9])") # pattern for value of transaction 0.00 / 00.00/ 000.00
  value = re.findall(value_pattern,line)[-1].replace(",",".")
  line = line.replace(value, " ")
  return value, line

def writeToCsv(output_file_name, transactions):
  with open(output_file_name, 'w', newline='', encoding='utf-8' ) as file:
    mycsv = csv.writer(file)
    for t in transactions:
      mycsv.writerow(t)


for line in lines:
  # Could not parse date from line, not a proper line ...
  if get_date(line) == None:
    transactions[-1][1] += line
    continue
  else:
    date, line = get_date(line)
    value, line = get_value(line)
    line = line.replace(",", " ").strip() # remove any comma in transaction, for CSV formatting.
    transactions.append([date, line, value])
writeToCsv(output_file, transactions)

""" print(type(transactions))
for transaction in transactions:
  for t in transaction:
    print(t, end="\t")
  print("\n") """