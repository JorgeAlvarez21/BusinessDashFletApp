import flet
import time
import os
from flet import (Stack, Radio, TextField, Theme, Image, ProgressBar, Divider, Checkbox, ListView, ListTile, RadioGroup, TextButton, Icon, Card, theme, border_radius, border, UserControl, View, ElevatedButton, AppBar, FilledTonalButton, padding,Column, Row, alignment, Container, margin, colors, icons, IconButton, FloatingActionButton, Page, TextStyle, ButtonStyle, Text, dropdown, Dropdown, CircleAvatar, theme )
from flet.border import BorderSide
from flet.ref import Ref
from flet.buttons import RoundedRectangleBorder
import pandas as pd
#Custom modules import
from sales_data_funcs import CleanedData
import app_controls as AppControls
from data_funcs import OrdersData, UpdateUserPreferences, FuncsHandler


# def salesData():
#     df1 = pd.read_csv('SampleData/EtsyDeposits2022.csv')
#     df2 = pd.read_csv('SampleData/EtsyDirectCheckoutPayments2022.csv')
#     sample_data = CleanedData(df1, df2)
#     return sample_data
data_handler = FuncsHandler()
class RefreshDF:
    def __init__(self):
        pass
    def getDF(self):
        df = data_handler.getData()
        return df

df_obj = RefreshDF()
df = df_obj.getDF()

print(df)
class RowWidgets:
    def __init__(self):
        self.add_ons_qty = 10
        if df.empty:
            self.orders_qty = 0    
        else:
            
            self.orders_qty = len(df.index)
        self.header_data = ['#', 'ID', 'Pic', 'Date', 'Item', 'Qty', 'Customer', 'Total', 'Source', 'Progress', 'View']
        self.widget_widths = [20, 55, 45, 80, 120, 70, 80, 60, 70, 110, 40]

    def getSingleWidth(self):
        # The row's whole width = 850
        width = 850 / self.add_ons_qty
        return width

    

def main(page: Page):
    page.title = "Orders"
    page.theme_mode = "light" 
    page.window_height = 950
    page.window_width = 1300
    page.window_frameless = False
    page.padding = padding.all(10)
    page.margin = margin.all(10)
    page.scroll = "always"
    page.splash = ProgressBar(visible=False)


    


    widget = RowWidgets()
    colors_dict = {'Closed' : 'Light Blue', 'Open': 'Green', 'On Transit': 'Orange', 'Canceled': 'Red'}

    def change_theme(e):
        page.splash.visible = True
        page.update()
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark" 
        page.splash.visible = False
        theme_button.selected = not theme_button.selected 
        time.sleep(0.2)
        page.update()

    theme_button = IconButton(
            icons.DARK_MODE,
            selected=False,
            selected_icon=icons.LIGHT_MODE,
            icon_size=35,
            tooltip="change theme",
            on_click=change_theme,
            style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ),
        )

    #Preparing data into rows and cols for display and manipulation
    def createTableHeader():
        widget_width= 683/ widget.add_ons_qty
        items=[]
        for num, i in enumerate(widget.header_data):
            items.append(
            Container(
                    content=Text(value=i, color=colors.BLUE_GREY_400),
                    alignment=alignment.center,
                    width= widget.widget_widths[num],
                    height=25,
#                    bgcolor=colors.AMBER,
                    border_radius=border_radius.all(5),
                )
            )
        return items
     
    def createRows():
        global refs
        #Create refs for rows
        refs = {}
        ref_names = []
        for i in range(widget.orders_qty):
            var = 'data_row_' + str(i)
            refs[var] = Ref[Row]()
        widget_width= 683/ widget.add_ons_qty
        items= []
        column = Column()
        for col_i in range(0, widget.orders_qty):
            row= Row(ref=refs.get('data_row_'+str(col_i)))
            for row_i in range(widget.add_ons_qty+1):
                if row_i == 0: #Select Checkbox
                    row.controls.append(
                        selectCheckBtn(col_i)
                    )
                elif row_i == 1: #ID
                    row.controls.append(
                        idField(col_i)
                    )
                elif row_i == 2:
                    row.controls.append(
                        picField(col_i)
                    )
                elif row_i == 3:
                    row.controls.append(
                        dateField(col_i)
                    )
                elif row_i == 4:
                    row.controls.append(
                        itemNameField(col_i)
                    )
                elif row_i == 5:
                    row.controls.append(
                        quantityField(col_i)
                    ) 
                elif row_i == 6:
                    row.controls.append(
                        customerNameField(col_i)
                    ) 
                elif row_i == 7:
                    row.controls.append(
                        totalField(col_i)
                    )
                elif row_i == 8:
                    row.controls.append(
                        sourceField(col_i)
                    ) 
                elif row_i == 9:
                    row.controls.append(
                        progressDropdown(col_i)
                    )
                else:
                    row.controls.append(
                                Container(
                                        content=Text(value=row_i),
                                        alignment=alignment.center,
                                        width= widget.widget_widths[int(row_i)],
                                        height=35,
            #                          bgcolor=colors.AMBER,
                    )
                )

            column.controls.append(row)
        items.append(column)

        return items


    
    def createColumns():
        header=createTableHeader()
        rows = createRows()
        items=[]
        # items.append(header)
        items.append(Row(controls=header))
        items.append(Container(margin=margin.only(bottom=2), padding=padding.only(bottom=5), content=Divider(height=5, thickness=1)))
        items.append(
            Container(Row(controls=rows)))
        return items

#Buttons Functionality and Logic

    def selectCheckBtn(index_value):
        return Container(width=widget.widget_widths[0],
            content= Checkbox(on_change=check_changed, data=index_value, fill_color=colors.BLUE_400))
    def check_changed(e):
        activated = False
        row_idx = e.control.data
        on_check = e.data
        all_row_controls = refs.get('data_row_'+str(row_idx)).current.controls

        #EXAMPLE change bgcolor of entire row for selected checkbox
        if on_check == 'true':
            for control in all_row_controls:
                control.bgcolor= colors.LIGHT_BLUE_100
                control.update()
        else:
            for control in all_row_controls:
                control.bgcolor= None
                control.update()
        #EXAMPLE2 change bgcolor of container col1, row1
        # refs.get('data_row_1').current.controls[1].bgcolor = colors.BLUE_200
        # refs.get('data_row_1').current.controls[1].update()
    def idField(index):
        return Container(width=widget.widget_widths[1],
            content= Text(df.index[index][:5])
        )
    def picField(index):
        img_path = df['Image Path'][index]
        return Container(width=widget.widget_widths[2], alignment=alignment.center,
            content=Image(src=img_path, border_radius=border_radius.all(10))
        )
    def dateField(index):
        date = df['Sale Date'][index].strftime('%y-%b-%d')
        return Container(width=widget.widget_widths[3], alignment=alignment.center,
            content=Text(date)
        )
    def itemNameField(index):
        item_name = df['Item-Item Name'][index]
        return Container(width=widget.widget_widths[4], alignment=alignment.center,
            content=Text(item_name)
        )
    def quantityField(index):
        qty = df['Item-Quantity'][index]

        return Container(width=widget.widget_widths[5], alignment=alignment.center,
            content=Text(str(qty))
        )
    def customerNameField(index):
        customer_name = df['Full Name'][index]

        return Container(width=widget.widget_widths[6], alignment=alignment.center,
            content=Text(str(customer_name))
        )
    def totalField(index):
        total = df['Order Total'][index]

        return Container(width=widget.widget_widths[6], alignment=alignment.center,
            content=Text('$ '+str(total))
        )
    def sourceField(index):
        source = df['Source'][index]
        return Container(width=widget.widget_widths[6], alignment=alignment.center,
            content=Text(str(source))
        )
    def progressDropdown(index):
        
        hint_value = df['Progress'][index]
        fill_color = colors_dict.get(hint_value)
        if fill_color == 'Light Blue':
            c = colors.LIGHT_BLUE_50
        elif fill_color == 'Green':
            c = colors.GREEN
        elif fill_color == 'Orange':
            c = colors.ORANGE
        elif fill_color == 'Red':
            c = colors.RED
        else:
            c= colors.AMBER
        return Container(width=widget.widget_widths[6], alignment=alignment.center, 
            content=Dropdown(
                data=index,
                content_padding=padding.only(top=1, left=5, right=5),
                on_change=progress_changed,
                width=widget.widget_widths[6],
                filled=True,
                bgcolor=c,
                height=25,
                hint_text=hint_value,
                text_size=12,
                hint_style=TextStyle(size=12),
                options=[
                    dropdown.Option("Closed"),
                    dropdown.Option("Open"),
                    dropdown.Option("On Transit"),
                    dropdown.Option("Canceled")
                ],
            )
        )
    def progress_changed(e):
        global df
        row_idx = e.control.data
        btn_control = refs.get('data_row_'+str(row_idx)).current.controls[9].content

        value= btn_control.value
        id =df.index[row_idx]
        fill_color = colors_dict.get(btn_control.value)
        d = {id:value}
        UpdateUserPreferences.progress_write_json(d)
        
    def selectTimeframeDpd(e):
        global df
        global data_handler
        print('Sending..', e.data)
        data_handler.setTimeframe(e.data)
        print('TEST xxxxxxx', data_handler.tmf_test())
        df = df_obj.getDF()
        print(df)
        ordersWidget.update()
        page.update()
        ###??????




    # Main App Screen

    ordersWidget = Container(
        border_radius=border_radius.all(30),
        alignment=alignment.top_left,
        height = 880,
        width = 1300,

        content=Row([ 
            Container(
                border_radius = border_radius.only(topLeft=30, bottomLeft=30),
                width=80,
                height=1200,
                alignment=alignment.center,
                bgcolor=colors.BLACK,
                content=Column(controls=[
                    Container(
                        width=50,
                        height=215,
                        padding = padding.only(bottom=20),
                    ),
                    Container(
                        width=50,
                        height=220,
                        alignment=alignment.center,
                        content=Column(spacing=0, alignment='center', controls=[
                            IconButton(on_click=lambda _:pages_control.swapPage('/orders'), icon=icons.NOTE_ALT, icon_size=30, icon_color=colors.WHITE, bgcolor=colors.BLACK12, style=ButtonStyle(side={"": BorderSide(0)}, padding=0)),
                        ])
                    ),
                    Container(
                        width=50,
                        height=345,
                        alignment=alignment.bottom_center,
                        padding = padding.only(bottom=20),
                        content= IconButton(icon=icons.ABC_OUTLINED, icon_size=30, icon_color=colors.WHITE)
                    )     
                ])
            ),
            #Page Begins here

            #MIDDLE
            Container(padding=padding.only(top=5, left=20), 
                content=Column(
                    controls=[
                        Container(width=850, height=850,
                            content=Column(spacing=0,
                                controls=[

                                    Container(height=220,
                                        content=Column([
                                            Container(height=100, padding=padding.only(top=50), margin=margin.all(0),
                                                content=(Row(alignment='center', 
                                                    controls=[
                                                    Container(width=600, 
                                                        content= TextField(
                                                            content_padding=padding.only(bottom=5, left=15),
                                                            text_align='justify',
                                                            cursor_height=14,
                                                            text_size=13,
                                                            height=35,
                                                            border_radius=border_radius.all(15),
                                                            hint_text="   Quick Search",
                                                            hint_style=TextStyle(size=13),
                                                            color=colors.BLACK,
                                                            bgcolor=colors.WHITE,
        
                                                            )
                                                    ),
                                                    Container(width=240,
                                                        content=Row(alignment='center', spacing=2,
                                                            controls=[
                                                                Container(
                                                                    content=Text('Meagan B.', size=14)),#Name
                                                                Container(
                                                                    padding=padding.only(left=10), content=Image(src='/media/fake-prof3.jpg', height=35, border_radius=border_radius.all(100))),#Image
                                                                Container(content=IconButton(icons.ARROW_DROP_DOWN))
                                                            ]
                                                        )
                                                        )
                                                ]))),
                                            Container(height=120, padding=padding.only(bottom=50), margin=margin.all(0),
                                            content=(Row([#The Orders and 4 buttons
                                                    Container(width=600,
                                                        content=Row(controls=[
                                                            Container(height=50, width=150,
                                                                content=Text('Orders', size=35, weight='w800', color=colors.BLACK)),
                                                            Container(height=35, width=120, margin=margin.all(0),
                                                            content=Dropdown( border_radius=border_radius.all(15), hint_text='Show: All', content_padding=padding.only(top=5, left=4), text_size=12, hint_style=TextStyle(size=13), on_change=selectTimeframeDpd,
                                                                options=[
                                                                    dropdown.Option("All"),
                                                                    dropdown.Option("Week"),
                                                                    dropdown.Option("Month"),
                                                                    dropdown.Option("6 Months"),
                                                                    dropdown.Option("Year"),
                                                                ],
                                                                width=200,
                                                            )),
                                                            Container(height=35, width=120,
                                                                content=Dropdown( border_radius=border_radius.all(15), hint_text= 'Group By: Item', content_padding=padding.only(top=5, left=4), text_size=12, hint_style=TextStyle(size=13),
                                                                options=[
                                                                    dropdown.Option("Red"),
                                                                    dropdown.Option("Green"),
                                                                    dropdown.Option("Blue"),
                                                                ],
                                                                width=200,
                                                            )),
                                                            Container(height=35, width=180,
                                                                content=Dropdown( border_radius=border_radius.all(15), hint_text= 'Sort By: Newest First', content_padding=padding.only(top=5, left=4), text_size=12, hint_style=TextStyle(size=13),
                                                                options=[
                                                                    dropdown.Option("Red"),
                                                                    dropdown.Option("Green"),
                                                                    dropdown.Option("Blue"),
                                                                ],
                                                                width=200,
                                                            )),

                                                        ])), 
                                                    Container(width=250, padding=padding.only(right=10),
                                                        content= Row(alignment='spaceBetween',
                                                            controls=[
                                                                IconButton(icons.FILTER_LIST),
                                                                Container(padding=padding.all(0), 
                                                                    content=ElevatedButton(text="New Order", height=35, width=120, style=ButtonStyle(bgcolor={'':colors.BLUE_ACCENT_700}, color={"":colors.WHITE})))
                                                        ])
                                                        ),
                                                ])))
                                        ])),
                                    Container(height=35, width=350,
                                        content=Row(
                                            controls=[
                                                TextButton(content=Container(Text("Select All", size=12))),
                                                TextButton(content=Container(Text("Edit", size=12))),
                                                TextButton(content=Container(Text("Delete", size=12))),
                                                TextButton(content=Container(Text("Change Status", size=12)))
                                                  

                                            ]
                                        )),
                                    Container(height=580,
                                        content=Column(scroll=True, controls=[
                                            Column(
                                            controls=[
                                                Container(width=850,
                                                    content=Column(spacing=4,
                                                        controls=
                                                        
                                                            createColumns()

                                                            

                                                                #All the widgets here
                                                                #Container(width= widget.getSingleWidth, height=40, )#bgcolor=colors.BLUE)
                                                    )
                                                )#Each Order Row
                                            ]
                                        )
                                        ])
                                        )
                                        

                                ]
                            )
                        )


                    ]
                )
            ),
            #LAST
            Container(padding=padding.only(top=10, left=20), bgcolor=colors.BLUE,
                content=Column(spacing=30,
                        controls=[
                            Container(padding=padding.only(left=200), content=theme_button),
                            Container(padding=padding.all(0), width=230, height=200, bgcolor=colors.RED, border_radius=border_radius.all(30),
                                content= Column(
                                    controls=[
                                    Container(padding= padding.only(left=20, top=10), content= Text('Recent Reviews', size=20)),
                                    Container(height=100, width=100, bgcolor=colors.ORANGE, content= Text('Coming soon', size=20))
                                    ]
                                )
                            ),

                            Container(padding=padding.all(0), width=230, height=200, bgcolor=colors.RED, border_radius=border_radius.all(30)),
                            Container(padding=padding.all(0), width=230, height=300, bgcolor=colors.RED, border_radius=border_radius.all(30)),
                        ]
                            )
                ),

            ])
        )

    page.add(ordersWidget)
    page.update()

flet.app(target=main, assets_dir="media") 



