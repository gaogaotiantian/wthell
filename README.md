# wthell

wthell is a debugging tool for python to interactively check frame stack when your code quit unexpectedly 

## Install

You can install ```wthell``` from pip

```
pip install wthell
```

## Usage

It's super easy to use wthell. Just import it and it's done!

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

back  -- go to outer frame | in     -- go to inner frame
clear -- reset the console | ctrl+D -- quit

>>> 
```

You will be in the frame(function) that raised exceptions in the beginning. You can type ```back``` to go to outer frame(its caller). 
You can type ```in``` to go to inner frame(when you already go out). wthell will record the full call stack so you can check any
frame. 

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

wthell behaves like an interactive shell. 

Happy debugging!

## License

Copyright Tian Gao, 2020.

Distributed under the terms of the [Apache 2.0 license](https://github.com/gaogaotiantian/wthell/blob/master/LICENSE).