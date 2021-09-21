import string
import pandas

from difflib import get_close_matches
from pandas import DataFrame, isnull

from pyglottolog import Glottolog
from cldfbench import catalogs
from selenium import webdriver

NAME = "Isaac Stead"
EMAIL = "isaac_stead@eva.mpg.de"
AUTHOR = "Dr. Pittayawat Pittayaporn (Joe)"

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def fill_language(driver, data, glottolog, lang_code):
    # First we need to get a language page with the right ID etc, so need to go
    # through the "Step 1: create" page
    driver.get("https://abvd.shh.mpg.de/austronesian/webedit.php?do=create")
    next_but = driver.find_element_by_xpath("/html/body/div/div[4]/form/p/input[1]")
    next_but.click() # Now we're on the entry page
    
    # Enter the language data. First, retrieve the fields we need...
    fields = [
        driver.find_element_by_name("language"),
        driver.find_element_by_name("author"),
        driver.find_element_by_name("ename"),
        driver.find_element_by_name("email"),
        driver.find_element_by_name("notes"),
    ]

    # Deal with the dialect codes Joe added
    if lang_code[-1] in string.digits:
        dialect_n = lang_code[-1]
        iso_code = lang_code[:3]
    else:
        iso_code = lang_code
        dialect_n = ""

    # Why is pyglottolog so SLOW when looking up by isocodes? 100% of one CPU core for 2 min
    languoid = glottolog.languoid(iso_code)

    # Fill in the language fields
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
    tables = [t for t in driver.find_elements_by_class_name("data")][1:]

    # Get rows, filtering headers
    rows = []
    for table in tables:
        rows.extend(table.find_elements_by_tag_name("tr")[1:])

    count = 0
    missed = []
    for row in rows:
        # Get gloss to use for lookup
        n, concept = [el.text.lower() for el in row.find_elements_by_tag_name("td")[:2]]
        # Get input fields
        item_field, annot_field, cognacy_field = row.find_elements_by_tag_name("input")
        # Lookup gloss in data for this language
        dfrow = data.query("DOCULECT == '{}' and CONCEPT == '{}'".format(lang_code, concept.lower()))

        # Sometimes there are two different entries for the same concept in a doculect... fuck
        # Fill out the fields, putting dups in same field as discussed with Mary
        if not dfrow.empty:
            items = ", ".join([s for s in dfrow["IPA"].tolist()])
            notes = [s for s in dfrow["NOTE"].tolist() if not isnull(s)]
            item_field.send_keys(items)
            count += 1
            if notes:
                annot_field.send_keys(", ".join(notes))
        else:
            missed.append(concept)

    data_concepts = data["CONCEPT"].tolist()

    maybe_matches = {}
    for con in missed:
        # Suggest similar concept glosses for ones we couldn't match
        close_matches = get_close_matches(con, data_concepts, cutoff=0.7)
        substring_matches = [s for s in data_concepts if con in s]
        maybe_matches[con] = set(close_matches + substring_matches)
        
    for con, mats in maybe_matches.items():
        print("Missed {}; Close matches are {}".format(con, mats))

    print("Entered {} forms out of {}, missed {}".format(
        count,
        len(data.query("DOCULECT == '{}'".format(lang_code))),
        len(missed)
    ))

        
if __name__ == "__main__":
    driver = webdriver.Firefox()
    data = pandas.read_csv("~/Projects/abvdinput/SWTclassification.tsv", sep="\t")
    glottolog = Glottolog(catalogs.Glottolog.default_location())

    fill_language(driver, data, glottolog, "tdd1")
