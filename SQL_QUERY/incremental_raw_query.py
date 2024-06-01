
truncate_scm_raw_zone_customers = """
truncate table scm_raw_zone.customers
"""

insert_scm_raw_zone_customers = """
insert  into  scm_raw_zone.customers (customer_id,
customer_name,
email,
phone,
address,
city,
country,
loyalty_points,Insertion_date)

with dwh as (
select 
customer_id,
customer_name,
email,
phone,
address,
city,
country,
loyalty_points
from scm_raw_zone.customers c 
),
insert_upd as (

select 
a.customer_id,
a.customer_name,
a.email,
a.phone,
a.address,
a.city,
a.country,
a.loyalty_points
from 
staging.customers a
left join dwh b  on a.customer_id  = b.customer_id 
where b.customer_id  is null or 

a.customer_name <> b.customer_name or 
a.email <> b.email or 
a.phone <> b.phone or 
a.address <> b.address or 
a.city <> b.city or 
a.country <> b.country or 
a.loyalty_points <> b.loyalty_points 


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a
"""



truncate_scm_raw_zone_employees =  """
truncate table scm_raw_zone.employees
"""

insert_scm_raw_zone_employees = """
insert  into  scm_raw_zone.employees (employee_id,
employee_name,
email,
phone,
address,
position,
salary,
hire_date,
Insertion_date)

with dwh as (
select 
employee_id,
employee_name,
email,
phone,
address,
position,
salary,
hire_date
from scm_raw_zone.employees c 
),
insert_upd as (

select 
a.employee_id,
a.employee_name,
a.email,
a.phone,
a.address,
a.position,
a.salary,
a.hire_date
from 
staging.employees a
left join dwh b  on a.employee_id  = b.employee_id 
where b.employee_id  is null or 
a.employee_name   <>  b.employee_name or 
a.email   <>  b.email or 
a.phone   <>  b.phone or 
a.address   <>  b.address or 
a.position   <>  b.position or 
a.salary   <>  b.salary or 
a.hire_date   <>  b.hire_date 


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""

truncate_scm_raw_zone_inventory = """
truncate table scm_raw_zone.inventory
"""


insert_scm_raw_zone_iventory = """
insert  into  scm_raw_zone.inventory (inventory_id,
product_id,
warehouse_id,
quantity,
location,
last_updated,
reorder_level,
Insertion_date)



with dwh as (
select 
inventory_id,
product_id,
warehouse_id,
quantity,
location,
last_updated,
reorder_level
from scm_raw_zone.inventory c 
),
insert_upd as (

select 
a.inventory_id,
a.product_id,
a.warehouse_id,
a.quantity,
a.location,
a.last_updated,
a.reorder_level
from 
staging.inventory a
left join dwh b  on a.inventory_id  = b.inventory_id 
where b.inventory_id  is null or 

a.product_id   <>  b.product_id or 
a.warehouse_id   <>  b.warehouse_id or 
a.quantity   <>  b.quantity or 
a.location   <>  b.location or 
a.last_updated   <>  b.last_updated or 
a.reorder_level   <>  b.reorder_level 


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""


truncate_scm_raw_zone_inventory_transactions = """
truncate table  scm_raw_zone.inventory_transactions
"""

insert_scm_raw_zone_inventory_transactions = """
insert  into  scm_raw_zone.inventory_transactions (
transaction_id,
inventory_id,
employee_id,
transaction_date,
quantity,
transaction_type,
notes,
Insertion_date)


with dwh as (
select 
transaction_id,
inventory_id,
employee_id,
transaction_date,
quantity,
transaction_type,
notes
from scm_raw_zone.inventory_transactions c 
),
insert_upd as (

select 
a.transaction_id,
a.inventory_id,
a.employee_id,
a.transaction_date,
a.quantity,
a.transaction_type,
a.notes
from 
staging.inventory_transactions a
left join dwh b  on a.transaction_id  = b.transaction_id 
where b.transaction_id  is null or 

a.inventory_id   <>   b.inventory_id or
a.employee_id   <>   b.employee_id or
a.transaction_date   <>   b.transaction_date or
a.quantity   <>   b.quantity or
a.transaction_type   <>   b.transaction_type or
a.notes   <>   b.notes 


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""


truncate_scm_raw_zone_order_details = """
truncate table scm_raw_zone.order_details
"""

insert_scm_raw_zone_order_details = """
insert  into  scm_raw_zone.order_details (
order_detail_id,
order_id,
product_id,
quantity,
unit_price,
discount,
total_price,
Insertion_date)


with dwh as (
select 
order_detail_id,
order_id,
product_id,
quantity,
unit_price,
discount,
total_price
from scm_raw_zone.order_details c 
),
insert_upd as (

select 
a.order_detail_id,
a.order_id,
a.product_id,
a.quantity,
a.unit_price,
a.discount,
a.total_price
from 
staging.order_details a
left join dwh b  on a.order_detail_id  = b.order_detail_id 
where b.order_detail_id  is null or 

a.order_id  <>  b.order_id  or 
a.product_id  <>  b.product_id  or 
a.quantity  <>  b.quantity  or 
a.unit_price  <>  b.unit_price  or 
a.discount  <>  b.discount  or 
a.total_price  <>  b.total_price  


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""


truncate_scm_raw_zone_orders = """
truncate table scm_raw_zone.orders
"""

insert_scm_raw_zone_orders = """

insert  into  scm_raw_zone.orders (
order_id,
customer_id,
warehouse_id,
employee_id,
order_date,
status,
total_amount,
payment_method,
Insertion_date)


with dwh as (
select 
order_id,
customer_id,
warehouse_id,
employee_id,
order_date,
status,
total_amount,
payment_method
from scm_raw_zone.orders c 
),
insert_upd as (

select 
a.order_id,
a.customer_id,
a.warehouse_id,
a.employee_id,
a.order_date,
a.status,
a.total_amount,
a.payment_method
from 
staging.orders a
left join dwh b  on a.order_id  = b.order_id 
where b.order_id  is null or 

a.customer_id <>  b.customer_id or 
a.warehouse_id <>  b.warehouse_id or 
a.employee_id <>  b.employee_id or 
a.order_date <>  b.order_date or 
a.status <>  b.status or 
a.total_amount <>  b.total_amount or 
a.payment_method <>  b.payment_method 


)


select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""



truncate_scm_raw_zone_payment = """
truncate table scm_raw_zone.payments
"""

insert_scm_raw_zone_payment = """

insert  into  scm_raw_zone.payments (
payment_id,
order_id,
payment_date,
amount,
payment_method,
Insertion_date)


with dwh as (
select 
payment_id,
order_id,
payment_date,
amount,
payment_method
from scm_raw_zone.payments c 
),
insert_upd as (

select 
a.payment_id,
a.order_id,
a.payment_date,
a.amount,
a.payment_method
from 
staging.payments a
left join dwh b  on a.payment_id  = b.payment_id 
where b.payment_id  is null or 

a.order_id <>   b.order_id or
a.payment_date <>   b.payment_date or
a.amount <>   b.amount or
a.payment_method <>   b.payment_method 
)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a
"""


truncate_scm_raw_zone_products = """
truncate table scm_raw_zone.products
"""

insert_scm_raw_zone_products = """
insert  into  scm_raw_zone.products (
product_id,
product_name,
category,
price,
weight,
manufacturer,
description,
sku,
color,
Insertion_date)


with dwh as (
select 
product_id,
product_name,
category,
price,
weight,
manufacturer,
description,
sku,
color
from scm_raw_zone.products c 
),
insert_upd as (

select 
a.product_id,
a.product_name,
a.category,
a.price,
a.weight,
a.manufacturer,
a.description,
a.sku,
a.color
from 
staging.products a
left join dwh b  on a.product_id  = b.product_id 
where b.product_id  is null or 

a.product_name <> b.product_name or 
a.category <> b.category or 
a.price <> b.price or 
a.weight <> b.weight or 
a.manufacturer <> b.manufacturer or 
a.description <> b.description or 
a.sku <> b.sku or 
a.color <> b.color 
)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a
"""

truncate_scm_raw_zone_returns = """
truncate table scm_raw_zone.returns
"""

insert_scm_raw_zone_returns = """
insert  into  scm_raw_zone.returns (
return_id,
order_id,
product_id,
return_date,
reason,
status,
Insertion_date)


with dwh as (
select 
return_id,
order_id,
product_id,
return_date,
reason,
status
from scm_raw_zone.returns c 
),
insert_upd as (

select 
a.return_id,
a.order_id,
a.product_id,
a.return_date,
a.reason,
a.status
from 
staging.returns a
left join dwh b  on a.return_id  = b.return_id 
where b.return_id  is null or 


a.order_id <>  b.order_id or 
a.product_id <>  b.product_id or 
a.return_date <>  b.return_date or 
a.reason <>  b.reason or 
a.status <>  b.status
)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""



truncate_scm_raw_zone_shipment = """
truncate table scm_raw_zone.shipments
"""

insert_scm_raw_zone_shipments = """

insert  into  scm_raw_zone.shipments (
shipment_id,
order_id,
warehouse_id,
employee_id,
shipment_date,
carrier,
tracking_number,
destination,
shipment_cost,
Insertion_date)


with dwh as (
select 
shipment_id,
order_id,
warehouse_id,
employee_id,
shipment_date,
carrier,
tracking_number,
destination,
shipment_cost
from scm_raw_zone.shipments c 
),
insert_upd as (

select 
a.shipment_id,
a.order_id,
a.warehouse_id,
a.employee_id,
a.shipment_date,
a.carrier,
a.tracking_number,
a.destination,
a.shipment_cost
from 
staging.shipments a
left join dwh b  on a.shipment_id  = b.shipment_id 
where b.shipment_id  is null or 



a.shipment_id <> b.shipment_id or 
a.order_id <> b.order_id or 
a.warehouse_id <> b.warehouse_id or 
a.employee_id <> b.employee_id or 
a.shipment_date <> b.shipment_date or 
a.carrier <> b.carrier or 
a.tracking_number <> b.tracking_number or 
a.destination <> b.destination or 
a.shipment_cost <> b.shipment_cost




)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""
 
truncate_scm_raw_zone_supplier = """
truncate table scm_raw_zone.suppliers
"""

insert_scm_raw_zone_supplier = """
insert  into  scm_raw_zone.suppliers (
supplier_id,
supplier_name,
contact_name,
contact_email,
contact_phone,
address,
website,
rating,
Insertion_date)


with dwh as (
select 
supplier_id,
supplier_name,
contact_name,
contact_email,
contact_phone,
address,
website,
rating
from scm_raw_zone.suppliers c 
),
insert_upd as (

select 
a.supplier_id,
a.supplier_name,
a.contact_name,
a.contact_email,
a.contact_phone,
a.address,
a.website,
a.rating
from 
staging.suppliers a
left join dwh b  on a.supplier_id  = b.supplier_id 
where b.supplier_id  is null or 


a.supplier_name <>  b.supplier_name or 
a.contact_name <>  b.contact_name or 
a.contact_email <>  b.contact_email or 
a.contact_phone <>  b.contact_phone or 
a.address <>  b.address or 
a.website <>  b.website or 
a.rating <>  b.rating 
)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""

truncate_scm_raw_zone_supplier_product = """
truncate table scm_raw_zone.suppliers_products
"""

insert_scm_raw_zone_suppliers_products = """
insert  into  scm_raw_zone.suppliers_products (
supplier_product_id,
supplier_id,
product_id,
unit_cost,
lead_time,
quantity_ordered,
Insertion_date)


with dwh as (
select 
supplier_product_id,
supplier_id,
product_id,
unit_cost,
lead_time,
quantity_ordered
from scm_raw_zone.suppliers_products c 
),
insert_upd as (

select 
a.supplier_product_id,
a.supplier_id,
a.product_id,
a.unit_cost,
a.lead_time,
a.quantity_ordered
from 
staging.suppliers_products a
left join dwh b  on a.supplier_product_id  = b.supplier_product_id 
where b.supplier_product_id  is null or 


a.supplier_id <>  b.supplier_id or 
a.product_id <>  b.product_id or 
a.unit_cost <>  b.unit_cost or 
a.lead_time <>  b.lead_time or 
a.quantity_ordered <>  b.quantity_ordered 
)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a

"""


truncate_scm_raw_zone_warehouse = """
truncate table scm_raw_zone.warehouses
"""

insert_scm_raw_zone_warehouse = """
insert  into  scm_raw_zone.warehouses (
warehouse_id,
warehouse_name,
location,
capacity,
manager,
operational_since,
num_employees,
Insertion_date)


with dwh as (
select 
warehouse_id,
warehouse_name,
location,
capacity,
manager,
operational_since,
num_employees
from scm_raw_zone.warehouses c 
),
insert_upd as (

select 
a.warehouse_id,
a.warehouse_name,
a.location,
a.capacity,
a.manager,
a.operational_since,
a.num_employees
from 
staging.warehouses a
left join dwh b  on a.warehouse_id  = b.warehouse_id 
where b.warehouse_id  is null or 


a.warehouse_name <> b.warehouse_name or 
a.location <> b.location or 
a.capacity <> b.capacity or 
a.manager <> b.manager or 
a.operational_since <> b.operational_since or 
a.num_employees <> b.num_employees 

)

select a.*,CURRENT_DATE AS Insertion_date from (
select * from dwh
union all 
select * from insert_upd
)a
"""

