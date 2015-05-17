#!/usr/bin/env python
#
# Task 04: Develop a program that does a
# bruteforce attack to find the password
# of a password protected ZIP file.
#
#    You can use the -m option to set the level
# of the attack: the default is zero and it will
# just try the words that are in the file. The
# level one also try some variations of these
# words and the level two will also try some
# combinations of these words and variations.
#
# Authors: Alex Silva Torres, RA 161939
#          Hilder Vitor Lima Pereira, RA 161440

import zipfile
import optparse
import itertools
from random import randint


class InvalidZip(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def bf_extract(zfile, password):
    res = True
    is_zip = zipfile.is_zipfile(zfile)
    if is_zip:
        zip = zipfile.ZipFile(zfile)
        try:
            zip.setpassword(password)
            zip.extractall()
        except:
            res = False
        finally:
            zip.close()
    else:
        raise InvalidZip("invalid zip file: " + zfile)

    return res


def try_word(word, zip_file):
    try:
        if bf_extract(zip_file, word):
            print "The password is " + word
            return True
        return False
    except InvalidZip:
        return False


def find_password(list_file, zip_file, mode):
    words = list_words(list_file)

    if words:
        if mode == 0:
            find_password_simple(words, zip_file)
        elif mode == 1:
            find_password_with_variations(words, zip_file)
        elif mode == 2:
            find_password_with_combinations(words, zip_file)


def list_words(list_file):
    words = []
    try:
        file = open(list_file)

        while True:
            line = file.readline()
            line = line[:-1]

            if not line:
                break

            words.append(line)

        return words

    except IOError:
        return False


def find_password_simple(words, zip_file):
    for word in words:
        try:
            found = try_word(word, zip_file)

            if found:
                return True

        except InvalidZip:
            return False

    return found


#   Mode 1
#   This function try some variations of the words inside the list_file as
# passwords for the zip_file.
#        I - try uppercased versions of the words
#        II - try lowercased versions of the words
#        III - try change just some letters to uppercase
#        IV - try replace some letters by another symbols (as E by 3, or k by |<, etc)
variations = []


def find_password_with_variations(words, zip_file):
    for word in words:
        # try all letters in uppercase
        found = try_uppercase(word, zip_file)
        if not found:
            found = try_lowercase(word, zip_file)
        if not found:
            found = try_some_uppercase(word, zip_file)
        if not found:
            found = try_simple_replacements(word, zip_file)
            simple_replacements = variations[-1]
        if not found:
            found = try_more_replacements(word, zip_file)
        if not found:
            found = try_more_replacements(simple_replacements, zip_file)
        if found:
            return True
    return False


# try all letters in uppercase
def try_uppercase(word, zip_file):
    up = word.upper()
    if not word.isupper():
        variations.append(up)
    return try_word(up, zip_file)


# try all letters in lower
def try_lowercase(word, zip_file):
    lower = word.lower()
    if not word.islower():
        variations.append(lower)
    return try_word(lower, zip_file)


# try first letters uppercase
def try_some_uppercase(word, zip_file):
    title = word.title()
    if not word.istitle():
        variations.append(title)
    return try_word(title, zip_file)


# try replace some chars (for example: teste --> t3st3)
def try_simple_replacements(word, zip_file):
    variations.append(word.replace("o", "0").replace("A", "4").replace("l", "1").replace("e", "3").replace("E", "3"))
    return try_word(variations[-1], zip_file)


# try replace some chars
def try_more_replacements(word, zip_file):
    variations.append(word.replace("k", "|<").replace("P", "|>").replace("p", "|>").replace("S", "5").replace("s", "5"))
    return try_word(variations[-1], zip_file)


#   Mode 2
#   This function try some combinations of the words and their variations as
# passwords for the zip_file.
#        I - try some sequences of words separated by white spaces
#        II - try some sequences of words separated by underscore
#        III - try just the first letters of each word in these sequences
#        IV - try concatenate the words and theirs variations with some numbers (as years, birthdays, etc)
def find_password_with_combinations(words, zip_file):
    words_and_variations = words + variations
    # Combining with some years
    if try_concat_years(words_and_variations, zip_file):
        return True

    # Combining with some birthdays
    if try_concat_birthdays(words_and_variations, zip_file):
        return True
    # try to combine the words the variations
    list1 = words + variations
    list2 = itertools.chain(words, variations)
    # Combining amoung themselves
    for word0 in words_and_variations:
        for word1 in list1:
            # using two words
            if try_phrase_and_first_letters(word0 + " " + word1, zip_file):
                return True
            if try_word(word0 + "_" + word1, zip_file):
                return True
            for word2 in list2:
                # using three words
                phrase = word0 + " " + word1 + " " + word2
                if try_phrase_and_first_letters(phrase, zip_file):
                    return True
                if try_word(word0 + "_" + word1 + "_" + word2, zip_file):
                    return True

    return False


# try the received phrase and also a word with the initial letter of each word of this phrase.
#   For example:  if phrase == "This is my Password", then it tries "TIMP" too
#                 if phrase == "Dad's name", then it tries "DN" too
def try_phrase_and_first_letters(phrase, zip_file):
    if try_word(phrase, zip_file):
        return True
    first_letters = [i[0].upper() for i in phrase.split()];
    if try_word("".join(first_letters), zip_file):
        return True
    return False


def try_concat_years(list_words, zip_file):
    for word in list_words:
        for year in range(1980, 2016):
            if try_word(word + str(year), zip_file):
                return True
            if try_word(str(year) + word, zip_file):
                return True

    return False


def try_concat_birthdays(list_words, zip_file):
    for month in range(1, 12):
        for day in range(1, 31):
            for year in range(1975, 2000):
                if randint(0, 9) == 7:
                    bday = str(month) + "-" + str(day) + "-" + str(year)
                    for word in list_words:
                        if try_word(word + bday, zip_file):
                            return True
                        if try_word(bday + word, zip_file):
                            return True
    return False


##########################
#       main function
##########################
def main():
    p = optparse.OptionParser("usage: %prog -l <dic name> -f <zip name> [-m <integer>(0, 1, 2)]")
    p.add_option('-l', help="Filename of the dictionary is required",
                 dest="list_file")
    p.add_option('-f', help="Filename of the zip is required",
                 dest="zip_file")
    p.add_option('-m', help="Mode of operation should be a integer:"+
                            "0 -> default: just try the words in the file (fast) 1 "+
                            "-> try some variations of the words 2 "+
                            "-> try several variations and combinations of the words (expensive) ",
                    type="int", dest="mode")

    options, arguments = p.parse_args()

    if not options.list_file or not options.zip_file:
        p.print_usage()
        return

    if options.mode in range(0,2):
        find_password(options.list_file, options.zip_file, options.mode)
    else:
        p.print_usage()
        return


if __name__ == "__main__":
    main()
