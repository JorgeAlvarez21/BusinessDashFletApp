import flet as ft
import pandas as pd


def createDataframe():
    names = ['Mickey', 'Barney', 'Lee', 'Kenny', 'Ruby', 'Jayden', 'Rob', 'Luna']
    scores = [9 , 7, 4, 9, 8 ,5 , 9, 10]
    levels = ['Junior', 'Junior', 'Senior', 'Junior', 'Freshman', 'Sophmore', 'Junior', 'Freshman']
    return pd.DataFrame({'names':names, 'scores':scores, 'levels':levels})



def main(page: ft.Page):
    page.theme_mode = "light" 
    page.window_height = 950
    page.window_width = 1300
    entries_plane = ft.Ref[ft.Column]()
    # Marking columns for deletion 
    df = createDataframe()
    rows_to_remove = [1, 3, 4]
    rem_names = [df.names[i] for i in rows_to_remove]
    print(rem_names)



    print("BEFORE REMOVING ROWS \n", df)

    def createRows():
        n_Rows = len(df.index)
        n_Cols = len(df.columns)
        amber_color = ft.colors.AMBER
        red_color = ft.colors.RED

        items= []
        column = ft.Column()
        for row_i in range(n_Rows):
            if row_i in rows_to_remove and df['names'].iloc[row_i] in rem_names:
                set_color = red_color
            else:
                set_color = amber_color
            row= ft.Row()
            for col_i in range(1, n_Cols+1):
                box_val = df.iloc[row_i][col_i-1]
                row.controls.append(
                    ft.Container(
                            content=ft.Text(value=f'Row:{row_i} -- Val:  {box_val}'),
                            alignment=ft.alignment.center,
                            width= 100,
                            height=60,
                            bgcolor=set_color,
                    )
                )
            column.controls.append(row)
        items.append(column)
        return items

    def createColumns():
        rows = createRows()
        items=[]
        items.append(ft.Container(margin=ft.margin.only(bottom=2), padding=ft.padding.only(bottom=5), content=ft.Divider(height=5, thickness=1)))
        items.append(
            ft.Container(ft.Row(controls=rows)))
        return items


    """This removeRows function where we remove the rows in the and we expect them to disappear from the Column, the variable df has been refreshed, 
        which is where they had been generated"""
        
    def removeRows(e):
        for row in rows_to_remove:
            df.drop(row, inplace=True)
        print("AFTER \n", df)
        page.add(ft.Text('Rows Removed', size=25))
        widget.update()
        entries_plane.current.clean()
        for entry in createColumns():
            entries_plane.current.controls.append(entry)
        
        page.update()
                                    
    widget = ft.Row(
        controls=[ft.Container(height=400, width=350, bgcolor=ft.colors.BLUE_600,
            content=ft.Column(scroll=True, controls=[
                ft.Column(
                controls=[
                    ft.Container(width=850,
                        content=ft.Column(ref=entries_plane, spacing=4
                                 #### HERE IS WERE WE ADD THE DATAFRAME ITEMS
                        )
                    )
                ]
            )
            ])
            ),

        ft.Container(content=
            ft.Column(
                controls=[
                    ft.Container(ft.Text('Remove Rows on Red', size=22, color=ft.colors.RED)),
                    ft.Container(ft.ElevatedButton('Click', on_click=removeRows)),
                    
                ]
            )
        )
    ])
    for entry in createColumns():
        entries_plane.current.controls.append(entry)
    page.add(widget)

ft.app(target=main)


