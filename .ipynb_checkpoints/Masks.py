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

modulename = 'py_Utils'
if modulename not in sys.modules:
    import Utils
    # adding an identifier to sys.modules to avoiding loading the same file multiple times
    sys.modules['py_Utils'] = None 
#else
   # Utils modules has already been loaded somewhere else


 
class Masks:
    # @param[in] self is this class
    # @param[in] geometry is a polygon
    # @param[in] self.gswBuffer is the pre-defined buffer used for surface water mask
    # @param[in] self.lmaskBuffer is the pre-defined buffer used for land surface mask
    # @param[in] self.forestMaskBuffer  is the pre-defined buffer used for forest loss
    # @param[in] self.aspectAscBuffer is the pre-defined buffer used for aspects ascending maps masks - recommended 0
    # @param[in] self.aspectDesBuffer  is the pre-defined buffer used for aspects descending maps masks - recommended 0
    def __init__(self,geometry,masks):
        self.gswBuffer = -1
        self.lmaskBuffer = -1
        self.forestMaskBuffer = -1
        self.aspectDesBuffer = -1
        self.aspectAscBuffer = -1
        self.forestYear = -1
        # aspects buffer will be 0 and not applied

        if ('gsw' in masks):
            self.gswBuffer = int(masks['gsw'])

        if ('lmask' in masks):
            self.lmaskBuffer = int(masks['lmask'])

        if ('aspectDes' in masks):
            self.aspectDesBuffer = int(masks['aspectDes'])

        if ('aspectAsc' in masks):
            self.aspectAscBuffer = int(masks['aspectAsc'])
                        
        if ('forestMask' in masks):
            tmp,self.startDate,self.endDate = masks['forestMask']
            #self.forestMaskBuffer = int(tmp)

        print(self.gswBuffer, self.lmaskBuffer, self.aspectDesBuffer, self.aspectAscBuffer, self.forestMaskBuffer, "+++++")

        self.dem = ee.Image('NASA/NASADEM_HGT/001').select('elevation').clip(geometry)
        self.aspect = ee.Terrain.aspect(self.dem)
       
        self.asc = (self.aspect.gt(202.5).And(self.aspect.lt(337.5)).And(self.aspect.eq(-1)))
        self.asc = Utils.filterSpeckles(self.asc,5,'circle')

        self.des = (self.aspect.gt(22.5).And(self.aspect.lt(157.5)).And(self.aspect.eq(-1)))
        self.des = Utils.filterSpeckles(self.des,5,'circle')
        # load ground surface water
        gsw = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').clip(geometry)
        self.occurrence = gsw.select('occurrence')
        # load a land mask
        self.landMask = ee.Image('CGIAR/SRTM90_V4').clip(geometry).mask()
        # Load Global Forest Change Data
        # "The Hansen et al. (2013) Global Forest Change dataset in Earth 
        # Engine represents forest change, at 30 meters resolution, globally, between 2000 and 2021."
        # These data are updated annually
        gfc2021 =ee.Image("UMD/hansen/global_forest_change_2021_v1_9").clip(geometry)
        # extract the band that gives me which year was each tree covered area lost
        self.lossYear = gfc2021.select(['lossyear']).clip(geometry)
        self.loss     = gfc2021.select(['loss'    ])
         
        self.startDisYear = 00
        self.endDisYear   = 21      
        self.combinedMask = ee.Image(1).clip(geometry)
        self.isCombineMaskCalculated = False
        self.geometry = geometry
       
    def updateNoSurfaceWaterMask(self,image):
        if(self.gswBuffer>0):
            gswMask = addBuffer(self.occurrence, self.gswBuffer).unmask(-999).eq(-999)
            return image.updateMask(gswMask)
        else:
            print("WARNING: Water mask not applied. Buffer needs to be > 0")
            return image

    def updateLandMask(self,image):
        if(self.lmaskBuffer>0):
           lmask = addBuffer(self.landMask, self.lmaskBuffer).add(1) 
           return image.updateMask(lmask)
        else : 
            print("WARNING: land mask not applied. Buffer needs to be > 0")
            return image

    def updateAscMask(self,image):
        return image.updateMask(self.asc)

            
    def updateDesMask(self,image):
        return image.updateMask(self.des) 

 
    def updateForestLostMask (self, image):   
        year = 2017
        yearNo = year - 2000
        YOI = self.lossYear.where(self.lossYear.gt(yearNo), 0)
        result = YOI.where(YOI.gt(0),1)
        resultUnmasked = result.unmask(0)
        return image.updateMask(addBuffer(result,self.forestMaskBuffer).unmask(-999).eq(-999))

    def getAscAspects(self):
        return self.asc
    
    def getDesAspects(self):
        return self.des

    def getAspects(self):
        return self.aspect

    ## @brief method that merges land surface and ocean/sea water into a single mask 
    # @brief buffer amount of meters to be added around the water areas 
    # @return the land mask of does not contain surface water
    def getNoSurfaceWaterMask (self,buffer):
        # Load a map containing the global surface water
        return  addBuffer(self.occurrence, buffer).unmask(-999).eq(-999)

    ## method that return land mask
    # buffer amount of meters to be added around the water areas 
    # @return the land mask of does not contain surface water
    def getlandMask (self,buffer):     
        return addBuffer(self.landMask, buffer).add(1)

    def getForestLostMask (self, startdate,enddate,buffer):
        startyear = ee.Date(startdate).get('year') 
        endyear   = ee.Date(enddate  ).get('year') 
        startyearNo = startyear.subtract(2000)
        endyearNo   = endyear.subtract(2000)

        YOI = self.lossYear.where(self.lossYear.gt(endyearNo), -1)
        YOI = YOI.where(YOI.lt(startyearNo),0)        
        YOI = YOI.where(YOI.gt(startyearNo),1)
        # buffer is required to clear previous history before unmasking 
        return addBuffer(YOI,buffer).unmask(-999).eq(-999)

    ## method that merges land surface and ocean/sea water into a single mask 
    # buffer amount of meters to be added around the water areas 
    # @return the land mask of does not contain surface water
    def getNoSurfaceWaterMaskNoBuffer (self):
        # Load a map containing the global surface water
        return  self.occurrence.unmask(-999).eq(-999)

    ## method that return land mask
    # buffer amount of meters to be added around the water areas 
    # @return the land mask of does not contain surface water
    def getlandMaskNoBuffer (self):     
        return self.landMask.add(1)


    ## Method that create a composite mask according to the input provided in the constructors
    def calculateCombinedMask(self):
        self.combinedMask = ee.Image(1).clip(self.geometry)
        
        if (self.gswBuffer>0):
            self.combinedMask = self.combinedMask.And(self.getNoSurfaceWaterMask(self.gswBuffer))

        if (self.lmaskBuffer>0):
            self.combinedMask = self.combinedMask.And(self.getlandMask(self.lmaskBuffer))

        #if (self.forestMaskBuffer>0):
        #    self.combinedMask = self.combinedMask.And(self.getForestLostMask(self.startDate,self.endDate,self.forestMaskBuffer))
        
        if (self.aspectDesBuffer==0):
            self.combinedMask = self.combinedMask.And(self.des)
        
        if (self.aspectAscBuffer==0):
            self.combinedMask = self.combinedMask.And(self.asc)

        self.isCombineMaskCalculated = True
        return self.combinedMask


    def updateCombinedMask(self,image):
        return image.updateMask(self.combinedMask)


    def exportCombinedMaskToDrive(self,scale,description,folder,projection):
        if (not self.isCombineMaskCalculated):
            self.calculateCombinedMask()
        # else:
        #   combined mask has already been calculated
        #print(self.geometry.getInfo()['coordinates'])
        
        print("STARTING BATCH SCRIPT FOR EXPORTING FILE")
        task = ee.batch.Export.image.toDrive(**{
            'image' : self.combinedMask,
            'description' : description,
            'folder' : folder,
            #'crs' : projection,
            'region': self.geometry.getInfo()['coordinates'],
            'scale': scale,
            'maxPixels': 1549491660
        })
        task.start()
        
        print("***END OF CALLING BATCH SCRIPT")
        


print("Masks class imported")