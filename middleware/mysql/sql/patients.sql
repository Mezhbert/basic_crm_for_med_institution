#create
CREATE TABLE "patients" (
"id"    INTEGER NOT NULL UNIQUE,
"name"  TEXT NOT NULL,
"birthdate"  TEXT NOT NULL,
"phone" TEXT NOT NULL,
"id_gender" INTEGER NOT NULL,
"weight"    REAL,
"height"    REAL,
"id_disability" INTEGER NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT),
FOREIGN KEY("id_disability") REFERENCES "disability_types"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
FOREIGN KEY("id_gender") REFERENCES "gender_types"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

#insert
INSERT INTO `patients`
(`name`, `birthdate`, `phone`, `id_gender`, `weight`, `height`, `id_disability`)
VALUES
(?, ?, ?, ?, ?, ?, ?);
#update
UPDATE `patients`
SET
`name` = ?,
`birthdate` = ?,
`phone` = ?,
`id_gender` = ?,
`weight` = ?,
`height` = ?,
`id_disability` = ?
WHERE `id` = ?;
#delete
DELETE FROM `patients`
WHERE `id`=?;
#select_all
SELECT `patients`.`id`,
    `patients`.`name`,
    `patients`.`birthdate`,
    `patients`.`phone`,
    `gender_types`.`type`,
    `patients`.`weight`,
    `patients`.`height`,
    `disability_types`.`type`
FROM `patients`, `gender_types`, `disability_types`
WHERE `patients`.`id_gender` = `gender_types`.`id` AND `patients`.`id_disability` = `disability_types`.`id`;
#find_by_name
SELECT `patients`.`id`,
    `patients`.`name`,
    `patients`.`birthdate`,
    `patients`.`phone`,
    `gender_types`.`type`,
    `patients`.`weight`,
    `patients`.`height`,
    `disability_types`.`type`
FROM `patients`, `gender_types`, `disability_types`
WHERE `patients`.`name` LIKE ? AND `patients`.`id_gender` = `gender_types`.`id` AND `patients`.`id_disability` = `disability_types`.`id`;
#find_by_id
SELECT `patients`.`id`,
    `patients`.`name`,
    `patients`.`birthdate`,
    `patients`.`phone`,
    `gender_types`.`type`,
    `patients`.`weight`,
    `patients`.`height`,
    `disability_types`.`type`
FROM `patients`, `gender_types`, `disability_types`
WHERE `patients`.`id` = ? AND `patients`.`id_gender` = `gender_types`.`id` AND `patients`.`id_disability` = `disability_types`.`id`;

#find_by_name_name_bd_phone
SELECT `patients`.`name`,
    `patients`.`birthdate`,
    `patients`.`phone`
FROM `patients`
WHERE `patients`.`name` LIKE ?;

#select_name_bd_phone
SELECT `patients`.`name`,
    `patients`.`birthdate`,
    `patients`.`phone`
FROM `patients`;
