CREATE DATABASE IF NOT EXISTS api;

CREATE USER IF NOT EXISTS 'api-user'@'localhost' IDENTIFIED BY '{{ db_password_api }}';
GRANT ALL PRIVILEGES ON api.* TO 'api-user'@'localhost';
flush privileges;

CREATE TABLE IF NOT EXISTS api.user (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(300) NOT NULL,
role VARCHAR(300) NOT NULL,
token VARCHAR(300) NOT NULL,
ip VARCHAR(300) NOT NULL);

DELETE FROM api.user;
INSERT INTO api.user(id, username, role, token, ip) values(1, 'admin', 'admin', 'X-AUTH-TOKEN;{{ admin_token }}', '127.0.0.1');
INSERT INTO api.user(id, username, role, token, ip) values(2, 'kmille', 'public', 'X-AUTH-TOKEN;{{ public_token }}', '127.0.0.1');
