
truncate_processing_zone_DimProducts = """
truncate table processing_zone.DimProducts
"""

insert_processing_zone_DimProducts = """
INSERT into processing_zone.DimProducts (ProductID, ProductName, Category, Price, Weight, Manufacturer, Description, SKU, Color, SupplierID, SupplierName, UnitCost, LeadTime,insertion_date)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    p.weight,
    p.manufacturer,
    p.description,
    p.sku,
    p.color,
    sp.supplier_id,
    s.supplier_name,
    sp.unit_cost,
    sp.lead_time,
    p.insertion_date
FROM scm_raw_zone.products p
LEFT JOIN scm_raw_zone.suppliers_products sp ON p.product_id = sp.product_id
LEFT JOIN scm_raw_zone.suppliers s ON sp.supplier_id = s.supplier_id
"""






truncate_processing_zone_DimSuppliers = """
truncate table processing_zone.DimSuppliers
"""

insert_DimSuppliers ="""

INSERT INTO processing_zone.DimSuppliers (SupplierID, SupplierName, ContactName, ContactEmail, ContactPhone, Address, Website, Rating,insertion_date)
SELECT 
    s.supplier_id,
    s.supplier_name,
    s.contact_name,
    s.contact_email,
    s.contact_phone,
    s.address,
    s.website,
    s.rating,
    s.insertion_date
FROM scm_raw_zone.suppliers s;
"""



truncate_processing_zone_DimWarehouses = """
truncate table processing_zone.DimWarehouses
"""

insert_DimWarehouses = """
INSERT INTO processing_zone.DimWarehouses (WarehouseID, WarehouseName, Location, Capacity, Manager, OperationalSince, NumEmployees, TotalInventory,insertion_date)
SELECT 
    w.warehouse_id,
    w.warehouse_name,
    w.location,
    w.capacity,
    w.manager,
    w.operational_since,
    w.num_employees,
    i.quantity AS TotalInventory,
    w.insertion_date
FROM scm_raw_zone.warehouses w
LEFT JOIN scm_raw_zone.inventory i ON w.warehouse_id = i.warehouse_id
"""



truncate_DimCustomers = """
truncate table processing_zone.DimCustomers
"""
insert_DimCustomers = """
INSERT INTO processing_zone.DimCustomers (CustomerID, CustomerName, Email, Phone, Address, City, Country, LoyaltyPoints,insertion_date)
SELECT 
    c.customer_id,
    c.customer_name,
    c.email,
    c.phone,
    c.address,
    c.city,
    c.country,
    c.loyalty_points,
    c.insertion_date
FROM scm_raw_zone.customers c
"""

truncate_DimEmployees = """
truncate table processing_zone.DimEmployees 
"""

insert_DimEmployees = """
INSERT INTO processing_zone.DimEmployees (EmployeeID, EmployeeName, Email, Phone, Address, Position, Salary, HireDate,insertion_date)
SELECT 
    e.employee_id,
    e.employee_name,
    e.email,
    e.phone,
    e.address,
    e.position,
    e.salary,
    e.hire_date,
    e.insertion_date
FROM scm_raw_zone.employees e
"""


truncate_DIM_datetime = """
truncate table processing_zone.DIM_datetime 
"""

insert_DIM_datetime = """

insert into   processing_zone.DIM_datetime  (timekey,date,year,quarter,month,day,dayofweek,weekofyear,isholiday)
WITH RECURSIVE date_generator(date_value) AS (
    SELECT
        '2023-01-01'::DATE
    UNION ALL
    SELECT
        (date_value + INTERVAL '1 day')::DATE
    FROM
        date_generator
    WHERE
        (date_value + INTERVAL '1 day')::DATE <= '2024-07-31'::DATE
),
date_details AS (
    SELECT
        date_value,
        EXTRACT(YEAR FROM date_value) AS year,
        CEIL(EXTRACT(MONTH FROM date_value) / 3.0) AS quarter,
        EXTRACT(MONTH FROM date_value) AS month,
        EXTRACT(DAY FROM date_value) AS day,
        EXTRACT(DOW FROM date_value) AS dayofweek,
        EXTRACT(WEEK FROM date_value) AS weekofyear,
        CASE
            WHEN date_value = DATE '2023-01-01' OR date_value = DATE '2024-07-31' THEN TRUE
            ELSE FALSE
        END AS isholiday
    FROM
        date_generator
),
data_to_insert AS (
    SELECT
        year * 10000 + month * 100 + day AS timekey,
        date_value AS date,
        year,
        quarter,
        month,
        day,
        dayofweek,
        weekofyear,
        isholiday
    FROM
        date_details
)


SELECT
    timekey,
    date,
    year,
    quarter,
    month,
    day,
    dayofweek,
    weekofyear,
    isholiday
FROM
    data_to_insert
    """
   

truncate_FactOrderDetails = """
truncate table processing_zone.FactOrderDetails
"""

insert_FactOrderDetails = """
INSERT INTO  processing_zone.FactOrderDetails (OrderDetailID, OrderID, ProductKey, CustomerKey, WarehouseKey, EmployeeKey,SupplierKey, OrderDateKey, Status, Quantity, UnitPrice, Discount, TotalPrice, TotalOrderAmount, PaymentMethod,insertion_date)



SELECT 
    od.order_detail_id,
    o.order_id,
    dp.ProductKey,
    dc.CustomerKey,
    dw.WarehouseKey,
    de.EmployeeKey,
    sp.SupplierKey,
    CAST(TO_CHAR(o.order_date, 'YYYYMMDD') AS date) AS OrderDateKey,
    o.status,
    od.quantity,
    od.unit_price,
    od.discount,
    od.total_price,
    o.total_amount,
    o.payment_method,
    od.insertion_date
FROM scm_raw_zone.order_details od
JOIN scm_raw_zone.orders o ON od.order_id = o.order_id
JOIN processing_zone.DimProducts dp ON od.product_id = dp.ProductID
join processing_zone.DimSuppliers sp on sp.supplierid  = dp.supplierid
JOIN processing_zone.DimCustomers dc ON o.customer_id = dc.CustomerID
JOIN processing_zone.DimWarehouses dw ON o.warehouse_id = dw.WarehouseID
JOIN processing_zone.DimEmployees de ON o.employee_id = de.EmployeeID
"""

truncate_FactTransactions = """
truncate table processing_zone.FactTransactions
"""

insert_FactTransactions = """
INSERT INTO processing_zone.FactTransactions (TransactionID, InventoryID, ProductKey, WarehouseKey, EmployeeKey, TransactionDateKey, Quantity, TransactionType, UnitCost, InventoryValue, CumulativeQuantity,insertion_date)

SELECT  distinct 
    it.transaction_id,
    it.inventory_id,
    dp.ProductKey,
    dw.WarehouseKey,
    de.EmployeeKey,
    CAST(TO_CHAR(it.transaction_date, 'YYYYMMDD') AS date) AS TransactionDateKey,
    it.quantity,
    it.transaction_type,
    sp.unit_cost,
    sp.unit_cost * it.quantity AS InventoryValue,
    SUM(it2.quantity * CASE WHEN it2.transaction_type = 'Addition' THEN 1 ELSE -1 END) 
        OVER (PARTITION BY i.product_id ORDER BY it2.transaction_date, it2.transaction_id 
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS CumulativeQuantity,
              it.insertion_date
FROM scm_raw_zone.inventory_transactions it
JOIN scm_raw_zone.inventory i ON it.inventory_id = i.inventory_id
JOIN scm_raw_zone.inventory_transactions it2 ON it2.inventory_id = i.inventory_id --AND it2.transaction_date <= it.transaction_date

JOIN scm_raw_zone.suppliers_products sp ON i.product_id = sp.product_id --AND i.warehouse_id = sp.supplier_id


JOIN processing_zone.DimProducts dp ON i.product_id = dp.ProductID
JOIN processing_zone.DimWarehouses dw ON i.warehouse_id = dw.WarehouseID
JOIN processing_zone.DimEmployees de ON it.employee_id = de.EmployeeID
WHERE dp.ProductKey IS NOT null
"""




