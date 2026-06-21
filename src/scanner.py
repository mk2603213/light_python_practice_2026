import datetime
import os
def scan_folder(path1):
    all_files = []
    def recurse(path2):
        try:
            vhod = os.listdir(path2)
        except (PermissionError, OSError):
            return
        for vh in vhod:
            all_path = os.path.join(path2, vh)

            # пропускаем скрытые файлы и папки
            if vh.startswith("."):
                continue

            if os.path.isdir(all_path):
                recurse(all_path)
            else:
                try:
                    size = os.path.getsize(all_path)
                    if size == 0:
                        continue
                    mtime_ts = os.path.getmtime(all_path)
                    mtime_str = datetime.datetime.fromtimestamp(mtime_ts).strftime('%Y-%m-%d %H:%M:%S')
                    all_files.append({'path': all_path, 'size': size, 'mtime': mtime_str})
                except (PermissionError, OSError):
                    continue
    recurse(path1)
    return all_files