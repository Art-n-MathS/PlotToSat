---
author:
- Milto Miltiadou[^1]
- Stuart Grieve
- Paloma Ruiz Benito
- Verónica Cruz-Alonso
- Julen Astigarraga
- Julián Tijerín Triviño
- Emily Lines
bibliography:
- Bibliography.bib
date: 30/08/2023
title: "**User Guide of PlotToSat**"
---

::: titlepage
:::

# License {#License}

PlotToSat is released under the GNU General Public Licence, Version 3.
The full description of the usage licence is available
here:[\<https://github.com/Art-n-MathS/PlotToSat/blob/main/License.txt\>](<https://github.com/Art-n-MathS/PlotToSat/blob/main/License.txt>){.uri}

The following paper should be cited in every publication using
PlotToSat: Miltiadou, M., Grieve, S., Ruiz-Benito, P., Astigarraga, J.,
Cruz-Alonso, V., Triviño, J.T., and Lines, E. (2024) PlotToSat: A Tool
for Generating Annual Time-Series from Sentinel-1 and Sentinel-2 at Each
Plot Within a Plot Network for Machine Learning Applications *Computers
& Geosciences*

Link to paper: [\<url\>](<url>){.uri}

The sample data are randomly created; they are well-distributed and lie
within Peninsular Spain.

# Introduction {#sec:Introduction}

## Motivation

Forest ecologists often gather data from predetermined sites known as
plots during fieldwork. These plots are usually circular and are defined
by a geo-location and a radius. Analysing data from these plots helps
ecologists gain a better understanding of ecosystem services and
dynamics. Many studies have incorporate Earth Observation (EO) data,
which includes satellite images and other remote sensing data, to
enhance their understanding of ecosystems. EO data provides valuable
information about various environmental factors on a larger scale, but
accessing and downloading these images can be time-consuming and
challenging, particularly when dealing with a large number of plots.

To address this issue and enhance scalability of ecosystem studies, we
have developed the tool 'PlotToSat.' PlotToSat is designed to bridge the
gap between plot-based data and Earth Observation data. PlotToSat aims
to make the process of extracting EO data at thousands of plot locations
more efficient and simplified. It will enable ecologists to better
analyse the relationships between local plot data and broader
environmental patterns.

## Software Functionality

\*\*\* PlotToSat takes as input from a few to hundred of thousands of
plot data located across various geographical regions and exports Earth
Observation data from multiple collections at each plot. Identifiers are
added to both plot and exported data and a script is provided for fusing
them so that plot names are retained. \"PlotToSat\" first computes the
pixelwise mean value for each calendar month, effectively reducing each
collection to twelve images; each image has multiple bands but each
image corresponds to the mean of a specific month. Following this, it
calculates the mean and standard deviation of the pixel values within
each plot. For every plot, the function exports twelve values per band
per collection corresponding to the twelve calendar months for. This
procedure **creates a spectral-temporal signature for each plot.**
Spectral-temporal signatures are important because they capture both the
temporal and spectral dimensions at each plot. This opens up
possibilities for phenological and time-series related studies. Standard
deviation is also provided for quality control. Figure
[5](#fig:workflow){reference-type="ref" reference="fig:workflow"} shows
the back-end processing workflow of the system, while Figure
[4](#fig:SPS){reference-type="ref" reference="fig:SPS"} depicts a
spectral-temporal signature of a plot extracted using PlotToSat. \*\*\*

![To define masks the user needs to first create a dictionary with the
masks of their interest and then import it into the Manager as shown in
this figure](img/ProcesingPipelinePlotToSAT.jpg){#fig:processingPipeline
width="90%"}

<figure id="fig:SPS">
<figure id="fig:SP1">
<img src="./img/SpectralTemporalExample.jpg" />
<figcaption>Example of Spectral Temporal Signature derived from
Sentinel-2 data with focus on the temporal aspect / annual phenology per
band</figcaption>
</figure>
<figure id="fig:SP2">
<img src="./img/SpectralTemporalExample2.jpg" />
<figcaption>Example of spectral-temporal Signature derived from
Sentinel-2 data with focus on the spectral aspect / spectral signature
per calendar month</figcaption>
</figure>
<figcaption>An illustrative example of a spectral-temporal signature at
a plot extracted using PlotToSat</figcaption>
</figure>

Figure [5](#fig:workflow){reference-type="ref" reference="fig:workflow"}
shows the user-interface. The user-interface is divided into four main
steps, along with two additional optional steps:

-   Step 1: Define the essential input parameters. These parameters
    include: (1) a .csv file containing the plot data, (2) the radius of
    the plot data, (3) the projection of the plot data, and (4) a
    geometry defining the study area.

-   Optional Step 1: After Step 1, users can decide whether to apply any
    of the available masks (aspects, surface water, forest disturbance,
    and land mask) to the selected collections.

-   Step 2: PlotToSat currently supports two EO collections (Sentinel-1
    and Sentinel-2). Users can choose to use one or both of these
    collections.

-   Step 3: Define the outputs; the system exports a spectral temporal
    signature for each plot and each collection into multiple .csv
    files, which are then stored on the user's Google Drive.

-   Step 4: Download the folder containing the exported .csv files from
    Google Drive and merge them using the provided script.

-   Optional Step 2: \*\*\* Tuning provided parameters to tackle
    potential errors that predominantly may occur because Google Earth
    Engine distributes processing power among its users by implementing
    processing limitations. Consequently, while users may face three
    potential errors, we also provide them with suggested solutions
    e.g., defining how many plots will be exported in each file in Step
    3.

![User's workflow of the system](img/PlotToSatDiagram.jpg){#fig:workflow
width="\\textwidth"}

This guide is designed to cater to the needs of various users. In a few
words, the user guide starts with essential information on how to
extract information from satellite data at plot locations and gradually
progresses to more technical details. In Section
[3](#sec:Installation){reference-type="ref"
reference="sec:Installation"}, the system's prerequisites are provided.
Section [4](#sec:instructions){reference-type="ref"
reference="sec:instructions"} first presents the necessary commands
required to achieve desirable results. These commands are divided into
six sections that correspond to the four main steps plus the two
optional ones explained above and depicted in the workflow diagram
(Figure [5](#fig:workflow){reference-type="ref"
reference="fig:workflow"}). Section
[6](#sec:Techical){reference-type="ref" reference="sec:Techical"} offers
background information and outlines the pre-processing steps employed
for each currently supported EO collection. It further explains the
selection of available masks. The collections, masks, and the Utils
module can be used as part of the main system or independently for other
applications. For this reason, Section
[6](#sec:Techical){reference-type="ref" reference="sec:Techical"}
provides an overview of the system architecture; how the modules are
interconnected to assist more experienced users.

# Installation {#sec:Installation}

This user guide assumes basic knowledge of Google Earth Engine and
Python. It also assumes that users have an account at
[\<https://code.earthengine.google.com/\>](<https://code.earthengine.google.com/>){.uri}.

PlotToSat is implemented using the Python API of Google Earth Engine in
IPython 3 (Jupyter). While Visual Studio Code (VS Code) is recommended
due to its status as a free, open-source, and cross-platform editor,
other IDEs should also function well.

The code is compatible with both Linux and Windows machines and is
available at:
[\<https://github.com/Art-n-MathS/PlotToSat\>](<https://github.com/Art-n-MathS/PlotToSat>){.uri}

Depending on your environment, you can install the dependencies as
follows:

              pip install ipython pandas numpy earthengine-api

              conda install -c conda-forge earthengine-api ipython pandas numpy

# Instructions: How to extract spectral-temporal signatures at plot locations  {#sec:instructions}

The system is modular, consisting of multiple classes, yet the user's
interaction is primarily with the Manager class. As explained in Section
[7](#sec:Advanced){reference-type="ref" reference="sec:Advanced"}, each
class can function autonomously for other applications. In this section,
the commands for extracting EO data at plot locations are supplied.

\*\*\*To demonstrate the simplicity of PlotToSat, \*\*\* Figure
[6](#fig:EssentialCode){reference-type="ref"
reference="fig:EssentialCode"} provides an example script encompassing
the essential commands requiring user definition to acquire from
multiple plots. It contains steps 1, 2 and 3 depicted in the workflow
(Figure [5](#fig:workflow){reference-type="ref"
reference="fig:workflow"}) and explained in Sections
[4.1](#sec:defPar){reference-type="ref" reference="sec:defPar"},
[4.2](#sec:addCols){reference-type="ref" reference="sec:addCols"} and
[4.3](#sec:defOuts){reference-type="ref" reference="sec:defOuts"}
respectively. \*\*\*The code is broken down and explained in Sections
[4.1](#sec:defPar){reference-type="ref" reference="sec:defPar"},
[4.2](#sec:addCols){reference-type="ref" reference="sec:addCols"} and
[4.3](#sec:defOuts){reference-type="ref" reference="sec:defOuts"}.
\*\*\* Section [4.4](#sec:mergingFiles){reference-type="ref"
reference="sec:mergingFiles"} explains how to merge the files exported
and an example script is also provided in that section. Sections
[4.5](#sec:maskscript){reference-type="ref" reference="sec:maskscript"}
and [4.6](#sec:errors){reference-type="ref" reference="sec:errors"}
provide the optional options and a complete example is provided after
these sections.

![A complete example script for extracting EO data at plot locations
using PlotToSat. The code is broken down and explained in Sections
[4.1](#sec:defPar){reference-type="ref" reference="sec:defPar"},
[4.2](#sec:addCols){reference-type="ref" reference="sec:addCols"} and
[4.3](#sec:defOuts){reference-type="ref" reference="sec:defOuts"}
](img/EssentialCode.jpg){#fig:EssentialCode width="75%"}

## Definition of input parameters {#sec:defPar}

The working directory should match the location of the .ipynb files for
PlotToSat. To begin, generate a new .ipynb file and **run
\"Manager.ipynb\"** to **import all the necessary libraries** as follow:

           %run Manager.ipynb

As mentioned earlier, users engage with the Manager only. To establish a
Manager instance, you'll require three inputs:

1.  A polygon that defines the study area

2.  A dictionary that contains all the relevant information about the
    field data

3.  The specific year for exporting the spectral-temporal signatures

**Definition of Study area**: Defining the study area is crucial to
prevent processing an excessive amount of unnecessary data. This is
accomplished by providing a polygon. Two examples are given. The initial
example retrieves a database containing all countries and designates
Spain as the area of interest:

           countries = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017')
           polygon = countries.filter(ee.Filter.eq('country_na', 'Spain'))

The second example employs a series of coordinates to define a polygon.
This polygon was generated using the \"Draw Shape\" feature in the
Graphical User Interface (GUI) of Google Earth Engine. The shape created
was saved in the Imports section, where the corresponding JavaScript
code is provided (See example at Figure
[7](#fig:GEEPol){reference-type="ref" reference="fig:GEEPol"}). To
translate this JavaScript code into Python API code, the \"var\"
declaration, the color-related code enclosed between \"/\*\" and
\"\*/\", and the semicolon \";\" at the end were omitted. The result is
as follows:

           polygon = ee.Geometry.Polygon(
                  [[[33.14051796676924, 35.11082029560011],
                  [32.90980507614424, 35.07486329511283],
                  [32.96473671676924, 34.948889010363565]]])

![How to find the coordinates of a drawn polygon on Google Earth
Engine](img/GettingPolygon.jpg){#fig:GEEPol width="75%"}

**Create a dictionary that holds the relevant plot information.** The
\"csvfilename\" parameter specifies the name and directory path of the
file containing the plot data in .csv file format. The \"proj\"
parameter designates the projection used for the plot data. \*\*\* The
'radius' parameter determines the radius of each plot, and the unit of
measurement is in meters as is the case with all distances measured in
Google Earth Engine. \*\*\* The \"xcol\" and \"ycol\" parameters
indicate the columns supplying the x and y coordinates, respectively, of
the centre of each plot. All these parameters are mandatory. Here is an
example of defining them:

           fieldData = {
                  "csvfilename"   : "./samplePlots.csv",
                  "proj"          :"EPSG:3042",
                  "radius"        :30,
                  "xcol"          :"CX",    
                  "ycol"          :"CY"
           }

**Specify the year of interest.** PlotToSAT processes data for a single
year in each run. The desired year of interest must be defined and
imported into the constructor of the Manager class. In the code snippet
below, we define a variable that contains a potential year of interest.

           year = 2017

Once the three inputs are defined as explained above, you can **create
an instance of the Manager** as follows:

           myManager = Manager(polygon,fieldData,year)

## Adding Earth Observation collections {#sec:addCols}

Once the Manager is constructed, the user can add the collections of
their interest. If the available collections are not known, the
following command can be utilised. It prints the available collections,
their call labels, and the GEE collections to be fetched:

           myManager.printAvailableCollections()

This should yield the following outcome since the system currently
supports two collections:

           There are  2 collections available within the system:
           label                   collection
           0  sentinel-1            COPERNICUS/S1_GRD
           1  sentinel-2  COPERNICUS/S2_SR_HARMONIZED

The users select collections using the function
addCollection(\<labelOfCollection\>, \<parameter\>). As previously
stated, the system currently supports two collections: Sentinel-1 and
Sentinel-2, with the respective labels 'sentinel-1' and 'sentinel-2'.
The \<parameter\> argument varies for each collection. For Sentinel-2,
it's an integer that defines the cloud coverage. It's worth mentioning
that additional cloud and shadow masking is applied to all images, as
explained in Section [6.2](#sec:s2){reference-type="ref"
reference="sec:s2"}. For Sentinel-1, the input parameter is a Boolean
value (True or False), which determines whether the aspect maps will be
applied; if the elevation gradient is high, shaded areas usually appear
on certain slopes. These shaded areas may be masked out using the aspect
map (further details are provided in Section
[6.1](#sec:s1){reference-type="ref" reference="sec:s1"}).

Users have the choice to use either one or both collections. \*\*\* Here
is an example of how to add both collections to the Manager with aspect
filters for Sentinel-1 and a threshold of 50% cloud coverage for
Sentinel-2:\*\*\*

           myManager.addCollection("sentinel-1", True) 
           myManager.addCollection("sentinel-2", 50  ) 

## Definition and exportation of outputs {#sec:defOuts}

Finally, we execute the following command to retrieve, interpret, and
export the spectral-temporal signatures as feature vectors. The
\"exportFeatures\" command requires two inputs: (1) the folder name
where the data will be exported on the user's Google Drive, and (2) the
starting name for the exported feature vectors. If the specified folder
does not already exist, GEE will create it. It's important to note that
GEE is unable to generate subfolders.

            myManager.exportFeatures("gdrivefolder", "outfeaturevectors")   

By executing the above command, a series of .csv files will be generated
within the \"gdrivefolder\" of the user's Google Drive. The system
divides the process into multiple subprocesses, producing multiple
output files, to mitigate possible errors, as explained in Section
[4.6](#sec:errors){reference-type="ref" reference="sec:errors"}. For
instructions on merging the series of .csv files, please refer to
Section [4.4](#sec:mergingFiles){reference-type="ref"
reference="sec:mergingFiles"}.

The essential commands described so far for exporting spectral-temporal
signatures from Sentinel-1 and Sentinel-2 collections at plot locations
are provided in a complete script in Figure
[6](#fig:EssentialCode){reference-type="ref"
reference="fig:EssentialCode"}.

## Downloading and merging exported files {#sec:mergingFiles}

This section focuses on the merging of multiple files generated by the
system into a single file. As mentioned in Section
[4.3](#sec:defOuts){reference-type="ref" reference="sec:defOuts"}, the
user specifies the name of a folder to which the generated .csv files
are exported. Users need (1) to download this folder from their Google
Drive and unzip its contents. Please note that, sometimes, GEE may
create two folders with the same name and distribute the generated .csv
files across both folders. This occurs due to GEE's concurrent data
processing. In such cases, users must download both folders and merge
their contents before proceeding with the script for file merging.

Additionally, users should: (2) Locate the exported files named
\"FieldDataWithIdentifiers.csv\" and \"SamplingSize.txt\". These files
are created in the same locations as the .ipynb files within the
PlotToSat framework. The first file duplicates the imported plot data
but includes an additional column labeled \"indexField\", which contains
identifiers used for merging the plot data with the exported EO data.
The second file contains the number of plots interpreted in each
iteration. Please note that the corresponding exported .csv files may
have fewer columns due to masked-out or defective pixels.

The merging script assumes that no errors occurred during the
exportation process and that the user intends to merge all the .csv
files into a single file. Figure
[8](#fig:MergingCsvFiles){reference-type="ref"
reference="fig:MergingCsvFiles"} provides an illustrative overview of
how the data is vertically and horizontally merged into a single .csv
file and Figure [9](#fig:MergingCode){reference-type="ref"
reference="fig:MergingCode"} provides a complete code example of how to
merge the exported .csv files. It's important to note that there might
be occasions when certain processes fail or the user wishes to merge
specific exported files. In such cases, users have the option to utilise
the dataframes provided by the pandas Python library to merge the files.

![Ways of merging exported .csv files: vertically and
horizontally](img/MergingCsvFiles.jpg){#fig:MergingCsvFiles width="55%"}

![This is a complete example script demonstrating how to merge all the
exported .csv files into one](img/MergingCode.jpg){#fig:MergingCode
width="90%"}

## Available masks {#sec:maskscript}

\*\*\* The following masks may be applied; ground surface water, land,
forest loss, ascending aspects and/or descending aspects. Section
[6.3](#sec:masks){reference-type="ref" reference="sec:masks"} provides
technical information about those masks with examples, while this
section focuses on how to use PlotToSat to apply them before extracting
EO information at plot locations. As shown in Figure
[10](#fig:setMasks){reference-type="ref" reference="fig:setMasks"}, the
user creates a dictionary containing the masks of interests. The
dictionary may contain from zero to multiple masks. Then the masks are
added to an instance of the class Manager. For example, in Figure
[10](#fig:setMasks){reference-type="ref" reference="fig:setMasks"}
\"myManager\" is an instance of the class Manager and \"myMasks\" is a
dictionary created containing the masks of the user's interests. The
user can use the command \"myManager.setMasks(myMasks) to set the masks
of interest. The chosen masks will be applied to all the EO collections
added to the system (Section [4.2](#sec:addCols){reference-type="ref"
reference="sec:addCols"}).

![To define masks the user needs to first create a dictionary with the
masks of their interest and then import it into the Manager as shown in
this figure](img/SetMasks.jpg){#fig:setMasks width="50%"}

To define a dictionary of masks, for each mask of interest you need (1)
its corresponding label (Table [1](#tab:Masks){reference-type="ref"
reference="tab:Masks"}) and (2) a buffer value. The buffer value defines
how much buffer will be added around the edges of the area to be
removed. To define the forest loss mask, a dictionary is required as
input; the dictionary should contain the start and end date of the
forest loss of interest, along with the buffer. Regarding the Descending
and the Ascending Aspects the buffer value must always be zero as a
median filter has already been applied and the segments of the aspects
are small so adding buffers could results into very little to no data
retained. Additionally, Descending and Ascending Masks should never be
applied simultaneously, as they have no overlap. If the user wants to
apply Ascending masks to the ascending Sentinel-1 data and Descending
masks to the descending Sentinel-1 data then the option provided in
Section [4.2](#sec:addCols){reference-type="ref"
reference="sec:addCols"} should be used while adding the Sentinel-1
collection to the Manager (i.e., myManager.addCollection(\"sentinel-1\",
True), where \"True\" implies using the aspects maps). Table
[1](#tab:Masks){reference-type="ref" reference="tab:Masks"} summarises
the inputs parameters of each available masks.

:::: center
::: {#tab:Masks}
  Mask                        label             Input Parameters
  ---------------------- ---------------- -----------------------------
  Ground surface water       \"gsw\"               \<buffer\>
  Land mask                 \"lmask\"              \<buffer\>
  Forest loss mask        \"forestMask\"     { 'buffer': \<buffer\>
                                           \"startDate\":\<startDate\>
                                            \"endDate\":\<endDate\>}
  Descending Aspects      \"aspectDes\"                 0
  (22.5-157.5)                            
  Ascending Aspects       \"aspectAsc\"                 0
  (202.5-337.5)                           

  : Available masks that can optionally be loaded to the system and
  applied to all chosen collections
:::
::::

Here is an example of how the user can define a surface mask with 30
meter buffer, a land surface mask with 30 meter buffer and a forest loss
mask from 2000 till 2017 with a 30 meter buffer. The masks dictionary,
named \"masks\" is then added to the instance of the Manager, named
\"myManager\". \*\*\*

           masks = {
                  "gsw": 30, 
                  "lmask": 30, 
                  "forestMask": {
                         "buffer":30, 
                         "startDate":'2000-01-01', 
                         "endDate":'2017-12-31'
                  }
           } 
           myManager.setMasks(masks)

The use of masks is presented in the complete code example depicted in
Figure [11](#fig:Code2){reference-type="ref" reference="fig:Code2"}.
This example code also includes examples on how to address potential
errors, as explained in Section [4.6](#sec:errors){reference-type="ref"
reference="sec:errors"}.

![A complete example script containing the optional
features](img/Code2.jpg){#fig:Code2 width="83%"}

## Dealing with potential errors {#sec:errors}

There are three \*\*\* known \*\*\* errors that you may encounter while
running PlotToSat:

1.  \"Maximum recursion depth exceeded in comparison\"

2.  \"Function() too deeply nested\"

3.  \"Computation timed out\"

The first two errors are closely associated, but the first will appear
when executing the iPython script, while the second will arise when
executing the batch script on the Tasks tab in GEE. Recursion is a
programming technique where a function calls itself directly or
indirectly to solve a problem. The \"Maximum recursion depth exceeded\"
error happens when a recursive function calls itself excessively,
surpassing the allocated memory for function calls within the program's
call stack. This error is often addressed by rewriting the code in an
iterative manner. However, it's important to note that GEE is a
functional programming language, intended to work with recursive
functions.

\*\*\* The primary solution implemented in PlotToSat is to subset the
imported plots, process those subsets iteratively and export them into
multiple files but the user may also increase the recursion depth.

There are two parameters to the provided solutions that the user may
tune. (1) Increasing the maximum recursion depth of the system enables
the system to process more data within a single subset, but it may
result in slowdowns or even crashes. If you choose to use this option,
it's important to understand its associated risks. The code for
increasing the maximum depth as follows:

           import sys
           sys.setrecursionlimit(n)

where 'n' represents the new recursion depth/limit. The default value is
1000, which is retrievable using the function
\"sys.getrecursionlimit()\".

\(2\) By deafault PlotToSat divides the plots into subsets. The default
number of plots per subset is 400. The user may increase this number to
reduce the number of batch script used as follow:

           myManager.setSampling(n)

where 'n' represents the number of plots that will be included in each
subset.

Increasing the number of plot per subsets is advantageous due to the
allocation of 3000 free batch scripts per user. Each subset processed
through PlotToSat generates a .csv file, consuming one batch script. In
cases of batch script exhaustion, users can initiate new academic
projects, granting an additional 3000 free batch scripts. Excessively
increasing this value may result in the previously mentioned errors. We
recommend extracting a subset of the plot data into a .csv file and
conducting tests, starting with 1000 plots per subset and adjusting this
number up or down to assess system compatibility until optimal tuning is
achieved. We advise against running this test on the entire dataset to
avoid unnecessary consumption of cloud resources and batch
scripts.\*\*\*

The final potential error occurs when a batch process is too large.
According to GEE's definition, a batch script can run for up to 5 days.
However, GEE aims to distribute resources evenly among users. Therefore,
if a user attempts to export an excessive amount of data, they might
encounter this error. If some of the .csv files fail to be exported, the
provided option of merging all the exported data into a single .csv file
will also fail. In such a case, it is recommended that the user
identifies the missing data and rerun only that specific dataset instead
of the entire dataset (to prevent excessive resource usage).
Subsequently, the user may need to merge the results using the
horizontal and vertical options from the pandas Python library or an
equivalent method.

The commands for tuning the errors are demonstrated in the complete code
example provided in Figure [11](#fig:Code2){reference-type="ref"
reference="fig:Code2"}.

# Outputs: What do I get and what does it mean {#sec:outputs}

\*\*\* In PlotToSat the mean of each month is taken, and twelve temporal
instances are provided for each band corresponding to each calendar
month. A unique prefix is added to the existing band names, representing
the months from 0 to 11, which correspond to January through December
respectively. **Each column name has the form A_B. The A part indicates
the temporal information of the signature and the part B the spectral
information of the signature.** For instance, \"0_B11\" designates band
B11 for the month of January. Each row within the exported .csv file
corresponds to a plot.

\*\*\* Figure [12](#fig:OutputExample){reference-type="ref"
reference="fig:OutputExample"} depicts how the multiple files are
initially exported along with the \"MergeCsvs\" folder that is created
once the provided script for merging them is applied. As shown on the
left-hand side of the image, there is a list of .csv files. These files
are an example of the potential outputs of PlotToSat exported on Google
Drive. The user needs to download the relevant folder and extract it.
\*\*\* Once the script for merging the files is executed, a folder named
\"MergedCsvs\" is generated. This folder contains two files: (1) The
first one contains the mean values of the pixels located inside each
plot, while (2) the second one contains their corresponding standard
deviation. \*\*\* In these files, the plot names and all the relevant
field information are retained, along with the spectral-temporal
signatures extracted from the selected collection(s). In the figure, the
\"CX\" and \"CY\" columns originate from the plot data and indicate the
geographical location of the plot centres. The data labelled as
\"0_VHAsc\" and \"0_VHDes\" are collected from the Sentinel-1 dataset.
The number \"0\" corresponds to the calendar month of January, \"VH\"
refers to polarisation, and \"Asc/Des\" stands for Ascending and
Descending orbit respectively. Similarly, in the Sentinel-2 dataset,
'0_B11' implies the mean value of band B11 during the month of January.

![ An example of how the data are exported. Once the script for merging
the data is run, the folder \"MergedCsvs\" is
created.](img/OutputExample.jpg){#fig:OutputExample width="\\textwidth"}

# Background information about available collections and masks {#sec:Techical}

In this section, we present background information, theoretical
concepts, and pre-processing steps concerning the collections and
selection of masking. Background information is provided to explain the
rationale behind the chosen pre-processing steps and decisions.

## Sentinel-1 {#sec:s1}

The Sentinel-1 mission comprises a constellation of two satellites that
gather C-band SAR (Synthetic Aperture Radar) data, offering a joint
revisit period of 6 days and a resolution of 10 metres. SAR systems are
active sensors that operate using microwave wavelengths. They emit
pulses sideways and gather information by measuring the round-trip time.
The selected wavelengths that these systems employ provide the advantage
of operating under various weather conditions; the acquired data are
minimally affected by clouds, illumination, and other atmospheric
conditions. In contrast to LiDAR, SAR data can penetrate through objects
and provide insights into the water content of trees and their
dielectric constant [@ahern1993seasonal].

PlotToSat uses the 'COPENICUS/S1_GRD' collection from GEE. Within this
collection, the data have undergone pre-processing using the Sentinel-1
Toolbox. According to the collection description, Thermal noise removal,
Radiometric calibration, and Terrain correction have been carried out.
It's worth noting, however, that SAR data contain speckle noise, which
appears in the images as \"salt-and-pepper\" artifacts
[@dasari2015importance]. Multiple filters have been developed to
mitigate speckle noise, but it's worth noting that due to the prior
ortho-rectification performed, some speckle noise has been blended into
neighbouring pixels. Regardless of this, a median filter is applied to
reduce the impact of the noise. Since PlotToSat is primarily developed
for forest research, the median filter is chosen because many other
filters focus on enhancing edges that are hard to find in a forest
canopy. Despite its simplicity, the median filter is well-suited for
forest structures as it reduces speckles without blending noise or
attempting to enhance features that hardly exist within a forest
[@miltiadou2022selection].

Additionally, an aspect not to be overlooked is the presence of shaded
areas in the SAR data. Given that SAR systems emit sidewise, many slopes
in mountainous regions often appear dark. To address this concern, one
solution involves the removal of these shaded regions through the
application of aspect maps derived from a digital elevation model. In
the PlotToSat framework, we leverage elevation data sourced from the
\"NASA/NASADEM_HGT/001\" collection. The slopes of the north-east, east,
and south-east directions (ranging from 22.5° to 157.5°) should align
with the non-shaded areas of the Ascending data. Similarly, the slopes
of the south-west, west, and north-west directions (ranging from 202.5°
to 337.5°) should align with the non-shaded Descending data
[@miltiadou2022selection].

Table [2](#tab:aspects){reference-type="ref" reference="tab:aspects"}
illustrates the selection of these non-shaded regions within a
mountainous expanse in Spain. However, researchers must take into
consideration whether they wish to mask the Ascending and Descending
data according to the morphology of the study area. While adding the
Sentinel-1 collection into the Manager of PlotToSAT using the
\"addCollection(\<collectionLabel\>,\<parameter\>)\" function, the
option to enable (True) or disable (False) this feature exist using the
\<parameter\> input option. A practical example is given Section
[4.2](#sec:addCols){reference-type="ref" reference="sec:addCols"}.\"

:::: center
::: {#tab:aspects}
   Sentinel-1 Image    Selected Aspects        Output
  ------------------ --------------------- --------------
     VV Ascending      22.5^o^--157.5^o^    Masked Image
                                           
    VV Descending     202.5^o^--337.5^oo^   Masked Image
                                           
     VH Ascending      22.5^o^--157.5^o^    Masked Image
                                           
    VH Descending     202.5^o^--337.5^oo^   Masked Image
                                           

  : This table shows examples of removing shaded areas from the SAR data
  using the corresponding aspects
:::
::::

SAR signals also reflect high in the presence of moisture, making them
highly sensitive to land surface water. To overcome this limitation when
seeking to understand forest structure, an option for a land surface
water mask is available. Technical details can be found in Section
[6.3](#sec:masks){reference-type="ref" reference="sec:masks"}, while
Section [4.5](#sec:maskscript){reference-type="ref"
reference="sec:maskscript"} provides an explanation on how to utilise
the masks in PlotToSat.

The interpretation of Sentinel-1 data is encapsulated within a class
module named 'Sentinel1.ipynb,' designed to function independently for
potential other projects. More in-depth technical information about the
interconnections among classes in PlotToSat is available in Section
[7](#sec:Advanced){reference-type="ref" reference="sec:Advanced"}.
However, if you prefer to skip this section and explore an example code
('Sentinel1_test.ipynb') showcasing the utilisation of the Sentinel-1
module, you can do so by following this link:
<https://github.com/Art-n-MathS/FLFPythonAPI_GEE/blob/main/.ipynb_checkpoints/Sentinel1_test.ipynb>.
This notebook provides information on how to use this module
independently from the main system.\"

## Sentinel-2 {#sec:s2}

The Sentinel-2 mission comprises a constellation of two satellites. It
is equipped with a Multi-spectral instrument, offering a resolution of
10 metres and a joint revisit period of 5 days. PlotToSat uses
Sentinel-2 L2 data sourced from the \"COPERNICUS/S2_SR_HARMONIZED\"
collection available on GEE. These data have undergone processing by
sen2cor, providing Bottom-Of-Atmosphere reflectance data. The digital
values (DN) within this collection are harmonized; since 2022-02-25, the
DN range of images with PROCESSING_BASELINE \"04.00\" or higher has been
shifted by 1000.

Unlike Sentinel-1 data, Sentinel-2 images are influenced by clouds, so
it is essential to clean the images to improve predictions. This is done
in two phases within the system:

1.  The first phase is conducted using the CLOUDY_PIXEL_PERCENTAGE
    threshold. This threshold is passed as a parameter in the Manager
    object while adding the collection. Any image with a pixel cloud
    percentage higher than the threshold is removed. For instance,
    \"myManager.addCollection(\"sentinel-2\", 50)\" adds the Sentinel-2
    collection to the Manager retaining only images with cloud coverage
    below 50%.

2.  The second phase involves applying cloud and shadow masking. The
    cloud masks for each image are extracted from the collection, and
    their corresponding cloud shadow masks are calculated based on the
    sun's position. The two masks, cloud and shadow, are then combined
    and applied. This process is performed individually on each image
    and is mapped onto the retrieved Sentinel-2 collection to facilitate
    parallel execution by GEE. Figure
    [\[fig:cloudmasking\]](#fig:cloudmasking){reference-type="ref"
    reference="fig:cloudmasking"} provides an example of applying the
    cloud and shadow mask.

<figure id="fig:MaskedImage">
<figure id="fig:CloudedImage">
<img src="./img/CloudedImage.jpeg" />
<figcaption>A Sentinel-2 image with clouds</figcaption>
</figure>
<figure id="fig:CloudNShadowMask">
<img src="./img/CloudsOfImage.jpeg" />
<figcaption>Calculated Cloud and Shadow Mask</figcaption>
</figure>
<figure id="fig:five over x">
<img src="./img/MaskedImage.jpeg" />
<figcaption>Image derived after cloud and shadow masking</figcaption>
</figure>
<figcaption>Example of applying cloud and shadow masking. </figcaption>
</figure>

The interpretation of Sentinel-2 is constructed into a class module
named \"Sentinel2.ipynb\" and it can be used independently for other
projects. Please refer to \"Sentinel2_test.ipynb\"
([\<https://github.com/Art-n-MathS/FLFPythonAPI_GEE/blob/main/.ipynb_checkpoints/Sentinel2b_test.ipynb\>](<https://github.com/Art-n-MathS/FLFPythonAPI_GEE/blob/main/.ipynb_checkpoints/Sentinel2b_test.ipynb>){.uri})
notebook for more information on how to use this module independently
from the main system.

## Masks {#sec:masks}

A few additional masks have been generated to further support cleaning
of data. As mentioned in Section
[4](#sec:instructions){reference-type="ref"
reference="sec:instructions"}, there are five masks available:

1.  Ground Surface Water

2.  Forest Loss

3.  Land Mask

4.  Ascending Aspect Masks

5.  Descending Aspect Masks

Information about the first three masks are provided in Sections
[\[sec:\]](#sec:){reference-type="ref" reference="sec:"}

## Ground Surface Water {#sec:gsw}

The first mask to be described is the ground water surface mask ('gsw').
SAR data reflect high in both moisture and structure. If we are
interested in acquiring information about forest structure, then ground
surface water may produce noise to the data acquired by Sentinel-1. We
shall, therefore, consider removing ground surface water to reduce
potential high values occurred due to the appearance of water. \*\*\*
The collection \"JRC/GSW1_0/GlobalSurfaceWater\" is used, which contains
maps about the presence of ground surface water from 1984 to 2015
[@pekel2016high]. \*\*\* The following table shows some examples of
masking out \"Embalse de la Peña del Águila\" dam in Spain.

::: center
        Image                   Mask                 Output
  ------------------ --------------------------- --------------
   Sentinel-1 Image     Ground Surface Water      Masked Image
     VV Ascending        Mask with no buffer     
                                                 
   Sentinel-1 Image   Ground Surface Water Mask   Masked Image
     VV Ascending         with 100m buffer       
                                                 

  : This table shows examples of masking out ground surface water from
  Sentinel-1 data.
:::

## Forest Loss {#sec:forestLoss}

\*\*\* Forest loss is a term used to define many factors that cause a
reduction in forest coverage. These factors include, but are not limited
to, wildfires, urbanisation, deforestation for agriculture, selective
logging, and human-induced land use [@curtis2018classifying]. The Hansen
Global Forest Change collection, defined as
\"UMD/hansen/global_forest_change_2022_v1_10\" in Google Earth Engine,
is used in PlotToSat. As of the publication date of PlotToSat, version
v1_10 was available. This version provides annual global maps of forest
loss between 2000 and 2022. The estimation of forest loss in these maps
is done using the spectral bands red, NIR, SWIR1, and SWIR2 of Landsat,
as outlined in the related paper [@hansen2013high]. Here, we present two
examples of forest loss. Table [3](#tab:fire){reference-type="ref"
reference="tab:fire"} provides examples of two fire events in the
Troodos mountain range, Cyprus: the first occurred in Saitas in 2007,
and the second took place in Solea in 2016. Table
[4](#tab:forestLoss){reference-type="ref" reference="tab:forestLoss"}
depicts deforestation in the north-west region of the State of Rodonia,
Brazil.

PlotToSat allows the user to mask out forest loss during the period of
their interest, ranging from one to multiple years. There are many uses
related to this feature. For example, fire events can alter forest
ecosystems [@cochrane1999fire], and during regeneration, the biomass of
shrubs differs from that in unburned areas [@aranha2020shrub].
Therefore, if we are interested in determining how much biomass a fully
grown forest naturally gains each year, it may be necessary to remove
plots located in areas that have been burnt.

As previously mentioned, PlotToSat is a highly flexible Object-Oriented
framework. Consequently, users can employ the Masks class and combine it
with either the Sentinel1 and/or Sentinel2 classes for various
applications. Example codes are provided in their respective
\*\_test.ipynb files on the GitHub repository
(<https://github.com/Art-n-MathS/PlotToSat>).

\*\*\*

:::: center
::: {#tab:fire}
  -------------------- -------------------------- --------------------------
   Before fire events   After the 1st fire event   After the 2nd fire event
       2000-2001               2001-2010                  2001-2017
                                                  
  -------------------- -------------------------- --------------------------

  : Example of images generated by applying Surface Water , Land Mask or
  both. Study area includes Akamas Peninsula, which is a Natura 2000
  site, and Paphos forest, Cyprus.
:::
::::

:::: center
::: {#tab:forestLoss}
  ----------- ----------- ----------- -----------
   Location    2000-2002   2000-2003   2000-2004
                                      
   2000-2005   2000-2006   2000-2007   2000-2008
                                      
   2000-2009   2000-2010   2000-2011   2000-2012
                                      
   2000-2013   2000-2014   2000-2015   2000-2016
                                      
   2000-2017   2000-2018   2000-2019   2000-2020
                                      
  ----------- ----------- ----------- -----------

  : Forest lost in North West of State of Rodonia, Brazil. Using the
  masks of PlotToSat and by choosing a different range of years each
  time the forest lost was masked out as shown below.
:::
::::

## Land Mask {#sec:landMask}

\*\*\*In PlotToSat land is masked using the Shuttle Radar Topography
Mission (SRTM) digital elevation dataset (\"CGIAR/SRTM90_V4\") provided
by CGIAR, NASA. Table [5](#tab:LSMaks){reference-type="ref"
reference="tab:LSMaks"} illustrates land masking, both in comparison to
and in combination with masking out ground surface water. \*\*\*

:::: center
::: {#tab:LSMaks}
   Surface Water              Land
  --------------- -----------------------------
     No Masks               Land Mask
                  
   Surface Water   Surface Water and Land Mask
                  

  : Example of images generated by applying Surface Water , Land Mask or
  both. Study area includes Akamas Peninsula, which is a Natura 2000
  site, and Paphos forest, Cyprus.
:::
::::

# System Architecture {#sec:Advanced}

The system is designed to be modular so that each module can be used
independently. Section [4](#sec:instructions){reference-type="ref"
reference="sec:instructions"} provides an explanation of how to use the
Manager module, which links all the implemented modules to extract
feature vectors from the plot data. Section
[5](#sec:outputs){reference-type="ref" reference="sec:outputs"} explains
the system's outputs. Section [6](#sec:Techical){reference-type="ref"
reference="sec:Techical"} delves into the technical information about
the collections, the decision-making process, and the necessary
pre-processing steps. This section provides an overview of the UML
(Unified Modified Language) diagram and the interaction between the
modules. The aim is to support users in utilising the modules
individually for other applications and extending PlotToSat to support
more collections.

Figure [17](#fig:UML){reference-type="ref" reference="fig:UML"} presents
the UML diagram for PlotToSat. UML stands for 'Unified Modelling
Language,' a standardized visual representation extensively employed in
software engineering and system design. This language facilitates the
modelling and visualization of a system's architecture, structure,
behaviour, and relationships. PlotToSat predominantly employs
aggregation, a concept that signifies one class encompassing other
classes, which can also exist autonomously. For instance, the Manager
class contains FieldData and Collections, while a Collection can stand
independently. In the primary system architecture, the classes consist
of Masks, Sentinel1, Sentinel2, FieldData, and Manager. All these
classes rely on the Utils module, which houses utility functions (e.g.,
adding buffers or applying Median filters). An additional supportive
class, MapsVisualisation, provides an interactive map. Although it isn't
utilised within the Manager, it finds purpose in associated test files
linked with each class. Each class is coupled with a corresponding test
file, aiding users in comprehending their independent use.

![The UML digram of PlotToSAT. The user interacts with the Manager
class. The architecture of the main system is shown in bold. Utils is an
essential supportive module, while MapsVisualisation class is an
additional class used for visualisation in the test files of each
module/class. ](img/UML.jpg){#fig:UML width="\\textwidth"}

# Related Forums and Social Media

To discuss what to include

Online social media are used for sharing PlotToSat updates and
discussing issues or potential improvements. Information about PlotToSat
can be found in the following:

-   Google Groups: [\<url\>](<url>){.uri}

-   Blogger: ART `&` M@thS [\<url\>](<url>){.uri}

    This blog provides a general overview of the functionalities of the
    system.

-   Twitter: `@DrMiltiadou`

-   YouTube Channel:
    [\<https://www.youtube.com/@MiltoMiltiadou\>](<https://www.youtube.com/@MiltoMiltiadou>){.uri}

# Acknowledgments

This project is funded by a UKRI Future Leaders Fellowship
(MR/T019832/1) and the Principal Investigator is Dr Emily Lines.

[^1]: Corresponding author and main programmer.
