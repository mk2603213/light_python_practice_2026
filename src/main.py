import sys
import os
from datetime import datetime
def scan(path):
    k = 0
    try:
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            if os.path.isfile(full_path):
                k += 1
                s = os.stat(full_path)
                print(full_path, s.st_size, "байт", datetime.fromtimestamp(s.st_mtime).strftime("%Y-%m-%d %H:%M:%S"))
            elif os.path.isdir(full_path):
                k += scan(full_path)  # прибавляем результат рекурсии
    except PermissionError:
        pass
    return k
def main():
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        print(path)
        count = scan(path)
        print("Итого файлов:", count)
    else:
        print("Ошибка, аргумент не передан")

if __name__ == "__main__":
    main()
