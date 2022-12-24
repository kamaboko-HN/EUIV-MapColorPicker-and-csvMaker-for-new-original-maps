import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import pyperclip as PyIP
import time

import blue
import land

class Application(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.pack()

        #master.geometry("300x300")
        master.title("MCPADM")
        
        MasterFrame = tk.Frame(self)
        
        menubar = tk.Menu(self)
        master.config(menu=menubar)
        
        mcpadm = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='M', menu=mcpadm)
        #mcpadm.add_command(label='仕様')
        mcpadm.add_command(label='Quit', command=self.Exit)
        
        definition_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Def', menu=definition_menu)
        definition_menu.add_command(label='open', command=self.LoadFromMakedDefinition)
        definition_menu.add_command(label='save', command=self.SaveToDefinition)
        
        MasterFrame.pack(anchor=tk.W)
        
        AFrame = tk.LabelFrame(MasterFrame, text="color", width=300, height=525)
        
        self.ColorLabel = tk.Label(AFrame, text="COLOR", height=5, width=30)
        HexFrame = tk.Frame(AFrame, height=1, width=300)
        self.HexText = tk.Text(HexFrame, height=1, width=10)
        self.check = tk.BooleanVar()
        self.check.set(True)
        self.HexAutoCopy = tk.Checkbutton(HexFrame, text="AutoCopy", variable=self.check)
        HexCopyButton = tk.Button(HexFrame, text="Copy", height=1, command=self.HexCopy)
        WaterProvinceButton = tk.Button(AFrame, text="Sea", height=3, width=30, command=self.PickSeaColor)
        LandProvincebutton = tk.Button(AFrame, text="Land", height=3, width=30, command=self.PickLandColor)
        
        UsedColorFrame = tk.LabelFrame(AFrame, text="UsedColor", height=100, width=300)
        self.SeaUsed = tk.Label(UsedColorFrame, text="UsedSeaColors:0")
        self.LandUsed = tk.Label(UsedColorFrame, text="UsedLandColors:0")
        self.TotalUsed = tk.Label(UsedColorFrame, text="TotalUsedColors:0")
        
        self.ERRORLabel = tk.Label(AFrame, fg="red")
        
        AFrame.pack(side = tk.LEFT, anchor=tk.N)
        AFrame.pack_propagate(0)
        self.ColorLabel.pack()
        
        HexFrame.pack()
        self.HexText.pack(side=tk.LEFT)
        self.HexAutoCopy.pack(side=tk.LEFT)
        HexCopyButton.pack(side=tk.LEFT)
        
        WaterProvinceButton.pack()
        LandProvincebutton.pack()
        UsedColorFrame.pack()
        UsedColorFrame.pack_propagate(0)
        self.SeaUsed.pack()
        self.LandUsed.pack()
        self.TotalUsed.pack()
        
        self.ERRORLabel.pack(side=tk.BOTTOM)
        
        definList = []
        self.definVar = tk.StringVar(value=definList)
        
        BFrame = tk.LabelFrame(MasterFrame, text="defintion", height= 600)
        
        self.SelectLabel = tk.Label(BFrame, height=1, width=45, text="Prov No. : On R click, hex copy to clipboard")
        self.SelectLabel.bind("<Button-3>", self.SelectHexCopy)
        self.definList = tk.Listbox(BFrame, height=30, width=50, listvariable=self.definVar)
        self.definList.bind('<<ListboxSelect>>', self.SetSelectHex)
        self.Yscrollbar = tk.Scrollbar(BFrame, orient=tk.VERTICAL, command=self.definList.yview)
        self.definList["yscrollcommand"] = self.Yscrollbar.set
        
        #BFrame.pack_propagate(0)
        BFrame.pack(side = tk.LEFT, anchor=tk.N)
        
        self.SelectLabel.pack(side=tk.TOP)
        
        self.definList.pack(side=tk.LEFT, fill=tk.Y)
        self.Yscrollbar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.SeaUsed_var = 0
        self.LandUsed_var = 0
        self.TotalUsed_var = 0
        
    def SelectHexCopy(self, *event):
        Hex = self.SelectLabel.cget("background")
        PyIP.copy(Hex)
        self.ERRORLabel.config(text="Copy to clipboard : " + Hex)
        
        print(Hex)
        
    def HexCopy(self):
        PyIP.copy(str(self.HexText.get("1.0", "end")))
        self.ERRORLabel.config(text="Copy to clipboard : " + str(self.HexText.get("1.0", "end")))
        
    def PickSeaColor(self):
        rgb = blue.pickBlue()
        if rgb == None:
            self.ERRORLabel.config(text="This type province colors were full used!!")
        else:
            self.ERRORLabel.config(text="")
            self.SetColorHex(rgb)
            self.SeaUsed_var += 1
            self.TotalUsed_var += 1
            self.SeaUsed.config(text="UsedSeaColors:"+str(self.SeaUsed_var))
            self.TotalUsed.config(text="TotalUsedColors:"+str(self.TotalUsed_var))
            self.SetList(rgb, "Sea")
            if self.check.get() == True:
                self.HexCopy()
    
    def PickLandColor(self):
        rgb = land.pickLand()
        if rgb == None:
            self.ERRORLabel.config(text="This type province colors were full used!!")
        else:
            self.ERRORLabel.config(text="")
            self.SetColorHex(rgb)
            self.LandUsed_var += 1
            self.TotalUsed_var += 1
            self.LandUsed.config(text="UsedLandColors:"+str(self.LandUsed_var))
            self.TotalUsed.config(text="TotalUsedColors:"+str(self.TotalUsed_var))
            self.SetList(rgb, "Land")
            if self.check.get() == True:
                self.HexCopy()
        
    def SetColorHex(self, RGB):
        Hex = self.RGBtoHex(RGB)
        print(Hex)
        self.ColorLabel.config(bg="#" + Hex)
        self.HexText.configure(state='normal')
        self.HexText.delete("1.0","end")
        self.HexText.insert("1.0", Hex)
        self.HexText.configure(state='disabled')
        self.update()
        
    def SetSelectHex(self, *event):
        ind = self.definList.curselection()
        var = self.definList.get(ind)
        var_list = var.split(";")
        prov_num = var_list[0]
        RGB = [int(var_list[1]), int(var_list[2]), int(var_list[3])]
        Hex = self.RGBtoHex(RGB)
        
        sorted_RGB = sorted(RGB)
        total = sorted_RGB[0] + sorted_RGB[2]
        reverse_RGB = [total-RGB[0], total-RGB[1], total-RGB[2]]
        
        self.SelectLabel.config(fg="#"+ self.RGBtoHex(reverse_RGB))
        self.SelectLabel.config(bg="#"+Hex)
        self.SelectLabel.config(text="Prov No." + prov_num + ": On R click, hex copy to clipboard")
        
    def RGBtoHex(self, RGB):
        Hex = [str(hex(RGB[0])).replace('0x', ''), str(hex(RGB[1])).replace('0x', ''), str(hex(RGB[2])).replace('0x', '')]
        print(Hex)
        for cou in range(0,3):
            print(cou)
            if len(Hex[cou]) == 1:
                Hex[cou] = "0" + Hex[cou]
        Hex = Hex[0]+Hex[1]+Hex[2]
        
        return Hex
        
    def SetList(self, RGB, type):
        #1;128;34;64;Stockholm;x
        ProvinceDef = str(self.TotalUsed_var) + ";" + str(RGB[0]) + ";" + str(RGB[1]) + ";" + str(RGB[2]) + ";" + "No." + str(self.TotalUsed_var) + ";" + type
        
        self.definList.insert(tk.END, ProvinceDef)
        
    def Exit(self):
        self.quit()
        
    def SaveToDefinition(self):
        defins = ["province;red;green;blue;x;x"]
        VarCou = self.definList.size()
        print(VarCou)
        for cou in range(0, VarCou):
            defins.append(self.definList.get(cou))
        print(defins)
        typ = [('definition','*.csv')] 
        dir = '../'
        path = fd.asksaveasfilename(filetypes = typ, initialdir = dir, defaultextension="csv")
        print(path)
        
        with open(path, mode='w') as file:
            file.write('\n'.join(defins))
            
    def LoadFromMakedDefinition(self):
        typ = [('definition','*.csv')] 
        dir = '../'
        path = fd.askopenfilename(filetypes = typ, initialdir = dir)
        print(path)
        
        with open(path, mode='r') as file:
            defins = [s.strip() for s in file.readlines()]
            
        defins.pop(0)
        
        defins_2 = defins.copy()
        
        check_made = defins_2[0].split(";")
        if self.definList.size() > 0:
            ans = mb.askokcancel("確認 : Check", "生成済みのdefintionsリストがあります。上書きしますか？\nThere is a list of defintions already generated. Do you want to overwrite it?")
        elif self.definList.size() == 0:
            ans = True
            if ans == True:
                if check_made[-1] == "Sea" or "Land":
                    SL_count = [0, 0]
                    for line in defins_2:
                        line_split = line.split(";")
                        if line_split[-1] == "Sea":
                            SL_count[0] += 1
                        elif line_split[-1] == "Land":
                            SL_count[1] += 1
                    
                    self.definList.delete(0, tk.END)
                    blue.resetSea()
                    land.resetLand()
                    self.SeaUsed_var = 0
                    self.LandUsed_var = 0
                    self.TotalUsed_var = 0
                    
                    if SL_count[0] > 0:
                        for cou in range(SL_count[0]):
                            blue.pickBlue()
                            self.SeaUsed_var += 1
                            self.TotalUsed_var += 1
                    
                    if SL_count[1] > 0:
                        for cou in range(SL_count[1]):
                            land.pickLand()
                            self.LandUsed_var += 1
                            self.TotalUsed_var += 1
                            
                    self.SeaUsed.config(text="UsedSeaColors:"+str(self.SeaUsed_var))
                    self.LandUsed.config(text="UsedLandColors:"+str(self.LandUsed_var))
                    self.TotalUsed.config(text="TotalUsedColors:"+str(self.TotalUsed_var))
                    
                    for line in defins:
                        self.definList.insert(tk.END, line)
                        
                    
                    
                else:
                    mb.showerror(" エラー : ERROR", "このファイルは当ソフトで作られたものではない可能性があるため開くことができません。\nThis file cannot be opened because it may not have been created by our software.")
        
        
        
def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()
    
    
    
#91 255 246
#29 0 255