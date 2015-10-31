
class Log(object):

    def __init__(self):
        pass

    def debug(self, msg):
        print 'DEBUG: %s' % msg

    def error(self, msg):
        print 'ERROR: %s' % msg
