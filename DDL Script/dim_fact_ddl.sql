CREATE table processing_zone.DimProducts (
    ProductKey INT PRIMARY KEY IDENTITY(1,1),
    ProductID INT UNIQUE,
    ProductName VARCHAR(50),
    Category VARCHAR(50),
    Price FLOAT,
    Weight FLOAT,
    Manufacturer VARCHAR(50),
    Description VARCHAR(255),
    SKU VARCHAR(36),
    Color VARCHAR(20),
    SupplierID INT,
    SupplierName VARCHAR(50),
    UnitCost FLOAT,
    LeadTime INT,
    insertion_date date
);
------------------------------


CREATE TABLE processing_zone.DimSuppliers (
    SupplierKey INT PRIMARY KEY IDENTITY(1,1),
    SupplierID INT UNIQUE,
    SupplierName VARCHAR(500),
    ContactName VARCHAR(500),
    ContactEmail VARCHAR(500),
    ContactPhone VARCHAR(200),
    Address VARCHAR(2550),
    Website VARCHAR(500),
    Rating INT,
    insertion_date date
);


CREATE TABLE processing_zone.DimWarehouses (
    WarehouseKey INT PRIMARY KEY IDENTITY(1,1),
    WarehouseID INT UNIQUE,
    WarehouseName VARCHAR(500),
    Location VARCHAR(500),
    Capacity INT,
    Manager VARCHAR(500),
    OperationalSince DATE,
    NumEmployees INT,
    TotalInventory INT,
    insertion_date  date
);


CREATE TABLE processing_zone.DimCustomers (
    CustomerKey INT PRIMARY KEY IDENTITY(1,1),
    CustomerID INT UNIQUE,
    CustomerName VARCHAR(500),
    Email VARCHAR(500),
    Phone VARCHAR(200),
    Address VARCHAR(2055),
    City VARCHAR(500),
    Country VARCHAR(500),
    LoyaltyPoints INT,
    insertion_date date
);


CREATE TABLE processing_zone.DimEmployees (
    EmployeeKey INT PRIMARY KEY IDENTITY(1,1),
    EmployeeID INT UNIQUE,
    EmployeeName VARCHAR(500),
    Email VARCHAR(500),
    Phone VARCHAR(200),
    Address VARCHAR(2055),
    Position VARCHAR(500),
    Salary INT,
    HireDate DATE,
    insertion_date date
);


CREATE TABLE IF NOT EXISTS processing_zone.dim_datetime
(
    timekey INTEGER   ENCODE az64
    ,date DATE   ENCODE az64
    ,"year" INTEGER   ENCODE az64
    ,quarter NUMERIC(12,0)   ENCODE az64
    ,"month" INTEGER   ENCODE az64
    ,"day" INTEGER   ENCODE az64
    ,dayofweek INTEGER   ENCODE az64
    ,weekofyear INTEGER   ENCODE az64
    ,isholiday BOOLEAN   ENCODE RAW
),




create     TABLE processing_zone.FactOrderDetails (
    OrderDetailKey INT PRIMARY KEY IDENTITY(1,1),
    OrderDetailID INT,
    OrderID INT,
    ProductKey INT,
    CustomerKey INT,
    WarehouseKey INT,
    EmployeeKey INT,
    SupplierKey int,
    orderdatekey date,
    Status VARCHAR(200),
    Quantity INT,
    UnitPrice FLOAT,
    Discount FLOAT,
    TotalPrice FLOAT,
    TotalOrderAmount FLOAT,
    PaymentMethod VARCHAR(200),
    insertion_date date,
    FOREIGN KEY (ProductKey) REFERENCES processing_zone.DimProducts(ProductKey),
    FOREIGN KEY (CustomerKey) REFERENCES processing_zone.DimCustomers(CustomerKey),
    FOREIGN KEY (WarehouseKey) REFERENCES processing_zone.DimWarehouses(WarehouseKey),
    FOREIGN KEY (EmployeeKey) REFERENCES processing_zone.DimEmployees(EmployeeKey),
    FOREIGN KEY (SupplierKey) REFERENCES processing_zone.DimSuppliers(SupplierKey)

--    FOREIGN KEY (OrderDateKey) REFERENCES processing_zone.DIM_datetime(TimeKey)
);






CREATE  TABLE     processing_zone.FactTransactions (  [rEAq$6Uv=qJ;jJi1az~],QLlRcL#)PoK
    TransactionKey INT PRIMARY KEY IDENTITY(1,1),
    TransactionID INT,
    InventoryID INT,
    ProductKey INT,
    WarehouseKey INT,
    EmployeeKey INT,
    TransactionDateKey date,
    Quantity INT,
    TransactionType VARCHAR(20),
    UnitCost FLOAT,
    InventoryValue FLOAT,
    CumulativeQuantity INT,
    insertion_date date,
    FOREIGN KEY (ProductKey) REFERENCES processing_zone.DimProducts(ProductKey),
    FOREIGN KEY (WarehouseKey) REFERENCES processing_zone.DimWarehouses(WarehouseKey),
    FOREIGN KEY (EmployeeKey) REFERENCES processing_zone.DimEmployees(EmployeeKey)
);
