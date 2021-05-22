# pipulator
A collision simulator designed to compute the digits of π, inspired by [this 3Blue1Brown video](https://www.youtube.com/watch?v=HEfHFsfGXjs). By default, the simulator will calculate 7 decimal digits of π by using a block with a mass of 1 quintillion kilograms.

To calculate more digits, increase `PI_PRECISION_VALUE` to the number of digits you wish to compute. Change `PHYSICS_ITERATIONS` to modify up the number of collisions computed per frame - I recommend keeping it below 15,000 to maintain a reasonable framerate.

## Prerequisites
Simply install `pyglet` before running:
```
$ pip install pyglet
```
