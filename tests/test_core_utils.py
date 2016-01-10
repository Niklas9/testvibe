
import testvibe.core.utils as utils


class TestUtils(object):

    def test_get_all_dirs(self):
        m = utils.get_all_dirs
        def listdir(path):
            return ['..', '.', 'fdsa', 'asdf', '.fdsa']
        def isdir(path):
            if path.startswith('.'):  return False
            return True
        assert (m('/tmp', listdirs_m=listdir, isdir_m=isdir)
                == set(('fdsa', 'asdf')))

    def test_get_path(self):
        m = utils.get_path
        assert m(['a/']) == 'a/'
        assert m(['1', '2', '3']) == '1/2/3'
        assert m(('tmp', 'test/vibe', 'logs')) == 'tmp/test/vibe/logs'
        assert m(['/tmp', 'testsuite.py']) == '/tmp/testsuite.py'

    def test_get_file_content(self):
        m = utils.get_file_content
        assert m('/tmp/asdf.txt', fh=FakeFileHandler()) == 'asdf'

    def test_copy_file(self):
        m = utils.copy_file
        fh = FakeFileHandler()
        m('/tmp/asdf.txt', '/tmp/fdsa.txt', search='as', replace='df', fh=fh)
        assert fh.f_obj.enter_called and fh.f_obj.exit_called

    def test_create_empty_file(self):
        m = utils.create_empty_file
        fh = FakeFileHandler()
        m('/tmp/asdf.txt', fh=fh)
        assert fh.f_obj.enter_called and fh.f_obj.exit_called

    def test_trim_cls_name(self):
        m = utils.trim_cls_name
        assert m('<class \'class\'>') == 'class'
        assert (m('<class \'project_template.UsersBasic\'>')
                == 'project_template.UsersBasic')


class FakeFileHandler(object):

    f_obj = None

    def __init__(self, *args, **kwargs):
        self.f_obj = self.FakeFileObject()

    def open(self, path, mode=None, encoding=None):
        return self.f_obj

    class FakeFileObject(object):

        content = None
        enter_called = None
        exit_called = None

        def __init__(self):
            self.enter_called = False
            self.exit_called = False

        def __enter__(self):
            self.enter_called = True
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.exit_called = True

        def read(self):
            return 'asdf'

        def write(self, content):
            self.content = content
