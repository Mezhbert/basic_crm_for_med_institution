#select
SELECT `medical_records`.`id`,
`patients`.`name`,
`medical_records`.`complaints`,
`medical_records`.`date`
FROM `medical_records`, `patients`
WHERE `medical_records`.`id_patient` = `patients`.`id`;

#find_by_name_with_names
SELECT `medical_records`.`id`,
`patients`.`name`,
`medical_records`.`complaints`,
`medical_records`.`date`
FROM `medical_records`, `patients`
WHERE `patients`.`name` LIKE ? AND `medical_records`.`id_patient` = `patients`.`id`;
