# wthell

wthell is a debugging tool for python to interactively check frame stack when your code did something unexpectedly

## Install

You can install ```wthell``` from pip

```
pip install wthell
```

## Usage

It's super easy to use wthell. Just run you script using wthell instead of python

```
wthell your_script.py args1 args2
```

Or you can import wthell in your script and run your script normally

```python
import wthell
```

If there's an uncaught exception, you will enter an interactive shell like this:

```python
  def g(a, b):
      a += h(a)
      b += 3
>     raise Exception("lol")


Exception raised: <class 'Exception'> lol

up(u)       -- go to outer frame  | down(d)  -- go to inner frame
clear(cl)   -- clear the console  | reset(r) -- back to trigger frame
continue(c) -- resume the program | ctrl+D   -- quit

>>> 
```

You will be in the frame(function) that raised exceptions in the beginning. 

* Type ```up``` to go to outer frame(its caller). 
* Type ```down``` to go to inner frame(when you already go out). 
* Type ```clear``` to clear the console prints
* Type ```reset``` to go back to the original frame that triggered wthell
* Type ```continue``` to resume the program

wthell will record the full call stack so you can check any frame. 

While you are in a stack, you can type anything that you want to evaluation to help you debug.

```python
>>> a
13
>>> a + 1
14
>>> h(a)
16
>>> 
```

Or you can trigger wthell anywhere in your code 

```python
def suspicious_function():
    # I want to check here!
    wthell.wth()
```

wthell behaves like an interactive shell. 

Happy debugging!

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the [Apache 2.0 license](https://github.com/gaogaotiantian/wthell/blob/master/LICENSE).