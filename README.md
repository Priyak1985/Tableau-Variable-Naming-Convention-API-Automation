#  Introduction 

This page will discuss an original concept of how to design Tableau report contents in a very simple yet efficient manner which would make  maintenance exceptionally easy. The concept originates from the simple naming guidelines that coders follow while coding in any language. A coder prefixes the variables used inside the code to identify the data types very easily. We inherit the same idea in the Tableau reporting framework and build from there. The idea does not relate visualizations. Rather, it is all about the many variables that power these visualizations from the background. First, we introduce a robust naming convention for creating the Tableau calculations. Once we have created every calculation by this standard, we go on to introduce a Tableau folder structure which would logically group the report elements so created. Finally, we present an API interface which will perform most of these design makeovers automatically with no impact on the visualizations. The automation piece is the central feature of this solution. Without the API it would have required an individual to go inside one Tableau report at a time and align the variables to the new standard. A task too onerous to appear worthwhile. Hence, the need for the API. The API allows the solution to scale.
Having said that, let us get started with the underlying concept:

#  Details of The Naming Convention

The two major elements within Tableau are the "Dimension" and "Measure" elements (categorical and numeric fields). The proposed variable structure appplies to both the dimension and Measure variables within Tableau.

###  Dimension Pane
Each element in a dimension pane can be classified by any one of the following.

 1. Source Dimensions: The original database columns that the report connects to. The fields should be kept at its original form and no renaming of the database fields should ideally occur.

 2. Internal Calculations: Can be defined as any non-numeric calculation that are not used in Tableau worksheets directly. Instead, they are referred by other secondary calculations. Hence, the name internal. While creating an internal calculation, one must use the prefix 'Calc_' in the name of the variable. Also, if the calculation happens to use any of the 'level of Detail' keywords, such as 'Include' or 'Fixed', one should use the prefix 'Calc_LOD_' and 'Calc_LODF_' respectively. The letter 'F' in 'Calc_LODF_’ identifies those variables which use the keyword 'Fixed' in the formula specifically. The merits of such detailed naming process will be discussed in the subsequent sections.

 
 3. Visualization Facing Calculations: Tableau calculations that are used directly in the visuals fall in this third category. The name of the variables will therefore be exactly the way one would need them to display on the charts. 
 However, there is one finer detail introduced for these categories of variables. Cases wherein a 'LOD' calculation must be used in a visualization: instead of placing them directly in a worksheet, first create an internal calculation (with the naming standard) with the actual formula of the LOD expression. Then, create a second variable that would simply have the name of the internal variable as its' formula (a variable wrapping another). This way, all 'LOD' calculations can be grouped together in one single place. It will be super convenient to browse through the entire series of special calculations.
 
![](https://github.com/Priyak1985/Tableau-Variable-Naming-Convention-API-Automation/blob/master/Screen%20shot%206.PNG)
 
![](https://github.com/Priyak1985/Tableau-Variable-Naming-Convention-API-Automation/blob/master/Screen%20shot%207.PNG)

Once we have created the dimension variables as per the standards, we could now group them logically inside Tableau within three major folders. The attached screen shot illustrates how to achieve it.

![](https://github.com/Priyak1985/Tableau-Variable-Naming-Convention-API-Automation/blob/master/Screen%20Shot%201.png)

###  Measure Pane

Using the same guidelines, we design the numeric calculations in the report. Each element in the measure pane can be labelled the same fashion as cited above. 

  1. Source measures: The original database numeric fields
  2. Internal calculations: The naming convention of applying prefixes being identical as that for dimensions.
  3. Visualization facing calculations: The naming convention remains identical as measures variables. Whenever LOD calculations are required to be used in a visual directly, we create an internal calculation first and then wrap it up with a second variable that refers to the internal calculation and used in the visuals. 
Thereafter, we apply the same folder structure to the measure pane as well.


![](https://github.com/Priyak1985/Tableau-Variable-Naming-Convention-API-Automation/blob/master/Screen%20Shot%202.png)


# Advantages of the Approach

This approach makes the design process extremely robust and streamlined. Reports that prove to be extremely heavy with complex and chain of calculations will benefit largely from the approach. The merit of keeping the special LOD calculations under one folder is that a developer can always keep track of how many LOD calculations does the report bear. Furthermore, Since context filters (or the lack of them) impacts LOD calculations (and does not impact the ones with 'Fixed' keyword), a developer can quickly browse through the entire set of special calculations prior to making any additions or modifications to the filters of a  Tableau report.
This design structure is very easy to introduce and extremely effective for complex reports with overwhelming number of calculations in the reports. 

# Automation of the Design Changes
The design structure so proposed has apparent merit. But was it to be implemented manually in existing reports, the effort needed to do so would have been a huge bottleneck. It requires tedious and prolonged efforts to go inside the reports, change the variable names one by one and thereafter, folder them appropriately. the initial pain would have outweighed the eventual gain of the design overhaul.
Thankfully, there is a way to avoid the bottleneck. I have designed a python API (shared here) that would do most of these heavy lifting by itself. When I say heavy lifting, that means the API successfully:    
                        1) Identifies and restores any database column renames.
                        2) Introduces the prefixing of Tableau calculations as applicable. 
                        3) Folders the variables the right way.

The API is written completely in Python. Please download the API form this [GOOGLE DRIVE LINK](https://drive.google.com/open?id=1iFmsKL2wDcoQsmgkqmuskVNsSc9L53rs)


# Instructions to Use the API

The API and the Tableau files identified for the transformation need to reside under the same folder. Once you click on the API tool, the API will scan the Tableau files (*.twb) placed in the same folder and create a sub-folder with the new transformed reports. The original reports will remain untouched. The API is called named 'Best_Practice_Implementation_Tool'.
It is a standalone executable with no external dependency. The API works on any Tableau version. Most of the reports I have tested have transformed successfully with no impact on the charts. 

However, some of the file copies may appear corrupt because of trying to introduce the final piece: the folders. Which is why the step of introducing the folders in the Tableau report has been kept optional in the API (The User will need to type yes or no to decide whether to apply folder structure). If the first run appears to have created a few corrupt files just repeat the run for those reports but opting out the folder creation step. Once the API performs the heavy lifting of renaming the Tableau fields appropriately, the foldering can always be done manually by a single click.


![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%203.PNG)

![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%204.PNG)


I am also aware of the fact that owing to certain use cases, rolling back the column renames is not preferred (the first step of the API). I have thus shared my code herewith. those who intend to use the tool only for restructuring the Tableau calculations could very well comment out the section of the code in which the database columns are restored.

I hope the tool and the concept shared herewith is received well and eases out a sizable amount of maintenance overhead for Tableau professionals. I look forward to receiving feedback on how you find the tool perform against your reports should you find the naming convention concept comprehensive. 
