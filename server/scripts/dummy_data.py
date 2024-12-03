import db
import random
from datetime import datetime, timedelta

# Data for insertion
countries = ["India", "United States", "Japan", "Germany", "Canada"]
industries = ["Technology", "Finance", "Healthcare", "Education", "Retail"]
tools = ["Git", "Bitbucket", "VS Code", "CLion", "PyCharm", "Jenkins", "Eclipse", "IntelliJ IDEA", "Sublime Text", "Atom",
          "GitLab", "Trello", "JIRA", "Postman", "Slack", "Zoom",
          "Visual Studio", "Notion", "Figma", "Tableau", "Xcode", "Android Studio"]
tool_types = ["IDE", "Collab"]
resources = [
    ("Stack Overflow", "Community Platform"),
    ("Khan Academy", "Course/Tutorial"),
    ("YouTube", "Media and Content"),
    ("Udemy", "Course/Tutorial"),
    ("W3Schools", "Documentation")
]
developer_types = ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Scientist"]
remote_policies = ["Remote", "Hybrid", "Onsite"]
working_times = ["FullTime", "PartTime"]
education_levels = [
    "Primary/elementary school", "Secondary school", "Bachelor''s degree", 
    "Master''s degree", "Professional degree", "Something else"
]
coding_levels = ["Professional", "Learning", "Other"]
genders = ["M", "F", "O"]
project_descriptions = [
    "AI-powered chatbot", "E-commerce website", 
    "Mobile banking app", "Social media analytics tool",
    "IoT Device Management System", "Healthcare Scheduling Platform"
]
technology_use_cases = [
    "Data analysis", "Machine learning", "Web development", 
    "Cybersecurity", "IoT applications"
]

tool_primary_purposes = [
    "Version Control", "Code Collaboration", "Code Editing", "Code Building", "Code Testing", "Code Deployment"
]

technology_types = ["Programming Language", "Framework", "Database"]

# Meaningful names
company_names = ["Google", "Microsoft", "Facebook", "Amazon", "Apple"]
technology_names = [
    "Python", "Java", "C++", "JavaScript", "React", "Angular", "Express", "MongoDB", "PostgreSQL",
      "Docker", "Kubernetes", "Ruby on Rails", "Flask", "Django", "TensorFlow", "PyTorch",
        "Redis", "GraphQL", "Elasticsearch", "Hadoop"
]

# Define possible roles for Assigned_To
roles = ["Tester", "Backend Engineer", "Frontend Engineer", "Product Manager", "Junior Developer", "DevOps"]

# Track used names
used_company_names = set()
used_tool_names = set()
used_project_names = set()

# Database connection and execution
conn = db.get_db_connection()
cur = conn.cursor()

def db_call(query):
    try:
        cur.execute(query)
        conn.commit()
    except Exception as e:
        print("Query Failed:", query)
        print(e)

# Helper functions
def random_date(start_year=2000, end_year=2020):
    start = datetime(year=start_year, month=1, day=1)
    end = datetime(year=end_year, month=12, day=31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def make_unique(name, used_names):
    """Ensures the given name is unique by appending a number if needed."""
    original_name = name
    counter = 1
    while name in used_names:
        name = f"{original_name}_{counter}"
        counter += 1
    used_names.add(name)
    return name

def insert_tool():
    for i, tool in enumerate(tools, start=1):
        name = make_unique(tool, used_tool_names)
        tool_type = random.choice(tool_types)
        sync_capability = random.choice(["Y", "N"])
        date_of_release = random_date()
        query = f"""
            INSERT INTO Tool (ToolID, Name, Type, SyncCapability, DateOfRelease)
            VALUES ({i}, '{name}', '{tool_type}', '{sync_capability}', '{date_of_release}');
        """
        db_call(query)

def insert_resources():
    for i, (resource, resource_type) in enumerate(resources, start=1):
        query = f"""
            INSERT INTO Resource (ResourceID, Name, Type) 
            VALUES ({i}, '{resource}', '{resource_type}');
        """
        db_call(query)

def insert_tool_primary_purposes():
    for tool_id in range(1, len(tools) + 1):
        purpose = random.choice(tool_primary_purposes)
        query = f"""
            INSERT INTO Tool_PrimaryPurposes (ToolID, PrimaryPurpose)
            VALUES ({tool_id}, '{purpose}');
        """
        db_call(query)

def insert_companies():
    for i, company in enumerate(company_names, start=1):
        name = make_unique(company, used_company_names)
        industry = random.choice(industries)
        country = random.choice(countries)
        gross_profit = random.randint(50000, 1000000)
        query = f"""
            INSERT INTO Company (CompanyID, Name, GrossProfit, Industry, Country)
            VALUES ({i}, '{name}', {gross_profit}, '{industry}', '{country}');
        """
        db_call(query)

def insert_projects():
    for i in range(1, 11):
        base_name = f"{random.choice(company_names)} {random.choice(project_descriptions)}"
        name = make_unique(base_name, used_project_names)
        company_id = random.randint(1, len(company_names))
        description = random.choice(project_descriptions)
        duration = random.randint(6, 24)
        budget = random.randint(10000, 500000)
        query = f"""
            INSERT INTO Project (ProjectID, CompanyID, Name, Description, Duration, Budget)
            VALUES ({i}, {company_id}, '{name}', '{description}', {duration}, {budget});
        """
        db_call(query)

def insert_technology_types():
    for i, tech_type in enumerate(technology_types, start=1):
        description = f"This is a {tech_type}."
        query = f"""
            INSERT INTO TechnologyType (TypeID, Name, Description)
            VALUES ({i}, '{tech_type}', '{description}');
        """
        db_call(query)

def insert_technologies():
    for i, name in enumerate(technology_names, start=1):
        date_of_release = random_date()
        type_id = random.randint(1, len(technology_types))
        query = f"""
            INSERT INTO Technology (TechID, Name, DateOfRelease, TypeID)
            VALUES ({i}, '{name}', '{date_of_release}', {type_id});
        """
        db_call(query)

def insert_technology_use_cases():
    for tech_id in range(1, len(technology_names) + 1):
        usecase = random.choice(technology_use_cases)
        query = f"""
            INSERT INTO Technology_UseCases (TechID, UseCase)
            VALUES ({tech_id}, '{usecase}');
        """
        db_call(query)

def insert_users():
    for i in range(1, 21):
        name = f"User {i}"
        education_level = random.choice(education_levels)
        coding_level = random.choice(coding_levels)
        years_coding = random.randint(0, 20)
        age = random.randint(18, 50)
        gender = random.choice(genders)
        location = random.choice(countries)
        query = f"""
            INSERT INTO User (UserID, Name, EducationLevel, CodingLevel, YearsCoding, Age, Gender, Location)
            VALUES ({i}, '{name}', '{education_level}', '{coding_level}', {years_coding}, {age}, '{gender}', '{location}');
        """
        db_call(query)

def insert_developer_types():
    for i, dev_type in enumerate(developer_types, start=1):
        popularity = random.randint(1, 10)
        experience = random.randint(0, 10)
        query = f"""
            INSERT INTO DeveloperType (TypeID, Name, PopularityRating, RequiredExperience)
            VALUES ({i}, '{dev_type}', {popularity}, {experience});
        """
        db_call(query)

def insert_positions():
    for i in range(1, 21):
        developer_type_id = random.randint(1, len(developer_types))
        company_id = random.randint(1, len(company_names))
        remote_policy = random.choice(remote_policies)
        salary = random.randint(50000, 200000)
        working_time = random.choice(working_times)
        query = f"""
            INSERT INTO Position (DeveloperTypeID, UserID, CompanyID, RemotePolicy, Salary, WorkingTime)
            VALUES ({developer_type_id}, {i}, {company_id}, '{remote_policy}', {salary}, '{working_time}');
        """
        db_call(query)

def insert_technology_dependencies():
    for _ in range(10):
        dependent_tech_id = random.randint(1, len(technology_names))
        supporting_tech_id = random.randint(1, len(technology_names))
        if dependent_tech_id != supporting_tech_id:
            query = f"""
                INSERT INTO Technology_Dependency (DependentTechID, SupportingTechID)
                VALUES ({dependent_tech_id}, {supporting_tech_id});
            """
            db_call(query)


# Function to insert data into Assigned_To
def insert_assigned_to():
    for project_id in range(1, 11):  # Assuming 10 projects
        user_count = random.randint(2, 5)  # Assign 2-5 users to each project
        assigned_users = random.sample(range(1, 21), user_count)  # Randomly pick unique users (1 to 20)
        for user_id in assigned_users:
            role = random.choice(roles)
            query = f"""
                INSERT INTO Assigned_To (UserID, ProjectID, Role)
                VALUES ({user_id}, {project_id}, '{role}');
            """
            db_call(query)

# Function to insert data into Learns_From
def insert_learns_from():
    for user_id in range(1, 21):  # Assuming 20 users
        resource_count = random.randint(2, 5)  # Each user learns from 2-5 resources
        learned_resources = random.sample(range(1, 6), resource_count)  # Assuming 5 resources
        for resource_id in learned_resources:
            query = f"""
                INSERT INTO Learns_From (UserID, ResourceID)
                VALUES ({user_id}, {resource_id});
            """
            db_call(query)

# Function to insert data into Project_Uses_Technology
def insert_project_uses_technology():
    for project_id in range(1, 11):  # Assuming 10 projects
        tech_count = random.randint(2, 4)  # Each project uses 2-4 technologies
        used_technologies = random.sample(range(1, 11), tech_count)  # Assuming 10 technologies
        for tech_id in used_technologies:
            query = f"""
                INSERT INTO Project_Uses_Technology (ProjectID, TechID)
                VALUES ({project_id}, {tech_id});
            """
            db_call(query)

# Function to insert data into Resource_Teaches_Technology
def insert_resource_teaches_technology():
    for tech_id in range(1, len(technology_names)+1): 
        resource_count = random.randint(1, 2)  # Each technology is taught by 1-2 resources
        teaching_resources = random.sample(range(1, 6), resource_count)  # Assuming 5 resources
        for resource_id in teaching_resources:
            query = f"""
                INSERT INTO Resource_Teaches_Technology (ResourceID, TechID)
                VALUES ({resource_id}, {tech_id});
            """
            db_call(query)

# Function to insert data into Resource_Uses_Tool
def insert_resource_uses_tool():
    for tool_id in range(1, len(tools)+1):
        resource_count = random.randint(1, 2)  # Each tool is used by 1-2 resources
        using_resources = random.sample(range(1, 6), resource_count)  # Assuming 5 resources
        for resource_id in using_resources:
            query = f"""
                INSERT INTO Resource_Uses_Tool (ToolID, ResourceID)
                VALUES ({tool_id}, {resource_id});
            """
            db_call(query)




def delete_all_data():
    """Deletes all data from all tables."""
    tables = [
        "Assigned_To", "Learns_From", "Project_Uses_Technology", "Resource_Teaches_Technology", "Resource_Uses_Tool",
        "Technology_Dependency", "Position", "DeveloperType", "User",
        "Technology", "TechnologyType", "Project", "Company", 
        "Tool_PrimaryPurposes", "Tool", "Resource"
    ]
    for table in tables:
        query = f"DELETE FROM {table};"
        db_call(query)
    print("All data deleted from all tables.")


# Main Execution
if __name__ == "__main__":
    # delete_all_data()
    insert_tool()
    insert_resources()
    insert_tool_primary_purposes()
    insert_companies()
    insert_projects()
    insert_technology_types()
    insert_technologies()
    insert_technology_use_cases()
    insert_users()
    insert_developer_types()
    insert_positions()
    insert_technology_dependencies()

    insert_assigned_to()
    insert_learns_from()
    insert_project_uses_technology()
    insert_resource_teaches_technology()
    insert_resource_uses_tool()
    print("Data Inserted Successfully!")