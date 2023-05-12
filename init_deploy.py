import re


def main():

    # lib書き換え
    lib_file = "requirements.txt"
    with open(lib_file) as f:
        lib_list = f.read().splitlines()

    def check(x): return not any(
        val in x for val in ["autopep8", "flaretool"])
    with open(lib_file, "w") as f:
        for lib_name in lib_list:
            if check(lib_name):
                f.write(lib_name.replace("==", ">=") + "\n")

    version_file = "repos/flaretool/VERSION.py"
    version_setup_file = "version.txt"

    # バージョン自動インクリメント

    # バージョン番号を取得
    with open(version_file) as f:
        current = f.read()
        version = re.search(r'(?<=VERSION\s=\s")[^"]+', current).group(0)

    # パッチバージョン番号をインクリメント
    major, minor, patch = map(int, version.split('.'))
    patch += 1
    new_version = f'{major}.{minor}.{patch}'

    with open(version_file, "w") as f:
        f.write(re.sub(r'(?<=VERSION\s=\s")[^"]+', new_version, current))

    with open(version_setup_file, "w") as f:
        f.write(new_version)


if __name__ == "__main__":
    main()
