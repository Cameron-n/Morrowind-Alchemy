CREATE TABLE Ingredient(
   `ID`                         VARCHAR(31) NOT NULL PRIMARY KEY
  ,`Ingredient`                       VARCHAR(38) NOT NULL
  ,`Weight`                     NUMERIC(4,2) NOT NULL
  ,`Value`                      INTEGER  NOT NULL
  ,`Origin`                     VARCHAR(23) NOT NULL
  ,`Icon`                       VARCHAR(29) NOT NULL
  ,`First Effect`               VARCHAR(26)
  ,`Blind`                      INTEGER  NOT NULL
  ,`Burden`                     INTEGER  NOT NULL
  ,`Chameleon`                  INTEGER  NOT NULL
  ,`Cure Blight Disease`        INTEGER  NOT NULL
  ,`Cure Common Disease`        INTEGER  NOT NULL
  ,`Cure Paralyzation`          INTEGER  NOT NULL
  ,`Cure Poison`                INTEGER  NOT NULL
  ,`Damage Agility`             INTEGER  NOT NULL
  ,`Damage Endurance`           INTEGER  NOT NULL
  ,`Damage Fatigue`             INTEGER  NOT NULL
  ,`Damage Health`              INTEGER  NOT NULL
  ,`Damage Intelligence`        INTEGER  NOT NULL
  ,`Damage Luck`                INTEGER  NOT NULL
  ,`Damage Magicka`             INTEGER  NOT NULL
  ,`Damage Personality`         INTEGER  NOT NULL
  ,`Damage Speed`               INTEGER  NOT NULL
  ,`Damage Strength`            INTEGER  NOT NULL
  ,`Damage Willpower`           INTEGER  NOT NULL
  ,`Detect Animal`              INTEGER  NOT NULL
  ,`Detect Enchantment`         INTEGER  NOT NULL
  ,`Detect Key`                 INTEGER  NOT NULL
  ,`Disintegrate Armor`         INTEGER  NOT NULL
  ,`Disintegrate Weapon`        INTEGER  NOT NULL
  ,`Dispel`                     INTEGER  NOT NULL
  ,`Divine Intervention`        INTEGER  NOT NULL
  ,`Drain Agility`              INTEGER  NOT NULL
  ,`Drain Alteration`           INTEGER  NOT NULL
  ,`Drain Endurance`            INTEGER  NOT NULL
  ,`Drain Fatigue`              INTEGER  NOT NULL
  ,`Drain Health`               INTEGER  NOT NULL
  ,`Drain Intelligence`         INTEGER  NOT NULL
  ,`Drain Luck`                 INTEGER  NOT NULL
  ,`Drain Magicka`              INTEGER  NOT NULL
  ,`Drain Mysticism`            INTEGER  NOT NULL
  ,`Drain Personality`          INTEGER  NOT NULL
  ,`Drain Sneak`                INTEGER  NOT NULL
  ,`Drain Speed`                INTEGER  NOT NULL
  ,`Drain Strength`             INTEGER  NOT NULL
  ,`Drain Willpower`            INTEGER  NOT NULL
  ,`Feather`                    INTEGER  NOT NULL
  ,`Fire Damage`                INTEGER  NOT NULL
  ,`Fire Shield`                INTEGER  NOT NULL
  ,`Fortify Acrobatics`         INTEGER  NOT NULL
  ,`Fortify Agility`            INTEGER  NOT NULL
  ,`Fortify Alchemy`            INTEGER  NOT NULL
  ,`Fortify Athletics`          INTEGER  NOT NULL
  ,`Fortify Attack`             INTEGER  NOT NULL
  ,`Fortify Blunt Weapon`       INTEGER  NOT NULL
  ,`Fortify Conjuration`        INTEGER  NOT NULL
  ,`Fortify Endurance`          INTEGER  NOT NULL
  ,`Fortify Fatigue`            INTEGER  NOT NULL
  ,`Fortify Health`             INTEGER  NOT NULL
  ,`Fortify Intelligence`       INTEGER  NOT NULL
  ,`Fortify Light Armor`        INTEGER  NOT NULL
  ,`Fortify Luck`               INTEGER  NOT NULL
  ,`Fortify Magicka`            INTEGER  NOT NULL
  ,`Fortify Marksman`           INTEGER  NOT NULL
  ,`Fortify Maximum Magicka`    INTEGER  NOT NULL
  ,`Fortify Mysticism`          INTEGER  NOT NULL
  ,`Fortify Personality`        INTEGER  NOT NULL
  ,`Fortify Restoration`        INTEGER  NOT NULL
  ,`Fortify Speechcraft`        INTEGER  NOT NULL
  ,`Fortify Speed`              INTEGER  NOT NULL
  ,`Fortify Strength`           INTEGER  NOT NULL
  ,`Fortify Unarmored`          INTEGER  NOT NULL
  ,`Fortify Willpower`          INTEGER  NOT NULL
  ,`Frost Damage`               INTEGER  NOT NULL
  ,`Frost Shield`               INTEGER  NOT NULL
  ,`Invisibility`               INTEGER  NOT NULL
  ,`Jump`                       INTEGER  NOT NULL
  ,`Levitate`                   INTEGER  NOT NULL
  ,`Light`                      INTEGER  NOT NULL
  ,`Lightning Shield`           INTEGER  NOT NULL
  ,`Mark`                       INTEGER  NOT NULL
  ,`Night Eye`                  INTEGER  NOT NULL
  ,`Paralyze`                   INTEGER  NOT NULL
  ,`Poison`                     INTEGER  NOT NULL
  ,`Recall`                     INTEGER  NOT NULL
  ,`Reflect`                    INTEGER  NOT NULL
  ,`Resist Blight Disease`      INTEGER  NOT NULL
  ,`Resist Common Disease`      INTEGER  NOT NULL
  ,`Resist Fire`                INTEGER  NOT NULL
  ,`Resist Frost`               INTEGER  NOT NULL
  ,`Resist Magicka`             INTEGER  NOT NULL
  ,`Resist Normal Weapons`      INTEGER  NOT NULL
  ,`Resist Paralysis`           INTEGER  NOT NULL
  ,`Resist Poison`              INTEGER  NOT NULL
  ,`Resist Shock`               INTEGER  NOT NULL
  ,`Restore Agility`            INTEGER  NOT NULL
  ,`Restore Athletics`          INTEGER  NOT NULL
  ,`Restore Destruction`        INTEGER  NOT NULL
  ,`Restore Endurance`          INTEGER  NOT NULL
  ,`Restore Fatigue`            INTEGER  NOT NULL
  ,`Restore Health`             INTEGER  NOT NULL
  ,`Restore Intelligence`       INTEGER  NOT NULL
  ,`Restore Luck`               INTEGER  NOT NULL
  ,`Restore Magicka`            INTEGER  NOT NULL
  ,`Restore Personality`        INTEGER  NOT NULL
  ,`Restore Restoration`        INTEGER  NOT NULL
  ,`Restore Speechcraft`        INTEGER  NOT NULL
  ,`Restore Speed`              INTEGER  NOT NULL
  ,`Restore Strength`           INTEGER  NOT NULL
  ,`Restore Willpower`          INTEGER  NOT NULL
  ,`Sanctuary`                  INTEGER  NOT NULL
  ,`Shield`                     INTEGER  NOT NULL
  ,`Shock Damage`               INTEGER  NOT NULL
  ,`Silence`                    INTEGER  NOT NULL
  ,`Slowfall`                   INTEGER  NOT NULL
  ,`Sound`                      INTEGER  NOT NULL
  ,`Spell Absorption`           INTEGER  NOT NULL
  ,`Stunted Magicka`            INTEGER  NOT NULL
  ,`Summon Scamp`               INTEGER  NOT NULL
  ,`Swift Swim`                 INTEGER  NOT NULL
  ,`Telekinesis`                INTEGER  NOT NULL
  ,`Vampirism`                  INTEGER  NOT NULL
  ,`Water Breathing`            INTEGER  NOT NULL
  ,`Water Walking`              INTEGER  NOT NULL
  ,`Weakness to Common Disease` INTEGER  NOT NULL
  ,`Weakness to Fire`           INTEGER  NOT NULL
  ,`Weakness to Frost`          INTEGER  NOT NULL
  ,`Weakness to Magicka`        INTEGER  NOT NULL
  ,`Weakness to Normal Weapons` INTEGER  NOT NULL
  ,`Weakness to Poison`         INTEGER  NOT NULL
  ,`Weakness to Shock`          INTEGER  NOT NULL
  ,`Reflect Damage`             INTEGER  NOT NULL
  ,`Insight`                    INTEGER  NOT NULL
  ,`Fortify Casting`            INTEGER  NOT NULL
  ,`Radiant Shield`             INTEGER  NOT NULL
  ,`Detect Invisibility`        INTEGER  NOT NULL
  ,`Detect Enemy`               INTEGER  NOT NULL
  ,`Detect Humanoid`               INTEGER  NOT NULL
  ,`Blink`                      INTEGER  NOT NULL
);
CREATE TABLE Effect(
   `Spell Effects`  VARCHAR(26) NOT NULL PRIMARY KEY
  ,`Base Cost`      NUMERIC(6,2)
  ,`Positive`       INTEGER 
  ,`HasNoDuration`  BIT 
  ,`HasNoMagnitude` BIT 
  ,`Icon`           VARCHAR(28) NOT NULL
);
CREATE TABLE Tool(
   `Name`    VARCHAR(31) NOT NULL PRIMARY KEY
  ,`Quality` FLOAT NOT NULL
  ,`Type`    VARCHAR(17) NOT NULL
  ,`Origin`  VARCHAR(15) NOT NULL
  ,`Icon`    VARCHAR(28) NOT NULL
);
CREATE TABLE NPCtoCell(
   `Name`       VARCHAR(23) NOT NULL PRIMARY KEY
  ,`Origin`     VARCHAR(15) NOT NULL
  ,`CellName`   VARCHAR(49) NOT NULL
  ,`CellX`      FLOAT  NOT NULL
  ,`CellY`      FLOAT  NOT NULL
  ,`isInterior` BOOL
);
CREATE TABLE IngtoNPC(
   `Name`    VARCHAR(31) NOT NULL
  ,`NPCName` VARCHAR(23) NOT NULL
  ,`Count`   INTEGER  NOT NULL
  ,PRIMARY KEY(`Name`,`NPCName`)
);
CREATE TABLE IngtoLoose(
   `ID`         VARCHAR(31) NOT NULL
  ,`Origin`     VARCHAR(15) NOT NULL
  ,`CellName`   VARCHAR(57) NOT NULL
  ,`CellX`      FLOAT NOT NULL
  ,`CellY`      FLOAT NOT NULL
  ,`IsInterior` BOOL
  ,`Count`      INTEGER  NOT NULL
  ,PRIMARY KEY(`ID`,`CellName`,`CellX`,`CellY`)
);
CREATE TABLE ContainertoCell(
   `ID`         VARCHAR(24) NOT NULL
  ,`Origin`     VARCHAR(20) NOT NULL
  ,`CellName`   VARCHAR(57) NOT NULL
  ,`CellX`      FLOAT NOT NULL
  ,`CellY`      FLOAT NOT NULL
  ,`IsInterior` BOOL
  ,`Count`      INTEGER  NOT NULL
  ,PRIMARY KEY(`ID`,`CellName`,`CellX`,`CellY`)
);
CREATE TABLE FloratoCell(
   `ID`         VARCHAR(23) NOT NULL
  ,`Origin`     VARCHAR(16) NOT NULL
  ,`CellName`   VARCHAR(56) NOT NULL
  ,`CellX`      FLOAT NOT NULL
  ,`CellY`      FLOAT NOT NULL
  ,`IsInterior` BOOL
  ,`Count`      INTEGER  NOT NULL
  ,PRIMARY KEY(`ID`,`CellName`,`CellX`,`CellY`)
);
CREATE TABLE LvlcretoCell(
   `ID`         VARCHAR(24) NOT NULL
  ,`Origin`     VARCHAR(15) NOT NULL
  ,`CellName`   VARCHAR(54) NOT NULL
  ,`CellX`      FLOAT NOT NULL
  ,`CellY`      FLOAT NOT NULL
  ,`IsInterior` BOOL
  ,`Count`      INTEGER  NOT NULL
  ,PRIMARY KEY(`ID`,`CellName`,`CellX`,`CellY`)
);