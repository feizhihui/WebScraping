# encoding=utf-8

class Person(object):
    def __init__(self, stuid=None, name=None, gender=None, birth=None, nation=None, college=None, major=None,
                 aclass=None, idcard=None):
        self.stuid = stuid
        self.name = name
        self.gender = gender
        self.birth = birth
        self.nation = nation
        self.college = college
        self.major = major
        self.aclass = aclass
        self.idcard = idcard

    def show(self):
        print self.stuid, self.name, self.gender, self.college, self.aclass
