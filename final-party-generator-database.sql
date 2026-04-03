-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `class_roles`
--

DROP TABLE IF EXISTS `class_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class_roles` (
  `class_role_id` int NOT NULL AUTO_INCREMENT,
  `class_id` int NOT NULL,
  `role_id` int NOT NULL,
  `suitability_score` decimal(3,2) NOT NULL,
  PRIMARY KEY (`class_role_id`),
  UNIQUE KEY `class_id` (`class_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `class_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `roles` (`role_id`),
  CONSTRAINT `fk_class_roles_class` FOREIGN KEY (`class_id`) REFERENCES `classes` (`class_id`),
  CONSTRAINT `chk_suitability_score` CHECK (((`suitability_score` >= 0) and (`suitability_score` <= 1)))
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class_roles`
--

LOCK TABLES `class_roles` WRITE;
/*!40000 ALTER TABLE `class_roles` DISABLE KEYS */;
INSERT INTO `class_roles` VALUES (1,1,3,0.10),(2,1,1,0.35),(3,1,2,1.00),(4,2,3,1.00),(5,2,1,0.90),(6,2,2,0.20),(7,3,3,1.00),(8,3,1,0.85),(9,3,2,0.45),(10,4,3,0.15),(11,4,1,0.60),(12,4,2,1.00),(13,5,3,0.55),(14,5,1,0.65),(15,5,2,0.80),(16,6,3,0.40),(17,6,1,0.55),(18,6,2,0.75),(19,7,3,0.80),(20,7,1,0.50),(21,7,2,0.30),(22,8,3,0.85),(23,8,1,0.70),(24,8,2,0.35);
/*!40000 ALTER TABLE `class_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `classes` (
  `class_type` varchar(15) NOT NULL,
  `strength` int NOT NULL,
  `dexterity` int NOT NULL,
  `constitution` int NOT NULL,
  `intelligence` int NOT NULL,
  `wisdom` int NOT NULL,
  `charisma` int NOT NULL,
  `class_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`class_id`),
  UNIQUE KEY `uq_class_type` (`class_type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES ('Barbarian',15,12,15,8,10,8,1),('Bard',8,14,12,10,10,15,2),('Cleric',10,10,14,8,15,12,3),('Fighter',15,13,14,8,10,8,4),('Ranger',10,15,13,10,14,10,5),('Rogue',8,15,13,14,10,10,6),('Sorcerer',8,13,14,10,8,15,7),('Warlock',8,13,10,10,12,15,8);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `races`
--

DROP TABLE IF EXISTS `races`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `races` (
  `race_type` varchar(15) NOT NULL,
  `strength` int NOT NULL,
  `dexterity` int NOT NULL,
  `constitution` int NOT NULL,
  `intelligence` int NOT NULL,
  `wisdom` int NOT NULL,
  `charisma` int NOT NULL,
  `race_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`race_id`),
  UNIQUE KEY `uq_race_type` (`race_type`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `races`
--

LOCK TABLES `races` WRITE;
/*!40000 ALTER TABLE `races` DISABLE KEYS */;
INSERT INTO `races` VALUES ('dragonborn',2,0,0,0,0,1,1),('dwarf',1,0,2,0,0,0,2),('elf',0,2,0,0,1,0,3),('gnome',0,1,0,2,0,0,4),('goliath',2,0,1,0,0,0,5),('human',0,1,0,1,0,1,6),('orc',2,0,1,0,0,0,7),('tiefling',0,0,0,1,0,2,8);
/*!40000 ALTER TABLE `races` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(15) NOT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (2,'Fighter'),(1,'Leader'),(3,'Support');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-03 12:28:50
