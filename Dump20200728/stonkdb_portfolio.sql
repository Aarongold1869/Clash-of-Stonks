-- MySQL dump 10.13  Distrib 8.0.20, for Win64 (x86_64)
--
-- Host: localhost    Database: stonkdb
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `portfolio`
--

DROP TABLE IF EXISTS `portfolio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `portfolio` (
  `PortID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `stock` varchar(45) DEFAULT NULL,
  `shares` int DEFAULT NULL,
  `total_cost` decimal(10,2) DEFAULT NULL,
  `avg_cost_per` decimal(10,2) GENERATED ALWAYS AS ((`total_cost` / `shares`)) VIRTUAL,
  `date_time` datetime DEFAULT NULL,
  PRIMARY KEY (`PortID`),
  KEY `fk_User2` (`UserID`),
  CONSTRAINT `fk_User2` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portfolio`
--

LOCK TABLES `portfolio` WRITE;
/*!40000 ALTER TABLE `portfolio` DISABLE KEYS */;
INSERT INTO `portfolio` (`PortID`, `UserID`, `stock`, `shares`, `total_cost`, `date_time`) VALUES (3,2,'ibm',10,3000.00,'2020-07-23 14:33:24'),(5,2,'tsla',1,1600.00,'2020-07-23 14:33:24'),(6,1,'tsla',3,3800.00,'2020-07-23 20:43:19'),(7,3,'amzn',3,9300.12,'2020-07-23 21:13:06'),(8,3,'tsla',5,8285.00,'2020-07-23 21:13:06'),(9,3,'ibm',0,0.00,'2020-07-23 21:13:06'),(10,3,'dal',5,131.40,'2020-07-23 21:13:06'),(11,1,'amzn',10,31000.40,'2020-07-23 20:43:19');
/*!40000 ALTER TABLE `portfolio` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-28 11:48:28
