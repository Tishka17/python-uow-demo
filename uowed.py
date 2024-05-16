from functools import wraps
from typing import Any, Protocol, TypeVar

ModelT = TypeVar("ModelT", contravariant=True)


class DataMapper(Protocol[ModelT]):
    """Class used by a UoW to flush changes to a database"""

    def insert(self, model: ModelT):
        raise NotImplementedError

    def delete(self, model: ModelT):
        raise NotImplementedError

    def update(self, model: ModelT):
        raise NotImplementedError


class UnitOfWork:
    def __init__(self):
        self.dirty = {}
        self.new = {}
        self.deleted = {}
        self.mappers = {}

    def register_dirty(self, model):
        model_id = id(model)
        if model_id in self.new:
            return
        self.dirty[model_id] = model

    def register_deleted(self, model):
        if isinstance(model, UoWModel):
            model = model._model

        model_id = id(model)
        if model_id in self.new:
            self.new.pop(model_id)
            return
        if model_id in self.dirty:
            self.dirty.pop(model_id)
        self.deleted[model_id] = model

    def register_new(self, model):
        model_id = id(model)
        self.new[model_id] = model
        return UoWModel(model, self)

    def commit(self):
        # here we can add optimizations like request batching
        # but it will also require extending of Mapper protocol
        for model in self.new.values():
            self.mappers[type(model)].insert(model)
        for model in self.dirty.values():
            self.mappers[type(model)].update(model)
        for model in self.deleted.values():
            self.mappers[type(model)].delete(model)


class UoWAttributeProxy:
    def __init__(self, attr, uow, model) -> None:
        self.__dict__["_attr"] = attr
        self._uow = uow
        self._model = model
        self._model_state = model.__dict__.copy()

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._attr, name)

        if callable(attr):
            return self.wrap_method(attr)

        return attr

    def wrap_method(self, method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            if self._model_state != self._model.__dict__:
                self._uow.register_dirty(self._model)
                self._model_state.update(self._model.__dict__)
            return result

        return wrapper

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name not in ("_uow", "_model", "_model_state"):
            setattr(self._attr, __name, __value)
            self._uow.register_dirty(self._model)

        else:
            super().__setattr__(__name, __value)

    def __str__(self) -> str:
        return str(self._attr)

    def __repr__(self) -> str:
        return repr(self._attr)


class UoWModel:
    def __init__(self, model, uow):
        for key, value in model.__dict__.items():
            if not getattr(value, "_uow_wrapped", False):
                setattr(model, key, UoWAttributeProxy(value, uow, model))

        self.__dict__["_model"] = model
        self.__dict__["_uow"] = uow

    def __getattr__(self, key):
        return getattr(self._model, key)

    def __setattr__(self, key, value):
        setattr(self._model, key, value)
        self._uow.register_dirty(self._model)
