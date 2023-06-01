# This code was modified from code generated with ChatGPT and it is not working

import ee
ee.Authenticate()

# Initialize the Earth Engine library
ee.Initialize()


# Get the asset roots for your account
asset_roots = ee.data.getAssetRoots()

# Loop through the asset roots to find the one associated with your account
for root in asset_roots['roots']:
    if root['id'] == 'users/Art-n-MathS':
        # Get the usage information for the account
        usage = root['quota']['usage']
        feature_vectors_used = usage['FEATURE_COLLECTION_ITEMS']
        print('Feature vectors used:', feature_vectors_used)
        break