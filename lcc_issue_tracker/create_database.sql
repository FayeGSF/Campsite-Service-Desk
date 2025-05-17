SET FOREIGN_KEY_CHECKS = 0;
-- Drop child tables first
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS issues;
-- Now it's safe to drop the parent table
DROP TABLE IF EXISTS users;

-- Re-enable foreign key check
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(60) NOT NULL,
    `password_hash` CHAR(60) BINARY NOT NULL,
    `email` VARCHAR(320) NOT NULL,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `location` VARCHAR(50) NOT NULL,
    `profile_image` VARCHAR(255),
    `role` ENUM('visitor', 'helper', 'admin') NOT NULL DEFAULT 'visitor',
    `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    PRIMARY KEY (`user_id`)
);

CREATE TABLE `issues` (
`issue_id` INT NOT NULL AUTO_INCREMENT,
`user_id` INT NOT NULL,
`summary` VARCHAR (255) NOT NULL,
`description` TEXT NOT NULL,
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
`status` ENUM('new', 'open', 'stalled', 'resolved') NOT NULL DEFAULT 'new',
PRIMARY KEY (`issue_id`),
CONSTRAINT `fk_user_id`
	FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON UPDATE CASCADE
);

CREATE TABLE `comments`(
`comment_id` INT NOT NULL AUTO_INCREMENT,
`issue_id` INT NOT NULL,
`user_id` INT NOT NULL,
`context` TEXT NOT NULL, 
`created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (`comment_id`),
CONSTRAINT `fk_issue_id_in_comments`
	FOREIGN KEY (`issue_id`)
    REFERENCES `issues` (`issue_id`)
    ON UPDATE CASCADE,
CONSTRAINT `fk_user_id_in_comments`
	FOREIGN KEY (`user_id`)
    REFERENCES `users` (`user_id`)
    ON UPDATE CASCADE
);
