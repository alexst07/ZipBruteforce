#!/usr/bin/env python
#
# Task 04: Develop a program that does a
# bruteforce attack to find the password
# of a password protected ZIP file.
#
# Authors: Alex Silva Torres, RA 161939
#          Hilder Vitor Lima Pereira, RA 161440

import zipfile
import optparse

class InvalidZip(Exception):
     def __init__(self, value):
         self.value = value

     def __str__(self):
        return repr(self.value)

def bf_extract(zfile, password):
    res = True
    if (zipfile.is_zipfile(zfile)):
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
    if bf_extract(zip_file, word):
        print "The password is " + word
        return True
    return False
 
def find_password(list_file, zip_file, mode):
    found = find_password_simple(list_file, zip_file)
    if not found and mode > 0:
        found = find_password_with_variations(zip_file)
    if not found and mode > 1:
        found = find_password_with_combinations(list_file, zip_file)
    if not found:
        print "Password not found"


# This function just try the words inside list_file as passwords for the zip_file
words = []
def find_password_simple(list_file, zip_file):
    try:
        file = open(list_file)
        found = False
        while not found:
            line = file.readline()
            line = line[:-1]

            if not line:
                break

            try:
                words.append(line)
                found = try_word(line, zip_file)

            except InvalidZip:
                break
        return found

    except IOError:
        return False

#   This function try some variations of the words inside the list_file as
# passwords for the zip_file.
#        I - try uppercased versions of the words
#        II - try lowercased versions of the words
#        III - try change just some letters to uppercase
#        IV - try replace some letters by another symbols (as E by 3, or k by |<, etc)
variations = []
def find_password_with_variations (zip_file):
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

def find_password_with_combinations (list_file, zip_file):
    print "combinations"
    return False

def main():
    p = optparse.OptionParser("usage: %prog -l <dic name> -f <zip name> [-m <integer>]")
    p.add_option('-l', help="Filename of the dictionary is required",
                 dest="list_file")
    p.add_option('-f', help="Filename of the zip is required",
                 dest="zip_file")
    p.add_option('-m', help="Mode of operation should be a integer:      0 -> default: just try the words in the file (fast)   1 -> try some variations of the words    2 -> try several variations and combinations of the words (expensive) ",
	             type="int",
                 dest="mode")


    options, arguments = p.parse_args()

    if not options.list_file or not options.zip_file:
        p.print_usage()
        return
    if not options.mode:
        options.mode = 0

    if options.mode < 0 or options.mode >= 3:
        print "Unknown mode %d. Using default (0)." % int(options.mode)
        options.mode = 0

    find_password(options.list_file, options.zip_file, options.mode)

if __name__ == "__main__":
    main()
