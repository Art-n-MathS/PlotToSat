
### **** NOTE: THIS CLASS IS NOT WORKING *** ###

import sys

# check if GEE is already imported to avoid requesting authenticatiation multiple times
modulename = 'ee'
if modulename not in sys.modules: 
   # import GEE and Authenticate, token or log in will be asked from web browser
   import ee
   ee.Authenticate()
   ee.Initialize()
else:
   print('GEE already imported')
   # google earth engine already imported and authenticated

"""
modulename = 'ipynb_masks'
if modulename not in sys.modules:
    %run Masks.ipynb
    sys.modules['ipynb_masks'] = None
#else
    # module already loaded

modulename = 'ipynb_Utils'
if modulename not in sys.modules:
    %run Utils.ipynb
    # adding an identifier to sys.modules to avoiding loading the same file multiple times
    sys.modules['ipynb_Utils'] = None 
#else
   # Utils modules has already been loaded somewhere else
"""

modulename = 'py_SatelitteCol'
if modulename not in sys.modules:
    from SatelitteCol import SatelitteCol
    # adding an identifier to sys.modules to avoiding loading the same file multiple times
    sys.modules['py_SatelitteCol'] = None 
#else
   # Utils modules has already been loaded somewhere else

class Sentinel2(SatelitteCol):
    def __init__(self,startDate,endDate,geometry, masks):
        SatelitteCol.__init__(self,startDate,endDate,geometry, masks)
        print('hello')
    




