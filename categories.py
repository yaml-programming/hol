from typing import Any, List, Self
from dataclasses import dataclass


class Quiver:
    def paths(self) -> Self:
        return self


@dataclass
class Morphism:
    source: Any
    target: Any


@dataclass
class Cat:
    """2-category of categories"""
    objects: Self
    morphisms: List[Morphism]

    def opposite(self) -> Self:
        return None
    
    def map(self, obj):
        """composing two category objects works as..."""
        self.morphisms
        pass

@dataclass
class Diagram(Cat):
    """
    A shaped diagram in a category C
    """
    shape: Cat
    C: Cat

class Free:
    """
    The free category on a “set of arrows", also called path category.
    The composition operation in this free category is the concatenation of sequences of edges.
    """
    def __init__(self, quiver: Quiver):
        self.quiver = quiver.paths()

    def opposite(self) -> Self:
        return Free(self.quiver.opposite())

    def map(self, obj):
        return self.quiver(obj)


# A free diagram in a category 
# 𝒞
#  is a diagram in 
# 𝒞
# whose shape is a free category
class FreeDiag:
    def __init__(self, shape: Free, C: Cat):
        self.quiver = shape.quiver
        self.C = C

    # devuelve un objeto en C
    # tengo que interpretar este diagrama como
    # un funtor X:J->C con J shape = Free(quiver)
    # y obj en quiver
    def map(self, obj):
        return self.quiver(obj)
        return self.C(obj)


# class Fun:
#     """
#     1-category of functors.
#     class of objects is the collection of all functors F:C->D.
#     morphisms are natural transformations between these functors.
#     A functor between small categories is a homomorphism of the underlying graphs that respects the composition of edges.
#     """
#     def __init__(self, C: Cat, D: Cat):
#         self.C = C
#         self.D = D

#     def map(self, obj) -> Any:
#         """maps obj in C to an object in D"""
#         return self.C(obj)


class SIndCat:
    """2-category of S-indexed categories"""
    def __init__(self, S: Cat):
        self.domain = S.opposite()
        self.codomain = Cat


# class CommaCat:
#     def __init__(self, f_C_to_D: Fun, g_E_to_D: Fun):
#         self.f_C_to_D = f_C_to_D
#         self.g_E_to_D = g_E_to_D


# class SIndFun:
#     def __init__(self, C: SIndCat, D: SIndCat, S: Cat):
#         self.C = C
#         self.D = D
#         self.S = S

