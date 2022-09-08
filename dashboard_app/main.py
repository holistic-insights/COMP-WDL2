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
from optimization import OPT

class GUI:
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
        
        tk.Label(self.master, text='Factors for decision support', font=('arial', 16, 'bold'), bg='white', fg='black').place(relx=0.5, rely=0.20, anchor='center')
        
        self.features_label = {'Dist. to attraction': 'dist_nearest_attraction', 'Dist. to cycle path': 'dist_nearest_cycle_path', 'Dist. to school': 'dist_nearest_school', 'Dist. to bus': 'dist_nearest_bus', 'Dist. to metro': 'dist_nearest_metro', 'Validations metro': 'validations_metro', 'Validations bus': 'validations_bus', 'Frequency metro': 'n_metro_trips', 'Frequency bus': 'n_bus_trips', 'Diversity metro': 'n_metro_routes', 'Diversity bus': 'n_bus_routes', 'Num metro stops': 'n_metro', 'Num bus stops': 'n_bus'}
        
        self.features_sliders = dict()
        for i, feat in enumerate(self.features_label.keys()):
            
            tk.Label(self.master, text=feat, font=('arial', 9), bg='white', fg='black').place(relx=0.05 + i*0.075, rely=0.26, anchor='center')
            sli = tk.Scale(self.master, from_=20, to=-20, orient='vertical', bg='white')
            sli.place(relx=0.05 + i*0.075, rely=0.33, anchor='center')
            
            self.features_sliders[feat] = sli

        
        self.img_path = 'default.png'
        img = Image.open(self.img_path)
        reduction = 2000 / img.size[0]
        score_img = img.resize((int(img.size[0]*reduction), int(img.size[1]*reduction)), Image.ANTIALIAS)
        score_img = ImageTk.PhotoImage(score_img)
        self.panel = tk.Label(self.master, image=score_img, bg='white')
        self.panel.image= score_img
        self.panel.place(relx = 0.5, rely = 0.65, anchor = "center")
        

        self.streambtn = tk.Button(self.master, text='Compute final score per zone', font=('arial', 14, 'normal'), command=self.get_score)
        self.streambtn.place(relx = 0.38, rely = 0.94, anchor = "center")
        
        self.cleanbtn = tk.Button(self.master, text='Clear', font=('arial', 14, 'normal'), command=self.clear)
        self.cleanbtn.place(relx = 0.5, rely = 0.94, anchor = "center")
        
        self.optbtn = tk.Button(self.master, text='Go to optimization', font=('arial', 14, 'normal'), command=self.optimization)
        self.optbtn.place(relx = 0.59, rely = 0.94, anchor = "center")   
        
    def optimization(self):
        
        if self.img_path == 'default.png':
            messagebox.showerror('Error', 'Please compute the final score before doing the optimization.')
        else:
            root2 = tk.Toplevel()
            OPT(root2)
            root2.mainloop()
    
    def clear(self):
        
        for slide in self.features_sliders.values():
            slide.set(0)
            
        self.panel.destroy()
        
        self.img_path = 'default.png'
        
        img = Image.open(self.img_path)
        reduction = 2000 / img.size[0]
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
        
        time.sleep(2)
        
        '''
        coefs = []
        feats = []
        
        for key in self.features_sliders:
            coefs.append(self.features_sliders[key].get())
            feats.append(self.features_label[key])
            
        self.coefs = pd.DataFrame({'feature': feats, 'coef': coefs})
        
        grid = pd.read_csv('aux_grid.csv').rename(columns={'Unnamed: 0': 'zone'})
        meta = grid[['zone', 'geometry']]
        X = grid.drop(columns=['zone', 'geometry']).to_numpy()
        self.features = grid.drop(columns=['zone', 'geometry']).columns.tolist()
        
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        grid = pd.DataFrame(X, columns=self.features)
        grid = pd.concat([meta, grid], axis=1)
        
        grid['score'] = grid.apply(self.compute_score, axis=1)
        
        grid['geometry'] = gpd.GeoSeries.from_wkt(grid['geometry'])
        grid = gpd.GeoDataFrame(grid, geometry='geometry')
        
        fig, ax = plt.subplots(1, 1, figsize=(20, 5))
        grid.plot(column='score', ax=ax, legend=True)
        plt.axis('off')
        fig.savefig('scores.png')
        plt.close('all')
        '''
        
        self.panel.destroy()
        
        if self.features_sliders['Dist. to cycle path'].get() == -20:
            self.img_path = 'scores2.png'
        else:
            self.img_path = 'scores1.png'
        
        #self.img_path = 'scores.png'
        img = Image.open(self.img_path)
        reduction = 2000 / img.size[0]
        score_img = img.resize((int(img.size[0]*reduction), int(img.size[1]*reduction)), Image.ANTIALIAS)
        score_img = ImageTk.PhotoImage(score_img)
        self.panel = tk.Label(self.master, image=score_img, bg='white')
        self.panel.image= score_img
        self.panel.place(relx = 0.5, rely = 0.65, anchor = "center")

        self.master.update_idletasks()
        
        
def main():

    root = tk.Tk()
    GUI(root)
    root.mainloop()

if __name__ == '__main__':
    
    main()