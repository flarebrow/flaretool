import glob
import os


def main():

    folder_path = "./repos/"
    prefix = "#!/bin/python\n# -*- coding: utf-8 -*-\n"

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(".py"):
                with open(file_path, 'r+') as f:
                    content = f.read()
                    if "#!/bin/python" not in content:
                        print(file_path, )
                        f.seek(0, 0)  # ファイルの先頭に戻る
                        f.write(prefix + content)
    pass


if __name__ == "__main__":
    main()
