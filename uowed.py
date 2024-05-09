class UowedGw:
    def insert(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError

    def update(self, model):
        raise NotImplementedError


class UoW:
    def __init__(self):
        self.dirty = {}
        self.new = {}
        self.deleted = {}
        self.repos = {}

    def register_dirty(self, model):
        model_id = id(model)
        if model_id in self.new:
            return
        self.dirty[model_id] = model

    def register_deleted(self, model):
        if isinstance(model, UowedModel):
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
        return UowedModel(model, self)

    def commit(self):
        for model in self.new.values():
            self.repos[type(model)].insert(model)
        for model in self.dirty.values():
            self.repos[type(model)].update(model)
        for model in self.deleted.values():
            self.repos[type(model)].delete(model)


class UowedModel:
    def __init__(self, model, uow):
        self.__dict__["_model"] = model
        self.__dict__["_uow"] = uow

    def __getattr__(self, key):
        return getattr(self._model, key)

    def __setattr__(self, key, value):
        setattr(self._model, key, value)
        self._uow.register_dirty(self._model)
