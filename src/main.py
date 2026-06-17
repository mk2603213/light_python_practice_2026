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


def collect_files(path, base_path=None):
    files = {}
    # Если это самый первый запуск, запоминаем истинный корень папки
    if base_path is None:
        base_path = os.path.abspath(path)

    try:
        for name in os.listdir(path):
            full = os.path.join(path, name)
            if os.path.isfile(full):
                # Считаем относительный путь ВСЕГДА от истинного корня (base_path)
                rel_path = os.path.relpath(full, base_path)
                files[rel_path] = get_hash(full)
            elif os.path.isdir(full):
                # Передаем истинный корень дальше вглубь рекурсии
                for rel, h in collect_files(full, base_path).items():
                    files[rel] = h
    except PermissionError:
        pass
    return files


def compare_with_backup(source_path, backup_path):
    src = collect_files(source_path)
    bak = collect_files(backup_path)

    missing = sorted(set(src) - set(bak))
    extra   = sorted(set(bak) - set(src))
    changed = sorted(f for f in src if f in bak and src[f] != bak[f])

    print("\nРезервная копия")
    for f in missing: print(f"  нет в бэкапе:    {f}")
    for f in changed: print(f"  изменён:         {f}")
    for f in extra:   print(f"  лишний в бэкапе: {f}")

    if not any([missing, changed, extra]):
        print("  Папки идентичны.")
def main():
    if len(sys.argv) < 2:
        print("Ошибка, аргумент не передан")
        return

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

    if len(sys.argv) >= 3:
        compare_with_backup(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()
