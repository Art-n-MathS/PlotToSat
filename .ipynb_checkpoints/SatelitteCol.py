## @package SatelitteCol
#  @author  Dr Milto Miltiadou
#  @date  Mar 2023
#  @version 1.0

#  This is a base class from where all collections classes inherit from

class SatelitteCol: 
    ## The Constructor
    #  
    def __init__(self,startDate,endDate,geometry, masks):
        self.startDate = startDate
        self.endDate   = endDate

        # apply water and land mask
        # create forest lost mask 
        year = ee.Date(endDate).get('year') 
        masksHandler = Masks(geometry,masks)
        combinedMask = masksHandler.calculateCombinedMask() # all 1 if no masks loaded
        # defining a collection with None variable
        self.col = None 
        





    ## Method that takes as input a year and a collection and returns a collection
    #  of 12 images representing each calendar month. Each image contains the 
    #  pixelwise average of its corresponding calendar month
    # @param i_year The year of interest
    # @param col The colection to be intepreted 
    def byMonth(self,i_year,col):
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
        