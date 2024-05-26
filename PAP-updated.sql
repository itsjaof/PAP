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
  `type` enum('CÓDIGO','TEÓRICA','SIMULADOR','EXAME') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
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
INSERT INTO `agenda` VALUES (2,3,'2025-02-12','EXAME'),(2,3,'2025-10-02','CÓDIGO'),(2,3,'2026-03-12','CÓDIGO'),(2,7,'2024-05-24','SIMULADOR'),(2,7,'2025-12-12','TEÓRICA'),(2,7,'2027-01-31','CÓDIGO'),(8,3,'2026-04-26','CÓDIGO');
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
  `type` enum('USER','STAFF','INSTRUTOR','ADMIN') CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `picture` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index` (`username`,`email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'admin','admin','ADMIN','admin@admin.pt','Administrador',1),(2,'staff','staff','STAFF','staff@staff.pt','Staff',0),(3,'utilizador','utilizador','USER','utilizador@gmail.com','Utilizador',0),(7,'utilizadorteste','teste','USER','teste@teste.com','Teste',0),(8,'professor','professor','STAFF','professor@teste.pt','Instrutor',0),(9,'instrutor','instrutor','INSTRUTOR','instrutor@email.pt','Instrutor',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (1,'Nome Teste','teste@email.com','Mensagem de teste'),(2,'Teste 2','teste2@teste.pt','Esta é a segunda mensagem de teste!'),(3,'João Ribeiro','joaoribeiro@esar.edu.pt','Teste');
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (7,'session:dae43e57-f677-48ec-aea6-61391e0fee8d',_binary '��&\0\0\0\0\0\0\0}�(�\n_permanent���username��admin�u.','2024-05-20 19:44:26'),(11,'session:5c78689d-c223-469a-b6f5-0fb416698698',_binary '��\0\0\0\0\0\0\0}��\n_permanent��s.','2024-05-20 20:46:46'),(16,'session:762a95f6-7a8b-424f-9a49-2bee68e9c265',_binary '��\0\0\0\0\0\0\0}��\n_permanent��s.','2024-05-20 21:03:08'),(17,'session:56f2bfce-3a2e-435c-b05a-ccb91af00522',_binary '��&\0\0\0\0\0\0\0}�(�\n_permanent���username��admin�u.','2024-05-20 21:06:03'),(19,'session:1ae0f852-7a1c-4a39-b731-6b4226000e12',_binary '��&\0\0\0\0\0\0\0}�(�\n_permanent���username��admin�u.','2024-05-21 09:41:23');
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
  CONSTRAINT `testemunhos_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `auth` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testemunhos`
--

LOCK TABLES `testemunhos` WRITE;
/*!40000 ALTER TABLE `testemunhos` DISABLE KEYS */;
INSERT INTO `testemunhos` VALUES (1,'Teste'),(8,'Teste do ID 4');
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

-- Dump completed on 2024-05-21  9:43:28
