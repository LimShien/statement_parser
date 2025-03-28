import pytesseract
from PIL import Image
import csv
import re
from datetime import datetime

# Load the image
image_path = "../Pictures/bank-statement.jpeg"
image = Image.open(image_path)
row_config = r'--oem 3 --psm 6'
# Perform OCR to extract text
extracted_text = pytesseract.image_to_string(image, config=row_config).strip()

# Display extracted text
#print(extracted_text)

lines = extracted_text.split("\n")
transactions = []
date_pattern = re.compile(r"\b(?:0?[1-9]|[12][0-9]|3[01])\s?(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b") # pattern for date formate 01Jan / 1 JAN
value_pattern = re.compile(r"\b([0-9]+.[0-9][0-9])") # pattern for value of transaction 0.00 / 00.00/ 000.00

def format_date(date):
  if " " not in date:
     month = re.search(r"[a-zA-Z]{3}",date).group()
     day = re.search(r"\d+", date).group()
     date = day + " "+ month
  return date 

for line in lines:
 # print(line)
  date = re.search(date_pattern,line).group()
  date = format_date(date)
    # remove date from line
  line = line.replace(date, " ")
  value = re.findall(value_pattern,line)[-1].replace(",",".")
  line = line.replace(value, " ")
  line = line.strip()
  transactions.append([date, line, value])
  

