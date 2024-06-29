-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema trip_lists_flask_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `trip_lists_flask_db` ;

-- -----------------------------------------------------
-- Schema trip_lists_flask_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `trip_lists_flask_db` DEFAULT CHARACTER SET utf8 ;
USE `trip_lists_flask_db` ;

-- -----------------------------------------------------
-- Table `trip_lists_flask_db`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_lists_flask_db`.`users` ;

CREATE TABLE IF NOT EXISTS `trip_lists_flask_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `trip_lists_flask_db`.`trips`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_lists_flask_db`.`trips` ;

CREATE TABLE IF NOT EXISTS `trip_lists_flask_db`.`trips` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `date` DATE NULL,
  `days` INT NULL,
  `location` VARCHAR(255) NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_trips_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_trips_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `trip_lists_flask_db`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `trip_lists_flask_db`.`lists`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_lists_flask_db`.`lists` ;

CREATE TABLE IF NOT EXISTS `trip_lists_flask_db`.`lists` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `trip_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_lists_trips_idx` (`trip_id` ASC) VISIBLE,
  CONSTRAINT `fk_lists_trips`
    FOREIGN KEY (`trip_id`)
    REFERENCES `trip_lists_flask_db`.`trips` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `trip_lists_flask_db`.`items`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `trip_lists_flask_db`.`items` ;

CREATE TABLE IF NOT EXISTS `trip_lists_flask_db`.`items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `unit` VARCHAR(255) NULL,
  `quantity` FLOAT NULL,
  `list_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `fk_items_lists1_idx` (`list_id` ASC) VISIBLE,
  CONSTRAINT `fk_items_lists1`
    FOREIGN KEY (`list_id`)
    REFERENCES `trip_lists_flask_db`.`lists` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
