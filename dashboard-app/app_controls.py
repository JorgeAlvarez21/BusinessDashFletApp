import matplotlib
import flet
from flet import (Stack, Image, Theme, ListTile, TextButton, Icon, Card, border_radius, border, UserControl, OutlinedButton,
 padding,Column, Row, alignment, Container, margin, colors, icons, IconButton, FloatingActionButton, Page,
  ButtonStyle, Text, dropdown, Dropdown, PopupMenuButton, PopupMenuItem, TextStyle, ElevatedButton)
from flet.border import BorderSide
from flet.buttons import RoundedRectangleBorder, StadiumBorder


from flet.matplotlib_chart import MatplotlibChart
import warnings
warnings.filterwarnings('ignore')



class DropdownOverview(UserControl):
    def build(self):
        self.dd_overview = PopupMenuButton(
            content=Stack(
                controls=[
                    Container(
                        width=70,
                        height=30, 
                        border_radius=border_radius.all(30), 
                        bgcolor=colors.LIGHT_BLUE_50),
                    Container(
                        width=70,
                        height=30,
                        alignment=alignment.center,
                        padding=padding.only(bottom=4),
                        content= Text('Overview', text_align='center', size=11, color=colors.BLUE_900)
                    )
                ]
            ),
            items=[
                PopupMenuItem(content=Text("Check power", size=10), icon=icons.POWER_INPUT, on_click=lambda _: print("Bsasadst clicked!")),
                PopupMenuItem(content=Text("Check power2", size=10), icon=icons.POWER_INPUT, on_click=lambda _: print("Button with a custom content clicked!")),
                PopupMenuItem(content=Text("Check power3", size=10), icon=icons.POWER_INPUT, on_click=lambda _: print("Button with a custom content clicked!")),
                PopupMenuItem(content=Text("Check power3", size=10), icon=icons.POWER_INPUT, on_click=lambda _: print("Button with a custom content clicked!")),
            ]
        )
        return self.dd_overview

    def overviewChanged(self, e):
        print(self.dd_overview.value)


        
class DropdownTimeframe(UserControl):
    def build(self):
        self.dd_timeframe= Container(
            padding=padding.only(left=20,right=30),
            content=Dropdown(
                label="",
                border_radius=border_radius.all(30),
                text_size=10,
                width=120,
                height=30,
                hint_text="Nov 15 - Nov 22",
                hint_style=TextStyle(size=10, color=colors.CYAN_600),
                content_padding=padding.only(top=10, left=10),
                border_width=0,
                bgcolor=colors.LIGHT_BLUE_50,
                filled=True,
                options=[
                    dropdown.Option("Nov 15 - Nov 22"),
                    dropdown.Option("Green"),
                    dropdown.Option("Blue"),
                ]
            )
        )
        return self.dd_timeframe


class ElevatedBtnOrders(UserControl):
    def build(self):
        self.ordersButton= ElevatedButton(on_click=self.ordersBtnClicked, height=25, width=75,
            content= Text('Orders', size=10, color=colors.INDIGO_200)
        )
        return self.ordersButton

    def ordersBtnClicked(self, e):
        print('Im clicked')


class ElevatedBtnDeposits(UserControl):
    def build(self):
        self.depositsButton= ElevatedButton(on_click=self.depositsBtnClicked, height=25, width=75,
            content= Text('deposits', size=10, color=colors.INDIGO_200)
        )
        return self.depositsButton

    def depositsBtnClicked(self, e):
        print('Im clicked')

class ElevatedBtnWeek(UserControl):
    def build(self):
        self.activated = True
        self.on_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.LIGHT_BLUE_50}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.off_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.WHITE}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.weekButton= ElevatedButton('Week', on_click=self.weekBtnClicked, height=30, width=80, style=self.on_style,
            # content= Text('Week', size=10, color=colors.INDIGO_200)
        )
        
        return self.weekButton

    def weekBtnClicked(self, e):
        if self.activated:
            self.weekButton.style=self.off_style
            self.activated = False
            self.weekButton.update()
        else:
            self.weekButton.style= self.on_style
            self.activated=True
            self.weekButton.update()



class ElevatedBtnMonth(UserControl):
    def build(self):
        self.activated = False
        self.on_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.LIGHT_BLUE_50}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.off_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.WHITE}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.monthButton= ElevatedButton('Month', on_click=self.monthBtnClicked, height=30, width=80, style=self.off_style)
        
        return self.monthButton

    def monthBtnClicked(self, e):
        if self.activated:
            self.monthButton.style=self.off_style
            self.activated = False
            self.monthButton.update()
        else:
            self.monthButton.style= self.on_style
            self.activated=True
            self.monthButton.update()


class ElevatedBtnYear(UserControl):
    def build(self):
        self.activated = False
        self.on_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.LIGHT_BLUE_50}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.off_style = ButtonStyle(color={"":colors.BLACK}, bgcolor={"":colors.WHITE}, elevation={"": 0}, side={'':BorderSide(0, colors.WHITE)})
        self.yearButton= ElevatedButton('Year', on_click=self.yearBtnClicked, height=30, width=80, style=self.off_style)

        return self.yearButton

    def yearBtnClicked(self, e):
        if self.activated:
            self.yearButton.style=self.off_style
            self.activated = False
            self.yearButton.update()
        else:
            self.yearButton.style= self.on_style
            self.activated=True
            self.yearButton.update()


class PoppedDownBtn(UserControl):
    def build(self):
        self.popped_down = PopupMenuButton(
            items=[
                PopupMenuItem(text="Item 1"),
                PopupMenuItem(icon=icons.POWER_INPUT, text="Check power"),
                PopupMenuItem(),  # divider
                PopupMenuItem(
                    text="Checked item", checked=False
                ),
            ]
        )
        return self.popped_down
                

matplotlib.use("svg")
def displayPlot():
    import pandas as pd
    import matplotlib.pyplot as plt
    import datetime
    from scipy.interpolate import make_interp_spline
    import numpy as np
    from matplotlib.collections import LineCollection



    df2 = pd.read_csv('SampleData/EtsyDirectCheckoutPayments2022.csv')

    df2['Order Date'] = pd.to_datetime(df2['Order Date'])
    all_time = df2.copy()
    all_time['Order Count'] = 1
    daily = all_time.groupby('Order Date').sum()[['Gross Amount', 'Fees', 'Net Amount', 'Posted Gross', 'Posted Fees', 'Posted Net', 'Listing Amount', 'Order Count']];
    weekly = daily.resample('W').sum()
    monthly = daily.resample('M').sum()
    yearly = daily.resample('Y').sum()



    # %matplotlib inline

    fig = plt.figure(figsize=(6, 3))
    date = weekly.index
    value = weekly['Gross Amount']

    # create integers from strings
    idx = range(len(date))
    xnew = np.linspace(min(idx), max(idx), 300)

    # interpolation
    spl = make_interp_spline(idx, value, k=3)
    smooth = spl(xnew)








    #Increasing the spacing will space out colors. -> More color tones but less smooth
    x = np.linspace(0,1, 400)
    y = np.linspace(0,1, 400)
    cols = np.linspace(0,1,len(x))

    points = np.array([xnew, smooth]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    fig, ax = plt.subplots(figsize=(9.5, 3.7))
    lc = LineCollection(segments, cmap='GnBu')
    lc.set_array(cols)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    fig.colorbar(line,ax=ax).remove()




    # plotting, and tick replacement
    plt.plot(xnew, smooth, linewidth=.7)
    plt.margins(.15, 0)
    frame = plt.gca()

    for spine in frame.spines.values():
        spine.set_visible(False)

    # remove all the ticks and directly label each bar with respective value
    plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='on')

    frame.xaxis.set_tick_params(length=0)
    frame.yaxis.set_tick_params(length=0)
    plt.xticks(idx, date.strftime('%b-%d'));
    return MatplotlibChart(fig, expand=True)
