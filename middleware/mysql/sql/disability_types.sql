#create
CREATE TABLE "disability_types" (
"id"    INTEGER NOT NULL UNIQUE,
"type"  TEXT NOT NULL,
PRIMARY KEY("id" AUTOINCREMENT)
);

#insert
INSERT INTO `disability_types`
(`type`)
VALUES
(?);

#select
SELECT `disability_types`.`id`,
    `disability_types`.`type`
FROM `disability_types`
ORDER BY `id`;
