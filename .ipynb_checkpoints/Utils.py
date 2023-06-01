import sys

# check if GEE is already imported to avoid requesting authenticatiation multiple times
modulename = 'ee'
if modulename not in sys.modules: 
   # import GEE and Authenticate, token or log in will be asked from web browser
    import ee
    ee.Authenticate()
    ee.Initialize()
#else:
   # google earth engine already imported and authenticated



## Function that adds a buffer around a given raster
# image: imported raster to be buffered 
# buffer: number of meters to add around the given raster
def addBuffer (image, buffer):
    if (buffer == 0):
       print("ERROR: Utils: Buffer must not be equal to zero")     
       exit(1)
    return ee.Image(1).cumulativeCost(image, buffer, True)
  
  


## This is a function that takes as input an image and applies a circlular 
# median filter with kernel size 3x3
# @param[in] img: image to be filtered
# @returns the filtered image
def filterSpeckles3x3 (img):
    #Apply a focal median filter
    return img.focalMedian(3,'circle','pixels').copyProperties(img, ['system:time_start'])

## This is a function that takes as input an image and applies a median filter 
# @param[in] img: image to be filtered
# @param[in] filterSize: size of filter to be applied e.g. 3 implies 3x3
# @param[in] filterShape: the shape of the filter. Options include: 'circle', 'square', 'cross', 'plus', octagon' and 'diamond'
# @returns the filtered image
def filterSpeckles (img, filterSize,filterShape):
    #Apply a focal median filter
    return img.focalMedian(filterSize,filterShape,'pixels').copyProperties(img, ['system:time_start'])





# @brief method that takes as input a collection, calculates pixelwise average for each month and returns a new collection
# @param[in] collection : the collection to be processed
# @return a collection annual monthly average pixel values

## Method that takes as input a year and a collection and returns a collection
#  of 12 images representing each calendar month. Each image contains the 
#  pixelwise average of its corresponding calendar month
# @param i_year The year of interest
# @param col The colection to be intepreted 
def byMonth(i_year,col):
    startDate = ee.Date.fromYMD(i_year, 1, 1)
    endDate = startDate.advance(1, 'year')
    tmpCol = col.filter(ee.Filter.date(startDate, endDate))
    return  ee.ImageCollection.fromImages(ee.List([
    (tmpCol.filter(ee.Filter.calendarRange( 1,  1, 'month')).mean().set('month', 1)),
    (tmpCol.filter(ee.Filter.calendarRange( 2,  2, 'month')).mean().set('month', 2)),
    (tmpCol.filter(ee.Filter.calendarRange( 3,  3, 'month')).mean().set('month', 3)),
    (tmpCol.filter(ee.Filter.calendarRange( 4,  4, 'month')).mean().set('month', 4)),
    (tmpCol.filter(ee.Filter.calendarRange( 5,  5, 'month')).mean().set('month', 5)),
    (tmpCol.filter(ee.Filter.calendarRange( 6,  6, 'month')).mean().set('month', 6)),
    (tmpCol.filter(ee.Filter.calendarRange( 7,  7, 'month')).mean().set('month', 7)),
    (tmpCol.filter(ee.Filter.calendarRange( 8,  8, 'month')).mean().set('month', 8)),
    (tmpCol.filter(ee.Filter.calendarRange( 9,  9, 'month')).mean().set('month', 9)),
    (tmpCol.filter(ee.Filter.calendarRange(10, 10, 'month')).mean().set('month',10)),
    (tmpCol.filter(ee.Filter.calendarRange(11, 11, 'month')).mean().set('month',11)),
    (tmpCol.filter(ee.Filter.calendarRange(12, 12, 'month')).mean().set('month',12))]))

## Method that removed a given period from the dataset
# @param startDate The starting date of the period to be removed
# @param endDate   The ending date of the period to be removed
# @param col       The collection to be interpreted
# @return The new collection that does not contain the removed period
def removePeriod(self,startDate, endDate, col):
    badDataFilter = ee.Filter.date(startDate,endDate)
    print("Period from ", startDate, " to ", endDate, " removed")
    return col.filter(badDataFilter.Not())







