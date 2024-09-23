#!/usr/bin/env python3

#Test input: ./summarize_paper_gpt.py -p ~/Documents/BIOL8530/1-s2.0-S0002929715004863-main.pdf

import os 
import PyPDF2 
import re 
from openai import OpenAI
import argparse as ap 
from secrets import ADRIANS_OPENAI_KEY

parser = ap.ArgumentParser(prog = "Summarize Research Papers", description = "Summarize research papers using GPT. Summarizes each page at a time.")
parser.add_argument("-p", "--pdf_path", help="path to pdf file", required=True)
parser.add_argument("-t", "--temp", help="tempature for the GPT model - 0 more conservative, 1 more liberal", type=float, default=0.9)
args = parser.parse_args()

#String that will contain the summary 
pdf_summary = ""

#Path to the PDF file requiring summarization 
pdf_file_path = args.pdf_path 

#Open pdf using PyPDF2 library 
pdf_file = open(pdf_file_path, "rb")

#Read pdf 
pdf_reader = PyPDF2.PdfReader(pdf_file) 

#Grabbing the api key - Replace this with you OpenAI key
client = OpenAI(api_key=ADRIANS_OPENAI_KEY)

#Loop through the pages in the PDF file, extracting the text and making calls to the GPT api 
for page_num in range(0, len(pdf_reader.pages)):
    #Extract the text from the page 
    page_text = pdf_reader.pages[page_num].extract_text().lower()

    #Make call to GPT 
    #Can edit the content of the user to get more in-depth breakdowns of each page 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful research assistant."}, 
        {"role": "user", "content": f"Summarize this: {page_text}"}],
        temperature=args.temp
    )

    print(response)

    #Extracting the page summary - Do not parse it like a dictionary but like an object being a ChatCompletion object 
    page_summary = response.choices[0].message.content 

    #Adding a newline to the summary 
    page_summary += "\n"

    #Generating a summary txt file and writing the output here 
    #Drop the file extension and add to the results 
    pdf_summary_file = pdf_file_path[:-4] + "_summary.txt"

    with open(pdf_summary_file, "a+") as file:
        file.write(page_summary)

#May want to summarize by section rather than by page 

