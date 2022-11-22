
#Imports
import os
import json
import ast
# import sqlite3
import re
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import make_interp_spline
import numpy as np
from matplotlib.collections import LineCollection
import sqlite3
pd.set_option('display.max_columns', None)




# PREPARING THE DATA

file_ext = 'updData'

etsy_orders = pd.read_csv(f'{file_ext}/etsy-sold-orders.csv')
etsy_deposits = pd.read_csv(f'{file_ext}/etsy-deposits.csv')
etsy_items = pd.read_csv(f'{file_ext}/etsy-sold-order-items.csv')
etsy_payments = pd.read_csv(f'{file_ext}/etsy-direct-checkout-payments.csv')

yoycol_orders = pd.read_csv(f'{file_ext}/yoycol-order-details.csv')

printify_orders = pd.read_csv(f'{file_ext}/printify-orders.csv')
printify_orders_2 = pd.read_csv(f'{file_ext}/printify-orders_2.csv')
printify_orders_3 = pd.read_csv(f'{file_ext}/printify_orders_3.csv')
printify_orders_4 = pd.read_csv(f'{file_ext}/printify_orders_4.csv')

#All orders data

items_cols_to_join = ['Order ID', 'Ship Name', 'Ship Address1', 'Ship Address2', 'Variations', 'Date Paid', 'Quantity', 'Item Total', 'Item Name', 'Transaction ID', 'Price']

items_to_join = etsy_items[items_cols_to_join]
items_to_join.columns = ['Order ID', 'Item-Ship Name', 'Item-Ship Address1', 'Item-Ship Address2', 'Item-Variations', 'Item-Date Paid', 'Item-Quantity', 'Item-Item Total', 'Item-Item Name', 'Item-Transaction ID', 'Item-Price']

orders_items_joined = etsy_orders.copy()
orders_items_joined = pd.merge(orders_items_joined,items_to_join,on='Order ID',how='outer')



def ordersDataTransform(**kwargs):
    # Combining all datasets of the same kind that come in multiples
    stores_ID_keys = {'etsy':"Order ID", 'printify': "Sales channel ID", 'yoycol':"Store order ID"}
    data_holder = {}
    for source, datasets in kwargs.items():
        order_frames = None
        if not isinstance(datasets, list):
            raise IndexError('InvalidIndexError -> dataset passed must be of type list including singular')
        if len(datasets) > 1:
            for i in range(len(datasets)):
                if order_frames is None:
                    order_frames = pd.DataFrame(datasets[0])
                    if i + 1 < len(datasets):
                        temp_frames = pd.concat([order_frames, pd.DataFrame(datasets[i+1])])
                        if order_frames.duplicated().any():
                            order_frames.drop_duplicates(inplace=True)
                        else:
                            order_frames = temp_frames
                    else:
                        data_holder[source] = order_frames
                else:
                    if i + 1 < len(datasets):
                        temp_frames = pd.concat([order_frames, pd.DataFrame(datasets[i+1])])
                        if order_frames.duplicated().any():
                            order_frames.drop_duplicates(inplace=True)
                        else:
                            order_frames = temp_frames
                    else:
                        data_holder[source] = order_frames
        else:
            data_holder[source] = pd.DataFrame(datasets[0])

    iter_index = 0
    on_key = 'Order ID'

    # Bring all datasets together for the final Orders_all dataset
    for src, data in data_holder.items():
        mapper_key = stores_ID_keys.get(src.lower())
        if mapper_key != on_key:
            data[on_key] = data[mapper_key]
            data.drop(columns=[mapper_key], inplace=True)
            data.columns = data.columns.map(lambda x: src[:4] + "-" + x if x != on_key else x)
            
            
        data.set_index('Order ID', inplace=True)
        data.index = data.index.map(lambda x:str(x))
        if iter_index == 0:
            orders_data = data
        else:
            orders_data = orders_data.join(data)
        iter_index += 1

    #Removing erraneus entry
    try:
        orders_data.drop(index='2581208238', inplace=True)
    except:
        pass

    
    orders_data['Sale Date'] = pd.to_datetime(orders_data['Sale Date'])
    orders_data['Source'] = orders_data.apply(lambda x: 'Printify' if not np.isnan(x['prin-Printify ID']) else 'Yoycol', axis=1)
    orders_data = orders_data.sort_values(['Sale Date'], ascending=False)
    return orders_data



# MAIN PAGE FUNCTIONS


# ['']


# ORDERS FUNCTIONS

class OrdersData:
    def __init__(self):
        #Key = OrderID column, will be used to querying.
        self.data = ordersDataTransform(etsy= [orders_items_joined], printify=[printify_orders, printify_orders_2, printify_orders_3, printify_orders_4], yoycol=[yoycol_orders])
        #Update ['Has Image'] field
        self.data = self.dataSetup(self.data)

    def dataSetup(self, df):
        #Product Image set up
        images_record = self.images_from_files(df['Item-Item Name'])
        no_image_path = 'media/products/no-prod-img.jpeg'
        df['Image Exists'] = df.index.map(lambda x: False if not images_record.get(str(x)) else True)
        df['Image Path'] = df.index.map(lambda x: 'media/products/'+images_record.get(str(x)) if images_record.get(str(x)) else no_image_path)
        eval_progress = self.progress_read_json()
        df['Progress'] = df.index.map(lambda x: eval_progress.get(x) if eval_progress.get(x) else 'Closed')
        return df

    def get_prod_img(self, key):
        get_query = self.data.index == key
        if get_query.any():
            return get_query
        else:
            return False

    def add_image_path(self):
        pass

    def insert_prod_image(self):
        pass
    #Will place image into folder and update images_record - key (Order Id) ,value(True or False)

    def images_from_files(self, df):
        media_dir = os.getcwd() + '/media' + '/products'
        product_names = os.listdir(media_dir)
        records = {}
        names = []
        for name in product_names:
            
            
            a = re.finditer(r'\.', name)
            spans = [x.start() for x in a]
            span= spans[-1]
            name_ext = name[span:]
            name_ = name[:spans[-1]]
            
            if name_ext in ['.png', '.jpg', '.jpeg']:
                names.append((name_, name_ext))

        for i, v in df.items():
            for n in names:
                if n[0] == v:
                    records[i] = n[0]+n[1]
        return records
    #Will scout files folder and return a dict with the orderID as key and image path as val
    #Ex. return d = {12392304: 'media/prod-imgs/luffys-hat.png}

    def progress_read_json(self):
        with open('user_data.txt', 'r') as f:
            json_data= f.read()
        data_dict = json.loads(json.dumps(ast.literal_eval(str(json_data))))
        if isinstance(data_dict, list):
            data_dict = {k: v for d in data_dict for k, v in d.items()}
        return data_dict

class UpdateUserPreferences:
    def progress_write_json(progress_dict):
        progress_dict = ','+str(progress_dict)
        with open('user_data.txt', 'a') as f:
            f.write(progress_dict)
        
            

# Adding new prefs to database approach

# def progress_field_change(id=None, new_status=None, new_color=None):
#     connection = sqlite3.connect('UsersData.db', timeout=10)
#     cursor = connection.cursor()
#     if id is not None:
#         try:
#             sql = 'insert or replace into OrderProgress(orderID, progress, progressColor) VALUES(?, ?, ?);'
#             cursor.execute(sql, (id, new_status, new_color))
#             connection.commit()
#             df = pd.read_sql_query('Select * from OrderProgress;', connection)
#             df.set_index(['Order ID'], inplace=True)
#             connection.close()
#         except:
#             connection.close()
#             raise NotImplementedError('Problem loading data into DB')
#         return df
#     df = pd.read_sql_query('Select * from OrderProgress;', connection)
#     df.set_index(['Order ID'], inplace=True)
#     connection.close()
#     print(df)
#     return df

class FuncsHandler:
    def __init__(self):
        self.timeframe = 'All'

    def setTimeframe(self, new_tm_f):
        self.timeframe = new_tm_f

    def filteredData(self, data, timeframe):
        dates = {'Week':7, 'Month':30, '6 Months': 182, 'Year':365}
        show_date = datetime.timedelta(days = dates.get(timeframe))
        today = datetime.datetime.now()

        mask = (data['Sale Date'] > today - show_date) & (data['Sale Date'] <= today)
        on_range_df = data.loc[mask]
        return on_range_df

    def getData(self):
        data = OrdersData().data
        if self.timeframe != 'All':
            return self.filteredData(OrdersData().data, self.timeframe)
        else:
            return data

    def tmf_test(self):
        return self.timeframe




