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
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `stock` varchar(45) DEFAULT NULL,
  `shares` int DEFAULT NULL,
  `cost_per` decimal(10,2) DEFAULT NULL,
  `investment` decimal(10,2) GENERATED ALWAYS AS ((`shares` * `cost_per`)) VIRTUAL,
  `date_time` datetime DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `fk_User1` (`UserID`),
  CONSTRAINT `fk_User1` FOREIGN KEY (`UserID`) REFERENCES `user` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` (`OrderID`, `UserID`, `stock`, `shares`, `cost_per`, `date_time`) VALUES (1,1,'tsla',10,1500.00,'2020-07-23 11:53:51'),(3,2,'ibm',10,300.00,'2020-07-23 12:02:38'),(4,2,'tsla',69,1600.00,'2020-07-23 12:23:30'),(5,2,'tsla',69,1600.00,'2020-07-23 12:26:11'),(6,2,'tsla',-100,1600.00,'2020-07-23 12:42:34'),(7,2,'tsla',-100,1600.00,'2020-07-23 12:43:01'),(8,2,'tsla',62,1600.00,'2020-07-23 12:44:15'),(9,1,'tsla',-10,1600.00,'2020-07-23 12:57:38'),(10,2,'tsla',1,1600.00,'2020-07-23 14:33:24'),(11,1,'tsla',3,1600.00,'2020-07-23 14:38:38'),(12,3,'amzn',10,3100.04,'2020-07-23 17:51:19'),(13,3,'tsla',10,1657.00,'2020-07-23 18:00:32'),(14,3,'ibm',1,128.35,'2020-07-23 18:10:16'),(15,3,'tsla',-5,1657.00,'2020-07-23 18:11:50'),(16,3,'ibm',-1,128.35,'2020-07-23 18:22:59'),(17,3,'amzn',-5,3100.04,'2020-07-23 18:25:52'),(18,3,'dal',5,26.28,'2020-07-23 18:26:11'),(19,1,'amzn',10,3100.04,'2020-07-23 20:43:19'),(20,3,'amzn',-2,3100.04,'2020-07-23 21:13:06');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-07-28 11:48:27
