import pandas as pd

# class SampledData:
#     def __init__(self, timeframe):
        #Accepts Daily, Weekly, Monthly and Yearly
        # if timeframe in ['Daily', 'Weekly', 'Monthly', 'Yearly']:
        #     self.timeframe()


class CleanedData:
    def __init__(self, deposits, payments):
        self.deposits = deposits
        self.summary = payments

        self.summary = self.dataTransform(self.summary)
        self.data_resampled = self.dataResampling(self.summary)
        self.timeframe = 'all_time'

    def timeframe_setter(self, new_timeframe):
        self.timeframe = new_timeframe




    def dataTransform(self, df):
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        return df

    def dataResampling(self, df):
        #Returns dates in dictionary
        df = df.copy()
        all_orders = sum(df.groupby('Order ID').count()['Payment ID'])
        #Resampling daily orders
        daily = df.groupby('Order Date')['Order ID'].count()
        weekly = daily.resample('W').sum()
        monthly = daily.resample('M').sum()
        yearly = daily.resample('Y').sum()
        dict = {'daily':daily, 'weekly':weekly, 'monthly':monthly, 'yearly': yearly, 'all_time':all_orders}
        return dict



        
    def retrieveGrossAmt(self):
        gross = self.summary['Gross Amount']
        return round(sum(gross), 2)