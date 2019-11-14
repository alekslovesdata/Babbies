from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from baby_names_orm import *
import random

'''
Hi! This is a pretty lazily written script that will generate a first and middle name based on some values you can
configure within the code. There's comments above most lines explaining what they do. 

This was written on Python 3.6 but should be 3.x compatible (probably 2.x also)
You'll need to have SQLAlchemy 

Names were taken from here: https://github.com/hadley/data-baby-names
They were then converted to the baby_names_database.db for easy querying with SQLAlchemy
'''

def syllables(word):
    # counts the syllables of a word - shamelessly stolen from stack
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count

# SQLAlchemy connection stuff
Engine = create_engine('sqlite:///baby_names_database.db')
Session = sessionmaker(bind=Engine)
working_session = scoped_session(Session)
Base.metadata.create_all(Engine)

# initialization for some letter checks in the main loop
vowels = 'aeiouy'
consonants = 'bcdfghjklmnpqrstvwxz'

# change the min and max years as you want, just note the absolute mins and maxes
year_min = 1880  # absolute min 1880
year_max = 2008  # absolute max 2008

# empty string initialization
baby_name = ''

# enter any letters/combination of letters you don't want the first/middle name to end with
unallowable_last_letters = ['k', 'c', 'ch', 'a']

# enter any letter/combination of letters you don't want to ever appear
unallowable_at_all = ['ak', 'ek', 'ac']

# enter any names you never want to see
no_names = ['fill', 'this', 'list', 'with', 'unacceptable', 'name']

# if you want a less common name lower the allowable percentage
# if you don't care set the allowable percentage to 1
allowable_percentage = 1

# the sex of the name per the social security listing
# possible options are 'boy' and 'girl'
sex = 'boy'

# generate 10 names! Change the 10 to something else if you want more or less
for j in range(10):
    baby_name = ''

    # make a first and a middle name - for first only remove 'middle' from the list
    for name in ['first_name', 'middle_name']:
        # picks a random year in the range you chose above
        target_year = random.randint(year_min, year_max)
        record_min = 0

        # set some syllable limits for the names if you're so inclined here
        if name == 'first_name':
            syllable_min = 1
            syllable_max = 100
        else:
            syllable_min = 1
            syllable_max = 100

        syllable_count = 0

        # hyper inefficient loop time!
        for i in range(10000):
            allowable_names = working_session.query(Name).filter(Name.Percent <= allowable_percentage,
                                                                 Name.Year == target_year,
                                                                 Name.Sex == sex)
            skip = random.randint(0, allowable_names.count()-1)

            possible_name = allowable_names[skip].Name.lower()

            syllable_count = syllables(possible_name)
            fail = False

            # Checks if the possible name is in your unacceptable names list
            if possible_name in no_names:
                fail = True

            # Checks if the first letter is a specific letter and fails if so
            # Use this if you dislike alliteration with your last name or just don't
            # like names that start with a specific letter. Comment out otherwise
            if possible_name[0] == 'c':
                fail = True

            # Checks if the last letters are unacceptable per the list defined above
            for thing in unallowable_last_letters:
                if possible_name[-len(thing):] == thing:
                    fail = True

            # Checks if specific unallowable strings exist in the name
            for thing in unallowable_at_all:
                if thing in possible_name:
                    fail = True

            # No double names!
            if possible_name in baby_name:
                fail = True

            # Some "flow" rules for the middle name in here
            if name == 'middle_name':
                # if the first letter of the middle name is the first letter of the first name, fail
                # (Can you tell I don't love alliteration?)
                if possible_name[0] == first_name[0]:
                    fail = True

                # If the last letter of the first name is a vowel and the first letter of the middle name is a vowel
                # we fail the name. This was a bit of a test, trying to prevent awkward sounding full names
                if first_name[-1] in vowels and possible_name[0] in vowels:
                    fail = True

                # if the last two letters of the first name are the same as the last two of the middle name - fail
                # another attempt at preventing awkward sounding names
                if first_name[-2:] == possible_name[-2:]:
                    fail = True

            # if we've made it through all of those weird checks - we just need to make sure the syllable count
            # is within range if it is, we've found a name!
            if fail is False:
                if syllable_count >= syllable_min and syllable_count <= syllable_max:
                    break
        if name == 'first_name':
            first_name = possible_name
        baby_name += possible_name[0].upper() + possible_name[1:] + ' '

    print(baby_name + 'LAST_NAME_HERE\n')
