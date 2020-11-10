-- phpMyAdmin SQL Dump
-- version 3.5.2.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2020 at 04:03 AM
-- Server version: 5.5.27
-- PHP Version: 5.4.7

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `barutest`
--

-- --------------------------------------------------------

--
-- Table structure for table `acct`
--

CREATE TABLE IF NOT EXISTS `acct` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `passhash` varchar(128) NOT NULL,
  `email` varchar(32) NOT NULL,
  `dept` varchar(20) NOT NULL,
  `date_create` datetime NOT NULL,
  `activated` tinyint(1) DEFAULT NULL,
  `lock` tinyint(1) DEFAULT NULL,
  `date_lock` datetime NOT NULL,
  `last_login` datetime NOT NULL,
  `last_host` varchar(20) NOT NULL,
  `last_ip` varchar(20) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `logbook`
--

CREATE TABLE IF NOT EXISTS `logbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no_wo` varchar(7) NOT NULL,
  `no_ifca` varchar(10) NOT NULL,
  `date_create` date NOT NULL,
  `unit` varchar(12) NOT NULL,
  `work_req` varchar(512) NOT NULL,
  `staff` varchar(64) NOT NULL,
  `work_act` varchar(10240) NOT NULL,
  `date_done` date NOT NULL,
  `time_done` varchar(10) NOT NULL,
  `received` tinyint(1) DEFAULT NULL,
  `wo_receiver` varchar(32) NOT NULL,
  `date_received` datetime NOT NULL,
  `time_create` varchar(10) NOT NULL,
  `status_ifca` varchar(10) NOT NULL,
  `auth_login` varchar(16) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `onprogress`
--

CREATE TABLE IF NOT EXISTS `onprogress` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no_ifca` varchar(10) NOT NULL,
  `date_update` datetime NOT NULL,
  `commit_update` varchar(512) NOT NULL,
  `auth_by` varchar(64) NOT NULL,
  `auth_login` varchar(16) NOT NULL,
  `auth_dept` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
