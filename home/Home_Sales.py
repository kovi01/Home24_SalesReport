# -*- coding: utf-8 -*-
"""untitled30.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/kovi01/68f0c36f94864758da9d9ce92dc4d1f8/untitled30.ipynb
"""

!pip install pyspark

import pyspark

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialize Spark session
spark = SparkSession.builder.appName("Marketing Campaign Report").getOrCreate()

# Load datasets
items = spark.read.load("/content/items.parquet")
itemsStock = spark.read.load("/content/itemsStock.parquet")
campaigns = spark.read.load("/content/campaigns.parquet")
customers = spark.read.load("/content/customers.parquet")
subscriptions = spark.read.load("/content/subscriptions.parquet")
events = spark.read.load("/content/events.parquet")

# Filter subscribed users
subscribed_users = subscriptions.filter(col("subscription_type") == "item_alert")

# Identify wishlist items
wishlist_events = events.filter(col("event_type") == "addToWishlist")

# Join to get wishlist items in stock and in an active campaign
wishlist_items_in_campaign = wishlist_events.join(items, wishlist_events.item_id == items.id) \
                                            .join(itemsStock, items.id == itemsStock.item_id) \
                                            .join(campaigns, items.id == campaigns.item_id) \
                                            .where(itemsStock.stock_quantity > 0)

# Calculate final price after discount
final_prices = wishlist_items_in_campaign.withColumn("final_price",
                                                     col("price") - (col("price") * col("discount") / 100))

# Join with customers to get user details
final_report = final_prices.join(customers, wishlist_events.customer_id == customers.id) \
                           .join(subscribed_users, customers.id == subscribed_users.customer_id) \
                           .select(customers.first_name, customers.email, items.name, items.url, "final_price")

# Show or save the report
final_report.show()  # or final_report.write.format("...").save("path_to_save_report")

from pyspark.sql.functions import col

# Filter subscribed users
subscribed_users = subscriptions.filter(col("subscription_type") == "item_alert")

# Identify wishlist or cart items
wishlist_or_cart_events = events.filter((col("event_type") == "addToWishlist") | (col("event_type") == "addToCart"))

# Join to get wishlist or cart items in stock and in an active campaign
wishlist_or_cart_items_in_campaign = wishlist_or_cart_events.join(items, wishlist_or_cart_events.item_id == items.id) \
                                            .join(itemsStock, items.id == itemsStock.item_id) \
                                            .join(campaigns, items.id == campaigns.item_id) \
                                            .where(itemsStock.stock_quantity > 0)

# Calculate final price after discount
final_prices = wishlist_or_cart_items_in_campaign.withColumn("final_price",
                                                     col("price") - (col("price") * col("discount") / 100))

# Join with customers to get user details
final_report = final_prices.join(customers, wishlist_or_cart_events.customer_id == customers.id) \
                           .join(subscribed_users, customers.id == subscribed_users.customer_id) \
                           .select(customers.first_name, customers.email, items.name, items.url, "final_price")
final_report.count()

final_report.write.csv("/content/FinalReport/report.parquet", header=True, mode="overwrite")

from google.colab import drive
drive.mount('/content/drive')

items.show()

campaigns.show()

itemsStock.show()

customers.show()

subscriptions.show()

events.show()

subscribed_users_check = subscriptions.filter(col("subscription_type") == "item_alert")
print("Subscribed users:", subscribed_users_check.count())

wishlist_events_check = events.filter(col("event_type") == "addToWishlist")
print("Wishlist add events:", wishlist_events_check.count())

wishlist_and_items = wishlist_events_check.join(items, wishlist_events_check.item_id == items.id)
print("Wishlist items found in items dataset:", wishlist_and_items.count())

items.createOrReplaceTempView("items")
itemsStock.createOrReplaceTempView("itemsStock")
campaigns.createOrReplaceTempView("campaigns")
customers.createOrReplaceTempView("customers")
subscriptions.createOrReplaceTempView("subscriptions")
events.createOrReplaceTempView("events")

test = spark.sql("""
select * from events e
join campaigns c on c.item_id = e.item_id """ )

test.show()

result = spark.sql("""
SELECT
    c.first_name,
    c.email,
    i.name AS item_name,
    i.url AS item_url,
    (i.price * (1 - CAST(camp.discount AS DECIMAL) / 100)) AS final_price
FROM
    events e
INNER JOIN
    campaigns camp ON e.item_id = camp.item_id
INNER JOIN
    itemsStock istock ON e.item_id = istock.item_id
INNER JOIN
    items i ON e.item_id = i.id
INNER JOIN
    subscriptions subs ON e.customer_id = subs.customer_id
INNER JOIN
    customers c ON e.customer_id = c.id
WHERE
    e.event_type in ('addToWishlist','addToCart')
    AND istock.stock_quantity > 0
    AND subs.subscription_type = 'item_alert'
GROUP BY
    c.first_name,
    c.email,
    i.name,
    i.url,
    i.price,
    camp.discount
""")

result.show()

test_query_1 = spark.sql("""
SELECT e.customer_id, i.id AS item_id, i.name
FROM events e
JOIN items i ON e.item_id = i.id
WHERE e.event_type in ('addToWishlist','addToCart')
""")

test_query_1.show()

test_query2 = spark.sql("""
select distinct e.event_type
from events e
 """)

test_query2.show()

test_query_2 = spark.sql("""
SELECT e.customer_id, i.id AS item_id, i.name, camp.name AS campaign_name
FROM events e
JOIN items i ON e.item_id = i.id
JOIN campaigns camp ON i.id = camp.item_id
WHERE e.event_type = 'addToWishlist'
""")

test_query_2.show()

test_query_3 = spark.sql("""
SELECT e.customer_id, i.id AS item_id, i.name, istock.stock_quantity
FROM events e
JOIN items i ON e.item_id = i.id
JOIN itemsStock istock ON i.id = istock.item_id
WHERE e.event_type = 'wishlist'
  AND istock.stock_quantity > 0
""")

test_query_3.show()

test_query_4 = spark.sql("""
SELECT DISTINCT e.customer_id
FROM events e
JOIN subscriptions subs ON e.customer_id = subs.customer_id
WHERE subs.subscription_type = 'item_alert'
""")

test_query_4.show()

test = spark.sql("""
select distinct subscription_type from subscriptions""")

test.show()