select p.product_category_name,sum(f.price)
from dim_product p inner join fact_orders f
on f.product_key =p.product_key 
group by p.product_category_name;

select s.seller_state,avg(f.delivery_days)
from dim_seller s inner join fact_orders f
on s.seller_key =f.seller_key 
group by s.seller_state;

select d.year,d.month_name,sum(f.price)
from dim_date d inner join fact_orders f
on d.date_key =f.date_key 
group by d.year,d.month_name

select s.seller_id,sum(f.price) revnue
from dim_seller s inner join fact_orders f
on s.seller_key =f.seller_key 
group by s.seller_id 
order by revnue desc
limit 10

select p.product_category_name,avg(f.review_score )
from dim_product p inner join fact_orders f
on f.product_key =p.product_key 
group by p.product_category_name;

with shipped as(
select order_id ,
(case
	when order_delivered_customer_date>order_estimated_delivery_date then 'late'
	else 'on_time'
end
) as delivery
from fact_orders fo 
)
select
    100.0 * count(case when delivery='on_time' then 1 end )
          / count(*) as percentage
from shipped;


select common_type,sum(total_price) from fact_orders 
group by common_type





