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

    if res:
        return True
    else:
        return False

def find_password(list_file, zip_file):
    try:
        file = open(list_file)

        while True:
            line = file.readline()
            line = line[:-1]

            if not line:
                break

            try:
                if bf_extract(zip_file, line):
                    print "The password is " + line
                    break

            except InvalidZip:
                break

    except IOError:
        return


def main():
    p = optparse.OptionParser()
    p.add_option('-l', help="Person is required",
                 dest="list_file")
    p.add_option('-f', help="Person is required",
                 dest="zip_file")

    options, arguments = p.parse_args()

    find_password(options.list_file, options.zip_file)


if __name__ == "__main__":
    main()