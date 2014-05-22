PyMarkovTextGenerator
=====================

Python script for generating random text strings.


Installation
-----------

```
pip install PyMarkovTextGenerator
```


Usage
-----

Start with creating a Markov object. There are two optional arguments - ```prob``` and ```level```. Default value
for ```prob``` is ```True``` and it means, that you want to prioritize the more frequent connections of words.
```level``` means a depth of  the chains, I will try to explain it with this example:

```python
Example sentence: "Hello world and hello to everyone."
Level 1:  {"Hello":"world", "world":"and", "and":"hello", "hello":"to", "to":"everyone."}
Level 2:  {("Hello","world"):"and", ("world","and"):"hello", ("and","hello"):"to", ("hello","to"):"everyone"}
Level 3:  {("Hello","world","and"):"hello", ("world","and","hello"):"to", ("and","hello","to"):"everyone"}
etc.
```

Level 1 will produce a very random mishmash of words, level 2 the standart pseudo-real text
and then every next level will make the text more "connected", but its basically useless
for our purpose without a very large text pool.

Then continue with parsing any ammount of text with ```parse(text)```. Currently there is no support for saving
parsed data into some database etc.

Random text is generated via ```generate``` function. Because there are many ways how to choose begging of
text and how to determine when to end, I decided to use ```startf``` and ```endf``` functions instead of some
arguments like ```length``` etc. Both functions must return boolean value.

```startf``` is called at the begginng of generate with self._database (parsed data) as an argument.
```endf``` is called after every iteration that append new value to quote string with that string as an argument.

Default value for ```startf``` is:
```python
lambda db: random.choice(filter(lambda val: val[0][0].isupper(), db))
```
And default value for ```endf```:
```python
lambda s: len(s.split()) > 10
```

Example
------
```python
from PyMarkovTextGenerator import Markov

m = Markov(prob=True, level=2)
with open(some_text_file) as file:
    m.parse(file.read())
    print m.generate()
```
