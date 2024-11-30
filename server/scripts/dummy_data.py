import db
from db import DB_TABLES
import random


nouns = [
    "apple","banana","cat","dog","elephant","frog","giraffe","horse","iguana","jaguar","kangaroo",
    "lion","monkey","nightingale","octopus","penguin","quail","rabbit","snake","tiger","umbrella",
    "violet","whale","x-ray","yak","zebra","mountain","river","ocean","forest","desert","city",
    "town","village","house","car","bike","book","pen","pencil","paper","computer","phone","table"]

adjectives = [
    "happy","sad","angry","calm","excited","bored","hungry","thirsty","tired","awake","smart","silly",
    "funny","serious","kind","cruel","brave","cowardly","honest","dishonest","loud","quiet","fast","slow",
    "big","small","tall","short","old","young","good","bad","beautiful","ugly","clean","dirty","wet","dry",
    "hot","cold","easy","difficult","possible","impossible","true","false","crazy", "extreme", "red", "blue"]

names_Bases = [
    "Alice","Bob","Charlie","David","Emily","Frank","Grace","Henry","Isabella","Jack","Karen",
    "Liam","Mia","Noah","Olivia","Peter","Quinn","Riley","Sophia","Thomas"]

industries = [
    "Technology","Healthcare","Finance","Education","Retail","Manufacturing","Construction",
    "Hospitality","Transportation","Energy","Media and Entertainment","Real Estate","Agriculture",
    "Legal","Consulting","Telecommunications","Automotive","Aerospace","Biotechnology","Government"
]

countries = [
    "United States","Canada","Mexico","Brazil","Argentina","China",
    "India","Japan","Russia","Australia","Germany","France","United Kingdom",
    "Italy","Spain","South Korea","Indonesia","Turkey","Nigeria","Egypt"
]
resource_types = ['Documentation','Community Platform','Course/Tutorial','Practical','Media and Content']

positions = [
    "Software Engineer","Data Scientist","DevOps Engineer","Cybersecurity Analyst",
    "Project Manager","Product Manager","Business Analyst"
]
EducationLevel =  ['Primary/elementary school','Secondary school','Bachelor''s degree','Master''s degree','Professional degree','Something else']
level = ['Professional','Learning','Other']
gender = ['M','F','O']
WFH = ['Remote','Hybrid','Onsite']
worktime = ['FullTime','PartTime']

tool_Names = []
resource_Names = []
tool_Primary_Purposes = []
company_names = []
project_name = []
tech_type_name = []
tech_name = []
names = []






def init_vals():
    for i in range(20):
        noun1 = nouns[random.randint(0, len(nouns)-1)]
        noun2 = nouns[random.randint(0, len(nouns)-1)]
        tool_Names.append(noun1 + " " + noun2)
    for i in range(20):
        noun1 = nouns[random.randint(0, len(nouns)-1)]
        noun2 = nouns[random.randint(0, len(nouns)-1)]
        resource_Names.append(noun1 + " " + noun2)
    for i in range(20):
        adj = adjectives[random.randint(0, len(adjectives)-1)]
        noun = nouns[random.randint(0, len(nouns)-1)]
        tool_Primary_Purposes.append(noun + " " + adj)
    for i in range(20):
        lev = level[random.randint(0, len(level)-1)]
        noun = nouns[random.randint(0, len(nouns)-1)]
        company_names.append(lev + " " + noun)
    for i in range(20):
        ind = industries[random.randint(0, len(industries)-1)]
        adj = adjectives[random.randint(0, len(adjectives)-1)]
        tech_name.append(ind + " " + adj)
    for i in range(20):
        ind = industries[random.randint(0, len(industries)-1)]
        project_name.append(ind + " " + str(random.randint(0, 100)))
    for i in range(20):
        ind = industries[random.randint(0, len(industries)-1)]
        tech_type_name.append(ind + " " + str(random.randint(0, 100)))
    for i in range(100):
        base = names_Bases[random.randint(0, len(names_Bases)-1)]
        names.append(base + " " + str(random.randint(0, 100)))
        

conn = db.get_db_connection()
cur = conn.cursor() 
def db_call(query):
    try:
        cur.execute(query)
        cur.fetchall()
        conn.commit()
    except Exception as e:
        print(query)
        print(e)

if __name__ == "__main__":
    init_vals()
    
    for i in range (1, len(tool_Names)):
        tool_type = 'IDE' if (random.randint(0,1) == 1) else 'Collab'
        yn = 'Y' if (random.randint(0,1) == 1) else 'N'
        query_string = """
            INSERT INTO `Tool` VALUES ({}, '{}', '{}', '{}', '{}');
            """.format(i, tool_Names[i], tool_type, yn, '2005-04-07')      
        db_call(query_string)
    for i in range (1, len(tool_Primary_Purposes)):
        tool_id = random.randint(1, len(tool_Names) -1)
        query_string = """
            INSERT INTO `Tool_PrimaryPurposes` VALUES ({}, '{}');
            """.format(tool_id, tool_Primary_Purposes[i])              
        db_call(query_string)
    for i in range (1, len(resource_Names)):
        resource_type = random.randint(0, len(resource_types) -1)
        query_string = """
            INSERT INTO `Resource` VALUES ({}, '{}', '{}');
            """.format(i, resource_Names[i], resource_types[resource_type])              
        db_call(query_string)
    for i in range (1, len(resource_Names)):
        tool_id = random.randint(1, len(tool_Names) -1)
        query_string = """
            INSERT INTO `Resource_Uses_Tool` VALUES ({}, {});
            """.format(tool_id, i)              
        db_call(query_string)
    for i in range (1, len(names)):
        EducationLevel_ = random.randint(0, len(EducationLevel) -1)
        level_ = random.randint(0, len(level) - 1)    
        YearsCoding_ = random.randint(1, 30)
        Age_ = random.randint(20, 65)
        gender_ = random.randint(0, len(gender) - 1)   

        query_string = """
            INSERT INTO `User` VALUES ({}, '{}', '{}', '{}', {}, {}, '{}', '{}');
            """.format(i, names[i], EducationLevel_, level[level_], YearsCoding_, Age_, gender[gender_], names[i])              
        db_call(query_string)
    for i in range (1, 10):
        PopularityRating_ = random.randint(1, 10)
        RequiredYears = random.randint(0, 10)   

        query_string = """
            INSERT INTO `DeveloperType` VALUES ({}, '{}', {}, {});
            """.format(i, adjectives[i], EducationLevel_, PopularityRating_, RequiredYears)              
        db_call(query_string)

    for i in range (1, len(company_names)):
        PopularityRating = random.randint(1, 100)
        industry = industries[random.randint(0, len(industries) -1)]
        country = countries[random.randint(0, len(countries) -1)]
        query_string = """
            INSERT INTO `Company` VALUES ({}, '{}', {}, '{}', '{}');
            """.format(i, company_names[i], PopularityRating, industry, country)              
        db_call(query_string)

    for i in range (1, len(project_name)):
        companyID = random.randint(1, len(company_names) -1)
        PopularityRating = random.randint(1, 100)
        desc = nouns[random.randint(0, len(nouns)-1)]
        durration = random.randint(1, 40)
        budget = random.randint(0, 99999)
    
        query_string = """
            INSERT INTO `Project` VALUES ({}, {}, '{}', '{}', {}, {});
            """.format(i, companyID, project_name[i], desc, durration, budget)              
        db_call(query_string)

    for i in range (1, len(tech_type_name)):
        adj1 = adjectives[random.randint(0, len(adjectives)-1)]
        adj2 = adjectives[random.randint(0, len(adjectives)-1)]
        
        query_string = """
            INSERT INTO `TechnologyType` VALUES ({}, '{}', '{}');
            """.format(i, tech_type_name[i], adj1 + " " + adj2)              
        db_call(query_string)
    for i in range (1, len(tech_name)):
        adj1 = adjectives[random.randint(0, len(adjectives)-1)]
        adj2 = adjectives[random.randint(0, len(adjectives)-1)]
        techtype = random.randint(1, len(tech_type_name) -1)

        query_string = """
            INSERT INTO `Technology` VALUES ({}, '{}', '{}', {});
            """.format(i, tech_name[i], '2001-01-01', techtype)              
        db_call(query_string)
    for i in range (1, 40):
        techId = random.randint(1, len(tech_name) -1)
        adj1 = adjectives[random.randint(0, len(adjectives)-1)]
        adj2 = adjectives[random.randint(0, len(adjectives)-1)]

        query_string = """
            INSERT INTO `Technology_UseCases` VALUES ({}, '{}');
            """.format(techId, adj1 + " " + adj2)              
        db_call(query_string)
    for i in range (1, 5):
        techId1 = random.randint(1, len(tech_name) -1)
        techId2 = techId1
        while techId1 is not techId2:
            techId2 = random.randint(1, len(tech_name) -1)

        query_string = """
            INSERT INTO `Technology_Dependency` VALUES ({}, '{}');
            """.format(techId1, techId2)              
        db_call(query_string)
    for i in range (1, 5):
        techId = random.randint(1, len(tech_name) - 1)
        resourceID = random.randint(1, len(resource_Names) - 1)

        query_string = """
            INSERT INTO `Resource_Teaches_Technology` VALUES ({}, {});
            """.format(resourceID, techId)              
        db_call(query_string)

    for i in range (50):
        devtype = random.randint(1, 9)
        userID = random.randint(1, len(names) -1)
        companyID = random.randint(1, len(company_names) -1)
        WFHPolicy = WFH[random.randint(0, len(WFH) -1)]
        workTime_= worktime[random.randint(0, len(worktime) -1)]
        salary = random.randint(0, 10_000_000)

        query_string = """
            INSERT INTO `Position` VALUES ({}, {}, {}, '{}', {}, '{}');
            """.format(devtype, userID, companyID, WFHPolicy, salary, workTime_)              
        db_call(query_string)
    for i in range (1, 50):
        projID = random.randint(1, len(project_name) - 1)
        techId = random.randint(1, len(tech_name) - 1)

        query_string = """
            INSERT INTO `Project_Uses_Technology` VALUES ({}, {});
            """.format(projID, techId)              
        db_call(query_string)
    for i in range (1, len(names)):
        projID = random.randint(1, len(project_name) - 1)
        adj = adjectives[random.randint(0, len(adjectives)-1)]

        query_string = """
            INSERT INTO `Assigned_To` VALUES ({}, {}, '{}');
            """.format(i, techId, adj)              
        db_call(query_string)
    for i in range (1, 50):
        userID = random.randint(1, len(names) - 1)
        resourceID = random.randint(1, len(resource_Names) - 1)

        query_string = """
            INSERT INTO `learns_from` VALUES ({}, {});
            """.format(userID, resourceID)              
        db_call(query_string)
        
    



# structire
#     'developer_type': 'DeveloperType',
#     'technology_type': 'TechnologyType',
#     'technology': 'Technology',
#     'technology_use_case': 'Technology_UseCases',
#     'tool': 'Tool',
#     'tool_primary_purpose': 'Tool_PrimaryPurposes',
#     'resource': 'Resource',
#     'company': 'Company',
#     'user': 'User',
#     'project': 'Project',
#     'assigned_to': 'Assigned_To',
#     'learns_from': 'Learns_From',
#     'project_uses_technology': 'Project_Uses_Technology',
#     'resource_teaches_technology': 'Resource_Teaches_Technology',
#     'resource_uses_tool': 'Resource_Uses_Tool',
#     'technology_dependency': 'Technology_Dependency',
#     'position': 'Position'

'''



-----------------
Add Tools 15
Add Tool_PrimaryPurposes 16
Add Resources 8
Add Resource_Uses_Tool 10
----------------- THIS IS WHERE I AM
Add User 17
Add DeveloperType 3 
Add Company 2
Add Project 6
---------------- HERE
Add TechnologyType 14
Add Technology 11
Add Technology_UseCases 13
Add Technology_Dependency 12
Add Resource_Teaches_Technology 9
------------------
Add Postion 5
Add Project_Uses_Technology 7
Add Assigned_To 1
Add learns_from 4










----------
Tools ###
Int
string (noun+noun)
'IDE','Collab'
'Y','N'
date
----------
Tool_PrimaryPurposes ###
ToolID
string (adj+noun)
----------
Resources ###
Int
String (noun+noun)
'Documentation','Community Platform','Course/Tutorial','Practical','Media and Content'
----------
Resource_Uses_Tool ###
toolId
resource
----------
----------
User ###
int
name
`EducationLevel` enum('Primary/elementary school','Secondary school','Bachelor''s degree','Master''s degree','Professional degree','Something else'
'Professional','Learning','Other'
int 
int 
'M','F','O'
string
-----------
DeveloperType ###
int
name
int
int
-----------
Company ###
int
name
int
sting
string
-----------
Project ###
int
int (company)
name
description
int
int
-------
Position ###
int (DeveloperType)
int (user)
int (company)
'Remote','Hybrid','Onsite'
int salary
'FullTime','PartTime'
-------
Project_Uses_Technology ###
int (project id)
int (tech id)
--------
Assigned_To ###
int (user id
int (project id)
string (role)
-------
learns_from ####
int (user id)
int (resource id)

'''