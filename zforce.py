import zipfile

def bf_extract(zfile, password):
    zip = zipfile.ZipFile(zfile)
    try:
        zip.setpassword(password)
        zip.extractall()
    except:
        pass
    finally:
        zip.close()

if __name__ == "__main__":
    bf_extract("spmv.zip", "ok")