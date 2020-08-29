__version__ = '1.0.0'
__author__ = 'Quanzhi(Allen) Bi'

from .cbapi import set_rapidapi_key
from .cbapi import get_people
from .cbapi import get_organizations

__all__ = ['cbapi']