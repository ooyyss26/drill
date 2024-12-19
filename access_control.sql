-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: access_control
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `facilities`
--

DROP TABLE IF EXISTS `facilities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities` (
  `facility_id` int NOT NULL,
  `facility_type_code` varchar(45) NOT NULL,
  `access_count` varchar(45) NOT NULL,
  `facility_name` varchar(45) NOT NULL,
  `facility_description` varchar(45) NOT NULL,
  `other_details` varchar(45) NOT NULL,
  `Ref_Facility_Types_facility_type_code` int NOT NULL,
  PRIMARY KEY (`facility_id`),
  KEY `fk_Facilities_Ref_Facility_Types_idx` (`Ref_Facility_Types_facility_type_code`),
  CONSTRAINT `fk_Facilities_Ref_Facility_Types` FOREIGN KEY (`Ref_Facility_Types_facility_type_code`) REFERENCES `ref_facility_types` (`facility_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities`
--

LOCK TABLES `facilities` WRITE;
/*!40000 ALTER TABLE `facilities` DISABLE KEYS */;
INSERT INTO `facilities` VALUES (1,'1','10','Main Menu','Main application menu','None',1),(2,'2','5','Employee Records','Records of all employees','Sensitive data',2),(3,'3','8','Dashboard','Main dashboard for reporting','None',3);
/*!40000 ALTER TABLE `facilities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facility_functional_areas`
--

DROP TABLE IF EXISTS `facility_functional_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facility_functional_areas` (
  `functional_area_code` int NOT NULL,
  `facility_id` varchar(45) NOT NULL,
  `Functional_Areas_functional_area_code` int NOT NULL,
  `Facilities_facility_id` int NOT NULL,
  PRIMARY KEY (`functional_area_code`),
  KEY `fk_Facility_Functional_Areas_Functional_Areas1_idx` (`Functional_Areas_functional_area_code`),
  KEY `fk_Facility_Functional_Areas_Facilities1_idx` (`Facilities_facility_id`),
  CONSTRAINT `fk_Facility_Functional_Areas_Facilities1` FOREIGN KEY (`Facilities_facility_id`) REFERENCES `facilities` (`facility_id`),
  CONSTRAINT `fk_Facility_Functional_Areas_Functional_Areas1` FOREIGN KEY (`Functional_Areas_functional_area_code`) REFERENCES `functional_areas` (`functional_area_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facility_functional_areas`
--

LOCK TABLES `facility_functional_areas` WRITE;
/*!40000 ALTER TABLE `facility_functional_areas` DISABLE KEYS */;
INSERT INTO `facility_functional_areas` VALUES (1,'1',1,1),(2,'2',2,2),(3,'3',3,3);
/*!40000 ALTER TABLE `facility_functional_areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `functional_areas`
--

DROP TABLE IF EXISTS `functional_areas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `functional_areas` (
  `functional_area_code` int NOT NULL,
  `parent_functional_area_code` varchar(45) NOT NULL,
  `functional_area_description` varchar(45) NOT NULL,
  `eg HR, Finance` varchar(45) NOT NULL,
  `Functional_Areas_functional_area_code` int NOT NULL,
  PRIMARY KEY (`functional_area_code`),
  KEY `fk_Functional_Areas_Functional_Areas1_idx` (`Functional_Areas_functional_area_code`),
  CONSTRAINT `fk_Functional_Areas_Functional_Areas1` FOREIGN KEY (`Functional_Areas_functional_area_code`) REFERENCES `functional_areas` (`functional_area_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `functional_areas`
--

LOCK TABLES `functional_areas` WRITE;
/*!40000 ALTER TABLE `functional_areas` DISABLE KEYS */;
INSERT INTO `functional_areas` VALUES (1,'0','Human Resources','HR',1),(2,'0','Finance','Finance',2),(3,'1','Recruitment','HR',1);
/*!40000 ALTER TABLE `functional_areas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ref_facility_types`
--

DROP TABLE IF EXISTS `ref_facility_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ref_facility_types` (
  `facility_type_code` int NOT NULL,
  `facility_type_description` varchar(45) NOT NULL,
  `eg Menus, Records, Screens` varchar(45) NOT NULL,
  PRIMARY KEY (`facility_type_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ref_facility_types`
--

LOCK TABLES `ref_facility_types` WRITE;
/*!40000 ALTER TABLE `ref_facility_types` DISABLE KEYS */;
INSERT INTO `ref_facility_types` VALUES (1,'Menu','Menus'),(2,'Record','Records'),(3,'Screen','Screens');
/*!40000 ALTER TABLE `ref_facility_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role_facility_access_rights`
--

DROP TABLE IF EXISTS `role_facility_access_rights`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role_facility_access_rights` (
  `facility_id` int NOT NULL,
  `role_code` varchar(45) NOT NULL,
  `CRUD_Value` varchar(45) NOT NULL,
  `eg R or RW` varchar(45) NOT NULL,
  `Facilities_facility_id` int NOT NULL,
  `Roles_role_code` int NOT NULL,
  PRIMARY KEY (`facility_id`),
  KEY `fk_Role_Facility_Access_Rights_Facilities1_idx` (`Facilities_facility_id`),
  KEY `fk_Role_Facility_Access_Rights_Roles1_idx` (`Roles_role_code`),
  CONSTRAINT `fk_Role_Facility_Access_Rights_Facilities1` FOREIGN KEY (`Facilities_facility_id`) REFERENCES `facilities` (`facility_id`),
  CONSTRAINT `fk_Role_Facility_Access_Rights_Roles1` FOREIGN KEY (`Roles_role_code`) REFERENCES `roles` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role_facility_access_rights`
--

LOCK TABLES `role_facility_access_rights` WRITE;
/*!40000 ALTER TABLE `role_facility_access_rights` DISABLE KEYS */;
INSERT INTO `role_facility_access_rights` VALUES (1,'1','RW','RW',1,1),(2,'2','R','R',2,2),(3,'3','RW','RW',3,3);
/*!40000 ALTER TABLE `role_facility_access_rights` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_code` int NOT NULL,
  `role_description` varchar(45) NOT NULL,
  `eg DBA, Project Mgr` varchar(45) NOT NULL,
  PRIMARY KEY (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Database Administrator','DBA'),(2,'Project Manager','Project Mgr'),(3,'Software Engineer','Engineer');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `role_code` varchar(45) NOT NULL,
  `user_frst_name` varchar(45) NOT NULL,
  `user_last_name` varchar(45) NOT NULL,
  `user_login` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `other_details` varchar(45) NOT NULL,
  `Roles_role_code` int NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_Users_Roles1_idx` (`Roles_role_code`),
  CONSTRAINT `fk_Users_Roles1` FOREIGN KEY (`Roles_role_code`) REFERENCES `roles` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'1','John','Doe','jdoe','password123','None',1),(2,'2','Jane','Smith','jsmith','securepass','None',2),(3,'3','Alice','Johnson','ajohnson','alice2023','None',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-19 16:50:38
