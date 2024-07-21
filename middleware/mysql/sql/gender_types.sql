#create
CREATE TABLE "gender_types" (
"id"    INTEGER NOT NULL UNIQUE,
"type"  TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
);

#insert
INSERT INTO `gender_types`
(`type`)
VALUES
(?);

#select
SELECT `gender_types`.`id`,
    `gender_types`.`type`
FROM `gender_types`
ORDER BY `id`;
