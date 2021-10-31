class Simulation(object):
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.__init__(*args, **kwds)
        return it

    def __init__(self, *args, **kwds):
        if 'car' in kwds:
            self.car = kwds['car']
        if 'trajet' in kwds:
            self.trajectoire = kwds['trajectoire']
        if 'bille' in kwds:
            self.bille = kwds['bille']
