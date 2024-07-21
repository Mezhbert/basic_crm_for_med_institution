#create
CREATE TABLE "appointments" (
"id"    INTEGER NOT NULL UNIQUE,
"id_doctor" INTEGER NOT NULL,
"id_patient"    INTEGER NOT NULL,
"date"  INTEGER NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT),
FOREIGN KEY("id_patient") REFERENCES "patients"("id") ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("id_doctor") REFERENCES "doctors"("id") ON DELETE CASCADE ON UPDATE CASCADE
);
#insert
INSERT INTO `appointments`
(`id_doctor`, `id_patient`, `date`)
VALUES
(?, ?, ?);
#update
UPDATE `appointments`
SET
`id_doctor` = ?,
`id_patient` = ?,
`date` = ?
WHERE `id` = ?;
#delete
DELETE FROM `appointments`
WHERE `id` = ?;
#select_all
SELECT `appointments`.`id`,
    `appointments`.`id_doctor`,
    `appointments`.`id_patient`,
    `appointments`.`date`
FROM `appointments`;
#select_with_names
SELECT `appointments`.`id`, `doctors`.`name`, `doctors`.`birthdate`, `patients`.`name`, `patients`.`birthdate`, `appointments`.`date`
FROM `appointments`, `doctors`, `patients`
WHERE `appointments`.`id_doctor` = `doctors`.`id` AND `appointments`.`id_patient` = `patients`.`id`;
#select_with_names_find_by_name
SELECT `appointments`.`id`, `doctors`.`name`, `doctors`.`birthdate`, `patients`.`name`, `patients`.`birthdate`, `appointments`.`date`
FROM `appointments`, `doctors`, `patients`
WHERE `appointments`.`id_doctor` = `doctors`.`id` AND `doctors`.`id` IN (SELECT `doctors`.`id` FROM `doctors` WHERE `doctors`.`name` LIKE ?)
AND `appointments`.`id_patient` = `patients`.`id` AND `patients`.`id` IN (SELECT `patients`.`id` FROM `patients` WHERE `patients`.`name` LIKE ?);
