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
 
def find_password(list_file, zip_file, mode):
    found = find_password_simple(list_file, zip_file)
    if not found and mode > 0:
        found = find_password_with_variations(list_file, zip_file)
    if not found and mode > 1:
        find_password_with_combinations(list_file, zip_file)

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
                if bf_extract(zip_file, line):
                    print "The password is " + line
                    found = True

            except InvalidZip:
                break
        return found

    except IOError:
        return False

def find_password_with_variations (list_file, zip_file):
    variations = []
    for word in words:
        # try all letters in uppercase
        if not word.isupper():
            up = word.upper()
            words.append(up)
            if bf_extract(zip_file, up):
                print "The password is " + up
                return True
        # try all letters in lower
        if not word.islower():
            lower = word.lower()
            words.append(lower)
            if bf_extract(zip_file, lower):
                print "The password is " + lower
                return True
        # try first letters uppercase
        if not word.istitle():
            title = word.title()
            words.append(title)
            if bf_extract(zip_file, title):
                print "The password is " + title
                return True
        # try replace some chars (for example: teste --> t3st3)
        words.append(word.replace("o", "0").replace("A", "4").replace("l", "1").replace("e", "3").replace("E", "3"))
        r = words[-1]
        if bf_extract(zip_file, r):
            print "The password is " + r
            return True

    return False


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
