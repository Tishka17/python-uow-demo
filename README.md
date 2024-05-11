## Unit of work example in Python

This is an example implementation of "Unit of Work" pattern.

It doesn't show optimal way to do it and has known limitations. 
It should be considered only as an educational material, not a ready-to-production code. 

In this example you can see:

* Unit of Work itself, which has own copy of mappers registry and affected models.
* A data mapper fake implementation to show when it is called
* A dataclass used as an anemic domain model
* A model wrapper so to keep business model clean. This can break the code which uses reflection. 
* An example of some business logic (interactor) and a database gateway for it.

