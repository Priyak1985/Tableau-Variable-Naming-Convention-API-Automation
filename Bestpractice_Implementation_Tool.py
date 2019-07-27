
import xml.etree.ElementTree as ET
import os
import pprint
import pandas as pd
from pandas import ExcelWriter
import random


# Author: Priyak Bandyopadhyay

# Read the file contents of present directory and iterate

print ('\n\n\n************** Executing Code to introduce best implementation practices in Tableau files  **************\n\n\n')


lcomplete_list1=[]
lcomplete_list2=[]

# Function that removes duplicates from a dictionary

def remove_dups (dct):
    dtemp={}
    for key,value in dct.items():
        if value not in dtemp.values():dtemp[key]=value
    return dtemp

# Start iteration 

for filename in os.listdir():
    if not filename.endswith('.twb'): continue
             # fullname = os.path.join(path, filename)
    print('1. Reading File:'+ filename+' ------------\n')
    
    tree = ET.parse(filename)
    root = tree.getroot()
    

            # print(ET.tostring(root, encoding='utf8').decode('utf8'))
# Declarations 
    d={}
    calculations={}
    dlod={}
    dlodf={}
    dinteger_values={}
    dstring_values={}
    ltemp=[]
    
# Obtaining column names which has got special LOD calculations and renamed columns in the tableau workbook

    for col in root.iter('column'):
        caption=col.get('caption')
        name=col.get('name')
        data_type=col.get('datatype')
        
        if caption is not None and col.get('param-domain-type') is None and  name.startswith('[Calculation_') or col.find('calculation')is not None:
            calculations[col.get('name')]=caption
            formula=col.find('calculation').get('formula')
            if formula is None: continue
            if '{'in formula and 'INCLUDE'in formula.upper() or 'EXCLUDE' in formula.upper():dlod[name]=caption
            if '{'in formula and 'FIXED' in formula.upper():dlodf[name] =caption

        if caption is not None and 'Calculation' not in col.get('name') and col.get('param-domain-type') is None and col.get('value') is None and col.find('calculation') is None:
            d[col.get('name')]=col.get('caption')
            # if caption is not None and 'Calculation' not in col.get('name') and col.get('param-domain-type') is None and col.get('value') is None and col.find('calculation') is None:
                # del col.attrib['caption']

# Removing duplicate entries from the names so collected 

    dresult=remove_dups (d)
    dcalc_new=remove_dups(calculations)

    dlod=remove_dups(dlod)
    dlodf=remove_dups(dlodf)

    print('2. Completed Identifying renamed columns (as follows:) ---------\n\n')
    pprint.pprint(list(dresult))

# Producing the list with list of  columns that are rolled back    
    
    for key,value in dresult.items():
        ltemp=[filename,key,value]
        lcomplete_list1.append(ltemp)
  
  
    print('3. Captured details in spreadsheet:-----\n\n')

    # Obtaining calculation variables that have been used in sheets


# Removing duplicate entries from the names so obtained
    dsheet_calc={}
    for sheet in root.iter('worksheet'):
        for ds in sheet.findall('./table/view/datasource-dependencies'):
            if ds.get('datasource')is None or 'Parameters' in ds.get('datasource'):continue
            for col in ds.findall('column'):
                caption=col.get('caption')
                calculation=col.find('calculation')
                if calculation is not None:
                    dsheet_calc[caption]=caption
    
    dsheet_calc_new=remove_dups(dsheet_calc)
  
# Renaming internal calculations as per best practices guidelines to the variables not used in worksheets
    
    dinternal_calc={}
    for col in root.iter('column'):
        if col.get('caption') is not None and col.find('calculation') is not None and col.get('param-domain-type') is None and col.get('caption') in dcalc_new.values() and col.get('name') not in dsheet_calc_new.values() :
            if 'Measure' in col.get('caption'):continue
            dinternal_calc[col.get('caption')]=col.get('caption')
            old=col.get('caption')
            new='Calc_'+old
            formula=col.find('calculation').get('formula')
            if formula is not None and '{' in formula and 'FIXED' in formula.upper():
                new='Calc_LODF_'+old
            if formula is not None and '{' in formula and ('INCLUDE'in formula.upper()or 'EXCLUDE'in formula.upper()):
                new='Calc_LOD_'+old
            col.set('caption',new)
      

    print('4.Identified & renamed internal variables in workbook (as follows:)-----\n\n')
    pprint.pprint(list(dinternal_calc))
    for key, value in dinternal_calc.items():
        ltemp=[filename,key,value]
        lcomplete_list2.append(ltemp)

# Creating Folder elements to contain the tableau fields
    print('\n------Introducing  folders (few reports may throw error. You could avaoid this step & perform the foldering manually).\n')
    str_choice=input('Continue to automated folder creation(y/n)?:')
    
    source_dimensions=ET.Element('folder',name='1.Source dimensions ',role='dimensions')
    internal_dimensions=ET.Element('folder',name='2.Internal calculations ',role='dimensions')
    visual_dimensions=ET.Element('folder',name='3.Visualization facing calculations ',role='dimensions')
    source_measures=ET.Element('folder',name='1.Source measures ',role='measures')
    internal_measures=ET.Element('folder',name='2.Internal calculations ',role='measures')
    visual_measures=ET.Element('folder',name='3.Visualization facing calculations ',role='measures')
    node=root.find('datasources')
    
        
# Iterating through each data source, scanning fields and placing each in the correct folder. 

    for ds in node.findall('datasource'):
        if str_choice == 'n':break
        if ds is None or ds.get('caption') is None or ds.get('name')=='Parameters': continue
        
        print( ' \n Adding folders to the data connection:\n'+ str(ds.get('caption')))
        col_names=ds.findall('column')
        metadata=ds.findall('./connection/metadata-records/metadata-record')
        extract=ds.findall('./extract/connection/metadata-records/metadata-record')
        col_instances=ds.findall('column-instance')
        groups=ds.findall('group')
        try:
            
            if metadata is None: continue
            for md in metadata:
                if md is None: continue
                if md.get('class')!='column' or md.find('local-name').text in dcalc_new.keys(): continue
                name=md.find('local-name').text
                if 'Measure' in name or 'Number of Records' in name:continue
                datatype=md.find('local-type').text
                
                if (datatype in['string','boolean','date','datetime']):
                    folder_item=ET.SubElement(source_dimensions,'folder-item')
                    folder_item.set('name',name)
                    folder_item.set('type','field')
                if datatype in ['integer','real']:
                    folder_item=ET.SubElement(source_measures,'folder-item')
                    folder_item.set('name',name)
                    folder_item.set('type','field')
            if extract is None : continue
            for md in extract:
                if md is None: continue
                if md.get('class')!='column' or md.find('local-name').text in dcalc_new.keys():continue
                name=md.find('local-name').text
                if 'Measure' in name or 'Number of Records' in name: continue
                datatype=md.find('local-type').text

                if (datatype in['string','boolean','date','datetime']):
                    folder_item=ET.SubElement(source_dimensions,'folder-item')
                    folder_item.set('name',name)
                    folder_item.set('type','field')

                if datatype in ['integer','real']:
                    folder_item=ET.SubElement(source_measures,'folder-item')
                    folder_item.set('name',name)
                    folder_item.set('type','field')



        except Exception as exc:
            print('a.Some elements could not be added to the folders:\n'+str(exc))
            pass
        
        try:
                    
            if col_names is None or col_names==[]: continue

            for col in col_names:
                if col is None or col.get('name') =='[Number of Records]' or 'Measure' in col.get('name'): continue
                if col.get('param-domain-type') is not None : continue
                caption=col.get('caption')

                if col.get('role')=='measure' and col.find('calculation') is None:
                    folder_item=ET.SubElement(source_measures,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
                if col.get('role')=='dimension' and col.find('calculation') is None:
                    folder_item=ET.SubElement(source_dimensions,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
             
                if caption is None: continue 
                if  col.get('role')=='measure' and caption.startswith('Calc_'):
                    folder_item=ET.SubElement(internal_measures,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
                
                if  col.find('calculation') is not None and col.get('role')=='measure' and not caption.startswith('Calc_'):
                    folder_item=ET.SubElement(visual_measures,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
                
            
                if  col.get('role')=='dimension' and caption.startswith('Calc_'):
                    folder_item =ET.SubElement(internal_dimensions,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
                if col.find('calculation') is not None  and col.get('role')=='dimension' and not caption.startswith('Calc_'):
                    folder_item =ET.SubElement(visual_dimensions,'folder-item')
                    folder_item.set('name',col.get('name'))
                    folder_item.set('type','field')
                    continue
             
        except Exception as exc:
            print('b.Some elements could not be added to the folders:\n'+str(exc))
            pass
        pos1=list(ds).index(col_names[-1])
        pos2=0
        pos3=0
        if col_instances !=[]: 
            posx=[i for i,x in enumerate(ds) if x == col_instances[-1]]
            pos2=posx[-1]
        if groups != []: 
            posx=[i for i,x in enumerate(ds) if x == groups[-1]]
            pos3=posx[-1]
        # pprint.pprint(groups)
        pos=max(pos1,pos2,pos3)+1
       

# Once the folder contents are created, adding the folders  to the file
        ds.insert(pos,source_dimensions)
        ds.insert(pos+1,source_measures)
        ds.insert(pos+2,internal_dimensions)
        ds.insert(pos+3,internal_measures)
        ds.insert(pos+4,visual_dimensions)
        ds.insert(pos+5,visual_measures)
    
    output_filename='New reports(best practices)/'+ filename[:-4]+ '_new.twb'
    if not os.path.exists('New reports(best practices)'):os.makedirs('New reports(best practices)')
    tree.write(open(output_filename,'wb'), encoding='utf-8')

    print('\n5. Successfully created new version of the workbook: '+filename[:-4]+'_new\n\n')
    print('============= moving onto the next workbook in the directory ================\n\n')

# Converting the list of renamed variables\internal calculations to an excel report

df1=pd.DataFrame(lcomplete_list1,columns=['Workbook name','Restored Source Column','Initially Renamed'])
df2=pd.DataFrame(lcomplete_list2,columns=['Workbook name','Internal variable name','Internal variable caption'])
del df2['Internal variable caption']
writer = pd.ExcelWriter('New reports(best practices)/Conversion report(best practices).xlsx', engine = 'xlsxwriter')
df1.to_excel(writer, sheet_name = 'Restored source column list',index=False)
df2.to_excel(writer, sheet_name = 'Internal calculations',index=False)
writer.save()
writer.close()
print('******************* Finished conversion of all workbooks in the directory **********************************\n\n')
input('Type any key')
