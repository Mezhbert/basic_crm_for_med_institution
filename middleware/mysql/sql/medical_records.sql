#create
CREATE TABLE "medical_records" (
"id"    INTEGER NOT NULL UNIQUE,
"id_patient"    INTEGER NOT NULL,
"date"  INTEGER NOT NULL,
"complaints"    TEXT NOT NULL,
"diagnosis" TEXT,
"allergy"   TEXT,
"treatment" TEXT,
"id_prescribed_medication"  INTEGER,
PRIMARY KEY("id" AUTOINCREMENT),
FOREIGN KEY("id_prescribed_medication") REFERENCES "medications"("id") ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY("id_patient") REFERENCES "patients"("id") ON DELETE CASCADE ON UPDATE CASCADE
);

#insert
INSERT INTO `medical_records`
(`id_patient`, `date`, `complaints`, `diagnosis`, `allergy`, `treatment`, `id_prescribed_medication`)
VALUES
(?, ?, ?, ?, ?, ?, ?);
#update
UPDATE `medical_records`
SET
`id_patient` = ?,
`date` = ?,
`complaints` = ?,
`diagnosis` = ?,
`allergy` = ?,
`treatment` = ?,
`id_prescribed_medication` = ?
WHERE `id` = ?;
#delete
DELETE FROM `medical_records`
WHERE `id` = ?;
#select_all
SELECT `medical_records`.`id`,
    `medical_records`.`id_patient`,
    `medical_records`.`date`,
    `medical_records`.`complaints`,
    `medical_records`.`diagnosis`,
    `medical_records`.`allergy`,
    `medical_records`.`treatment`,
    `medical_records`.`id_prescribed_medication`
FROM `medical_records`;
#select_with_names
SELECT `medical_records`.`id`,
`patients`.`name`,
`medical_records`.`date`,
`medical_records`.`complaints`,
`medical_records`.`diagnosis`,
`medical_records`.`allergy`,
`medical_records`.`treatment`,
`medications`.`title`
FROM `medical_records`, `patients`, `medications`
WHERE `medical_records`.`id_patient` = `patients`.`id` AND `medical_records`.`id_prescribed_medication` = `medications`.`id`;
#find_by_patient_id
SELECT `medical_records`.`id`,
`medical_records`.`date`,
`medical_records`.`complaints`,
`medical_records`.`diagnosis`,
`medical_records`.`allergy`,
`medical_records`.`treatment`,
`medications`.`title`
FROM `medical_records`, `medications`
WHERE `medical_records`.`id_patient` = ? AND `medical_records`.`id_prescribed_medication` = `medications`.`id`;

#find_by_medication_id
SELECT `medical_records`.`id`,
`patients`.`name`,
`medical_records`.`date`,
`medical_records`.`complaints`,
`medical_records`.`diagnosis`,
`medical_records`.`allergy`,
`medical_records`.`treatment`
FROM `medical_records`, `patients`
WHERE `medical_records`.`id_prescribed_medication` = ? AND `medical_records`.`id_patient` = `patients`.`id`;

#find_by_name_with_names
SELECT `medical_records`.`id`,
    `patients`.`name`,
    `medical_records`.`date`,
    `medical_records`.`complaints`,
    `medical_records`.`diagnosis`,
    `medical_records`.`allergy`,
    `medical_records`.`treatment`,
    `medications`.`title`
FROM `medical_records`, `patients`, `medications`
WHERE `patients`.`name` LIKE ? AND `medical_records`.`id_patient` = `patients`.`id` AND `medical_records`.`id_prescribed_medication` = `medications`.`id`;
