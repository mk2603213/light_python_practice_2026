import sys
import os
from scanner import scan_folder
from dublicat import poisk_dublicat
from check_backup import sravnenie

def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py <путь_к_папке>")
        print("Использование: python main.py <оригинал> <бэкап>")
        sys.exit(1)

    target_folder = sys.argv[1]
    if not os.path.isdir(target_folder):
        print(f"Ошибка: папка '{target_folder}' не существует или недоступна.")
        sys.exit(1)

    print(f"Принят путь: {target_folder}")
    print(f"Сканирование папки: {target_folder}\n")

    files = scan_folder(target_folder)
    print(f"Найдено файлов: {len(files)}\n")
    print("Найдены файлы:")
    for f in files:
        print(f"Путь: {f['path']}, Размер: {f['size']} байт, Дата: {f['mtime']}")

    dublicat = poisk_dublicat([f['path'] for f in files])
    if not dublicat:
        print("Дубликатов нет")
    else:
        print(f"\nНайдено групп дубликатов: {len(dublicat)}")
        for h, paths in dublicat.items():
            print(f"\nХеш: {h}")
            for p in paths:
                print(f"  {p}")

    if len(sys.argv) >= 3:
        backup_path = sys.argv[2]
        if not os.path.isdir(backup_path):
            print(f"Ошибка: папка бэкапа '{backup_path}' не существует")
            sys.exit(1)

        print("\nСравнение с резервной копией")
        only_orig, only_back, modified = sravnenie(target_folder, backup_path)

        if only_orig:
            print("\nФайлы, отсутствующие в бэкапе:")
            for p in only_orig:
                print(f"  {p}")
        if only_back:
            print("\nЛишние файлы в бэкапе:")
            for p in only_back:
                print(f"  {p}")
        if modified:
            print("\nИзменённые файлы:")
            for p in modified:
                print(f"  {p}")
        if not (only_orig or only_back or modified):
            print("Папки полностью совпадают (по содержимому).")

if __name__ == "__main__":
    main()