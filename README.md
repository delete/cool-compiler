# Cool Language Compiler
> Compiler for [Cool Language](http://theory.stanford.edu/~aiken/software/cool/cool.html) created for the compilers' class from my Computer Science degrees.

![](http://i.imgur.com/ivygr2X.png)

## Installation

Clone the project:

```
$ git clone https://github.com/delete/cool-compiler.git
$ cd cool-compiler/
```

Install the requirements packages:

> See [here](https://pip.pypa.io/en/stable/installing/) how to install pip.

`$ pip install -r requirements.txt`


## Usage example

Web app:

> Only lexical and syntatic analyzers are working on web app for now, if you want use semantic, please, run from terminal.

`$ python2 app.py`

Access:
`http://127.0.0.1:5000/`

Run from the terminal:

`$ python2 compiler.py examples/hello-world.cl`

> If no message appear, then everything is fine.
