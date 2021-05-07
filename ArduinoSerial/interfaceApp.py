# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:48:43 2021

@author: Justas
"""

'''-------------------------------------------------------------------------------------------------------
------------------------------------------------LIBRARIES AND CONSTANTS-----------------------------------
-------------------------------------------------------------------------------------------------------'''

import tkinter as tk
from  tkinter import font as tkFont
import numpy as np
import sys

# Arrow strings
up = '\N{UPWARDS BLACK ARROW}'
down = '\N{DOWNWARDS BLACK ARROW}'
right = '\N{RIGHTWARDS BLACK ARROW}'
left = '\N{LEFTWARDS BLACK ARROW}'

# Filename to save data
filename = 'current'

# CONSTANTS
ROWS = 4
COLS = 4
# CH_LIST = np.arange(16).astype(str)  # a list for channel numbers - it can be modified later manually when wires are connected
CH_LIST = ['13', '12', '15', '14', '7', '6', '4', '5', '9', '8', '10', '11', '2', '3', '0', '1']  # refer to emitter scheme
'''        0    1    2    3    4    5    6    7    8    9    10    11    12    13    14    15'''


'''-------------------------------------------------------------------------------------------------------
-----------------------------------------------------CLASS------------------------------------------------
-------------------------------------------------------------------------------------------------------'''


class Interface():
    
    def __init__(self, master):
        self.master = master  # initialising window
        
        # Matrices for storing button objects needed for update methods
        self.phase_btn_matrix = []
        self.pixel_btn_matrix = []
        
        self.voltage_matrix = []  # entry objects matrix to enter voltage
        self.enter_btn_matrix = []  # matrix of 'Enter' buttons (they update entries value and checks if entered value is valid)
        
        # Matrices for reading data
        self.pixel_click = np.zeros((ROWS,COLS), dtype=bool)  # matrix to determine which pixel is on or off
        self.phase_click = np.zeros((ROWS,COLS), dtype=bool)  # matrix to determine which phase button is on or off
        
        # Creating phase and pixel buttons
        self.insertPhaseBtns()
        self.insertPixels()
        
        # Creating other interface elements
        self.insertEntryLabels()
        self.insertExportBtn()
        self.insertSetAllBtns()
        self.insertVoltageAllEntry()
        
        
    def insertPhaseBtns(self):
        # Inserting phase control buttons
        ROWS_PHS = [0, 2, 4, 6]  # additional list to position buttons for easier layout
        
        for col in range(COLS):
            phase_row_matrix = []
            
            for ind_row, row in enumerate(ROWS_PHS):
                # Phase button
                phase_btn = tk.Button(self.master,
                                      text='+\u03C0',
                                      bg='yellow',
                                      height=1,
                                      width=2,
                                      command=lambda x=ind_row, y=col: self.updatePhaseBtns(x, y)
                                      )
                phase_btn['font'] = font_phase
                phase_btn.grid(row=row, column=col, sticky="n", padx=0, pady=25)
                phase_row_matrix.append(phase_btn)
            
            self.phase_btn_matrix.append(phase_row_matrix)
    
    def insertPixels(self):
        # Inserting pixel buttons
        ROWS_PIX = [1, 3, 5, 7]  # additional list to position buttons for easier layout
        
        for col in range(COLS):
            pixel_row_matrix = []
            
            for ind_row, row in enumerate(ROWS_PIX):
                # Pixel button
                btn = tk.Button(self.master,
                                text=pixelPolArrow(ind_row, col), #'(%d, %d)' % (col, row),
                                bg='red',
                                height=1,
                                width=3,
                                command=lambda x=ind_row, y=col: self.updatePixels(x, y)
                                )
                btn['font'] = font_pix
                btn.grid(row=row, column=col, padx=10, pady=10)
                pixel_row_matrix.append(btn)
                
            self.pixel_btn_matrix.append(pixel_row_matrix)
    
    def insertEntryLabels(self):
        ROWS_PHS = [0, 2, 4, 6]
        
        for col in range(COLS):
            voltage_row_matrix = []
            enter_btn_row_matrix = []
            
            for ind_row, row in enumerate(ROWS_PHS):
                
                # Voltage entry widget
                voltage = tk.Entry(self.master,
                                 width=5,
                                 )
                voltage.grid(row=row, column=col, sticky="s", padx=20, pady=0)
                voltage.insert(0, '0')  # default value is 0
                
                
                ch1, ch2 = assignLabel(ind_row, col)
                # Inserting label
                label = tk.Label(self.master,
                                 text=ch1 + '&' + ch2 + ':',
                                )
                label.grid(row=row, column=col, sticky="sw")
                
                # Enter button
                enter = tk.Button(self.master,
                                  text='Enter',
                                   command=lambda x=ind_row, y=col:self.updateVoltage(x, y),
                                 )
                enter.grid(row=row, column=col, sticky="se")
                
                # Append entry object and enter button to row matrix
                voltage_row_matrix.append(voltage)
                enter_btn_row_matrix.append(enter)
            
            # Append row matrixes to 
            self.voltage_matrix.append(voltage_row_matrix)
            self.enter_btn_matrix.append(enter_btn_row_matrix)
    
    def updatePixels(self, row, col):
        row_add, col_add = additionalIndices(row, col)  # add additional indices to update
        
        # Updates color of pixels
        if self.pixel_click[row][col] == True:
            # Updates initially clicked pixel
            self.pixel_btn_matrix[col][row].config(bg = 'red')
            self.pixel_click[row][col] = False
            
            # Updates additional pixel
            self.pixel_btn_matrix[col_add][row_add].config(bg = 'red')
            self.pixel_click[row_add][col_add] = False

        else:
            # Updates initially clicked pixel
            self.pixel_btn_matrix[col][row].config(bg = 'green')
            self.pixel_click[row][col] = True
            
            # Updates additional pixel
            self.pixel_btn_matrix[col_add][row_add].config(bg = 'green')
            self.pixel_click[row_add][col_add] = True
    
    def updatePhaseBtns(self, row, col):
        row_add, col_add = additionalIndices(row, col)# add additional indices to update
        
        if self.phase_click[row][col] == True:
            # Updates color of initially clicked and additional phase button
            self.phase_btn_matrix[col][row].config(bg = 'yellow')
            self.phase_click[row][col] = False
            
            self.phase_btn_matrix[col_add][row_add].config(bg = 'yellow')
            self.phase_click[row_add][col_add] = False
        else:
            # Updates initially clicked phase and additional phase button
            self.phase_btn_matrix[col][row].config(bg = 'blue')
            self.phase_click[row][col] = True
            
            self.phase_btn_matrix[col_add][row_add].config(bg = 'blue')
            self.phase_click[row_add][col_add] = True
            
            
        # Updates arrows direction of corresponding pixels
        if self.phase_click[row][col] == False:
            self.pixel_btn_matrix[col][row].config(text=pixelPolArrow(row, col))
            self.pixel_btn_matrix[col_add][row_add].config(text=pixelPolArrow(row_add, col_add))
        else:
            self.pixel_btn_matrix[col][row].config(text=pixelPolArrowINV(row, col))
            self.pixel_btn_matrix[col_add][row_add].config(text=pixelPolArrowINV(row_add, col_add))
    
    def updateVoltage(self, row, col):
        voltage_value = self.voltage_matrix[col][row].get()  # gets voltage value from pixel where enter button was pressed
        
        row_add, col_add = additionalIndices(row, col)  # add additional indices to update
        
        # Handling errors
        try:
            float(voltage_value)  # convert entered value to float
        
            if float(voltage_value) >= 0 and float(voltage_value) <=10:  # if  voltage value entered is between 0 and 10 V
                # Sets voltage of additional pixel
                self.voltage_matrix[col_add][row_add].delete(0, last=300)  # deletes any value which existed before
                self.voltage_matrix[col_add][row_add].insert(0, voltage_value)  # puts a new value on additional pixel
            else:  # if entered voltage value is too high or too low
                self.voltage_matrix[col][row].delete(0, last=300)  # deletes value of initial entry
                self.voltage_matrix[col_add][row_add].delete(0, last=300)  # deletes value of additional entry
                
                self.voltage_matrix[col][row].insert(0, '0')  # inserts 0 instead of bad value
                self.voltage_matrix[col_add][row_add].insert(0, '0')  # inserts 0 instead of bad value
                print('Inappropriate value.')
            
        except ValueError:
            self.voltage_matrix[col][row].delete(0, last=300)  # deletes value of initial entry
            self.voltage_matrix[col_add][row_add].delete(0, last=300)  # deletes value of additional entry
            
            self.voltage_matrix[col][row].insert(0, '0')  # inserts 0 instead of a bad value
            self.voltage_matrix[col_add][row_add].insert(0, '0')  # inserts 0 instead of a bad value
            
            print('Use numbers.')
    
    def insertSetAllBtns(self):
        # turnOn button turns on all buttons
        self.allTurnedOn = False  # initially this button is off (it is assumed all pixels are off too)
        
        turnOn = tk.Button(self.master,
                          text='Turn on all btns',
                          height=2,
                          width=12,
                          bg='red',
                          )
        turnOn['font'] = font_phase
        turnOn.grid(row=ROWS*2-2, column=COLS+1, padx=10, pady=10)
        
        turnOn.bind("<Button-1>", self.turnOnAll)
    
    def turnOnAll(self, event):  # turns on/off all pixels
        # Checks state of all buttons and if they are all of (on)
        allTrue = np.all(self.pixel_click == True)
        allFalse = np.all(self.pixel_click == False)
        
        if allTrue:
            self.allTurnedOn = True
        if allFalse:
            self.allTurnedOn = False
    
    
        if self.allTurnedOn == False:
            self.pixel_click = np.ones((ROWS,COLS), dtype=bool)
            self.allTurnedOn = True
            
        else:  # if self.allTurnedOn == True
            self.pixel_click = np.zeros((ROWS,COLS), dtype=bool)
            self.allTurnedOn = False
        
        # Update color of pixels
        for col in range(COLS):
            for row in range(ROWS):
                self.updatePixels(row, col)
    
    def insertExportBtn(self):
        # 'Export' button to export configuration of buttons to file
        exportBtn = tk.Button(self.master,
                              text='Export',
                              height=1,
                              width=5,
                              bg='white',
                              )
        exportBtn['font'] = font_exp
        exportBtn.grid(row=ROWS*2-1, column=COLS+1, padx=10, pady=10)
        
        exportBtn.bind("<Button-1>", self.exportFunction)  # executes exportFunction when clicked
    
    def exportFunction(self, event):
        # Export commands to text file
        orig_stdout = sys.stdout
        f = open(filename, 'w')
        sys.stdout = f
        
        self.translate()  # translate matrices to serial commands
        
        sys.stdout = orig_stdout
        f.close()
        
        print('Data saved in ', filename, '.', sep='')
    
    def translate(self):  # translate matrices to arduino serial commands
    
        ROWS_TR = [0, 2]  # only 0th and 2nd rows are used for commands TRanslation
        
        ch_ind1, ch_ind2 = 0, 1
        
        for i, row in enumerate(ROWS_TR):
            
            for col in range(COLS):
                
                if self.pixel_click[row][col] == True:
                    
                    # Enable channels
                    print('en', CH_LIST[ch_ind1], sep='')
                    print('en', CH_LIST[ch_ind2], sep='')
                    
                    if self.phase_click[row][col] == False:  # no phase correction is required
                    
                        # Setup DACs
                        print('dac', CH_LIST[ch_ind1], ' ', '0V', sep='')
                        print('dac', CH_LIST[ch_ind2], ' ', str(self.voltage_matrix[col][row].get()), 'V', sep='')
                        
                    else:  # if phase inversion is required
                    
                        # Setup DACs in reverse order
                        print('dac', CH_LIST[ch_ind1], ' ', str(self.voltage_matrix[col][row].get()), 'V', sep='')
                        print('dac', CH_LIST[ch_ind2], ' ', '0V', sep='')
                
                # Increase channel indices by 2 to move on to the next pair of pixels, because a pair of pixels requires 2 channels
                ch_ind1 += 2
                ch_ind2 += 2
    
    def insertVoltageAllEntry(self):
        # Inserts an entry which allows to set voltage of every pixel on the grid to specified value
        ROW_V_ALL = 5  # number of row where elements for entry are generated
        
        self.entryVoltageAll = tk.Entry(self.master,
                              width=10,
                              )
        self.entryVoltageAll.grid(row=ROW_V_ALL, column=COLS, columnspan=2, padx=0, pady=20, sticky="n")
        
        labelAll = tk.Label(self.master,
                         text='Set voltage to all pixels',
                         )
        labelAll.grid(row=ROW_V_ALL, column=COLS+1, sticky="n")
        
        voltageAllBtn = tk.Button(self.master,
                                  text='Enter all',
                                  height=1,
                                  width=7,
                                  )
        voltageAllBtn.grid(row=ROW_V_ALL, column=COLS+1, padx=0, pady=50, sticky="n")
        voltageAllBtn.bind("<Button-1>", self.setVoltageAllFunction)
    
    def setVoltageAllFunction(self, event):
        voltage_value = self.entryVoltageAll.get()  # get value from entry
        
        # Handling errors
        try:
            float(voltage_value)  # convert entered value to float
        
            if float(voltage_value) >= 0 and float(voltage_value) <=10:  # if  voltage value entered is between 0 and 10 V
                
            # Set voltage to 'voltage_value' of all pixels
                for col in range(COLS):
                    for row in range (ROWS):
                        self.voltage_matrix[row][col].delete(0, last=300)
                        self.voltage_matrix[row][col].insert(0, voltage_value)
            
            else:  # if entered voltage value is too high or too low
            
                self.entryVoltageAll.delete(0, last=300)  # deletes value of initial entry
                self.entryVoltageAll.insert(0, '0')  # inserts 0 instead of bad value
                
                # Set voltage to 0 of every pixel
                for col in range(COLS):
                    for row in range (ROWS):
                        self.voltage_matrix[row][col].delete(0, last=300)
                        self.voltage_matrix[row][col].insert(0, '0')
                
                print('Inappropriate value.')
                
        except ValueError:  # if entered value cannot be converted to a number
        
            self.entryVoltageAll.delete(0, last=300)  # deletes value of initial entry
            self.entryVoltageAll.insert(0, '0')  # inserts 0 instead of a bad value
            
            # Set voltage to 0 of every pixel
            for col in range(COLS):
                for row in range (ROWS):
                    self.voltage_matrix[row][col].delete(0, last=300)
                    self.voltage_matrix[row][col].insert(0, '0')
            
            print('Use numbers.')
'''-------------------------------------------------------------------------------------------------------
---------------------------------------------------FUNCTIONS----------------------------------------------
-------------------------------------------------------------------------------------------------------'''

# Finds additional button which is connected to initially clicked one
def additionalIndices(row, col):  # row, col - initial, row2, col2 - additional indices
    if col == 0 or col == 2:
        if row == 0 or row == 2:
            row2 = row + 1
            col2 = col + 1
        else:
            row2 = row - 1
            col2 = col + 1
    
    else:  # if col == 1 or col == 3
        if row == 0 or row == 2:
            row2 = row + 1
            col2 = col - 1
        else:
            row2 = row - 1
            col2 = col - 1
            
    return row2, col2

# Functions responsible for assigning arrows (strings) with correct pixels
def pixelPolArrow(row, col):  # when phase button is not pressed
    if (row+col) % 2 == 0:
        pixel_text = right
    else:
        pixel_text = up
    return pixel_text
def pixelPolArrowINV(row, col):  # when phase button is pressed
    if (row+col) % 2 == 0:
        pixel_text = left
    else:
        pixel_text = down
    return pixel_text

def assignLabel(row, col):  # assigns label with correct channels (next to pixel)
    chan1, chan2 = '', ''
    
    # Assigning channel number shown by each label
    if (col==0 and row==0) or (col==1 and row==1):
        chan1 = CH_LIST[0]
        chan2= CH_LIST[1]
    elif (col==1 and row==0) or (col==0 and row==1):
        chan1 = CH_LIST[2]
        chan2= CH_LIST[3]
    elif (col==2 and row==0) or (col==3 and row==1):
        chan1 = CH_LIST[4]
        chan2= CH_LIST[5]
    elif (col==3 and row==0) or (col==2 and row==1):
        chan1 = CH_LIST[6]
        chan2= CH_LIST[7]
    elif (col==0 and row==2) or (col==1 and row==3):
        chan1 = CH_LIST[8]
        chan2= CH_LIST[9]
    elif (col==1 and row==2) or (col==0 and row==3):
        chan1 = CH_LIST[10]
        chan2= CH_LIST[11]
    elif (col==2 and row==2) or (col==3 and row==3):
        chan1 = CH_LIST[12]
        chan2= CH_LIST[13]
    elif (col==3 and row==2) or (col==2 and row==3):
        chan1 = CH_LIST[14]
        chan2= CH_LIST[15]
        
    return chan1, chan2

'''-------------------------------------------------------------------------------------------------------
---------------------------------------------------MAIN---------------------------------------------------
-------------------------------------------------------------------------------------------------------'''

if __name__ == '__main__':
    
    window = tk.Tk()
    window.title('16-Pixel Emitter')
    
    # Selects font type and size for different elements
    font_pix = tk.font.Font(family='Arial', size=40)
    font_phase = tk.font.Font(family='Arial', size=10)
    font_exp = tk.font.Font(family='Arial', size=20)
    
    app = Interface(window)
    window.mainloop()
    
    print('App closed.')

'''-------------------------------------------------------------------------------------------------------
---------------------------------------------------END----------------------------------------------------
-------------------------------------------------------------------------------------------------------'''
