
from pathlib import Path
from math import isnan
from pandas import DataFrame, isnull, read_csv, read_excel

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


CONCEPT_INDEX = {'hand': 1, 'left': 2, 'right': 3, 'leg/foot': 4, 'to walk': 5, 'road/path': 6, 'to come': 7, 'to turn (veer to the side, as in turning left)': 8, 'to swim': 9, 'dirty': 10, 'dust': 11, 'skin': 12, 'back (body part)': 13, 'belly': 14, 'bone': 15, 'intestines': 16, 'liver': 17, 'breast': 18, 'shoulder': 19, 'to know, be knowledgeable': 20, 'to think': 21, 'to fear': 22, 'blood': 23, 'head': 24, 'neck': 25, 'hair (of the head)': 26, 'nose': 27, 'to breathe': 28, 'to sniff, smell': 29, 'mouth': 30, 'tooth': 31, 'tongue': 32, 'to laugh': 33, 'to cry': 34, 'to vomit': 35, 'to spit': 36, 'to eat': 37, 'to chew (a: general term; b: chew betel)': 38, 'to cook (a: general term; b: boil food)': 39, 'to drink': 40, 'to bite': 41, 'to suck': 42, 'ear': 43, 'to hear': 44, 'eye': 45, 'to see': 46, 'to yawn': 47, 'to sleep': 48, 'to lie down (to sleep)': 49, 'to dream': 50, 'to sit': 51, 'to stand': 52, 'person/human being': 53, 'man/male': 54, 'woman/female': 55, 'child': 56, 'husband': 57, 'wife': 58, 'mother': 59, 'father': 60, 'house': 61, 'thatch/roof': 62, 'name': 63, 'to say': 64, 'rope': 65, 'to tie up, fasten': 66, 'to sew (clothing)': 67, 'needle': 68, 'to hunt (for game)': 69, 'to shoot (an arrow)': 70, 'to stab, pierce': 71, 'to hit (with stick, club)': 72, 'to steal': 73, 'to kill': 74, 'to die, be dead': 75, 'to live, be alive': 76, 'to scratch (an itch)': 77, 'to cut, hack (wood)': 78, 'stick/wood': 79, 'to split (transitive)': 80, 'sharp': 81, 'dull, blunt': 82, 'to work (in garden, field)': 83, 'to plant': 84, 'to choose': 85, 'to grow (intransitive)': 86, 'to swell (as an abcess)': 87, 'to squeeze (as juice from a fruit)': 88, 'to hold (in the fist)': 89, 'to dig': 90, 'to buy': 91, 'to open, uncover': 92, 'to pound, beat (as rice or prepared food)': 93, 'to throw (as a stone)': 94, 'to fall (as a fruit)': 95, 'dog': 96, 'bird': 97, 'egg': 98, 'feather': 99, 'wing': 100, 'to fly': 101, 'rat': 102, 'meat/flesh': 103, 'fat/grease': 104, 'tail': 105, 'snake': 106, 'worm (earthworm)': 107, 'louse (a: general term, b: head louse)': 108, 'mosquito': 109, 'spider': 110, 'fish': 111, 'rotten (of food, or corpse)': 112, 'branch (the branch itself, not the fork of the branch)': 113, 'leaf': 114, 'root': 115, 'flower': 116, 'fruit': 117, 'grass': 118, 'earth/soil': 119, 'stone': 120, 'sand': 121, 'water (fresh water)': 122, 'to flow': 123, 'sea': 124, 'salt': 125, 'lake': 126, 'woods/forest': 127, 'sky': 128, 'moon': 129, 'star': 130, 'cloud (white cloud, not a rain cloud)': 131, 'fog': 132, 'rain': 133, 'thunder': 134, 'lightning': 135, 'wind': 136, 'to blow (a: of the wind, b: with the mouth)': 137, 'warm (of weather)': 138, 'cold (of weather)': 139, 'dry (a: general term, b: to dry up)': 140, 'wet': 141, 'heavy': 142, 'fire': 143, 'to burn (transitive)': 144, 'smoke (of a fire)': 145, 'ash': 146, 'black': 147, 'white': 148, 'red': 149, 'yellow': 150, 'green': 151, 'small': 152, 'big': 153, 'short (a: in height, b: in length)': 154, 'long (of objects)': 155, 'thin (of objects)': 156, 'thick (of objects)': 157, 'narrow': 158, 'wide': 159, 'painful, sick': 160, 'shy, ashamed': 161, 'old (of people)': 162, 'new': 163, 'good': 164, 'bad, evil': 165, 'correct, true': 166, 'night': 167, 'day': 168, 'year': 169, 'when? (question)': 170, 'to hide (intransitive)': 171, 'to climb (a: ladder, b: mountain)': 172, 'at': 173, 'in, inside': 174, 'above': 175, 'below': 176, 'this': 177, 'that': 178, 'near': 179, 'far': 180, 'where? (question)': 181, 'i': 182, 'thou': 183, 'he/she': 184, 'we (a: inclusive, b: exclusive)': 185, 'you': 186, 'they': 187, 'what? (question)': 188, 'who? (question)': 189, 'other': 190, 'all': 191, 'and': 192, 'if': 193, 'how? (question)': 194, 'no, not': 195, 'to count': 196, 'one (1)': 197, 'two (2)': 198, 'three (3)': 199, 'four (4)': 200, 'five (5)': 201, 'six (6)': 202, 'seven (7)': 203, 'eight (8)': 204, 'nine (9)': 205, 'ten (10)': 206, 'twenty (20)': 207, 'fifty (50)': 208, 'one hundred (100)': 209, 'one thousand (1,000)': 210}
    

class AbvdError(Exception):
    pass


class AbvdBot:

    def __init__(self, uname, password):
        self.driver = webdriver.Firefox()
        # Log in to ABVD web interface
        self.driver.get("https://abvd.shh.mpg.de/")
        self.driver.find_element(By.NAME, "user").send_keys(uname)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "login").click()
        #self.driver.implicitly_wait(1) # Yuck
        self.logged_in = True
        self.data_loaded = False


    def load_sheet(self, path):
        path = Path(path)
        if path.suffix == ".csv":
            self.data = read_csv(path, sep=",")
        elif path.suffix == ".tsv":
            self.data = read_csv(path, sep="\t")
        elif path.suffix == ".xlsx":
            self.data = read_excel(path, header=0)
        else:
            raise AbvdError("Don't know how to read {}: suffix not recognised".format(str(path)))
        self.data_loaded = True

    def enter_cognate_codes(self, languages=[], overwrite=False, save_input=False, stop_at=None):
        """Enter cognate codes from spreadsheet into ABVD.
        """
        if not self.data_loaded:
            raise AbvdError("AbvdBot has no data loaded!")
        # First we need to navigate to the subgroup cognacy page,
        # since just going to the page for the cognate ID doesn't seem
        # to display TK
        self.driver.get("https://abvd.shh.mpg.de/edt/austronesian/do_subcognacy.php")
        # Find the TKAN button (lol)
        btn = self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[2]/td/ul/li[1]/a")
        btn.click()
        # Now the box has all the IDs in it we can click the "Begin cognatising!" button
        self.driver.find_element(By.ID, "go").click()
        edited = {}
        # Whew.. now we're on the "Sub-Cognacy Judgements" page.
        for concept, index in CONCEPT_INDEX.items():
            if stop_at == index:
                break
            # "Hand" is the first page, so no need to select from list. God this is hacky lol
            data = self.driver.find_element(By.CLASS_NAME, "data")
            entries = data.find_elements(By.TAG_NAME, "tr")[1:] # Skip header row

            for entry in entries:
                lang_id, lang, form = [tag.text for tag in entry.find_elements(By.TAG_NAME, "td")[:3]]
                if lang in languages:
                    field = entry.find_element(By.TAG_NAME, "input")
                    # Debugging, check we got the right shit
                    print(lang_id, lang, form, concept, field)
                    # Get the cognate code for this language and concept
                    code = self.get_code(concept, lang)
                    if code and field.get_attribute("value") == None:
                        field.send_keys(code)

            # Now all the codes are filled in, save and then load the next concept page
            save = self.driver.find_element(By.ID, "save")
            if save_input:
                save.click() # DANGER DANGER DANGER
            select = Select(self.driver.find_element(By.ID, "word"))
            select.select_by_value(str(index + 1))
            submit = self.driver.find_element(
                By.XPATH,
                "/html/body/table/tbody/tr/td[2]/form[1]/input[2]"
            )
            submit.click()

                
    def get_code(self, concept, language):
        # TODO: remove hardcoding to spreadsheet colnames
        if not self.data_loaded:
            raise AbvdError("No spreadsheet loaded!")
        # God pandas sucks. Why is simple filtering so... baroque?
        cols = self.data[["Language", "Word", "Cognacy"]]
        rows = cols[cols["Language"].isin([language])] 
        rows = rows[rows["Word"].isin([concept])]
        if not rows.empty:
            code = rows["Cognacy"].iloc[0] # There are dups, but they should have the same code
            if not isnan(code):
                return code
        else:
            return False


def run(pw):
    joe_langs = [
        "Tai Nüa 1", "Tai Nüa 2", "Tai Nüa 3", "Tai Nüa 4",
        "Shan", "Southern Thai", "Thai", "Lao", "Tai Dam 1", "Tai Dam 2"
    ]
    bot = AbvdBot("isaac", pw)
    bot.load_sheet("/home/isaac/projects/abvdinput/data/abvd-taikadai-isaac.xlsx")
    bot.enter_cognate_codes(languages=joe_langs, save_input=True)
