CREATE DATABASE  IF NOT EXISTS `pap` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `pap`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: pap
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `agenda`
--

DROP TABLE IF EXISTS `agenda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `agenda` (
  `teacher_id` int NOT NULL,
  `student_id` int NOT NULL,
  `date` date NOT NULL,
  `type` enum('CÃ“DIGO','TEÃ“RICA','SIMULADOR','EXAME') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`teacher_id`,`student_id`,`date`),
  KEY `agenda_auth_FK_1` (`student_id`),
  CONSTRAINT `agenda_auth_FK` FOREIGN KEY (`teacher_id`) REFERENCES `auth` (`id`),
  CONSTRAINT `agenda_auth_FK_1` FOREIGN KEY (`student_id`) REFERENCES `auth` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agenda`
--

LOCK TABLES `agenda` WRITE;
/*!40000 ALTER TABLE `agenda` DISABLE KEYS */;
INSERT INTO `agenda` VALUES (2,3,'2024-07-25','TEÃ“RICA');
/*!40000 ALTER TABLE `agenda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `type` enum('USER','STAFF','ADMIN') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `picture` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`username`,`email`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'admin','admin','ADMIN','admin@admin.pt','Administrador',0),(2,'staff','staff','STAFF','staff@staff.pt','Staff',0),(3,'utilizador','utilizador','USER','utilizador@gmail.com','Utilizador',0);
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'JoÃ£o','joao@email.com','Mensagem de teste.');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `data` blob,
  `expiry` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (7,'session:dae43e57-f677-48ec-aea6-61391e0fee8d',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-20 19:44:26'),(11,'session:5c78689d-c223-469a-b6f5-0fb416698698',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-05-20 20:46:46'),(16,'session:762a95f6-7a8b-424f-9a49-2bee68e9c265',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-05-20 21:03:08'),(17,'session:56f2bfce-3a2e-435c-b05a-ccb91af00522',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-20 21:06:03'),(19,'session:1ae0f852-7a1c-4a39-b731-6b4226000e12',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-21 09:50:24'),(22,'session:af998435-af8d-4212-b17a-41c2898f1e8b',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-25 09:24:40'),(30,'session:3c084aa8-1f00-42e9-951a-66465b7891c6',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-05-26 16:03:49'),(31,'session:43270922-8f7a-4422-8b40-4abb85c14345',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-27 10:33:54'),(33,'session:53d9ffbc-5492-4363-a38b-192dbd77839f',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-27 16:29:46'),(34,'session:4384c80d-d79e-4aad-aafb-877b044c6820',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-05-31 21:08:26'),(40,'session:98c33664-09cd-4469-af53-a09d4f217be7',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-06-01 15:45:03'),(42,'session:bb1421bd-c146-44b3-a259-48ca1299cbd4',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œstaff”u.','2024-06-03 17:18:16'),(43,'session:d4fc903e-da84-456c-b498-c52e7ee5403e',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-06-04 10:04:55'),(44,'session:8dd0eaad-af5d-43d6-91f1-3746713cee15',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 11:02:54'),(46,'session:8fac8055-93d7-4e75-a76b-0fa7e97367e3',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 15:47:09'),(47,'session:c341c763-c723-46b8-ba1a-2d1d0bb8284c',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 15:47:09'),(48,'session:6177a801-221b-4abb-920a-4f4e275df5ba',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 15:47:09'),(49,'session:7c65ce98-4f51-460f-88e6-edeb29c75107',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 15:47:09'),(50,'session:eea123cd-ca74-4b07-a4ff-7d17f47cb4ca',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 15:47:11'),(52,'session:25608f69-2a54-4b84-9610-47dc35278a1b',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 16:06:20'),(53,'session:30db9fa4-581a-49f1-9bdb-2bc2e3ab59aa',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-06-04 16:13:00'),(54,'session:89a36b87-a14a-4843-a44c-2aaaf42ab492',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-04 16:15:46'),(55,'session:f3d765c2-78b9-487f-be18-f719bcb2a285',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 08:51:44'),(56,'session:c96b839d-c9ac-449b-b2a2-99f119e47529',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 08:53:28'),(57,'session:d27557c0-1a4b-4bed-97b1-2f3e204f57d7',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:33'),(58,'session:a207bc1a-684d-46cd-b4f6-147600328545',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:32'),(59,'session:a5215586-7f0e-47f1-9cbe-db13540b2862',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:32'),(60,'session:b870e203-36db-4430-b79f-0d9687fefe46',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:32'),(61,'session:d50e52b9-4a9f-4af4-b242-bdb5ac7cc205',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:32'),(62,'session:b2ab58f7-38ec-41d8-9ce7-265d82d14daa',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-06-05 10:48:32'),(66,'session:79578147-817d-464d-9f4d-bf1adff40d47',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-06-06 11:11:40'),(69,'session:cb331f63-46ce-40a9-9901-3f89ca4a09e4',_binary '€•+\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œ\nutilizador”u.','2024-06-06 15:59:49'),(72,'session:96ce3c92-aa41-48eb-a237-3e36501a15ff',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œstaff”u.','2024-06-06 22:20:38'),(73,'session:2d487d93-d4be-47e4-a26b-9b866b452492',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œstaff”u.','2024-06-06 22:26:27'),(74,'session:cb69ec76-00aa-4ab6-a534-aba33b00e097',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-06-06 22:35:05'),(76,'session:df10924a-f99c-4080-838e-4c0621b1f387',_binary '€•0\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œutilizadorteste”u.','2024-07-04 19:17:42'),(78,'session:6eaa278c-423c-4b24-9409-90f2db7f0dc0',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-05 16:42:39'),(84,'session:dd8cc662-d07e-4146-a0a1-07b4bdd00d6d',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-06 00:15:25'),(85,'session:9a4618f7-0e8e-4c93-ab7d-9069115f9e49',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-07-06 09:26:25'),(86,'session:5202b222-9c60-4658-84dd-485d52c467f3',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-06 15:12:32'),(87,'session:adcef0e9-5653-4103-ad5a-d1c93c2c4e0f',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-06 19:16:37'),(88,'session:02baa76f-e4e2-4164-80e7-569f4962c366',_binary '€•\0\0\0\0\0\0\0}”Œ\n_permanent”ˆs.','2024-07-07 12:25:35'),(90,'session:c3de5934-2c6d-455a-b073-052ea937d9ef',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-07 13:51:20'),(91,'session:03c206ea-f712-469f-88e9-5fd1dc60c3d7',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-07 16:11:43'),(95,'session:7e30c6b6-bd3d-4bd9-b2fb-635fe84ddc6b',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-07 20:38:10'),(102,'session:ac938366-bf62-4cfa-bf43-2dc168193c62',_binary '€•&\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œadmin”u.','2024-07-07 23:15:54'),(103,'session:50ebe4b8-fe09-4fd8-b71e-933ac6cc938e',_binary '€•+\0\0\0\0\0\0\0}”(Œ\n_permanent”ˆŒusername”Œ\nUtilizador”u.','2024-07-07 23:33:43');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testemunhos`
--

DROP TABLE IF EXISTS `testemunhos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testemunhos` (
  `userid` int NOT NULL,
  `testemunho` varchar(250) NOT NULL,
  PRIMARY KEY (`userid`),
  CONSTRAINT `testemunhos_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `auth` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testemunhos`
--

LOCK TABLES `testemunhos` WRITE;
/*!40000 ALTER TABLE `testemunhos` DISABLE KEYS */;
INSERT INTO `testemunhos` VALUES (3,'Um testemunho de teste.');
/*!40000 ALTER TABLE `testemunhos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-07 23:36:50
