# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Strip all whitespace from strings
        feild_names = adapter.field_names()
        for feild_name in feild_names:
            if feild_name != 'description':
                value = adapter.get(feild_name)
                adapter[feild_name] = value.strip()
        
        ## Category & Product Type --> switch to lowercase
        lowercase_keys = ['catagory', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', ' ')
            adapter[price_key] = float(value)
            
        ## Availbaility  --> exact number of books in stocks
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')    
        if len(split_string_array) <2:
            adapter['availability'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['availability'] = int(availability_array[0])

        ## Reviews --> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_string)

        ## Stars --> convert text to number
        stars_string = adapter.get('stars')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()

        if stars_text_value == 'zero':
            adapter['stars'] = 0
        elif stars_text_value == 'one':
            adapter['stars'] = 1
        elif stars_text_value == 'two':
            adapter['stars'] = 2
        elif stars_text_value == 'three':
            adapter['stars'] = 3
        elif stars_text_value == 'four':
            adapter['stars'] = 4
        elif stars_text_value == 'five':
            adapter['stars'] = 5
        


        return item
    

import mysql.connector

class SaveToMySQLPipeLine:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'bookuser',
            password = 'secretpass',
            database = 'books' 
        )
        ## Create cursor, to excuate comands
        self.cur = self.conn.cursor()
        # Create table if it does not exist
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id int NOT NULL AUTO_INCREMENT,
                url VARCHAR(225),
                title text,
                upc VARCHAR(255),
                product_type VARCHAR(225),
                price_excl_tax DECIMAL,
                price_incl_tax DECIMAL,
                tax DECIMAL,
                availability INTEGER,
                num_reviews INTEGER,
                stars INTEGER,
                catagory VARCHAR(225),
                description TEXT,
                price DECIMAL,
                PRIMARY KEY (id)
            )
        """)
    def process_item(self, item, spider):
        # Inserting the scraped data into the 'books' table
        self.cur.execute("""
            INSERT INTO books (
                url, title, upc, product_type, price_excl_tax, price_incl_tax,
                tax, availability, num_reviews, stars, catagory, description, price
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item.get('url'),
            item.get('title'),
            item.get('upc'),
            item.get('product_type'),
            item.get('price_excl_tax'),
            item.get('price_incl_tax'),
            item.get('tax'),
            item.get('availability'),
            item.get('num_reviews'),
            item.get('stars'),
            item.get('catagory'),
            item.get('description'),
            item.get('price'),
        ))

    # Commit the transaction to save the data to the database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.conn.close()    
        

