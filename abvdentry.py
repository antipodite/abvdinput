import string

import pandas
from numpy import isnan
from pandas import DataFrame
from pyglottolog import Glottolog
from selenium import webdriver

NAME = "Isaac Stead"
EMAIL = "isaac_stead@eva.mpg.de"
AUTHOR = "Pittayawat Pittayaporn (Joe)"

# Load classification spreadsheet
DATA = pandas.read_csv("~/Projects/abvdinput/SWTclassification.tsv", sep="\t")

# Webdriver setup
BROWSER = webdriver.Firefox()
creation_page = 

def get_new_language_page():
    BROWSER.get("https://abvd.shh.mpg.de/austronesian/webedit.php?do=create")
    next_but = 

def fill_set_data(page, lang_code):
        # Retrieve the fields we need
    fields = [
        page.find_element_by_name("language"),
        page.find_element_by_name("author"),
        page.find_element_by_name("ename"),
        page.find_element_by_name("email"),
        page.find_element_by_name("notes"),
    ]
    # Retrieve name of language
    glottolog = Glottolog("/Users/isaac_stead/Projects/github/glottolog")

    if lang_code[-1] in string.digits:
        dialect_n = lang_code[-1]
        lang_code = lang_code[:3]
    else:
        dialect_n = ""

    languoid = glottolog.languoid(lang_code)

    # Fill in the fields
    field_data = [
        " ".join([languoid.name, dialect_n]),
        AUTHOR,
        NAME,
        EMAIL,
        "\n".join(["Glottocode: " + languoid.glottocode, "iso code: " + languoid.iso_code])
    ]
    for field, datum in zip(fields, field_data):
        field.send_keys(datum)
        
    # Filter non-entry tables
    tables = [t for t in page.find_elements_by_class_name("data")][1:]
    # Get rows, filtering headers
    rows = []
    for table in tables:
        rows.extend(table.find_elements_by_tag_name("tr")[1:])

    for row in rows:
        # Get gloss to use for lookup
        n, concept = row.find_elements_by_class_name("td")[:2]
        # Get input fields
        item_field, annot_field, cognacy_field = row.find_elements_by_class_name("input")
        # Lookup gloss in data for this language
        dfrow = DATA.query("DOCULECT == lang_code and CONCEPT == concept")
        # Fill out the fields
        item_field.send_keys(dfrow.IPA[0])
        if not isnan(dfrow.NOTE):
            item_field.send_keys(dfrow.NOTE[0])
        
if __name__ == "__main__":
    fill_language_info("tdd1")
