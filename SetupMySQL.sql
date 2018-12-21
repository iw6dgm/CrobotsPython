CREATE TABLE `robots` (
  `id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(12) NOT NULL DEFAULT '''',
  `code` longtext CHARACTER SET utf8 NOT NULL,
  `author` varchar(45) NOT NULL DEFAULT '''',
  `email` varchar(45) NOT NULL DEFAULT '''',
  `validation` varchar(45) NOT NULL DEFAULT '''',
  `creationtime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `status` smallint(5) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `NAMEIDX` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=943 DEFAULT CHARSET=utf8;

CREATE TABLE `results_f2f` (
  `robot` varchar(45) NOT NULL DEFAULT '',
  `games` int(10) unsigned NOT NULL DEFAULT '0',
  `wins` int(10) unsigned NOT NULL DEFAULT '0',
  `ties` int(10) unsigned NOT NULL DEFAULT '0',
  `points` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`robot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Results of F2F';

CREATE TABLE `results_3vs3` (
  `robot` varchar(45) NOT NULL DEFAULT '',
  `games` int(10) unsigned NOT NULL DEFAULT '0',
  `wins` int(10) unsigned NOT NULL DEFAULT '0',
  `ties` int(10) unsigned NOT NULL DEFAULT '0',
  `points` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`robot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Results of 3vs3';

CREATE TABLE `results_4vs4` (
  `robot` varchar(45) NOT NULL DEFAULT '',
  `games` int(10) unsigned NOT NULL DEFAULT '0',
  `wins` int(10) unsigned NOT NULL DEFAULT '0',
  `ties` int(10) unsigned NOT NULL DEFAULT '0',
  `points` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`robot`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Results of 4vs4';


DELIMITER $$
CREATE DEFINER=`crobots`@`%` PROCEDURE `pSetupResultsF2F`()
BEGIN
TRUNCATE TABLE results_f2f;
INSERT INTO results_f2f(robot)
SELECT lower(LEFT(name,character_length(name)-2)) AS robot
FROM robots
WHERE status=2;
COMMIT;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`crobots`@`%` PROCEDURE `pSetupResults3VS3`()
BEGIN
TRUNCATE TABLE results_3vs3;
INSERT INTO results_3vs3(robot)
SELECT lower(LEFT(name,character_length(name)-2)) AS robot
FROM robots
WHERE status=2;
COMMIT;
END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`crobots`@`%` PROCEDURE `pSetupResults4VS4`()
BEGIN
TRUNCATE TABLE results_4vs4;
INSERT INTO results_4vs4(robot)
SELECT lower(LEFT(name,character_length(name)-2)) AS robot
FROM robots
WHERE status=2;
COMMIT;
END$$
DELIMITER ;



