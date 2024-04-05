Your marketing colleagues want to create a new email sendout to increase sales. Their idea is to send an email for all customers who have recently shown interest in products that are now part of a discount campaign.

Your task is to generate a report that will enable this email sendout. You can use either Scala Spark or PySpark.

This report should contain the following information:
- first name and email of users who:
    - are subscribed to the item alerts mailing list
    - have at least one item in wishlist that:
        - is part of an active campaign
        - is in stock
- name, url and final price of items in user's wishlist and in an active campaign

Your inputs are:

- items - Products in the webshop (id, name etc.)
- itemsStock - Stock information of each product
- campaigns - Currently running campaigns
- customers - Webshop customers
- subscriptions - Mailing list subscriptions
- events - Events representing customers' interactions with the webshop