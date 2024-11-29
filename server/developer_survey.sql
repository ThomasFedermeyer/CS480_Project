-- MySQL dump 10.13  Distrib 9.0.1, for macos14 (arm64)
--
-- Host: localhost    Database: developer_survey
-- ------------------------------------------------------
-- Server version	9.0.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Assigned_To`
--

DROP TABLE IF EXISTS `Assigned_To`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Assigned_To` (
  `UserID` int NOT NULL,
  `ProjectID` int NOT NULL,
  `Role` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserID`,`ProjectID`),
  KEY `ProjectID` (`ProjectID`),
  CONSTRAINT `assigned_to_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `assigned_to_ibfk_2` FOREIGN KEY (`ProjectID`) REFERENCES `Project` (`ProjectID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Assigned_To`
--

LOCK TABLES `Assigned_To` WRITE;
/*!40000 ALTER TABLE `Assigned_To` DISABLE KEYS */;
INSERT INTO `Assigned_To` VALUES (1,1,'Backend API developer'),(1,2,'AI model trainer'),(2,3,'Frontend Developer');
/*!40000 ALTER TABLE `Assigned_To` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Company`
--

DROP TABLE IF EXISTS `Company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Company` (
  `CompanyID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `GrossProfit` int DEFAULT NULL,
  `Industry` varchar(50) DEFAULT NULL,
  `Country` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`CompanyID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Company`
--

LOCK TABLES `Company` WRITE;
/*!40000 ALTER TABLE `Company` DISABLE KEYS */;
INSERT INTO `Company` VALUES (1,'Google',1000000,'Internet Search',NULL),(2,'Endowus',100000,'Fintech','Singapore');
/*!40000 ALTER TABLE `Company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `DeveloperType`
--

DROP TABLE IF EXISTS `DeveloperType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `DeveloperType` (
  `TypeID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `PopularityRating` int DEFAULT NULL,
  `RequiredExperience` int DEFAULT NULL,
  PRIMARY KEY (`TypeID`),
  CONSTRAINT `developertype_chk_1` CHECK ((`PopularityRating` between 1 and 10))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `DeveloperType`
--

LOCK TABLES `DeveloperType` WRITE;
/*!40000 ALTER TABLE `DeveloperType` DISABLE KEYS */;
INSERT INTO `DeveloperType` VALUES (1,'Data Engineer',5,1),(2,'Full-Stack Engineer',10,2),(3,'AI Engineer',10,2);
/*!40000 ALTER TABLE `DeveloperType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Learns_From`
--

DROP TABLE IF EXISTS `Learns_From`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Learns_From` (
  `UserID` int NOT NULL,
  `ResourceID` int NOT NULL,
  PRIMARY KEY (`UserID`,`ResourceID`),
  KEY `ResourceID` (`ResourceID`),
  CONSTRAINT `learns_from_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `learns_from_ibfk_2` FOREIGN KEY (`ResourceID`) REFERENCES `Resource` (`ResourceID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Learns_From`
--

LOCK TABLES `Learns_From` WRITE;
/*!40000 ALTER TABLE `Learns_From` DISABLE KEYS */;
INSERT INTO `Learns_From` VALUES (1,1),(3,3);
/*!40000 ALTER TABLE `Learns_From` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Position`
--

DROP TABLE IF EXISTS `Position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Position` (
  `DeveloperTypeID` int NOT NULL,
  `UserID` int NOT NULL,
  `CompanyID` int NOT NULL,
  `RemotePolicy` enum('Remote','Hybrid','Onsite') NOT NULL,
  `Salary` int NOT NULL,
  `WorkingTime` enum('FullTime','PartTime') NOT NULL,
  PRIMARY KEY (`DeveloperTypeID`,`UserID`,`CompanyID`),
  KEY `UserID` (`UserID`),
  KEY `CompanyID` (`CompanyID`),
  CONSTRAINT `position_ibfk_1` FOREIGN KEY (`DeveloperTypeID`) REFERENCES `DeveloperType` (`TypeID`),
  CONSTRAINT `position_ibfk_2` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`),
  CONSTRAINT `position_ibfk_3` FOREIGN KEY (`CompanyID`) REFERENCES `Company` (`CompanyID`),
  CONSTRAINT `position_chk_1` CHECK ((`Salary` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Position`
--

LOCK TABLES `Position` WRITE;
/*!40000 ALTER TABLE `Position` DISABLE KEYS */;
INSERT INTO `Position` VALUES (2,1,2,'Remote',22500,'FullTime'),(2,3,1,'Onsite',42500,'FullTime');
/*!40000 ALTER TABLE `Position` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Project`
--

DROP TABLE IF EXISTS `Project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Project` (
  `ProjectID` int NOT NULL AUTO_INCREMENT,
  `CompanyID` int DEFAULT NULL,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(500) DEFAULT NULL,
  `Duration` int NOT NULL,
  `Budget` int DEFAULT NULL,
  PRIMARY KEY (`ProjectID`),
  KEY `CompanyID` (`CompanyID`),
  CONSTRAINT `project_ibfk_1` FOREIGN KEY (`CompanyID`) REFERENCES `Company` (`CompanyID`),
  CONSTRAINT `project_chk_1` CHECK ((`Duration` >= 1)),
  CONSTRAINT `project_chk_2` CHECK ((`Budget` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Project`
--

LOCK TABLES `Project` WRITE;
/*!40000 ALTER TABLE `Project` DISABLE KEYS */;
INSERT INTO `Project` VALUES (1,2,'Asset Transfer','Clients can transfer their instruments from external sites to our accounts',2,10000),(2,1,'Google Search','A search engine to search all web pages',24,100000),(3,1,'GPay','A payment portal',12,10000);
/*!40000 ALTER TABLE `Project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Project_Uses_Technology`
--

DROP TABLE IF EXISTS `Project_Uses_Technology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Project_Uses_Technology` (
  `ProjectID` int NOT NULL,
  `TechID` int NOT NULL,
  PRIMARY KEY (`ProjectID`,`TechID`),
  KEY `TechID` (`TechID`),
  CONSTRAINT `project_uses_technology_ibfk_1` FOREIGN KEY (`ProjectID`) REFERENCES `Project` (`ProjectID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `project_uses_technology_ibfk_2` FOREIGN KEY (`TechID`) REFERENCES `Technology` (`TechID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Project_Uses_Technology`
--

LOCK TABLES `Project_Uses_Technology` WRITE;
/*!40000 ALTER TABLE `Project_Uses_Technology` DISABLE KEYS */;
INSERT INTO `Project_Uses_Technology` VALUES (2,2),(3,2),(3,3),(3,4);
/*!40000 ALTER TABLE `Project_Uses_Technology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resource`
--

DROP TABLE IF EXISTS `Resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resource` (
  `ResourceID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Type` enum('Documentation','Community Platform','Course/Tutorial','Practical','Media and Content') NOT NULL,
  PRIMARY KEY (`ResourceID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resource`
--

LOCK TABLES `Resource` WRITE;
/*!40000 ALTER TABLE `Resource` DISABLE KEYS */;
INSERT INTO `Resource` VALUES (1,'StackOverflow','Community Platform'),(3,'Khan Academy','Course/Tutorial');
/*!40000 ALTER TABLE `Resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resource_Teaches_Technology`
--

DROP TABLE IF EXISTS `Resource_Teaches_Technology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resource_Teaches_Technology` (
  `ResourceID` int NOT NULL,
  `TechID` int NOT NULL,
  PRIMARY KEY (`ResourceID`,`TechID`),
  KEY `TechID` (`TechID`),
  CONSTRAINT `resource_teaches_technology_ibfk_1` FOREIGN KEY (`ResourceID`) REFERENCES `Resource` (`ResourceID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `resource_teaches_technology_ibfk_2` FOREIGN KEY (`TechID`) REFERENCES `Technology` (`TechID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resource_Teaches_Technology`
--

LOCK TABLES `Resource_Teaches_Technology` WRITE;
/*!40000 ALTER TABLE `Resource_Teaches_Technology` DISABLE KEYS */;
INSERT INTO `Resource_Teaches_Technology` VALUES (1,1),(1,2),(3,2),(3,3),(1,4);
/*!40000 ALTER TABLE `Resource_Teaches_Technology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Resource_Uses_Tool`
--

DROP TABLE IF EXISTS `Resource_Uses_Tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Resource_Uses_Tool` (
  `ToolID` int NOT NULL,
  `ResourceID` int NOT NULL,
  PRIMARY KEY (`ToolID`,`ResourceID`),
  KEY `ResourceID` (`ResourceID`),
  CONSTRAINT `resource_uses_tool_ibfk_1` FOREIGN KEY (`ToolID`) REFERENCES `Tool` (`ToolID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `resource_uses_tool_ibfk_2` FOREIGN KEY (`ResourceID`) REFERENCES `Resource` (`ResourceID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Resource_Uses_Tool`
--

LOCK TABLES `Resource_Uses_Tool` WRITE;
/*!40000 ALTER TABLE `Resource_Uses_Tool` DISABLE KEYS */;
INSERT INTO `Resource_Uses_Tool` VALUES (29,3);
/*!40000 ALTER TABLE `Resource_Uses_Tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Technology`
--

DROP TABLE IF EXISTS `Technology`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Technology` (
  `TechID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `DateOfRelease` date NOT NULL,
  `TypeID` int NOT NULL,
  PRIMARY KEY (`TechID`),
  KEY `TypeID` (`TypeID`),
  CONSTRAINT `technology_ibfk_1` FOREIGN KEY (`TypeID`) REFERENCES `TechnologyType` (`TypeID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Technology`
--

LOCK TABLES `Technology` WRITE;
/*!40000 ALTER TABLE `Technology` DISABLE KEYS */;
INSERT INTO `Technology` VALUES (1,'C++','2001-01-01',1),(2,'Python','2005-04-07',1),(3,'React','2010-04-07',2),(4,'Javascript','2005-04-07',1);
/*!40000 ALTER TABLE `Technology` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Technology_Dependency`
--

DROP TABLE IF EXISTS `Technology_Dependency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Technology_Dependency` (
  `DependentTechID` int NOT NULL,
  `SupportingTechID` int NOT NULL,
  PRIMARY KEY (`DependentTechID`,`SupportingTechID`),
  KEY `SupportingTechID` (`SupportingTechID`),
  CONSTRAINT `technology_dependency_ibfk_1` FOREIGN KEY (`DependentTechID`) REFERENCES `Technology` (`TechID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `technology_dependency_ibfk_2` FOREIGN KEY (`SupportingTechID`) REFERENCES `Technology` (`TechID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Technology_Dependency`
--

LOCK TABLES `Technology_Dependency` WRITE;
/*!40000 ALTER TABLE `Technology_Dependency` DISABLE KEYS */;
INSERT INTO `Technology_Dependency` VALUES (2,1),(4,3);
/*!40000 ALTER TABLE `Technology_Dependency` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Technology_UseCases`
--

DROP TABLE IF EXISTS `Technology_UseCases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Technology_UseCases` (
  `TechID` int NOT NULL,
  `UseCase` varchar(200) NOT NULL,
  PRIMARY KEY (`TechID`,`UseCase`),
  CONSTRAINT `technology_usecases_ibfk_1` FOREIGN KEY (`TechID`) REFERENCES `Technology` (`TechID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Technology_UseCases`
--

LOCK TABLES `Technology_UseCases` WRITE;
/*!40000 ALTER TABLE `Technology_UseCases` DISABLE KEYS */;
INSERT INTO `Technology_UseCases` VALUES (1,'Class Based'),(1,'Embedded Software'),(2,'AI Architectures'),(2,'Data Manipulation'),(3,'Frontend design'),(3,'Managing States'),(4,'Graphics'),(4,'Web development');
/*!40000 ALTER TABLE `Technology_UseCases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TechnologyType`
--

DROP TABLE IF EXISTS `TechnologyType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TechnologyType` (
  `TypeID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`TypeID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TechnologyType`
--

LOCK TABLES `TechnologyType` WRITE;
/*!40000 ALTER TABLE `TechnologyType` DISABLE KEYS */;
INSERT INTO `TechnologyType` VALUES (1,'Programming Language','Set of rules and syntax used to write instructions that computers can execute to perform specific tasks. It bridges the gap between human ideas and machine operations'),(2,'Framework','Pre-built set of tools, libraries, and guidelines that simplifies software development by providing a structured foundation for building applications. It helps streamline repetitive tasks and enforces best practices.');
/*!40000 ALTER TABLE `TechnologyType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tool`
--

DROP TABLE IF EXISTS `Tool`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tool` (
  `ToolID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Type` enum('IDE','Collab') NOT NULL,
  `SyncCapability` enum('Y','N') DEFAULT NULL,
  `DateOfRelease` date NOT NULL,
  PRIMARY KEY (`ToolID`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tool`
--

LOCK TABLES `Tool` WRITE;
/*!40000 ALTER TABLE `Tool` DISABLE KEYS */;
INSERT INTO `Tool` VALUES (27,'Git','Collab','Y','2005-04-07'),(28,'CLion','IDE','N','2015-04-14'),(29,'VSCode','IDE','N','2015-04-14');
/*!40000 ALTER TABLE `Tool` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tool_PrimaryPurposes`
--

DROP TABLE IF EXISTS `Tool_PrimaryPurposes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tool_PrimaryPurposes` (
  `ToolID` int NOT NULL,
  `PrimaryPurpose` varchar(200) NOT NULL,
  PRIMARY KEY (`ToolID`,`PrimaryPurpose`),
  CONSTRAINT `tool_primarypurposes_ibfk_1` FOREIGN KEY (`ToolID`) REFERENCES `Tool` (`ToolID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tool_PrimaryPurposes`
--

LOCK TABLES `Tool_PrimaryPurposes` WRITE;
/*!40000 ALTER TABLE `Tool_PrimaryPurposes` DISABLE KEYS */;
INSERT INTO `Tool_PrimaryPurposes` VALUES (27,'Collab between developers'),(27,'Version control for code'),(29,'Also supports Mysql operations'),(29,'IDE for coding in all languages');
/*!40000 ALTER TABLE `Tool_PrimaryPurposes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `User` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `EducationLevel` enum('Primary/elementary school','Secondary school','Bachelor''s degree','Master''s degree','Professional degree','Something else') NOT NULL,
  `CodingLevel` enum('Professional','Learning','Other') NOT NULL,
  `YearsCoding` int DEFAULT NULL,
  `Age` int NOT NULL,
  `Gender` enum('M','F','O') NOT NULL,
  `Location` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`UserID`),
  CONSTRAINT `user_chk_1` CHECK ((`YearsCoding` >= 0)),
  CONSTRAINT `user_chk_2` CHECK ((`Age` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'Mehul Mathur','Master\'s degree','Professional',5,23,'M','USA'),(2,'Krishna','Master\'s degree','Professional',10,28,'M','USA'),(3,'Hrushikesh Joshi','Master\'s degree','Professional',7,25,'M','USA'),(4,'Mehak Mathur','Bachelor\'s degree','Learning',NULL,19,'F','India');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-28 20:35:32
