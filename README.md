This is a simple and probably quite inefficien random text generator based on Markov chains.  
It creates and stores chains for you, buy for any real use other than testing, you should reimplement demo functions.

Example:
```python
from markov import *

#Create an instance of MarkovGenerator binded to shelve file
mg = MarkovGenerator('path_to_shelve_file')

#Create chain, pass name and markov chain order (see theory behind markov chains)
mg.add_chain("test", 2)

#List chains in this shelve file
mg.chains

#Build chain from source, pass path to file and chain
mg.build_chain(parse('path_to_src'), mg.chains.test)

#Repeat untl you have your chain ready

#Generate text from chain
mg.generate_sentence(mg.chains.test)
```
