#create
CREATE TABLE "medications" (
"id"    INTEGER NOT NULL UNIQUE,
"title" TEXT NOT NULL UNIQUE,
"desc"  TEXT NOT NULL,
"contraindication"  TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
);

#insert
INSERT INTO `medications`
(`title`, `desc`, `contraindication`)
VALUES
(?, ?, ?);

#update
UPDATE `medications`
SET
`title` = ?,
`desc` = ?,
`contraindication` = ?
WHERE `id` = ?;

#delete
DELETE FROM `medications`
WHERE ?;

#select_all
SELECT `medications`.`id`,
`medications`.`title`,
`medications`.`desc`,
`medications`.`contraindication`
FROM `medications`;

#find_by_id
SELECT `medications`.`id`,
    `medications`.`title`,
    `medications`.`desc`,
    `medications`.`contraindication`
FROM `medications`
WHERE `medications`.`id` = ?;

#find_by_name
SELECT `medications`.`id`,
    `medications`.`title`,
    `medications`.`desc`,
    `medications`.`contraindication`
FROM `medications`
WHERE `medications`.`title` LIKE ?;

#find_by_name_without_id
SELECT `medications`.`title`,
    `medications`.`desc`,
    `medications`.`contraindication`
FROM `medications`
WHERE `medications`.`title` LIKE ?;

#select_without_id
SELECT `medications`.`title`,
    `medications`.`desc`,
    `medications`.`contraindication`
FROM `medications`;
