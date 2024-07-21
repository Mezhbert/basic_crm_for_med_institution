#create
CREATE TABLE "redirects" (
"id"	INTEGER,
"id_patient"	INTEGER NOT NULL UNIQUE,
"id_doctor_from"	INTEGER NOT NULL,
"reason"	TEXT,
"id_doctor_to"	INTEGER NOT NULL,
"date"	TEXT NOT NULL,
"diagnosis"	TEXT,
"id_prescribed_medication"	INTEGER NOT NULL,
FOREIGN KEY("id_patient") REFERENCES "patients"("id") ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("id_doctor_to") REFERENCES "doctors"("id") ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("id_prescribed_medication") REFERENCES "medications"("id") ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("id_doctor_from") REFERENCES "doctors"("id") ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY("id_patient" AUTOINCREMENT)
);

#insert
INSERT INTO `redirects`
(`id_patient`, `id_doctor_from`, `reason`, `id_doctor_to`, `date`, `diagnosis`, `id_prescribed_medication`)
VALUES (?, ?, ?, ?, ?, ?, ?);

#update
UPDATE `redirects`
SET
`id_patient` = ?,
`id_doctor_from` = ?,
`reason` = ?,
`id_doctor_to` = ?,
`date` = ?,
`diagnosis` = ?,
`id_prescribed_medication` = ?
WHERE `id` = ?;

#delete
DELETE FROM `redirects`
WHERE ?;

#select_all
SELECT `redirects`.`id`,
`redirects`.`id_patient`,
`redirects`.`id_doctor_from`,
`redirects`.`reason`,
`redirects`.`id_doctor_to`,
`redirects`.`date`,
`redirects`.`diagnosis`,
`redirects`.`id_prescribed_medication`
FROM `redirects`;

#select_with_names
SELECT `redirects`.`id`,
`patients`.`name`,
`doctors`.`name`,
`redirects`.`reason`,
`doctors`.`name`,
`redirects`.`date`,
`redirects`.`diagnosis`,
`medications`.`title`
FROM `redirects`, `patients`, `doctors`, `medications`
WHERE `redirects`.`id_patient` = `patients`.`id` AND `redirects`.`id_doctor_from` = `doctors`.`id` AND `redirects`.`id_doctor_to` = `doctors`.`id` AND `redirects`.`id_prescribed_medication` = `medications`.`id`;

#find_by_name_with_names
SELECT `redirects`.`id`,
`patients`.`name`,
`doctors`.`name`,
`redirects`.`reason`,
`doctors`.`name`,
`redirects`.`date`,
`redirects`.`diagnosis`,
`medications`.`title`
FROM `redirects`, `patients`, `doctors`, `medications`
WHERE `patients`.`name` LIKE ? AND `redirects`.`id_patient` = `patients`.`id` AND `redirects`.`id_doctor_from` = `doctors`.`id` AND `redirects`.`id_doctor_to` = `doctors`.`id` AND `redirects`.`id_prescribed_medication` = `medications`.`id`;
