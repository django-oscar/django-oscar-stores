from . import abstract_models
from oscar.core.loading import is_model_registered


__all__ = []


if not is_model_registered('stores', 'StoreAddress'):
    class StoreAddress(abstract_models.AbstractStoreAddress):
        pass

    __all__.append('StoreAddress')


if not is_model_registered('stores', 'StoreGroup'):
    class StoreGroup(abstract_models.AbstractStoreGroup):
        pass

    __all__.append('StoreGroup')


if not is_model_registered('stores', 'Store'):
    class Store(abstract_models.AbstractStore):
        pass

    __all__.append('Store')


if not is_model_registered('stores', 'OpeningPeriod'):
    class OpeningPeriod(abstract_models.AbstractOpeningPeriod):
        pass

    __all__.append('OpeningPeriod')


if not is_model_registered('stores', 'StoreStock'):
    class StoreStock(abstract_models.AbstractStoreStock):
        pass

    __all__.append('StoreStock')
