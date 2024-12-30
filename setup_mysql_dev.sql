-- Create a database, userand give priviledges--
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev';
GRANT SELECT ON perfomance_scheme.* TO 'hbnb_dev';
FLUSH PRIVILEGES;
