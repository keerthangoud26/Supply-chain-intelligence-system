-- Drop old tables if rerunning
DROP TABLE IF EXISTS sales_fact CASCADE;
DROP TABLE IF EXISTS manufacturing CASCADE;
DROP TABLE IF EXISTS logistics CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS products CASCADE;


-- PRODUCTS TABLE
CREATE TABLE products (
    sku VARCHAR(50) PRIMARY KEY,
    product_type VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL
);


-- SUPPLIERS TABLE
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    lead_time INT,
    defect_rate FLOAT,
    inspection_result VARCHAR(50)
);


-- INVENTORY TABLE
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    stock_level INT,
    availability INT,
    order_quantity INT,
    FOREIGN KEY (sku) REFERENCES products(sku)
);


-- LOGISTICS TABLE
CREATE TABLE logistics (
    shipment_id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    shipping_carrier VARCHAR(100),
    shipping_time INT,
    shipping_cost FLOAT,
    transportation_mode VARCHAR(50),
    route VARCHAR(100),
    FOREIGN KEY (sku) REFERENCES products(sku)
);


-- MANUFACTURING TABLE
CREATE TABLE manufacturing (
    manufacturing_id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    production_volume INT,
    manufacturing_lead_time INT,
    manufacturing_cost FLOAT,
    FOREIGN KEY (sku) REFERENCES products(sku)
);


-- SALES FACT TABLE
CREATE TABLE sales_fact (
    sale_id SERIAL PRIMARY KEY,
    sku VARCHAR(50),
    units_sold INT,
    revenue_generated FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku) REFERENCES products(sku)
);


-- CHECK TABLES CREATED
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';