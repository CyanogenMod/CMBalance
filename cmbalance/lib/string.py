
def convert_bytes(bytes):
    bytes = float(bytes)

    if bytes >= 1024 ** 4:
        terabytes = bytes / (1024 ** 4)
        size = '%.2f TB' % terabytes
    elif bytes >= 1024 ** 3:
        gigabytes = bytes / (1024 ** 3)
        size = '%.2f GB' % gigabytes
    elif bytes >= 1024 ** 2:
        megabytes = bytes / (1024 ** 2)
        size = '%.2f MB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2f KB' % kilobytes
    else:
        size = '%.2f B' % bytes

    return size
