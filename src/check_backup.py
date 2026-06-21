import os
from scanner import scan_folder
from dublicat import poisk_hasha
def scan(folder_path):
    files = scan_folder(folder_path)
    file_map = {}
    for f in files:
        full_path = f['path']
        rel_path = os.path.relpath(full_path, folder_path)
        file_hash = poisk_hasha(full_path)
        file_map[rel_path] = {
            'size': f['size'],
            'mtime': f['mtime'],
            'hash': file_hash
        }
    return file_map
def sravnenie(original_path, backup_path):
    orig_map = scan(original_path)
    back_map = scan(backup_path)

    only_original = []
    only_backup = []
    modified = []

    for rel_path, orig_info in orig_map.items():
        if rel_path not in back_map:
            only_original.append(rel_path)
        else:
            back_info = back_map[rel_path]
            if orig_info['hash'] != back_info['hash']:
                modified.append(rel_path)

    for rel_path in back_map:
        if rel_path not in orig_map:
            only_backup.append(rel_path)

    return only_original, only_backup, modified