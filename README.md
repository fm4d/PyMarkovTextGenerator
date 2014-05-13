PyMarkovTextGenerator
=====================

Python script for generating random text strings.


Usage
-----

Start with creating a Markov object. There are two optional arguments - prob and level. Default value for prob is  
True and it means, that you want to prioritize the more frequent connections of words. Level means depth of  
the chains, I will try to explain it with this example -

```python
Example sentence: "Hello world and hello to everyone."
Level 1:  {"Hello":"world", "world":"and", "and":"hello", "hello":"to", "to":"everyone."}
Level 2:  {("Hello","world"):"and", ("world","and"):"hello", ("and","hello"):"to", ("hello","to"):"everyone"}
Level 3:  {("Hello","world","and"):"hello", ("world","and","hello"):"to", ("and","hello","to"):"everyone"}
etc.
```

Level 1 will produce a very random mishmash of words, level 2 the standart pseudo-real text and then every next  
level will make the text more "connected", but its basically useless for our purpose without a very large text pool.  

Then continue with parsing any ammount of text with parse(text) and generate a random text with
generate(). It takes two arguments - startf and endf. Startf is used to find a beggining of the string. Default value is 
```python
lambda: random.choice(filter(lambda v: v[0][0].isupper(), self._database))
```
= choose random key which starts with uppercase. You can provide any function that returns key.

Function endf is called every time a new value is appended to the random string and its purpose is to check if  
script shoud continue generating or it is good enought to be returned. Default value is
```python
lambda s: len(s.split()) > 10
```
= return string if its lenght is 11. Check test.py for a more complex version of endf.

Example
-------
```python
m = Markov(prob=True, level=2)
with open("text-test") as file:
    m.parse(file.read())
    print m.generate()
```
