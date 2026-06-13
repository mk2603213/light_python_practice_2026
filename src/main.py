import sys
import os
import hashlib
from datetime import datetime

def get_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        data = f.read()
    h.update(data)
    return h.hexdigest()
def scan(path, hashes):
    k = 0
    try:
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                k += 1
                s = os.stat(full_path)
                print(full_path, s.st_size, "байт", datetime.fromtimestamp(s.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
                h = get_hash(full_path)
                if h not in hashes:
                    hashes[h] = []
                hashes[h].append(full_path)
            elif os.path.isdir(full_path):
                k += scan(full_path, hashes)  # прибавляем результат рекурсии
    except PermissionError:
        pass
    return k
def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        print(path)
        hashes = {}
        count = scan(path, hashes)
        print("Итого файлов:", count)
        for h, files in hashes.items():
            if len(files) > 1:
                print("Дубликаты:")
                for f in files:
                    print(" ", f)
    else:
        print("Ошибка, аргумент не передан")

if __name__ == "__main__":
    main()
