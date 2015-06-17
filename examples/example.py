from PyMarkovTextGenerator import Markov


def end(s):
    interpunction = (".", "?", "!")
    if s[len(s)-1] in interpunction and len(s.split()) > 10:
        return True
    else:
        return False

m = Markov(prob=True, level=2)
with open("text-test") as file:
    m.parse(file.read())
    print m.generate(endf=end)
