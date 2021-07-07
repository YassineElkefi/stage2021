-- MySQL Script generated by MySQL Workbench
-- Wed Jun 30 15:35:24 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema stage2021
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema stage2021
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `stage2021` DEFAULT CHARACTER SET utf8 ;
USE `stage2021` ;

-- -----------------------------------------------------
-- Table `stage2021`.`agent`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`agent` (
  `ncnss` INT(11) NOT NULL,
  `nom` VARCHAR(20) NOT NULL,
  `prenom` VARCHAR(20) NOT NULL,
  `tel_ag` VARCHAR(12) NOT NULL,
  `mail_ag` VARCHAR(255) NOT NULL,
  `adresse_ag` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`ncnss`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `stage2021`.`region`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`region` (
  `id_region` INT(11) NOT NULL,
  `libellé_region` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id_region`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `stage2021`.`bureau_poste`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`bureau_poste` (
  `id_bp` INT(11) NOT NULL,
  `nom_bp` VARCHAR(255) NOT NULL,
  `code_postal` VARCHAR(8) NOT NULL,
  `reg` INT(11) NOT NULL,
  PRIMARY KEY (`id_bp`),
  INDEX `FK_REG` (`reg` ASC) VISIBLE,
  CONSTRAINT `FK_REG`
    FOREIGN KEY (`reg`)
    REFERENCES `stage2021`.`region` (`id_region`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `stage2021`.`client`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`client` (
  `id` INT(11) NOT NULL,
  `libellé` VARCHAR(100) NOT NULL,
  `telephone` VARCHAR(20) NOT NULL,
  `fax` VARCHAR(20) NOT NULL,
  `adresse` VARCHAR(255) NOT NULL,
  `mail` VARCHAR(150) NOT NULL,
  `agent_ncnss` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `agent_ncnss`),
  INDEX `fk_client_agent1_idx` (`agent_ncnss` ASC) VISIBLE,
  CONSTRAINT `fk_client_agent1`
    FOREIGN KEY (`agent_ncnss`)
    REFERENCES `stage2021`.`agent` (`ncnss`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `stage2021`.`service`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`service` (
  `id_service` INT(11) NOT NULL,
  `libellé_service` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id_service`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `stage2021`.`depot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stage2021`.`depot` (
  `id_depot` INT(11) NOT NULL,
  `service` INT(11) NOT NULL,
  `bureau` INT(11) NOT NULL,
  `client` INT(11) NOT NULL,
  `date_envoi` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `montant` INT(11) NOT NULL,
  `nombre` INT(11) NOT NULL,
  PRIMARY KEY (`id_depot`),
  INDEX `FK_SERV` (`service` ASC) VISIBLE,
  INDEX `FK_BUR` (`bureau` ASC) VISIBLE,
  INDEX `FK_CLI` (`client` ASC) VISIBLE,
  CONSTRAINT `FK_BUR`
    FOREIGN KEY (`bureau`)
    REFERENCES `stage2021`.`bureau_poste` (`id_bp`),
  CONSTRAINT `FK_CLI`
    FOREIGN KEY (`client`)
    REFERENCES `stage2021`.`client` (`id`),
  CONSTRAINT `FK_SERV`
    FOREIGN KEY (`service`)
    REFERENCES `stage2021`.`service` (`id_service`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;