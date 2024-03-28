-- Paso 1: Borrar la base y las tablas si es que existen
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS customers;
DROP DATABASE IF EXISTS store_db;

-- Paso 2: Crear la base de datos y seleccionarla
CREATE DATABASE IF NOT EXISTS store_db;
USE store_db;

-- Paso 3: Crear las tablas "customers" y "payments"
CREATE TABLE IF NOT EXISTS customers (
   customerNumber   INT UNSIGNED  NOT NULL AUTO_INCREMENT,
   customerName     VARCHAR(50)   NOT NULL,
   phone            VARCHAR(50)   NOT NULL,
   addressLine1     VARCHAR(50)   NOT NULL,
   addressLine2     VARCHAR(50)   DEFAULT NULL,
   city             VARCHAR(50)   NOT NULL,
   province            VARCHAR(50)   DEFAULT NULL,
   postalCode       VARCHAR(15)   DEFAULT NULL,
   country          VARCHAR(50)   NOT NULL,
   createdDate     TIMESTAMP              NOT NULL DEFAULT CURRENT_TIMESTAMP,
   updatedDate     TIMESTAMP              NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (customerNumber)
);

CREATE TABLE IF NOT EXISTS payments (
   customerNumber  INT UNSIGNED           NOT NULL,
   checkNumber     VARCHAR(50)            NOT NULL,
   paymentDate     DATE                   NOT NULL,
   amount          DECIMAL(8,2) UNSIGNED  NOT NULL,
   PRIMARY KEY  (customerNumber,checkNumber),
   FOREIGN KEY (customerNumber) REFERENCES customers (customerNumber)
      ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Paso 4: Insertar registros en las tablas
INSERT INTO customers (customerName, phone, addressLine1, city, country)
VALUES
  ('Mario Santos', '+54 9 11 1234 5678', 'Calle Falsa 123', 'Buenos Aires', 'Argentina'),
  ('Emilio Ravenna', '+54 9 11 8765 4321', 'Avenida Simulación 456', 'Córdoba', 'Argentina'),
  ('Pablo Lamponne', '+54 9 11 2468 1357', 'Carrera Simulada 789', 'Rosario', 'Argentina'),
  ('Gabriel Medina', '+54 9 11 7531 8642', 'Pasaje Fingido 987', 'Mendoza', 'Argentina'),
  ('Franco Milazzo', '+54 9 11 3847 6291', 'Ruta Ficticia 321', 'Salta', 'Argentina'),
  ('Marcos Molero', '+54 9 11 9512 4863', 'Camino Imaginario 753', 'Mar del Plata', 'Argentina'),
  ('Martin Vanega', '+54 9 11 5763 2198', 'Boulevard Inventado 864', 'San Miguel de Tucumán', 'Argentina'),
  ('Jose Feller', '+54 9 11 3185 7426', 'Plaza Hipotética 246', 'La Plata', 'Argentina'),
  ('Arturo Gaona', '+54 9 11 9263 7514', 'Alameda Irreal 159', 'Salta', 'Argentina'),
  ('Lucio Bonelli', '+54 9 11 4682 3571', 'Paseo Imaginado 853', 'Córdoba', 'Argentina');

INSERT INTO payments (customerNumber, checkNumber, paymentDate, amount)
VALUES
  (1, 1001, '2023-07-01', 348.50),
  (1, 1002, '2023-07-05', 953.25),
  (2, 2001, '2023-07-02', 486.10),
  (2, 2002, '2023-07-06', 230.40),
  (3, 3001, '2023-07-03', 824.60),
  (3, 3002, '2023-07-07', 178.90),
  (4, 4001, '2023-07-04', 768.75),
  (4, 4002, '2023-07-08', 983.60),
  (5, 5001, '2023-07-05', 513.20),
  (5, 5002, '2023-07-09', 400.90),
  (6, 6001, '2023-07-06', 762.30),
  (6, 6002, '2023-07-10', 654.75),
  (7, 7001, '2023-07-07', 199.80),
  (7, 7002, '2023-07-11', 852.50),
  (8, 8001, '2023-07-08', 501.30),
  (8, 8002, '2023-07-12', 442.40),
  (9, 9001, '2023-07-09', 710.20),
  (9, 9002, '2023-07-13', 234.50),
  (10, 10001, '2023-07-10', 374.80),
  (10, 10002, '2023-07-14', 790.30),
  (1, 11001, '2023-07-11', 590.70),
  (1, 11002, '2023-07-15', 445.90),
  (2, 12001, '2023-07-12', 675.50),
  (2, 12002, '2023-07-16', 308.40),
  (3, 13001, '2023-07-13', 478.10),
  (3, 13002, '2023-07-17', 502.60),
  (4, 14001, '2023-07-14', 761.90),
  (4, 14002, '2023-07-18', 235.75),
  (5, 15001, '2023-07-15', 400.25),
  (5, 15002, '2023-07-19', 570.60);

-- Paso 5: Aplicar cambios a la tabla "customers"
-- Se insertan registros nuevos y se modifican registros existentes
INSERT INTO customers (customerName, phone, addressLine1, city, province, postalCode, country)
VALUES ('Pedro Velazco', '+54 9 11 2222 2222', 'Calle Nueva 456', 'Ciudad Nueva', 'NV', '54321', 'Argentina');

UPDATE customers
SET addressLine1 = 'Calle Actualizada 789', phone = '+54 9 11 9999 9999'
WHERE customerName = 'Franco Milazzo';

-- Paso 6: Aplicar cambios a la tabla "payments"
-- Se insertan registros nuevos
INSERT INTO payments (customerNumber, checkNumber, paymentDate, amount)
VALUES
  (1, 3001, '2023-07-26', 10000.50),
  (2, 3002, '2023-07-26', 7500.20),
  (3, 3003, '2023-07-26', 5075.00);
