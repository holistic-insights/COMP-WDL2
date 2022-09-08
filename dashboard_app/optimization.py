# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:23:27 2021

@author: João Afonso
"""


import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from PIL import ImageTk, Image
from sklearn.preprocessing import StandardScaler
import time
from tkinter import messagebox

class OPT:
    def __init__(self, master):

        # Initialize master widget
        self.master = master 
        self.master.geometry('1500x800')
        self.master.title("YODAS")
        self.master.configure(background='white')
        self.master.state('zoomed')

        try:
            self.master.iconbitmap('yodas.ico')
        except:
            pass

        # Create top frame for the probe input
        self.probe_frame = tk.Frame(self.master, bg='#3C78D8')
        tk.Label(self.probe_frame, text='Soft-mobility drop-off zones optimization', font=('arial', 20, 'bold'), bg='#3C78D8', fg='white').pack(side='left', anchor='c', pady=50, expand=True)
        self.probe_frame.pack(side='top', fill='x', expand=False)
        
        tk.Label(self.master, text='Restrictions for the optimization algorithm', font=('arial', 16, 'bold'), bg='white', fg='black').place(relx=0.5, rely=0.20, anchor='center')
        
        self.features_label = {'Radius of no drop-offs': 15, 'Minimum drop-offs per parish': 20}
        
        self.features_sliders = dict()
        for i, feat in enumerate(self.features_label.keys()):
            
            tk.Label(self.master, text=feat, font=('arial', 11), bg='white', fg='black').place(relx=0.42 + i*0.15, rely=0.26, anchor='center')
            sli = tk.Scale(self.master, from_=self.features_label[feat], to=0, orient='vertical', bg='white')
            sli.place(relx=0.42 + i*0.15, rely=0.33, anchor='center')
            
            self.features_sliders[feat] = sli

        img = Image.open('default_opt.png')
        reduction = 1400 / img.size[0]
        score_img = img.resize((int(img.size[0]*reduction), int(img.size[1]*reduction)), Image.ANTIALIAS)
        score_img = ImageTk.PhotoImage(score_img)
        self.panel = tk.Label(self.master, image=score_img, bg='white')
        self.panel.image= score_img
        self.panel.place(relx = 0.5, rely = 0.65, anchor = "center")
        

        self.streambtn = tk.Button(self.master, text='Run optimization algorithm', font=('arial', 14, 'normal'), command=self.get_score)
        self.streambtn.place(relx = 0.44, rely = 0.94, anchor = "center")
        
        self.cleanbtn = tk.Button(self.master, text='Clear', font=('arial', 14, 'normal'), command=self.clear)
        self.cleanbtn.place(relx = 0.56, rely = 0.94, anchor = "center")
        
    
    def clear(self):
        
        for slide in self.features_sliders.values():
            slide.set(0)
            
        self.panel.destroy()
        
        self.img_path = 'default_opt.png'
        
        img = Image.open(self.img_path)
        reduction = 1400 / img.size[0]
        score_img = img.resize((int(img.size[0]*reduction), int(img.size[1]*reduction)), Image.ANTIALIAS)
        score_img = ImageTk.PhotoImage(score_img)
        self.panel = tk.Label(self.master, image=score_img, bg='white')
        self.panel.image= score_img
        self.panel.place(relx = 0.5, rely = 0.65, anchor = "center")
        
        self.master.update_idletasks()
    
    def compute_score(self, row):
        
        score = 0
        
        for col in self.features:
            coef_ = self.coefs.loc[self.coefs['feature'] == col]['coef'].item()
            score += (row[col] * coef_)
            
        return score    
    
    def get_score(self):
        
        time.sleep(4)
        
        self.panel.destroy()
        
        if self.features_sliders['Minimum drop-offs per parish'].get() == 0:
            self.img_path = 'sol1.png'
        else:
            self.img_path = 'sol2.png'
        
        #self.img_path = 'scores.png'
        img = Image.open(self.img_path)
        reduction = 1400 / img.size[0]
        score_img = img.resize((int(img.size[0]*reduction), int(img.size[1]*reduction)), Image.ANTIALIAS)
        score_img = ImageTk.PhotoImage(score_img)
        self.panel = tk.Label(self.master, image=score_img, bg='white')
        self.panel.image= score_img
        self.panel.place(relx = 0.5, rely = 0.65, anchor = "center")

        self.master.update_idletasks()
        
def main():

    root = tk.Tk()
    OPT(root)
    root.mainloop()

if __name__ == '__main__':
    
    main()