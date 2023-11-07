[YAML] is a human-friendly data serialization language for all programming languages.

Embedded mathematical tools for all programming languages.

> YAML represents any native data structure using three node kinds: sequence, mapping and scalar - any datum with opaque structure presentable as a series of Unicode characters.
>
> Combined, these primitives generate directed graph structures

Category Theory provides several tools to interpret graphs, such as the [Quiver] category.

> a functor F:Quiv→Cat is an embedding

which is exactly what we look for in an embedded language.

We work with high level concepts without defining a new language syntax, even avoiding parsers altogether.

[YAML]: https://yaml.org/
[Quiver]: https://ncatlab.org/nlab/show/quiver

# Usage

```sh
python . examples/hello-world.yaml
```
```yaml
Hello world!
```

# Development

Run `make` to compose and build gifs for all YAML files.

# Mathematical foundations

* nLab: [nPOV]
* Haskell: functional
* Coq: type theory

The YAML language is chosen because it fits Category Theory like a glove.
* graphs
* objects
* recursivity

Categorical tools provide the necessary glue from graphs to the whole math ecosystem.

# Language

YAML is a human-friendly language and is suited for describing object relations.

The languages that helped me bridge math to programming:
* Haskell: do notation
* Scala: for comprehensions, cats
* Smalltalk: method call syntax
* LISP: code as data
* UNIX: pipelining

My intuition came from the observation that I was writing the same code time and time again.
Even though functional patterns are available in most languages,
every time I wanted to tap into the most powerful features I was stopped.

# Operating system

This tool has important considerations for the development environment:
* UNIX: follows philosophy and is deeply integrated
* Smalltalk: follows design principles

Even when using UNIX, we want to follow Smalltalk design principles as well.

Code editing:
* support in all OSs
* wide variety of features in YAML
* unified sdlc language

# Runtime

Though this tool is a runtime, the language itself is not defined in terms of a runtime.
Graph operations don't have a concept of failing.

* Smalltalk: virtual machine
* LISP: little bytecode


[nPOV]: https://ncatlab.org/nlab/show/nPOV
