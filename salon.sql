-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: dbbeautysalon
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `calendar`
--

DROP TABLE IF EXISTS `calendar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `calendar` (
  `idDay` datetime NOT NULL,
  `idMaster` int NOT NULL,
  `freeTime` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idMaster`,`idDay`),
  CONSTRAINT `calendar_ibfk_1` FOREIGN KEY (`idMaster`) REFERENCES `master` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `calendar`
--

LOCK TABLES `calendar` WRITE;
/*!40000 ALTER TABLE `calendar` DISABLE KEYS */;
INSERT INTO `calendar` VALUES ('2021-12-07 00:00:00',1,'0-14'),('2021-12-08 00:00:00',1,'0-14'),('2021-12-11 00:00:00',1,'0-14'),('2021-12-12 00:00:00',1,'0-14'),('2021-12-09 00:00:00',2,'0-14'),('2021-12-10 00:00:00',2,'0-14'),('2021-12-13 00:00:00',2,'0-14'),('2021-12-14 00:00:00',2,'0-14'),('2021-12-07 00:00:00',3,'14-24'),('2021-12-08 00:00:00',3,'14-24'),('2021-12-11 00:00:00',3,'14-24'),('2021-12-12 00:00:00',3,'14-24'),('2021-12-09 00:00:00',4,'14-24'),('2021-12-10 00:00:00',4,'14-24'),('2021-12-13 00:00:00',4,'14-24'),('2021-12-14 00:00:00',4,'14-24');
/*!40000 ALTER TABLE `calendar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `master`
--

DROP TABLE IF EXISTS `master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `master` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lastname` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `service` varchar(50) DEFAULT NULL,
  `isTop` tinyint(1) DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `countClient` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `master`
--

LOCK TABLES `master` WRITE;
/*!40000 ALTER TABLE `master` DISABLE KEYS */;
INSERT INTO `master` VALUES (1,'Растремина','Анастасия','маникюр,педикюр',0,5,1),(2,'Пупкина','Васелина','наращивание ресниц',0,0,0),(3,'Чушкина','Маргарита','маникюр,педикюр',1,0,0),(4,'Небукина','Ирина','эпиляция',0,0,0);
/*!40000 ALTER TABLE `master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `record` (
  `idUser` int NOT NULL,
  `idMaster` int NOT NULL,
  `idService` int NOT NULL,
  `time` varchar(50) DEFAULT NULL,
  `idDay` datetime NOT NULL,
  PRIMARY KEY (`idUser`,`idMaster`,`idService`,`idDay`),
  KEY `idMaster` (`idMaster`),
  KEY `idService` (`idService`),
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`idMaster`) REFERENCES `master` (`id`),
  CONSTRAINT `record_ibfk_2` FOREIGN KEY (`idService`) REFERENCES `service` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
INSERT INTO `record` VALUES (168671681,1,1,'13','2021-12-02 00:00:00'),(168671681,1,1,'13','2021-12-08 00:00:00');
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `service` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `priceTop` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `time` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,'маникюр',2000,1000,3),(2,'педикюр',2500,1500,3),(3,'наращивание ресниц',3500,2200,5),(4,'эпиляция',900,500,1);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-07 15:14:15
