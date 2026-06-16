import pandas as pd
import numpy as np
import logging

logger=logging.getLogger(__name__)

def core(data):
    try:
        data['orders']['order_purchase_timestamp']=pd.to_datetime(data['orders']['order_purchase_timestamp'])
        data['orders']['order_approved_at']=pd.to_datetime(data['orders']['order_approved_at'])
        data['orders']['order_delivered_carrier_date']=pd.to_datetime(data['orders']['order_delivered_carrier_date'])
        data['orders']['order_delivered_customer_date']=pd.to_datetime(data['orders']['order_delivered_customer_date'])
        data['orders']['order_estimated_delivery_date']=pd.to_datetime(data['orders']['order_estimated_delivery_date'])
        data['orders']['delivery_days']=(data['orders']['order_delivered_customer_date']-data['orders']['order_purchase_timestamp']).dt.days
        data['orders']=data['orders'].dropna(subset='order_id')
        data['orders']=data['orders'][data['orders']['order_status']!='unavailable']
        data['orders']=data['orders'][data['orders']['order_status']!='unavailable']

        data['order_items']=data['order_items'][data['order_items']['freight_value']>0]
        data['order_items']=data['order_items'][data['order_items']['price']>0]
        data['order_items']=data['order_items'].dropna(subset=['order_id','product_id'])

        data['order_payments']=data['order_payments'].groupby('order_id').agg(
        total_price=('payment_value', 'sum'),
        common_type=('payment_type', pd.Series.mode)).reset_index()

        data['order_reviews']=data['order_reviews'].sort_values('order_id')
        data['order_reviews']=data['order_reviews'].drop_duplicates(subset='order_id',keep='last')
        data['order_reviews']['review_score']=data['order_reviews']['review_score'].fillna(data['order_reviews']['review_score'].median())
        data['order_reviews']=data['order_reviews'].dropna(columns=['review_comment_title','review_comment_message'],inplace=True)

        data['customers']=data['customers'].drop_duplicates(subset='customer_unique_id')
        data['customers']['customer_city']=data['customers']['customer_city'].str.title()
        data['customers']['customer_state']=data['customers']['customer_state'].str.upper()

        data['products']=pd.merge(data['products'],data['product_category_name_translation'],on='product_category_name')
        data['products']['product_category_name']=data['products']['product_category_name'].fillna('Unknown')
        col=['product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm']
        data['products'][col]=data['products'][col].fillna(data['products'][col].median())
        data['products']['product_weight_g'] = (pd.to_numeric(data['products']['product_weight_g'], errors='coerce').fillna(0).astype(float))
        data['products']['product_length_cm'] = (pd.to_numeric(data['products']['product_length_cm'], errors='coerce').fillna(0).astype(float))


        data['sellers']['seller_city']=data['sellers']['seller_city'].str.title()
        data['sellers']['seller_state']=data['sellers']['seller_state'].str.upper()
        data['sellers']=data['sellers'].drop_duplicates(subset='seller_id')

        data['dim_date'] = pd.DataFrame({
        'date': data['orders']['order_purchase_timestamp']})
        data['dim_date']['date']=pd.to_datetime(data['dim_date']['date'])
        data['dim_date']['year']=data['dim_date']['date'].dt.year
        data['dim_date']['quarter']=data['dim_date']['date'].dt.quarter
        data['dim_date']['month']=data['dim_date']['date'].dt.month
        data['dim_date']['month_name']=data['dim_date']['date'].dt.month_name()
        data['dim_date']['week']=data['dim_date']['date'].dt.weekday
        data['dim_date']['week_day']=data['dim_date']['date'].dt.day_of_week
        data['dim_date']['day']=data['dim_date']['date'].dt.isocalendar().week
        data['dim_date']['is_weekend']=data['dim_date']['day'].isin(['Saturday','Sunday'])
        logger.info("The data is cleaned")
        return data

    except Exception as e:
        logger.error(f"we got a problem in the core:{e}")
        raise