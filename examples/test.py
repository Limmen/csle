import os

def tail(f, window=1) -> str:
    """
    Returns the last `window` lines of file `f` as a list of bytes.

    :param f: the file object
    :param window: the window size
    :return: the parsed lines
    """
    if window == 0:
        return ''
    BUFSIZE = 1024
    f.seek(0, 2)
    end = f.tell()
    nlines = window + 1
    data = []
    while nlines > 0 and end > 0:
        i = max(0, end - BUFSIZE)
        nread = min(end, BUFSIZE)

        f.seek(i)
        chunk = f.read(nread)
        data.append(chunk)
        nlines -= chunk.count("\n")
        end -= nread
    return '\n'.join(''.join(reversed(data)).splitlines()[-window:])


if __name__ == '__main__':
    if os.path.exists("/var/log/csle/cluster_manager.log"):
        with open("/var/log/csle/cluster_manager.log", 'r') as fp:
            data = tail(fp, window=100).split("\n")
            print(f"Got tail data:{data}")
            logs = data