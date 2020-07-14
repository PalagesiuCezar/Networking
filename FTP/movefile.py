import os

def copyfile():
    filename = "test"
    BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
    DEST_FOLDER = "testfolder"
    try:
        with open(BASE_FOLDER + "/" + filename, 'rb') as f1:
            lines = f1.read(1024)
        print("Avem fisierul pe care vrem sa-l copiem")

        with open(BASE_FOLDER + '/' + DEST_FOLDER + '/' + "muitsa", 'wb') as f2:
            f2.write(lines)
            print("Am copiat fisierul cu success!")
    except:
        print("Nu exista!")

if __name__ == "__main__":
    copyfile()