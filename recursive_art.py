"""
Create recursive art

@author: Emma Mack
"""

import random
import math
from PIL import Image

#I attempted to "go beyond" and got pretty far, but eventually ran into a wall.
#When generate_art runs, it does not use random_f_lambda.
def random_f_lambda(min_depth, max_depth, current_depth = 1):
    """Builds a random function of x and y of depth at least min_depth and depth
    at most max_depth.

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        Float

    >>> random_f_lambda(6,8,.5,.7)

    """
    #if at or above min depth, certain probablilty that recursion will end
    if current_depth >= min_depth:
        #probability is inversely proportional to dist between min and max depth
        if random.randint(min_depth, max_depth) == min_depth:
            return random.choice([lambda x,y: x, lambda x,y: y])
    if current_depth == max_depth:
        return random.choice([lambda x,y: x, lambda x,y: y])

    # func_choices = ["prod", "avg", "cos_pi", "sin_pi", "square", "round"]
    func_choices = ["cos_pi", "prod"]
    choice = random.choice(func_choices)


    a = random_f_lambda(min_depth, max_depth, current_depth+1)
    b = random_f_lambda(min_depth, max_depth, current_depth+1)

    if choice == "cos_pi":
        func = lambda x, y: math.cos(math.pi*a)
    if choice == "prod":
        func = lambda x, y: a*b
    return func

def random_f(min_depth, max_depth, current_depth = 1):
    """Builds a random function of depth at least min_depth and depth at most
    max_depth.

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.

    >>> random_f(4,1)

    """
    #if at or above min depth, certain probablilty that recursion will end
    if current_depth >= min_depth:
        #probability is inversely proportional to dist between min and max depth
        if random.randint(min_depth, max_depth) == min_depth:
            return random.choice([["x"],["y"]])
    if current_depth == max_depth:
        return random.choice([["x"],["y"]])

    #randomly selects a func
    func_choices = ["prod", "avg", "cos_pi", "sin_pi", "square", "round"]
    choice = random.choice(func_choices)

    #broken into functions that create two new recursive trees and those that create one
    if choice == "cos_pi" or choice == "sin_pi" or choice == "square" or choice == "round":      #funcs with 1 arg
        func = [choice, random_f(min_depth, max_depth, current_depth+1)]
    if choice == "prod" or choice == "avg":           #funcs with 2 args
        func = [choice, random_f(min_depth, max_depth, current_depth+1),
                        random_f(min_depth, max_depth, current_depth+1)]
    return func


def eval_f(f, x, y):
    """Evaluate the random function f with inputs x,y.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function

    Returns:
        The function value

    Examples:
        >>> eval_f(["cos_pi",["prod",["x"],["y"]]],1, 2)
        3.0
    """
    operation = f[0]

    #base case
    if operation == "x":
        return x
    if operation == "y":
        return y

    #recursively evaluate function based on operation
    if operation == "prod":
        mult1, mult2 = f[1], f[2]
        return eval_f(mult1,x,y)*eval_f(mult2,x,y)
    if operation == "avg":
        return (eval_f(f[1],x,y)+eval_f(f[2],x,y))/2
    if operation == "cos_pi":
        return math.cos(math.pi*eval_f(f[1],x,y))
    if operation == "sin_pi":
        return math.sin(math.pi*eval_f(f[1],x,y))
    if operation == "square":
        return eval_f(f[1],x,y)**2
    if operation == "round":
        return round(eval_f(f[1],x,y))
    else:
        raise Exception("Invalid input")



def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_width = input_interval_end - input_interval_start
    output_width = output_interval_end - output_interval_start
    amt_into_interval = (val - input_interval_start)/input_width
    return output_interval_start + output_width*amt_into_interval


def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255, suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels

    r_f = random_f(6,8)
    g_f = random_f(6,8)
    b_f = random_f(6,8)

    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(eval_f(r_f,x,y)),
                color_map(eval_f(g_f,x,y)),
                color_map(eval_f(b_f,x,y)),
            )

    im.save(filename)
    im.show()


if __name__ == '__main__':
    import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(random_f_lambda, globals(), verbose = True)
    # print(random_f_lambda(6,8,.5,.7))
    generate_art("myart8.png")
