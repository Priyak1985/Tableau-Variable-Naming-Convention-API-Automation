# Introduction : Tableau Naming standard for calculations and automating it by an API

This page will discuss an original concept of how to design Tableau report contents in a simple yet efficient manner. This discussion is not about the best ways of designing visuals. Rather, it is about an efficient method to create and store the series of variables that power these visuals. This concept makes maintenance of Tableau reports exceptionally easy and streamlined. 
The core idea behind the concept originates from the simple coding guidelines that every coder follows. While writing a code, a coder always prefixes his variables used in the code to identify the data types. This practice has multiple merits. We inherit the same practice in a Tableau reporting environment.

At first, we introduce a robust naming convention for creating every single Tableau calculation within a workbook. Thereafter, we introduce a Tableau folder structure which would logically group the fields and calculations. Finally, we present an API tool which will perform most of these design transitions in the workbook automatically with no impact on the visualizations. 
This automation feature is the center piece of this design proposal. It is the automation part that makes this solution truly novel. Making these design tweaks manually requires significant efforts and would have otherwise proved a letdown while trying to use this solution in Realtime use cases. The automation allows the solution to scale.

Having said that, Let us get started with the first piece.

#  Details of The Naming Convention

The two major field identifiers within Tableau are the "Dimension" and "Measure". The proposed solution covers both the Dimension and Measure elements.
###  Dimension Pane
Each element in a dimension pane can be classified by any one of the following.

 1. Source Dimensions: The original database columns that the report connects to. The fields should be kept at its original form and no renaming of the database fields should ideally occur.

 2. Internal Calculations: Any non-numeric calculation(built on top of the source dimensions) that are not used in any Tableau worksheet directly. Instead, they are referred by other calculations. Hence the name Internal. While creating these internal calculations, one must use the prefix 'Calc_' in the name of the variables. Also, if the calculation happens to use any of the 
'level of Detail' keywords, such as: 'Include' or 'Fixed', One would need to use the prefix 'Calc_LOD_' and 'Calc_LODF_' respectively. The letter 'F' in 'Calc_LODF_’ identifies those variable which use the keyword 'Fixed' in the formula specifically. The merits of such detailed naming standards will be discussed in the subsequent sections.

 
 3. Visualization Facing Calculations: Tableau calculations that are used directly in the visuals fall in this third category. The name of the variables will therefore be exactly the way one would like them to appear on the charts.
There is one finer detail to take note of. In cases wherein a 'LOD' calculation must be used in a visualization: instead of using them directly in a worksheet, create an internal calculation (with naming standard) with the formula. Then, create a visualization facing variable that would just have the name of this internal variable as its formula. In this way, one could logically store every special calculation of the workbook at one single place. Changes made to the calculations will still percolate up to the charts.

Once we have created the dimension calculations abiding to the above standards, we could now group them logically within three major folders. The attached screen shot illustrates how to achieve it.

![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%201.PNG)

###  Measure Pane

Using the same guidelines, we design the numeric calculations in the report. Each element in the measure pane can be categorized in the same fashion as cited above. 

  1. Source measures: The original database numeric fields
  2. Internal calculations: The naming convention of applying prefixes being identical as that for dimensions.
  3. Visualization facing calculations: The naming convention remains identical as measures variables. Whenever LOD calculations are required to be used in a visual directly, we create an internal calculation first and then wrap it up with a second variable (visualization facing). This second variable will be used in the visuals instead. 
Thereafter, we apply the same folder structure to the measure pane as well.


![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%202.PNG)


# Advantages of the Approach

This approach makes the design process extremely robust and streamlined. Reports that prove to be extremely heavy with complex and chain of calculations will benefit largely from the approach. The merit of keeping the special LOD calculations under one folder is that a developer can always keep track of how many LOD calculations lie in the report. Furthermore, since context filters (or the lack of them) impacts LOD calculations (depending on the usage of 'Fixed' keyword) , a developer can quickly browse through the entire set of special calculations prior to making any additions or modifications to the filters of a report. Such as trying to gauge how many special calculations may get upset if a filter is removed from context.
This design structure is very easy to introduce and extremely effective for complex reports with series of calculations in the reports. 

# Automation of the Design Transition
The design structure so proposed here has indeed merit. But should it to be implemented to existing reports manually, the effort needed to do so would have been a clear spoiler. It requires tedious development work to go inside the reports and change the variable names one by one. The initial pain would have outweighed the eventual gain comfortably.
Thankfully, there is a way to avoid the bottleneck. I have designed a python API (shared here ) that would do most of these heavy lifting by itself. When I say 'heavy lifting’, it means the API
    
                        1) Identifies and restores any database column renames.
                        2) Applies the naming convention of prefixing Tableau calculations. 
                        3) Folders the variables the right way.

This is repeated for each data source a workbook connects to. 

# Instructions to Use the API

The API will scan the Tableau files (.twb) placed in the same folder as that of the API and create a sub-folder with the new transformed reports. The original reports will remain untouched. The API is called the ‘Best_Practice_Implementation_Tool'.
its a standalone executable with no external dependency. The API works on any Tableau version. 

Most of the reports I have tested have transformed successfully with no impact on the charts. However, some of the new files may appear corrupt because of trying to introduce the final piece -the Tableau folders. 
Which is why the step of introducing the folders has been kept optional in the API ( The User will need to type yes or no to decide whether to apply folder structure) . Once the API performs the heavy lifting of renaming the Tableau fields appropriately, the foldering can always be done manually by a single click.


![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%203.PNG)

![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%204.PNG)


I am aware of the fact that certain use cases will also require retaining the database column renames in the reports as opposed to revert them. I have thus shared my python code herewith. those who intend to use the tool only for the purpose of restructuring the Tableau calculations could very well comment out the section of the code in which the database columns rename are restored.

I hope the concept and the tool shared herewith are received well and curbs a sizable amount of maintenance overhead that Tableau developers must bear. The solution should be able to scale to a large number of report repository without any hassle.

I look forward to the feedback from users who get to test the tool it against their Tabeleau workbooks.

