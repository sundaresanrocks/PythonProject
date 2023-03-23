

class person:
    def __init__(self, fn, ln):
        self.fn = fn
        self.ln = ln

    def welcome(self):
        return "Welcome {} {} ".format(self.fn, self.ln)


class Student(person):
  def __init__(self, fname, lname, year):
    super().__init__(fname, lname)
    self.graduationyear = year

  def welcome(self):
    return "Welcome {} {} {}".format(self.fn, self.ln, str(self.graduationyear))

class Counter:
    def __init__(self):
        self.__current = 0

    def increment(self):
        self.__current += 1

    def value(self):
        return self.__current

    def reset(self):
        self.__current = 0


# print(counter.__current)

counter = Counter()
print(counter._Counter__current)

