
import codecs
import os


FILEMODE_READ = 'r'
FILEMODE_WRITE = 'w'
FILE_ENCODING_UTF8 = 'utf-8'
STRING_BASE_DIR = '%s/'
STRING_EMPTY = ''
STRING_SLASH = '/'
STRING_UNDERSCORE = '_'

def get_all_dirs(path):
    dirs = set()
    for f in os.listdir(path):
        if os.path.isdir(f):
            dirs.add(f)
    return dirs

def get_path(fps):
    path = STRING_EMPTY.join(STRING_BASE_DIR % fp for fp in fps)
    if path.endswith(STRING_SLASH):
        return path[:-1]
    return path

def get_file_content(path):
    with codecs.open(path, FILEMODE_READ, encoding=FILE_ENCODING_UTF8) as f:
        content = f.read()
    return content

def copy_file(src, dest, search=None, replace=None):
    with codecs.open(src, FILEMODE_READ, encoding=FILE_ENCODING_UTF8) as f:
        src_content = f.read()
    if search is not None and replace is not None:
        src_content = src_content.replace(search, replace)
    with codecs.open(dest, FILEMODE_WRITE, encoding=FILE_ENCODING_UTF8) as f:
        f.write(src_content)

def create_empty_file(path):
    with codecs.open(path, FILEMODE_WRITE, encoding=FILE_ENCODING_UTF8) as f:
        pass  # just an empty file