class Test:
    def __getitem__(self, key):
            return getattr(self, key)

    def Variable(self):
        print('variable')

test = Test()
test['Variable']()