import ee

# Trigger the authentication flow.
ee.Authenticate()

# Initialize the library.
ee.Initialize()

# this is a global variable
# buffer for surface water
buffer = 50
# buffer for forest loss
bufferFL = 30


# Load a map containing the global surface water
gsw = ee.Image('JRC/GSW1_0/GlobalSurfaceWater')
occurrence = gsw.select('occurrence')

# Load a land mask
landMask = ee.ImageC('CGIAR/SRTM90_V4').mask();    

print ("   ***   EXIT   ***")