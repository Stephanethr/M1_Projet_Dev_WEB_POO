from item_class import Item


class Equipment(Item):
    def __init__(self, targs, stat):
        super().__init__(targs, stat)
        self._lClasses = targs['classList']
        self._place = targs['place']
