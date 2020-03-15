# -*- coding: utf-8 -*-
u"""Klasa przechowująca wektor j"""



import random
import math


class Vector():
    """
        Class used to represent Vector

        ...

        Attributes
        ----------
        size : int
            size of vector(default 3)
        numbers : list
            vector respresented as a list ex. [x,y,z]
        """
    def __init__(self, size=3, numbers=[]):
        """
                Parameters:
                ----------
                param size: int
                    size(dimension) of vector(default 3)
                param numbers: list
                    vector represnted as a list (not required)

                """
        self.size = size
        self.numbers = numbers

    def generate_numbers(self):
        """Generates random parameters of vector

                Parameters:
                ----------
                """
        for i in range(self.size-len(self.numbers)):
            self.numbers.append(random.randint(-100,100))

    def load_vector(self, ls):
        """Loads parameters of vector as a list

                Parameters:
                ----------
                param ls: list
                    List with paramters of vector

                """
        try:
            if type(ls) == list and len(ls)==self.size:
                self.numbers = ls
            if len(ls)>self.size:
                raise ValueError
            if type(ls) != list:
                raise NameError("Type of argument is wrong")
        except ValueError:
            raise ValueError("Incorrect size of lists")


    def add_elements(self, list1, list2):
        """Returns list of adding two lists

                Parameters:
                ----------
                param list1: list1
                    The first list to add
                param list2L list2
                    The second list to add

                """
        list3 = []
        for i in range(len(list1)):
            list3.append(list1[i] + list2[i])
        return list3

    def radd_elements(self, list1, list2):
        """Returns list of substrating two lists

                Parameters:
                ----------
                param list1: list1
                    The first list to add
                param list2L list2
                    The second list to add
                """
        list3 = []
        for i in range(len(list1)):
            list3.append(list1[i] - list2[i])
        return list3

    def __add__(self, other):
        """Adds two vectors to each other

                        Parameters:
                        ----------
                        param other: class Vector object
                            The second vector to add

                        """

        try:
            if self.size != other.size:
                raise ValueError
            summed_numbers = self.add_elements(list1=self.numbers, list2=other.numbers)
            return Vector(size=len(self.numbers), numbers=summed_numbers)

        except ValueError:
            raise ValueError ("Size of both list are not equal!")


    def __sub__(self, other):
        """Substracts two vectors to each other

                        Parameters:
                        ----------
                        param other: class Vector object
                            The second vector to add

                        """
        try:
            if self.size != other.size:
                raise ValueError
            summed_numbers = self.radd_elements(list1=self.numbers, list2=other.numbers)
            return Vector(size=len(self.numbers), numbers=summed_numbers)


        except ValueError:
            raise ValueError ("Size of both list are not equal!")
    def scale_vector(self, scalar):
        """Multiplies a vector by a number.

                        Parameters:
                        ----------
                        param scalar: float
                            Scalar of a vector


                        """
        self.numbers = [x * scalar for x in self.numbers]
        return Vector(size=len(self.numbers), numbers=self.numbers)
    def length(self):
        """Returns length of the vector

                        Parameters:
                        ----------
                        """
        square_values = [x**2 for x in self.numbers]
        return math.sqrt(sum(square_values))
    def sum_of_elements(self):
        """Returns sum of paramters

                        Parameters:
                        ----------
                        """
        return sum(self.numbers)

    def scalar_multiplying(self, second_vector):
        """Returns a vector that is a product of scalar_multiplying of two vectors

                        Parameters:
                        ----------
                        param second_vector: class Vector object
                            The second Vector of scalar multiplying


                        """
        try:
            if self.size != second_vector.size:
                raise ValueError
            z = []
            for i in range(self.size):
                z.append(self.numbers[i]* second_vector.numbers[i])
            return Vector(size=self.size, numbers=z)
        except ValueError:
            raise ValueError ("Size error")
    def __str__(self):
        """Returns a string representation of Vector

                        Parameters:
                        ----------

                        """
        return f"Vector: {tuple(self.numbers)}\nSize of Vector:{self.size} "

    def __getitem__(self, item):
        """Allow to access parameters of a vector as a list

                        Parameters:
                        ----------

                        """
        return self.numbers[item]
    def __contains__(self, item):
        """Allow to check if there is a paramter with command in.

                        Parameters:
                        ----------
                            param item: double


                        """
        if item in self.numbers:
            return True
        else:
            return False
if __name__ == "__main__":
    #Testing package
    x = Vector(3, [1,1,1])
    y = Vector(3, [1,2,3])
    print(x+y)
    help(Vector.generate_numbers)
    print(1 in x)
