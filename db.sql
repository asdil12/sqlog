-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 172.17.0.1
-- Erstellungszeit: 29. Jul 2020 um 12:31
-- Server-Version: 10.4.13-MariaDB
-- PHP-Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Datenbank: `sqlog`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `qsos`
--

CREATE TABLE `qsos` (
  `id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  `my_callsign` varchar(32) NOT NULL,
  `callsign` varchar(32) NOT NULL,
  `name` varchar(32) DEFAULT NULL,
  `freq` float NOT NULL,
  `band` varchar(8) NOT NULL,
  `mode` varchar(16) NOT NULL,
  `rst_rcvd` varchar(3) DEFAULT NULL,
  `rst_sent` varchar(3) DEFAULT NULL,
  `qsl` enum('sent','requested','confirmed') DEFAULT NULL,
  `my_qth` varchar(128) DEFAULT NULL,
  `my_sota_ref` varchar(16) DEFAULT NULL,
  `my_gridsquare` varchar(6) DEFAULT NULL,
  `my_lat` float DEFAULT NULL,
  `my_lon` float DEFAULT NULL,
  `qth` varchar(128) DEFAULT NULL,
  `sota_ref` varchar(16) DEFAULT NULL,
  `gridsquare` varchar(6) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `distance` float DEFAULT NULL,
  `remarks` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `summits`
--

CREATE TABLE `summits` (
  `ref` varchar(16) NOT NULL,
  `name` varchar(64) NOT NULL,
  `region` varchar(64) NOT NULL,
  `association` varchar(64) NOT NULL,
  `altitude` smallint(6) NOT NULL,
  `lat` float NOT NULL,
  `lon` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `qsos`
--
ALTER TABLE `qsos`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `summits`
--
ALTER TABLE `summits`
  ADD PRIMARY KEY (`ref`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `qsos`
--
ALTER TABLE `qsos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

