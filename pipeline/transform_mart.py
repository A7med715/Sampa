import pandas as pd
import numpy as np
import logging

logger=logging.getLogger(__name__)

def mart(data):
    dim_data={}
    try:
        try:
            dim_data['dim_customer']=pd.merge(data['customers'],data['orders'],on='customer_id')
            dim_data['dim_customer']['customer_key']=range(1,len(dim_data['dim_customer'])+1)
            dim_data['dim_customer']['valid_from']=dim_data['dim_customer']['order_purchase_timestamp']
            dim_data['dim_customer']['valid_to']='9999-12-31'
            dim_data['dim_customer']['current']=True
            del dim_data['dim_customer']['order_id']
            del dim_data['dim_customer']['order_approved_at']
            del dim_data['dim_customer']['order_delivered_carrier_date']
            del dim_data['dim_customer']['order_delivered_customer_date']
            del dim_data['dim_customer']['order_estimated_delivery_date']
            del dim_data['dim_customer']['order_purchase_timestamp']
            del dim_data['dim_customer']['order_status']
            del dim_data['dim_customer']['delivery_days']
        except Exception as e:
            logger.error(f'The customer dimension failed:{e}')
        
        try:
            dim_data['dim_product']=data['products'].copy()
            dim_data['dim_product']['product_key']=range(1,len(dim_data['dim_product'])+1)
        except Exception as e:
            logger.info(f'the product dimension failed:{e}')
        
        try:
            dim_data['dim_seller']=data['sellers']
            dim_data['dim_seller']['seller_key']=range(1,len(dim_data['dim_seller'])+1)
        except Exception as e:
            logger.error(f"the sellers dimesion failed:{e}")
        
        try:
            data['dim_date']['date_key']=data['dim_date']['date'].dt.strftime('%Y%m%d')
            data['dim_date']['date_key']=data['dim_date']['date_key'].astype(int)
            dim_data['dim_date']=data['dim_date']
        except Exception as e:
            logger.error(f'the date dimennsion failed:{e}')
        
        try:
            dim_data['fact_orders']=data['order_items']

            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],data['orders'],on='order_id')
            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],data['order_payments'],on='order_id')
            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],data['order_reviews'],on='order_id')

            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],dim_data['dim_customer'][['customer_id','customer_key']],on='customer_id')
            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns='customer_id')
            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],dim_data['dim_product'][['product_id','product_key']],on='product_id')
            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns='product_id')
            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],dim_data['dim_seller'][['seller_id','seller_key']],on='seller_id')
            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns='seller_id')
            dim_data['fact_orders']=pd.merge(dim_data['fact_orders'],dim_data['dim_date'][['date','date_key']],left_on='order_purchase_timestamp',right_on='date')
            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns='order_purchase_timestamp')

            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns=['review_comment_title','review_comment_message'], inplace=True)
            dim_data['fact_orders']=dim_data['fact_orders'].drop(columns=['order_approved_at','order_delivered_carrier_date'], inplace=True)


            dim_data['fact_orders']['order_item_key']=range(1,len(dim_data['fact_orders'])+1)
        except Exception as e:
            logger.error(f'the fact table failed with error{e}')
        logger.info('the data had been marted!!')
        return dim_data
    except:
        logger.error('there was an error in marting the data')

