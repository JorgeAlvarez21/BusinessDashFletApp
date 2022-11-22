import flet
import os
from flet import (Stack, Radio, TextField, Image, Divider, ListTile, RadioGroup, TextButton, Icon, Card, theme, border_radius, border, UserControl, View, ElevatedButton, AppBar, FilledTonalButton, padding,Column, Row, alignment, Container, margin, colors, icons, IconButton, FloatingActionButton, Page, TextStyle, ButtonStyle, Text, dropdown, Dropdown, CircleAvatar, theme )
from flet.border import BorderSide
from flet.buttons import RoundedRectangleBorder
import pandas as pd
#Custom modules import
from sales_data_funcs import CleanedData
import app_controls as AppControls


class SelectedRowChange:
    def __init__(self):
        self.all_selects = {}
        
    def InsertRows(self, order_data):
        row_l = len(order_data)
        if not isinstance(order_data, dict):
            raise TypeError('data passed must be a dict')
        else:
            if len(row_l) == 1:
                self.all_selects[order_data.get('Order ID')] = order_data
            elif len(row_l) >1:
                for k in order_data.keys():
                    self.all_selects[order_data.get('Order ID')] = order_data
            else:
                raise ValueError('Selection invalid, must have at least 1 selected row')
    
    def __str__(self):
        return(self.all_selects)


