# Introduction : A Concept for Best  Design Practice, Tableau Reports

This page will discuss an original concept of how to design Tableau report contents in a very simple yet efficient manner which would make future maintenance of the contents exceptionally easy. The concept originates from the simple naming guidelines that coders follow while coding in any language. While writing a code , a coder prefixes his variables used in the code to identify the data types easily.

We inherit the same idea in the tableau reporting framework. At first, we introduce a robust naming convention for creating every single Tableau calculations within a workbook. Once we have created every calculation by this standard, we go on to introduce a Tableau folder structure which would logically group the data source fields as well as calculations built on top of them. 
Finally, we present an API tool which will perform most of these design transitions automatically with no impact on the visualizations. 

The automation feauture is the centre piece of  this design proposal.It is the automation part that makes the solution really attractive. Making these design tweaks manually requires significant efforts and would have otherwise proved a strong letdown when trying to use this proposal in realtime scnarios.The automation allows the solution to scale.

Having said that ,Let us get started with the the first piece.

#  Details of The Naming Convention

The two major field identifiers within tableau are the "Dimension" and "Measure". The proposed variable structure is applied to both the dimension and Measure pane. The concept is similar for both dimension and measure variables.Details follow:

###  Dimension Pane
Each element in a dimension pane can be classified by any one of the following.

 1. Source Dimensions: The original database columns that the report connects to. The fields should be kept at its original form and no renaming of the database fields should ideally occur.

 2. Internal Calculations: Any non numeric calculation variables that are not used in any tableau worksheets directly. Instead they are referred by other calculations. Hence the name Internal. While creating an internal calculation, one must use the prefix 'Calc_' in the name of the variable. Also, if the calculation happens to use any of the 'level of Detail' keywords, such as 'Include' or 'Fixed', One would need to use the prefix 'Calc_LOD_' and 'Calc_LODF_' respectively. The letter 'F' in 'Calc_LODF_'  identifies those variable which use the keyword 'Fixed' in the formula specifically. The merits of such detailed naming standards will be discussed in the subsequent sections.

 
 3. Visualization Facing Calculations: Tableau calculations that are used directly in the visuals fall in this third category. The name of the variables will therefore be exactly the way once would like to appear on the charts. There is one finer detail introduced here. In cases wherein a 'LOD' calculation has to be used in a visualization: instead of using them directly in a worksheet, create an internal calculation (with the right naming standard) first with the formula. Then, create a variable that would just have the name of the internal variable you just created.In this way, one could keep track of the number 

Once we have created the dimension calculations abiding to the above standards, we could now group them logically within tableau within three major folders. The attached screen shot illustrates how to achieve it.

![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%201.PNG)

###  Measure Pane

Using the same guidelines, we design the numeric calculations in the report. Each element in the measure pane can be categorized in the same fashion as cited above. 

  1. Source measures : The original database numeric fields
  2. Internal calculations : The naming convention of applying prefixes being identical as that for dimensions.
  3. Visualization facing calculations : The naming convention remains identical as measures variables. Whenever LOD calculations are required to be used in a visual directly, we create an internal calculation first and then wrap it up with a second variable ( visualization facing) that refers to the internal calculation. This second variable will be used in the visuals instead. 
Thereafter, we apply the same folder structure to the measure pane as well.


![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%202.PNG)


# Advantages of the Approach

This approach makes the design process extremely robust and streamlined. Reports that prove to be extremely heavy with complex and chain of calculations will benefit largely from the approach. The merit of keeping the special LOD calculations under one folder is that a developer can always keep track of how many LOD calculations does the report have even if they scale very quickly. Furthermore, Since context filters ( or the lack of them) impacts LOD calculations ( and does not impact the ones with 'Fixed' keyword) , a developer can quickly browse through the entire set of special calculations prior to making any additions or modifications to the filters of a report.
This design structure is very easy to introduce and extremely effective for complex reports with series of calculations in the reports. 

# Automation of the Design Transition
The design structure so proposed here has definite merit. But was it to be implemented manually to existing reports manually, the effort needed to do so would have been a bottleneck. It requires tedious effort to go inside the reports change the variable names one by one and thereafter folder them appropriately. the initial pain would have outweighed the gain.
Thankfully, there is a way to avoid the bottleneck. I have designed a python API ( shared here ) that would do most of these heavy lifting by itself. When I say Heavy lifting , it means that for each data connection in the report , the API
    
                        1) Identifies and restores any database column renames.
                        2) Applies the naming convention of prefixing tableau calculations. 
                        3) Folders the variables the right way.


# Instructions to Use the API

The API will scan the tableau files (.twb) placed in the same folder as that of the API and create a sub-folder with the new transformed reports. The original reports will remain untouched. The API is called the  'Best_Practice_Implementation_Tool'.its a standalone executable with no external dependency.

The API works on any tableau version. Most of the reports I have tested have transformed successfully with no impact on the charts. However, some of the file copies may appear corrupt as a result of trying to introduce the final piece -the Tableau folders. Which is why the step of introducing the folders in the tableau report has been kept optional in the API ( The User will need to type yes or no to decide whether to apply folder structure) . Once the API performs the heavy lifting of renaming the tableau fields appropriately, the foldering can always be done manually by a single click.


![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%203.PNG)

![](https://github.com/Priyak1985/Tableau-Best-Practice-Concept/blob/master/Screen%20shot%204.PNG)


I am aware of the fact that certain use cases will require to keep the database column renames in the reports. I have thus shared my python code herewith. those who intend to use the tool only for the purpose of restructuring the tableau calculations could very well comment out the section of the code in which the database columns renames are restored.

I hope the tool and the concept shared herewith are received well and eases out a sizable amount of maintenance overhead.The solution should be able to scale to a large number of report repository.I look forward to the feedback from users who get to test it against their tabeleau workbooks. 
