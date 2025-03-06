-- Enable Referential Integrity 
PRAGMA foreign_keys = 1;

DROP TABLE IF EXISTS demo;
DROP TABLE IF EXISTS tbl_items;

CREATE TABLE tbl_items(
  item_id VARCHAR(5),
  sku VARCHAR(10),
  item_name VARCHAR(30),
  item_cat VARCHAR(20),
  item_size VARCHAR(10),
  item_price INT,
  Primary KEY(item_id)
 );

INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It001', 'HDR-CAP-MD', 'Cappuccino', 'Hot Drinks', 'Medium', 3.45);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It002', 'HDR-CAP-LG', 'Cappuccino', 'Hot Drinks', 'Large', 3.75);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It003', 'HDR-LAT-MD', 'Latte', 'Hot Drinks', 'Medium', 3.45);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It004', 'HDR-LAT-LG', 'Latte', 'Hot Drinks', 'Large', 3.75);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It005', 'HDR-FLT', 'Flat White', 'Hot Drinks',  'N/A', 3.15);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It006', 'HDR-CRM-MD', 'Caramel Macchiato' , 'Hot Drinks','Medium', 4.20);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It007', 'HDR-CRM-LG', 'Caramel Macchiato' , 'Hot Drinks','Large', 4.60);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It008', 'HDR-ESP', 'Espresso','Hot Drinks' , 'N/A', 2.15);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It009', 'HDR-MOC-MD', 'Mocha','Hot Drinks' , 'Medium', 4.00);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It010', 'HDR-MOC-LG', 'Mocha','Hot Drinks' , 'Large', 4.60);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It011', 'HDR-WMO-MD', 'White Mocha' ,'Hot Drinks', 'Medium', 4.50);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It012', 'HDR-WMO-LG', 'White Mocha' ,'Hot Drinks', 'Large', 4.70);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It013', 'HDR-HCH-MD', 'Hot Chocolate', 'Hot Drinks', 'Medium', 4.20);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It014', 'HDR-HCH-LG', 'Hot Chocolate', 'Hot Drinks', 'Large', 4.60);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It015', 'CDR-CCF-MD', 'Cold Coffee', 'Cold Drinks', 'Medium', 3.45);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It016', 'CDR-CCF-LG', 'Cold Coffee', 'Cold Drinks', 'Large', 3.75);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It017', 'CDR-CMO-MD', 'Cold Mocha', 'Cold Drinks', 'Medium', 4.00);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It018', 'CDR-CMO-LG', 'Cold Mocha', 'Cold Drinks', 'Large', 4.60);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It019', 'CDR-ICT-MD', 'Iced Tea', 'Cold Drinks', 'Medium', 3.25);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It020', 'CDR-ICT-LG', 'Iced Tea', 'Cold Drinks', 'Large', 3.55);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It021', 'CDR-LMN-MD', 'Lemonade', 'Cold Drinks', 'Medium', 3.35);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It022', 'CDR-LMN-LG', 'Lemonade', 'Cold Drinks', 'Large', 3.75);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It023', 'SNK-SHC', 'Sandwich Ham & Cheese', 'Snacks', 'N/A', 5.60);
INSERT INTO tbl_items(item_id, sku, item_name, item_cat, item_size, item_price) VALUES ('It024', 'SNK-SSM', 'Sandwich Salami & Mozzarella', 'Snacks', 'N/A', 5.50);
