# -*- coding: utf-8 -*-
"""Copy of New_AgendaBuilder_22_9_sat.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1hR4rRcllDP1rJJ0nrB-ZFPraoaj5k93o
"""

! pip install langchain[all]
! pip install langchain_community[all]
! pip install unstructured[all]
! pip install openai[all]
! pip install python-docx
! pip install pdfminer.six
! pip install pillow_heif
! pip install nltk
! pip install spacy
! pip install unstructured_inference
! pip install -U langchain-unstructured
! pip install unstructured
! pip install unstructured[local-inference]
! pip install pdf2image
! pip install pdfminer.six
! apt-get install poppler-utils
! apt-get install tesseract-ocr
!pip uninstall -y nltk
!pip install nltk
! openai migrate
! pip install openai==0.28
# ! pip list

! pip install pdf2image
! pip install pdfminer.six

import re
import json
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain_unstructured import UnstructuredLoader
import openai
import os
from unstructured.partition.docx import partition_docx
from unstructured.partition.doc import partition_doc
from unstructured.partition.xlsx import partition_xlsx
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.email import partition_email
from unstructured.cleaners.core import clean
import nltk
import spacy
nltk.download('words')
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('averaged_perceptron_tagger')
nltk.download('state_union')
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
nlp = spacy.load('en_core_web_sm')

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = 'https://micodefest-oai.openai.azure.com/'  # Your Azure OpenAI resource's endpoint value .
openai.api_key = '3a039447ea0141e08f19fba1024c427d'

def get_completion(text, prompt, model="GPT3516KTEST"):
    messages = [{ "role": "system", "content": text}, {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
    )
    resp = response.choices[0].message["content"]
    return resp

class Agenda_Builder:

    def __init__(self):
        self.file_content=""

    #Extracting contents from pdf
    def extract_text(self,filename):
        try:
            loader=UnstructuredFileLoader(filename)
            docs=loader.load()
            return docs
        except FileNotFoundError:
            print("The file does not exists")


    #Cleaning the extracted contents
    def clean_text(self,filename):
        concatenated_RFP_text_by_category = {}
        file_extension = os.path.splitext(filename)[1].lower()

        if file_extension == '.docx':
            elements = partition_docx(filename=filename)
        elif file_extension == '.doc':
            elements = partition_doc(filename=filename)
        elif file_extension == '.xlsx':
            elements = partition_xlsx(filename=filename)
        elif file_extension == '.pdf':
            elements = partition_pdf(filename)
        elif file_extension == '.eml':
            elements = partition_email(filename)
        else:
            raise ValueError("Unsupported file format")

        if ((file_extension == '.docx') or (file_extension == '.doc')):

            for elem in elements:
                category = elem.category
                RFP_text = elem.text
                cleaned_text = clean(RFP_text, extra_whitespace=True, dashes=True)

                if category in concatenated_RFP_text_by_category:
                    concatenated_RFP_text_by_category[category].append(cleaned_text)
                else:
                    concatenated_RFP_text_by_category[category] = [cleaned_text]
                # print(concatenated_RFP_text_by_category)
            for category, RFP_text in concatenated_RFP_text_by_category.items():
                if category in ["Title", "UncategorizedText", "Table"]:
                    concatenated_RFP_text = ' '.join(RFP_text)
                    print(f'Category {category}: {concatenated_RFP_text}')
                    # doc=nlp(concatenated_RFP_text)
                    # sentences=list(doc.sents)
                    # print("--------------Sentences-----------------")
                    # print(sentences)
                    # print("-----------------------------------------")
                    # for token in doc:
                        #print(token.text)
                        #ents=[(e.text,e.start_char,e.end_char,e.label_) for e in doc.ents]
                             #if e.label_ in ["EVENT", "DATE", "TIME"]]
                        #print(ents)
                        #displayc.render(doc,style='ent',jupyter=True)


                    print("\n")

        elif file_extension == '.xlsx':
            for elem in elements:
                category = elem.category
                RFP_text = elem.text
                cleaned_text = clean(RFP_text, extra_whitespace=True, dashes=True)

                if category in concatenated_RFP_text_by_category:
                    concatenated_RFP_text_by_category[category].append(cleaned_text)
                else:
                    concatenated_RFP_text_by_category[category] = [cleaned_text]
    # print(concatenated_RFP_text_by_category)
                for category, RFP_text in concatenated_RFP_text_by_category.items():
                    if category in ["Table"]:
                        concatenated_RFP_text = ' '.join(RFP_text)
                        # doc=nlp(concatenated_RFP_text)
                        # sentences=list(doc.sents)
                        # print(sentences)
                        # for token in doc:
                        #     print(token.text)
                        #     ents=[(e.text,e.start_char,e.end_char,e.label_) for e in doc.ents]
                        #     #if e.label_ in ["EVENT", "DATE", "TIME"]]
                        #     print(ents)

        elif file_extension == '.pdf':
            for elem in elements:
                category = elem.category
                RFP_text = elem.text

                cleaned_text = clean(RFP_text, extra_whitespace=True, dashes=True)

                if category in concatenated_RFP_text_by_category:
                    concatenated_RFP_text_by_category[category].append(cleaned_text)
                else:
                    concatenated_RFP_text_by_category[category] = [cleaned_text]
            print(concatenated_RFP_text_by_category)
            for category, RFP_text in concatenated_RFP_text_by_category.items():
                if category in ["NarrativeText", "UncategorizedText", "Title"]:
                    concatenated_RFP_text = ' '.join(RFP_text)
                #     doc=nlp(concatenated_RFP_text)
                #     sentences=list(doc.sents)
                #     print(sentences)
                #     for token in doc:
                #         #print(token.text)
                #         ents=[(e.text,e.start_char,e.end_char,e.label_) for e in doc.ents]
                        #print(ents)
        return concatenated_RFP_text_by_category

    def ai_prompt(self,cl_text):

        print("-------------------------------------------------------------------------------")

        prompt = """



                    Context and Role:
                    - You are an expert backend event scheduler working at a prestigious hotel.
                    - Your primary responsibility is to meticulously extract event agenda details from unstructured text documents (RFPs) presented in tabular form.
                    - Your commitment is to provide accurate and complete information in a structured JSON format.



                    Output Format:
                    - Generate JSON objects with the following keys for each event: date, day, startTime, endTime, functionType, setupStyle, peopleCount, comments.
                    - Ensure that each JSON object contains all of the specified keys.
                    - Verify that all values are correctly populated.



                    Extraction Requirements:
                    - For every row in the RFP that provides event agenda details, it is imperative to generate a corresponding, accurately formatted row in the JSON output.
                    - Pay meticulous attention to detail, ensuring that no rows from the RFP are missed during extraction.
                    - Never combine multiple rows from the RFP into a single row in the JSON output, and do not permit the division of a single RFP row into multiple JSON rows.
                    - Achieve comprehensive coverage by including all events mentioned in the RFP, regardless of the total number of rows.



                    Specific Date Range Instructions:
                    - If the RFP provides a specific date range (e.g., "Sep 1 2023 - Sep 7 2023"), explicitly create entries for each day within the range. Ensure no days are omitted.
                    - Always format dates as MM/DD/YYYY.



                    Output Structure:
                    - Maintain the JSON output structure consistently, which should always have the following format:
                    {
                        "events": [
                            {
                                "date": "MM/DD/YYYY",
                                "day": "Day of the week",
                                "startTime": "Start time",
                                "endTime": "End time",
                                "functionType": "Event type",
                                "setupStyle": "Setup style",
                                "peopleCount": "Number of people",
                                "comments": "Additional comments"
                            }
                        ]
                    }



                    Comprehensive Coverage Assurance:
                    - Prioritize thoroughness and diligence to ensure no event agenda details are missed. Review the generated JSON output meticulously to confirm that all rows from the RFP are accurately captured.


                    Your role demands the utmost precision. Your task is to meticulously extract event agenda details from tabular
                    RFP text while strictly adhering to the specified guidelines. The resulting JSON output should consistently
                    adhere to the defined structure and content requirements, and all responses should be deterministic with a temperature of 0.
          """
        response = get_completion(cl_text,prompt)

        return response
        #save_file=open("interim_file.json","w")
        #json.dump(response,save_file,indent=6)

    def post_processing(self,res):
        # List of synonyms
        function_types = [
            'Board Meeting', 'Box Lunch', 'Breakfast', 'Breakfast Buffet', 'Breakout', 'Brunch', 'Ceremony', 'Changing Room',
            'Coat Check', 'Cocktail Reception', 'Coffee Break', 'Continental Breakfast', 'Continuous Break', 'Dance', 'Dinner',
            'Dinner Buffet', 'Exhibits', 'General Session', 'Holding Room', 'Hospitality Room', 'In-house Meeting', 'Interview',
            'Lunch', 'Lunch Buffet', 'Meal on Own', 'Meeting', 'Menu Tasting', 'No Agenda Hold', 'Off Site', 'Office', 'Reception',
            'Recreation', 'Registration', 'Rehearsal', 'Room Ready', 'Set Up', 'Speaker Room', 'Special',
            'Storage', 'Teardown',
            'Trade Show'
        ]

        setup_styles = [
            "Chevron Schoolroom", "Chevron Theatre", "Cocktail Rounds", "Conference",
            "Conference 2 per 6", "Conference 3 per 8","Crescent Rounds", "Exhibits",
            "Hollow Square", "Hollow Square 2 per 6", "Hollow Square 3 per 8", "Lounge", "Off Site",
            "Oval Conference", "Registration", "Rounds of 10", "Rounds of 12", "Rounds of 6",
            "Rounds of 8", "Schoolroom", "Schoolroom 2 per 6","Schoolroom 3 per 8", "Special",
            "Storage", "Theatre", "U-Shape", "U-Shape 2 per 6", "U-Shape 3 per 8"
        ]

        # f=open('interim_file.json')
        # data=json.load(f)
        #
        # Create a prompt to find the most identical synonym

        prompt = """

        - For each record in input json, perform ALL of the below

            - Scrutinize functionType and setupStyle for the presence of "24-hour hold" or "registration counters," and ensure that this information is consistently and prominently included in the comments section.

            - If the functionType is specified as "24-hour hold," unconditionally set the endTime to 6:00 PM.

            - If funtionType is not in the given function_types list replace funtionType with the closest value from function_types list.

            - If setupStyle is not in the given setup_styles list replace setupStyle with the closest value from setup_styles list.


            - If there are identifical rows (all key values match) in json, remove duplicates

            Output Structure:
            - Maintain the JSON output structure consistently, which should always have the following format:
            {
                "events": [
                    {
                        "date": "MM/DD/YYYY",
                        "day": "Day of the week",
                        "startTime": "Start time",
                        "endTime": "End time",
                        "functionType": "Event type",
                        "setupStyle": "Setup style",
                        "peopleCount": "Number of people",
                        "comments": "Additional comments"
                    }
                ]
            }

        """

        resp = get_completion(f"""{res}""",prompt)

        # Print the updated response
        print("Updated response:", resp)

def main():
    # filename='Tractor_Supply.xlsx'
    filename='/content/sample_data/Los Angeles Hotel 1183_2024 space addendum_dl.pdf'

    AB=Agenda_Builder()

    pdf_text=AB.extract_text(filename)

    cln_text=AB.clean_text(filename)

    response=AB.ai_prompt(str(cln_text))

  #  print("------------- Extracted Text------------------------------")
    #print(pdf_text)
    #print('\n')
    print("-------------Cleaned Text---------------------------------")
    print(cln_text)
    print('\n')
    print("-------------Prompt Output--------------------------------")
    print(response)
    print('\n')
    print("-------------Post processing------------------------------")
    AB.post_processing(response)

"""**Validating the NLTK Libriry**"""

import nltk

# Download the 'punkt' tokenizer models
nltk.download('punkt')

print(nltk.data.path)

# Set NLTK data path
nltk.data.path.append('/root/nltk_data')

"""**Validating the NLTK Libriry - Word Tokenizer**"""

import nltk

# Download the 'punkt' tokenizer models
nltk.download('punkt')

# Test tokenization
from nltk.tokenize import word_tokenize

text = "Hello, how are you doing today?"
tokens = word_tokenize(text)
print(tokens)

! pip install -U langchain-unstructured
# ! pip uninstall langchain-unstructured

if __name__ == "__main__":
    main()

"""**Verify API Keys and Permissions - Access denied due to Virtual Network/Firewall rules**"""

import openai

# Set your API key
openai.api_key = '3a039447ea0141e08f19fba1024c427d'

# Example request to the OpenAI API
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Translate the following English text to French: 'Hello, how are you?'",
    max_tokens=60
)

print(response.choices[0].text.strip())