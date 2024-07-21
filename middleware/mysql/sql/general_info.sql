#count_doctors
SELECT count(*)
FROM `doctors`;

#count_patients
SELECT count(*)
FROM `patients`;

#count_patients_without_disablity
SELECT count(*)
FROM `patients`
WHERE `patients`.`id_disability` = 1;

#count_patients_with_1_disablity
SELECT count(*)
FROM `patients`
WHERE `patients`.`id_disability` = 2;

#count_patients_with_2_disablity
SELECT count(*)
FROM `patients`
WHERE `patients`.`id_disability` = 3;

#count_patients_with_3_disablity
SELECT count(*)
FROM `patients`
WHERE `patients`.`id_disability` = 4;

#count_patients_with_4_disablity
SELECT count(*)
FROM `patients`
WHERE `patients`.`id_disability` = 5;

#count_medications
SELECT count(*)
FROM `medications`;
