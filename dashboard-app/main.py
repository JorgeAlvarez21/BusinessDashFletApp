import flet
import os
import time
from flet import (Stack, Image, ProgressBar, Theme, theme, ListTile, TextButton, Icon, Card, border_radius, border, UserControl, View, ElevatedButton, AppBar, FilledTonalButton,
 padding,Column, Row, alignment, Container, margin, colors, icons, IconButton, FloatingActionButton, Page, TextStyle, ButtonStyle, Text, dropdown, Dropdown, CircleAvatar, theme )
from flet.border import BorderSide
from flet.buttons import RoundedRectangleBorder
import pandas as pd
#Custom modules import
from sales_data_funcs import CleanedData
import app_controls as AppControls
import page_views as views
def salesData():
    df1 = pd.read_csv('SampleData/EtsyDeposits2022.csv')
    df2 = pd.read_csv('SampleData/EtsyDirectCheckoutPayments2022.csv')
    sample_data = CleanedData(df1, df2)
    return sample_data


def main(page: Page):

    page.window_height = 950
    page.window_width = 1300
    page.window_frameless = False
    page.padding = padding.all(10)
    page.margin = margin.all(10)
    page.splash = ProgressBar(visible=False)
    page.theme_mode = "light" 

    sample_data = salesData()

    def viewRedirect(view_name):
        page.views.clear()
        page.route=view_name
        initial = View(
                "/home",
                [
                    AppBar(title=Text("Flet app"), bgcolor=colors.SURFACE_VARIANT),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        page.views.append(initial)

        
        if page.route == "/orders":
            view = views.ordersPage()
            page.views.append(view)
        page.update()

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

    appCanvas = Container(
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
                            content= IconButton(icon=icons.HOME, icon_size=23, icon_color=colors.WHITE, on_click=lambda _: pages_control.swapPage('/home'))
                        ),
                        Container(
                            width=50,
                            height=220,
                            alignment=alignment.center,
                            content=Column(spacing=0, alignment='center', controls=[
                                IconButton(on_click=lambda _:pages_control.swapPage('/orders'), icon=icons.NOTE_ALT, icon_size=30, icon_color=colors.WHITE, bgcolor=colors.BLACK12, style=ButtonStyle(side={"": BorderSide(0)}, padding=0)),
                                IconButton(icon=icons.ATTACH_MONEY, icon_size=23, icon_color=colors.WHITE, bgcolor=colors.BLACK12, style=ButtonStyle(side={"": BorderSide(0)}, padding=0))
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
            
            Container(padding=padding.only(left=30, top=30), margin=margin.all(0),
                content=Column(
                    controls=[
                        Container(height=170, width=700,
                            content=Row(alignment='spaceBetween', 
                                controls=[Container(width=350,padding=padding.only(top=30),
                                    content=Column(
                                        controls=[                                
                                            Text('Monitor health of your business', color=colors.BLACK, size=30, weight="w900", font_family='Raleway'),
                                            Text('Control and analyze your data in the easiest way', color=colors.BLACK)
                                        ]
                                    )
                                ),
                                Container(width=260, alignment=alignment.bottom_left, padding= padding.only(bottom=10),
                                    content=Row(
                                        controls=[
                                            AppControls.ElevatedBtnWeek(), 
                                            AppControls.ElevatedBtnMonth(),
                                            AppControls.ElevatedBtnYear(),
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                       #Hide here 
                        Container(height=260, width=730,
                            content=Row(alignment='center',spacing=10, controls=[
                                Container(border_radius=border_radius.all(35), width=230, height=240,
                                    content=Stack( 
                                        controls=[
                                            #Image(src="media/motorbike-world-travel-woman.png", opacity=.4, fit='fill', border_radius=border_radius.all(35), width=230, height=240),
                                            Image(src="media/world-vector.png", opacity=.2, fit='fill', border_radius=border_radius.all(35), width=230, height=240,),
                                            Container(width=230, height=240, border_radius=border_radius.all(35), opacity=.5, bgcolor=colors.GREEN_400),

                                            Container(width=230, height=240,  border_radius=border_radius.all(35), padding=padding.only(top=30, left=15),
                                                content=Column(
                                                    controls=[
                                                        Row(
                                                            controls=[
                                                                Text("Views", color=colors.BLACK, weight='bold', size=20),
                                                                Icon(icons.ALBUM, color=colors.BLACK),
                                                            ]
                                                        ),
                                                        Text("Music by Julie Gable.", color=colors.BLACK)
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),
                                Container(border_radius=border_radius.all(35), width=230, height=240,
                                    content=Stack( 
                                        controls=[
                                            #Image(src=f"media/animated-woman-shopping-business.png", width=230, height=240, opacity=.4, fit='fill', border_radius=border_radius.all(35)),
                                            Image(src=f"media/purchases-test.jpeg", width=230, height=240, opacity=.4, fit='fill', border_radius=border_radius.all(35)),
                                            Container(width=230, height=240,  border_radius=border_radius.all(35), opacity=.5, bgcolor=colors.LIGHT_BLUE_300),

                                            Container(width=230, height=240,  border_radius=border_radius.all(35), padding=padding.only(top=30, left=15),
                                                content=Column(
                                                    controls=[
                                                        Row(
                                                            controls=[
                                                                Text("Purchases", color=colors.BLACK, weight='bold', size=20),
                                                                Icon(icons.ALBUM, color=colors.BLACK),
                                                            ]
                                                        ),
                                                        Text("Music by Julie Gable.", color=colors.BLACK)
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),
                                Container(border_radius=border_radius.all(35), width=230, height=240,
                                    content=Stack(
                                        controls=[
                                            #Image(src=f"media/illustration-woman-stairs-clipart.png", width=230, height=240, opacity=.4, fit='fill', border_radius=border_radius.all(35)),
                                            Image(src=f"media/net-amount-test.jpeg", width=230, height=240, opacity=.4, fit='fill', border_radius=border_radius.all(35)),
                                            Container(width=230, height=240, bgcolor=colors.AMBER_700, border_radius=border_radius.all(35), opacity=.5),

                                            Container(width=230, height=240,  border_radius=border_radius.all(35), padding=padding.only(top=30,bottom=20, left=15),
                                                content=Column(alignment='spaceBetween',
                                                    controls=[
                                                        Row(
                                                            controls=[
                                                                Text("Net Amount", color=colors.BLACK, weight='bold', size=20),
                                                                Icon(icons.ALBUM, color=colors.BLACK),
                                                            ]
                                                        ),
                                                        Container(alignment=alignment.bottom_right, padding=padding.only(right=20), content=Text(f"$  {sample_data.retrieveGrossAmt()}", size=25, weight='bold',  color=colors.BLACK))
                                                        
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                ),

     
                            ])
                        ),

                        Container(height=450, width=800,# bgcolor=colors.BLUE_100, opacity=.3,
                            content=Column(spacing=0,
                                controls=[
                                    Container(opacity=1, padding=padding.all(0),
                                        content=Row(
                                            controls=[
                                                Container(height=60, width=300, alignment=alignment.bottom_center, padding=padding.only(left=0, bottom=10,right=45),
                                                content=Text('Total Profit', size=25, color=colors.BLACK)),
                                                Container(Container(height=60, width=400, #bgcolor=colors.DEEP_PURPLE_700,
                                                    content=Row(alignment='end', spacing=0,
                                                        controls=[
                                                            
                                                            AppControls.DropdownOverview(),
                                                            AppControls.DropdownTimeframe()
                                                            
                                                        ]
                                                    )
                                                ))
                                            ])
                                    ),
                                    Container(padding=padding.only(top=0, bottom=50, right=60, left=0), margin=margin.all(0), height=400, width=800, alignment=alignment.top_center,
                                        content=AppControls.displayPlot())
                                ]
                            )
                        )
                    ]
                )   
            ),

            Container(width=290, height=820, padding=padding.only(top=75, right=10),
                content=Column(spacing=5,
                    controls=[
                     #Container(padding=padding.only(left=150), content=theme_button),  #Enables Theme Selection
                        Container(border_radius=border_radius.all(30), height=360, width=310,
                        #    content=Image(src='profile-picture.png', height=380, width=330, fit='fill', border_radius=border_radius.all(30))),
                            content=Image(src='architecture-bld-placehorder.png', height=380, width=310, fit='fill', border_radius=border_radius.all(30))),
                        Container(width=330, height=55,
                            content=Row(
                                controls=[
                                    AppControls.ElevatedBtnOrders(),
                                    AppControls.ElevatedBtnDeposits(),
                                    Container(padding=padding.only(left=90), content=AppControls.PoppedDownBtn())
                                    
                                ]
                            )
                        ),
                        Container(width=330, height=320,
                            content=Column(spacing=20,
                                controls=[
                                    Container(border_radius=border_radius.all(40), height=90,bgcolor=colors.DEEP_ORANGE_400,
                                        content=Row(alignment='spaceEvenly',
                                            controls=[
                                                #Container(padding=padding.only(left=10), content=Image(src='/media/fake-prof1.jpeg', height=60, border_radius=border_radius.all(100))),#Image
                                                Container(padding=padding.only(left=10), content=Image(src='/media/fake-profile1.jpeg', height=60, width=60, border_radius=border_radius.all(100))),# Dummy Img
                                                Container(
                                                    content=Text('Evelyn Winn', size=15)
                                                ),#Name
                                                Container(IconButton(icons.ARROW_CIRCLE_UP)),#Payment
                                            ]
                                        )),
                                    Container(border_radius=border_radius.all(40), height=90,
                                        content=Row(alignment='spaceEvenly',
                                            controls=[
                                               # Container(padding=padding.only(left=10), content=Image(src='/media/fake-prof2.jpeg', height=60, border_radius=border_radius.all(100))),#Image
                                                Container(padding=padding.only(left=10), content=Image(src='/media/fake-profile2.jpeg', height=60, width=60, border_radius=border_radius.all(100))),# Dummy Img
                                                Container(
                                                    content=Text('Celest Daniels', size=15)
                                                ),#Name
                                                Container(IconButton(icons.ARROW_CIRCLE_UP)),#Payment
                                            ]
                                        )),
                                    Container(border_radius=border_radius.all(40), height=90,
                                        content=Row(alignment='spaceEvenly',
                                            controls=[
                                              #  Container(padding=padding.only(left=10), content=Image(src='/media/fake-prof3.jpg', height=60, border_radius=border_radius.all(100))),#Image
                                                Container(padding=padding.only(left=10), content=Image(src='/media/fake-profile3.jpeg', height=60, width=60, border_radius=border_radius.all(100))),# Dummy Img
                                                Container(
                                                    content=Text('Julio Tatcher', size=15)
                                                ),#Name
                                                Container(IconButton(icons.ARROW_CIRCLE_UP)),#Payment
                                            ]
                                        )),
                                ]
                            )),
                    ]
                )
            )
        ])
    )

    
    

    class PageRoutesControl:
        def __init__(self):
            self.saved_pages = ['/home', '/orders']
            self.on_page = '/home'  # Initial Route
            self.swapTrigger()


        def swapPage(self, new_page):
            # if new_page not in self.saved_pages:
            #     raise NameError('Page not found in routes')
            self.on_page = new_page
            self.swapTrigger()
        
        def swapTrigger(self):
            page.route = self.on_page

            pageSetup()


    def pageSetup():
        if page.route == '/home':
            page.clean()
            page.add(appCanvas)
        elif page.route == '/orders':
            page.clean()
            views.ordersPage(page)
            page.update()   

        

    def route_change(route):
        page.add(Text(f"New route: {route}"))
        if page.route == '/home':
            page.clean()
            page.add(appCanvas)
        elif page.route == '/orders':
            page.clean()
            views.ordersPage(page)
            page.update()   


    page.on_route_change = route_change
    page.update()       

    pages_control = PageRoutesControl()

flet.app(target=main, assets_dir="media") 
