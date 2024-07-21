#create
CREATE TABLE "doctors" (
"id"    INTEGER NOT NULL UNIQUE,
"name"  TEXT NOT NULL,
"birthdate" TEXT NOT NULL,
"job"   TEXT NOT NULL,
"wage"  INTEGER NOT NULL,
"phone" TEXT NOT NULL UNIQUE,
PRIMARY KEY("id" AUTOINCREMENT)
);

#insert
INSERT INTO `doctors`
(`name`, `birthdate`, `job`, `wage`, `phone`)
VALUES
(?, ?, ?, ?, ?);

#update
UPDATE `doctors`
SET
`name` = ?,
`birthdate` = ?,
`job` = ?,
`wage` = ?,
`phone` = ?
WHERE `id` = ?;
#delete
DELETE FROM `doctors`
WHERE `id`=?;

#select_all
SELECT `doctors`.`id`,
    `doctors`.`name`,
    `doctors`.`birthdate`,
    `doctors`.`job`,
    `doctors`.`wage`,
    `doctors`.`phone`
FROM `doctors`;
#find_by_name
SELECT `doctors`.`id`,
    `doctors`.`name`,
    `doctors`.`birthdate`,
    `doctors`.`job`,
    `doctors`.`wage`,
    `doctors`.`phone`
FROM `doctors`
WHERE `doctors`.`name` LIKE ?;

#find_by_name_name_bd_phone
SELECT `doctors`.`name`,
    `doctors`.`birthdate`,
    `doctors`.`phone`
FROM `doctors`
WHERE `doctors`.`name` LIKE ?;

#select_name_bd_phone
SELECT `doctors`.`name`,
    `doctors`.`birthdate`,
    `doctors`.`phone`
FROM `doctors`;
