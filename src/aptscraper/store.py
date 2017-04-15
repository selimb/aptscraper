import os


class _Database(object):
    def __init__(self, db_fpath):
        self.items = open(db_fpath).read().split('\n')
        self.db_f = open(db_fpath, 'a')

    def add(self, data_id):
        self.items.append(data_id)
        self.db_f.write('%s\n' % data_id)

    def query(self, data_id):
        return data_id in self.items

    def close(self):
        self.db_f.close()


def init_db(db_fpath):
    if not os.path.exists(db_fpath):
        open(db_fpath, 'w').write('')
    db = _Database(db_fpath)
    return db
