import hashlib
def poisk_hasha(file_path):
    hash = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            while True:
                chast = f.read(8192)  # читаем по кускам, а не весь файл сразу
                if not chast:
                    break
                hash.update(chast)
        return hash.hexdigest()
    except OSError:
        return None
def poisk_dublicat(file_paths):
    odinak = {}
    for path in file_paths:
        h = poisk_hasha(path)
        if h is not None:
            if h not in odinak:
                odinak[h] = []
            odinak[h].append(path)
    result = {}
    for h, paths in odinak.items():
        if len(paths) > 1:
            result[h] = paths
    return result