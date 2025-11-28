
DROP DATABASE IF EXISTS masterpol_partners;
CREATE DATABASE masterpol_partners CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE masterpol_partners;

CREATE TABLE product_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  production_coefficient DECIMAL(10,4) NOT NULL
);

CREATE TABLE product (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_type_id INT NOT NULL,
  name VARCHAR(255) NOT NULL,
  sku VARCHAR(50) UNIQUE,
  min_price_for_partner DECIMAL(12,2),
  FOREIGN KEY (product_type_id) REFERENCES product_type(id)
);

CREATE TABLE material_type (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  defect_percent DECIMAL(8,6) NOT NULL
);

CREATE TABLE partner (
  id INT AUTO_INCREMENT PRIMARY KEY,
  partner_type VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  director_fullname VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(50),
  legal_address TEXT,
  inn VARCHAR(20),
  rating INT DEFAULT 0 CHECK (rating >= 0),
  logo_path VARCHAR(255)
);

CREATE TABLE partner_sales (
  id INT AUTO_INCREMENT PRIMARY KEY,
  partner_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity BIGINT NOT NULL,
  sale_date DATE NOT NULL,
  FOREIGN KEY (partner_id) REFERENCES partner(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE INDEX idx_partner_name ON partner(name);
CREATE INDEX idx_sales_partner ON partner_sales(partner_id);

INSERT INTO material_type (name, defect_percent) VALUES
('Тип материала 1', 0.0010),
('Тип материала 2', 0.0095),
('Тип материала 3', 0.0028),
('Тип материала 4', 0.0055),
('Тип материала 5', 0.0034);

INSERT INTO product_type (name, production_coefficient) VALUES
('Ламинат', 2.35),
('Массивная доска', 5.15),
('Паркетная доска', 4.34),
('Пробковое покрытие', 1.50);

INSERT INTO product (product_type_id, name, sku, min_price_for_partner) VALUES
((SELECT id FROM product_type WHERE name='Паркетная доска'),'Паркетная доска Ясень темный однополосная 14 мм','8758385',4456.90),
((SELECT id FROM product_type WHERE name='Паркетная доска'),'Инженерная доска Дуб Французская елка однополосная 12 мм','8858958',7330.99),
((SELECT id FROM product_type WHERE name='Ламинат'),'Ламинат Дуб дымчато-белый 33 класс 12 мм','7750282',1799.33),
((SELECT id FROM product_type WHERE name='Ламинат'),'Ламинат Дуб серый 32 класс 8 мм с фаской','7028748',3890.41),
((SELECT id FROM product_type WHERE name='Пробковое покрытие'),'Пробковое напольное клеевое покрытие 32 класс 4 мм','5012543',5450.59);

INSERT INTO partner (partner_type, name, director_fullname, email, phone, legal_address, inn, rating) VALUES
('ЗАО','База Строитель','Иванова Александра Ивановна','aleksandraivanova@ml.ru','493 123 45 67','652050, Кемеровская область, город Юрга, ул. Лесная, 15','2222455179',7),
('ООО','Паркет 29','Петров Василий Петрович','vppetrov@vl.ru','987 123 56 78','164500, Архангельская область, город Северодвинск, ул. Строителей, 18','3333888520',7),
('ПАО','Стройсервис','Соловьев Андрей Николаевич','ansolovev@st.ru','812 223 32 00','188910, Ленинградская область, город Приморск, ул. Парковая, 21','4440391035',7),
('ОАО','Ремонт и отделка','Воробьева Екатерина Валерьевна','ekaterina.vorobeva@ml.ru','444 222 33 11','143960, Московская область, город Реутов, ул. Свободы, 51','1111520857',5),
('ЗАО','МонтажПро','Степанов Степан Сергеевич','stepanov@stepan.ru','912 888 33 33','309500, Белгородская область, город Старый Оскол, ул. Рабочая, 122','5552431140',10);

INSERT INTO partner_sales (partner_id, product_id, quantity, sale_date) VALUES
((SELECT id FROM partner WHERE name='База Строитель'),(SELECT id FROM product WHERE name='Паркетная доска Ясень темный однополосная 14 мм'),15500,'2023-03-23'),
((SELECT id FROM partner WHERE name='База Строитель'),(SELECT id FROM product WHERE name='Ламинат Дуб дымчато-белый 33 класс 12 мм'),12350,'2023-12-18'),
((SELECT id FROM partner WHERE name='База Строитель'),(SELECT id FROM product WHERE name='Ламинат Дуб серый 32 класс 8 мм с фаской'),37400,'2024-06-07'),
((SELECT id FROM partner WHERE name='Паркет 29'),(SELECT id FROM product WHERE name='Инженерная доска Дуб Французская елка однополосная 12 мм'),35000,'2022-12-02'),
((SELECT id FROM partner WHERE name='Паркет 29'),(SELECT id FROM product WHERE name='Пробковое напольное клеевое покрытие 32 класс 4 мм'),1250,'2023-05-17'),
((SELECT id FROM partner WHERE name='Паркет 29'),(SELECT id FROM product WHERE name='Ламинат Дуб дымчато-белый 33 класс 12 мм'),1000,'2024-06-07'),
((SELECT id FROM partner WHERE name='Паркет 29'),(SELECT id FROM product WHERE name='Паркетная доска Ясень темный однополосная 14 мм'),7550,'2024-07-01'),
((SELECT id FROM partner WHERE name='Стройсервис'),(SELECT id FROM product WHERE name='Паркетная доска Ясень темный однополосная 14 мм'),7250,'2023-01-22'),
((SELECT id FROM partner WHERE name='Стройсервис'),(SELECT id FROM product WHERE name='Инженерная доска Дуб Французская елка однополосная 12 мм'),2500,'2024-07-05'),
((SELECT id FROM partner WHERE name='Ремонт и отделка'),(SELECT id FROM product WHERE name='Ламинат Дуб серый 32 класс 8 мм с фаской'),59050,'2023-03-20'),
((SELECT id FROM partner WHERE name='Ремонт и отделка'),(SELECT id FROM product WHERE name='Ламинат Дуб дымчато-белый 33 класс 12 мм'),37200,'2024-03-12'),
((SELECT id FROM partner WHERE name='Ремонт и отделка'),(SELECT id FROM product WHERE name='Пробковое напольное клеевое покрытие 32 класс 4 мм'),4500,'2024-05-14'),
((SELECT id FROM partner WHERE name='МонтажПро'),(SELECT id FROM product WHERE name='Ламинат Дуб дымчато-белый 33 класс 12 мм'),50000,'2023-09-19'),
((SELECT id FROM partner WHERE name='МонтажПро'),(SELECT id FROM product WHERE name='Ламинат Дуб серый 32 класс 8 мм с фаской'),670000,'2023-11-10'),
((SELECT id FROM partner WHERE name='МонтажПро'),(SELECT id FROM product WHERE name='Паркетная доска Ясень темный однополосная 14 мм'),35000,'2024-04-15'),
((SELECT id FROM partner WHERE name='МонтажПро'),(SELECT id FROM product WHERE name='Инженерная доска Дуб Французская елка однополосная 12 мм'),25000,'2024-06-12');
ALTER TABLE partner ADD COLUMN deleted_at DATETIME NULL AFTER rating;