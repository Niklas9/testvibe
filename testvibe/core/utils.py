
import codecs
import os

CLS_NAME_PREFIX = '<class \''
CLS_NAME_SUFFIX_LEN = 2
FILEMODE_READ = 'r'
FILEMODE_WRITE = 'w'
FILE_ENCODING_UTF8 = 'utf-8'
STRING_BASE_DIR = '%s/'
STRING_EMPTY = ''
STRING_SLASH = '/'
STRING_UNDERSCORE = '_'

def get_all_dirs(path, listdirs_m=None, isdir_m=None):
    if listdirs_m is None:  listdirs_m = os.listdir
    if isdir_m is None:  isdir_m = os.path.isdir
    dirs = set()
    for f in listdirs_m(path):
        if isdir_m(f):
            dirs.add(f)
    return dirs

def get_path(fps):
    path = STRING_EMPTY.join(STRING_BASE_DIR % fp for fp in fps)
    return path[:-len(STRING_SLASH)]

def get_file_content(path, fh=None):
    if fh is None:  fh = codecs
    with fh.open(path, mode=FILEMODE_READ, encoding=FILE_ENCODING_UTF8) as f:
        content = f.read()
    return content

def copy_file(src, dest, search=None, replace=None, fh=None):
    if fh is None:  fh = codecs
    with fh.open(src, mode=FILEMODE_READ, encoding=FILE_ENCODING_UTF8) as f:
        src_content = f.read()
    if search is not None and replace is not None:
        src_content = src_content.replace(search, replace)
    with fh.open(dest, mode=FILEMODE_WRITE, encoding=FILE_ENCODING_UTF8) as f:
        f.write(src_content)

def create_empty_file(path, fh=None):
    if fh is None:  fh = codecs
    with fh.open(path, mode=FILEMODE_WRITE, encoding=FILE_ENCODING_UTF8) as f:
        pass  # just an empty file

def trim_cls_name(s):
    return s.replace(CLS_NAME_PREFIX, STRING_EMPTY)[:-CLS_NAME_SUFFIX_LEN]
