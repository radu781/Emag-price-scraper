CREATE TABLE `emag` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    `link` varchar(255) NOT NULL,
    `image` varchar(255) NOT NULL,
    `price` varchar(50) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `link` (`link`),
) ENGINE = InnoDB AUTO_INCREMENT = 25801 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `trackings` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `item_id` int NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 30 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
CREATE TABLE `users` (
    `id` int unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `password` varchar(64) NOT NULL,
    `permissions` int NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB AUTO_INCREMENT = 2 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
