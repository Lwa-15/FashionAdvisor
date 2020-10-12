from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv
import numpy as np
import random
from random import randint
import cv2

################################################################################################### Layout + Title    
class DataCollection:
    def __init__(self, master):
        self.master = master
        self.master.title("Clothing Entry")
        self.master.geometry("1350x1350+0+0")
        self.master.configure(background="LightSteelBlue1")
        global Colour, Clothing, Other, Rating
        Colour = StringVar()
        Clothing = StringVar()
        Other = StringVar()
        Rating = IntVar()

################################################################################################### Function definition

        def Reset():
            Colour.set("")
            Clothing.set("")
            self.cmbClothing.current(0)
            Other.set("")
            Rating.set("")
            self.txtColour.focus()
    
        def Exit():
            Exit=messagebox.askyesno("Exit Program","Confirm that you want to exit")
            if Exit > 0:
                root.destroy()
                
        def NextWindow():
            self.Recommendation = Toplevel(self.master)
            self.application = Recommendation(self.Recommendation)

        def Validate():
            Correct = True
            if Colour.get() == "":
                messagebox.showinfo("Presence Error", "You must select a colour through either typing the colour in or capturing the colour using a camera")
                Correct = False
            if Clothing.get() == "":
                messagebox.showinfo("Presence Error", "You must select a piece of clothing")
                Correct = False
            if Rating.get() == "":
                messagebox.showinfo("Presence Error", "You must enter a clothing rating")
                Correct = False
            if Rating.get() < 0 or Rating.get() > 10:
                messagebox.showinfo("Range Error", "Rating must be more than 0 and less than 10")
                Correct = False
            
            if Correct == True:
                if Other.get() != "Other":
                    Data = [Colour.get(), Clothing.get(), Rating.get()]
                elif Other.get() == "Other":
                    Data = [Colour.get(), Other.get(), Rating.get()]
                with open(r"F:\EPQ\EPQ Artefact\User.csv", "a") as WriteData:
                    Writer = csv.writer(WriteData, delimiter=",")
                    Writer.writerow(Data)
                NextWindow(self)
                
        def EuclideanDistance(Colour, AverageRGB):
            SquaredDistance = (Colour[0] - AverageRGB[0])**2 + (Colour[1] - AverageRGB[1])**2 + (Colour[2] - AverageRGB[2])**2
            return np.sqrt(SquaredDistance)

        def ColourCapture():
            Count = 0
            TotalRed = 0
            TotalGreen = 0
            TotalBlue = 0
            PixelValues = []
            camera = cv2.VideoCapture(0)
            cv2.namedWindow("Feed")
            while True:
                _, frame = camera.read()
                cv2.rectangle(frame, (80,285), (200,165), (255,255,255), 2)
                cv2.imshow("Feed", frame)
                    
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    break
            while Count < 10:
                XCoordinate = random.randint(80, 200)
                YCoordinate = random.randint(165, 285)
                if YCoordinate == 80 or YCoordinate == 165 or XCoordinate == 80 or XCoordinate == 165:
                    XCoordinate = random.randint(80,200)
                    YCoordinate = random.randint(165,285)
                Count += 1
                PixelValue = frame[XCoordinate, YCoordinate]
                TotalRed += PixelValue[2]
                TotalGreen += PixelValue[1]
                TotalBlue += PixelValue[0]
                PixelValues.append(PixelValue)
                AverageRed = round(TotalRed / 10)
                AverageGreen = round(TotalGreen / 10)
                AverageBlue = round(TotalBlue / 10)

            AverageRGB = [AverageRed, AverageGreen, AverageBlue]
            print(AverageRGB)
                
            ColoursAndRGB = {
            "Maroon": [128,0,0],
            "Brown": [165, 42, 42],
            "Crimson": [220,20,60],
            "Red": [255,0,0],
            "Orange": [255,69,0],
            "Olive": [128,128,0],
            "Yellow": [255,255,0],
            "Dark Green": [0,100,0],
            "Forest Green": [34,139,34],
            "Grass Green": [124,252,0],
            "Green": [0,128,0],
            "Lime": [0,255,0],
            "Light Green": [0, 255, 127],
            "Teal": [0,128,128],
            "Cyan": [0,255,255],
            "Turquoise": [64, 224, 208],
            "Light Blue": [135,206,235],
            "Navy": [0,0,128],
            "Dark Blue": [0,0,139],
            "Medium Blue": [0,0,205],
            "Blue": [0,0,255],
            "Indigo": [75,0,130],
            "Dark Magenta": [139,0,139],
            "Purple": [128,0,128],
            "Magenta": [255,0,255],
            "Deep Pink": [255,20,147],
            "Pink": [255,192,203],
            "Salmon": [250,128,114],
            "Beige": [245,245,220],
            "Chocolate": [210,105,30],
            "Slate Grey": [112,128,144],
            "Black": [0,0,0],
            "Grey": [128,128,128],
            "Silver": [192,192,192],
            "White": [255,255,255],
            }

            Labels = []
            Distance = []
            for Colour in ColoursAndRGB.values():
                Distance.append(EuclideanDistance(Colour, AverageRGB))
                for Label in ColoursAndRGB.keys():
                    Labels.append(ColoursAndRGB[Label])
            Shortest = Labels[Distance.index(min(Distance))]

            for key, value in ColoursAndRGB.items():
                if value == Shortest:
                    Label = key
                    self.txtColour.insert(0, Label)
            cv2.destroyAllWindows()

        MainFrame = Frame(self.master)
        MainFrame.grid()
        MainFrame.config(background="LightSteelBlue1")
    
        FrameTitle = Frame(MainFrame, bd=10, width=1350, padx=20, relief=RIDGE)
        FrameTitle.pack(side=TOP)
        self.Title = Label(FrameTitle, font=("Courier New", 40), text="Clothing Entry", padx=2)
        self.Title.grid()

################################################################################################### Data Entry
        DataFrame = Frame(MainFrame, bd=10, width=800, height=1200, padx=20, relief=RIDGE)
        DataFrame.pack()
        DataFrame.config(background="LightSteelBlue1")

        self.lblColour = Label(DataFrame, font=("Courier New", 20), text="Colour:", padx=2)
        self.lblColour.grid(row=0, column=0, sticky=W)
        self.txtColour = Entry(DataFrame, font=("Courier New", 20), textvariable=Colour)
        self.txtColour.grid(row=0, column=1, sticky=W)
        self.btnColour = Button(DataFrame, text="Capture Colour", font=("Courier New", 15), command=ColourCapture)
        self.btnColour.grid(row=0, column=2, sticky=W)
        self.txtColour.focus()

        self.Pad1 = Label(DataFrame, font=("Courier New", 20), text="", padx=2)
        self.Pad1.grid(row=1, column=0, sticky=W)
        
        self.lblClothing = Label(DataFrame, font=("Courier New", 20), text="Clothing:", padx=2)
        self.lblClothing.grid(row=2, column=0, sticky=W)
        self.cmbClothing = ttk.Combobox(DataFrame, font=("Courier New", 20), textvariable=Clothing, state="readonly")
        self.cmbClothing["value"] = ["", "Shirt", "Jeans","Trousers","T-shirt","Jumper","Jacket","Shorts","Coat","Hat","Socks","Blazer","Tie", "Scarf", "Other"]
        self.cmbClothing.current(0)
        self.cmbClothing.grid(row=2, column=1, sticky=W)

        self.Pad2 = Label(DataFrame, font=("Courier New", 20), text="", padx=2)
        self.Pad2.grid(row=3, column=0, sticky=W)
        
        self.lblOther = Label(DataFrame, font=("Courier New", 20), text="If Other, Please Specify Clothing:", padx=2)
        self.lblOther.grid(row=4, column=0, sticky=W)
        self.txtOther = Entry(DataFrame, font=("Courier New", 20), textvariable=Other)
        self.txtOther.grid(row=4, column=1, sticky=W)

        self.Pad3 = Label(DataFrame, font=("Courier New", 20), text="", padx=2)
        self.Pad3.grid(row=5, column=0, sticky=W)
        
        self.lblRating = Label(DataFrame, font=("Courier New", 20), text="Rating (0 to 10):", padx=2)
        self.lblRating.grid(row=6, column=0, sticky=W)
        self.txtRating = Entry(DataFrame, font=("Courier New", 20), textvariable=Rating)
        self.txtRating.grid(row=6, column=1, sticky=W)

        self.lblColour.config(background="LightSteelBlue1")
        self.lblClothing.config(background="LightSteelBlue1")
        self.lblOther.config(background="LightSteelBlue1")
        self.lblRating.config(background="LightSteelBlue1")
        self.Pad1.config(background="LightSteelBlue1")
        self.Pad2.config(background="LightSteelBlue1")
        self.Pad3.config(background="LightSteelBlue1")

################################################################################################### Buttons
        
        ButtonFrame = Frame(root, bd=10, width=1350, height=50, padx=20, relief=RIDGE)
        ButtonFrame.grid(row=4,column=0)
        ButtonFrame.config(background="LightSteelBlue1")
        self.btnReset = Button(ButtonFrame, text="Reset", font=("Courier New", 20), command = Reset, width=24, bd=4)
        self.btnReset.grid(row=0, column=0)
        self.btnExit = Button(ButtonFrame, text="Exit", font=("Courier New", 20), command = Exit, width=24, bd=4)
        self.btnExit.grid(row=0, column=1)
        self.btnRecommend = Button(ButtonFrame, text="Recommend", font=("Courier New", 20), command=NextWindow, width=24, bd=4)
        self.btnRecommend.grid(row=0, column=2)

class Recommendation:
    def __init__(self, master):
        self.master = master
        self.master.title("Clothing Entry")
        self.master.geometry("1350x1350+0+0")
        self.master.configure(background="LightSteelBlue1")

        Colours = ["Maroon","Brown","Crimson","Red","Orange","Olive","Yellow","Dark Green",
        "Forest Green","Grass Green","Green","Lime","Light Green","Teal","Cyan",
        "Turquoise","Light Blue","Navy","Dark Blue","Medium Blue","Blue","Indigo",
        "Dark Magenta","Purple","Magenta","Deep Pink","Pink","Salmon","Beige","Chocolate",
        "Slate Grey","Black","Grey","Silver","White"]
        UserColour = Colour.get()

        MainFrame = Frame(self.master)
        MainFrame.grid()
        MainFrame.config(background="LightSteelBlue1")

        FrameTitle = Frame(MainFrame, bd=10, width=1350, padx=20, relief=RIDGE)
        FrameTitle.pack(side=TOP)
        self.Title = Label(FrameTitle, font=("Courier New", 40), text="Recommendaton", padx=2)
        self.Title.grid()
################################################################################################### Function definition
        def PreviousWindow():
            self.Data = Toplevel(self.master)
            self.application = DataCollection(self.Data)

        def Selection():
            if Radio.get() == 1:
                self.txtRecommendations.delete("1.0", END)
                Title = "What similar users like:\n"
                SimilarUserLike()
            elif Radio.get() == 2:
                self.txtRecommendations.delete("1.0", END)
                Title = "Complementary Colours:\n"
                self.txtRecommendations.insert(END, Title)
                self.txtRecommendations.insert(END, Complement + "\n")
            elif Radio.get() == 3:
                self.txtRecommendations.delete("1.0", END)
                Title = "Analogous Colours:\n"
                self.txtRecommendations.insert(END, Title)
                Analogous = AnalogousRecommendations(Colours, UserColour)
                self.txtRecommendations.insert(END, Analogous[0] + "\n")
                self.txtRecommendations.insert(END, Analogous[1] + "\n")
                self.txtRecommendations.insert(END, Analogous[2] + "\n")
            elif Radio.get() == 4:
                self.txtRecommendations.delete("1.0", END)
                Title = "Triad Colours:\n"
                self.txtRecommendations.insert(END, Title)
                Triad = TriadRecommendations(Colours, UserColour)
                self.txtRecommendations.insert(END, Triad[0] + "\n")
                self.txtRecommendations.insert(END, Triad[1] + "\n")
                self.txtRecommendations.insert(END, Triad[2] + "\n")

        def ReadAndRecommend():
            List1 = []
            List2 = []

            with open(r"User.csv", "r") as File:
                Reader = csv.reader(File, delimiter=",")
                next(Reader)
                for line in Reader:
                    if line:
                        if line[2] != "":
                            List1.append(int(line[2]))

            with open(r"OtherUsers.csv", "r") as Read:
                ReadUsers = csv.reader(Read, delimiter=",")
                for OthersLine in ReadUsers:
                    if OthersLine:
                        if OthersLine[2] != "":
                            List2.append(int(OthersLine[2]))

            while len(List1) != len(List2):
                if len(List1) <= len(List2):
                    List1.append(0)
                elif len(List2) < len(List1):
                    List2.append(0)

            intersection = len(list(set(List1).intersection(List2)))
            union = (len(List1) + len(List2)) - intersection
            Jaccard = float(intersection / union)

            Dot = np.dot(List1, List2)
            Magnitudes = np.linalg.norm(List1) * np.linalg.norm(List2)
            Cosine = Dot / Magnitudes

            Mean = int(sum(List2) / len(List2))
            
            if Jaccard >= 0 and Cosine < 1:
                with open("OtherUsers.csv", "r") as Read:
                    ReadUsers = csv.reader(Read, delimiter=",")
                    for OthersLine in ReadUsers:
                        if OthersLine:
                            if int(OthersLine[2]) >= Mean and OthersLine[0] != "":
                                self.txtRecommendations.insert(END, OthersLine[0] + " ")
                                self.txtRecommendations.insert(END, OthersLine[1] + "\n" )

        def SimilarUserLike():
            with open("OtherUsers.csv", "r") as Read:
                ReadUsers = csv.reader(Read, delimiter=",")
                for OthersLine in ReadUsers:
                    if OthersLine:
                        if OthersLine[0] != "":
                            self.txtRecommendations.insert(END, OthersLine[0] + " ")
                            self.txtRecommendations.insert(END, OthersLine[1] + "\n" )
                            
        def ComplementaryRecommendations(Colours, UserColour):
            Complementary = {
            "Maroon": "Grass Green",
            "Brown": "Indigo",
            "Crimson": "Dark Magenta",
            "Red": "Green",
            "Orange": "Blue",
            "Olive": "Medium Blue",
            "Yellow": "Purple",
            "Dark Green": "Salmon",
            "Forest Green": "Blue",
            "Grass Green": "Maroon",
            "Green": "Red",
            "Lime": "Black",
            "Light Green": "Salmon",
            "Teal": "Orange",
            "Cyan": "Red",
            "Turquoise": "Black",
            "Light Blue": "Olive",
            "Navy": "Silver",
            "Dark Blue": "Grey",
            "Medium Blue": "Olive",
            "Blue": "Orange",
            "Indigo": "Brown",
            "Dark Magenta": "Dark Green",
            "Purple": "Yellow",
            "Deep Pink": "Olive",
            "Pink": "Grass Green",
            "Salmon": "Dark Green",
            "Beige": "Indigo",
            "Chocolate": "Indigo",
            "Slate Grey": "Red",
            "Black": "White",
            "Grey": "Light Blue",
            "Silver": "Navy",
            "White": "Black",
            }
            Complement = ""
            for key, value in Complementary.items():
                if key == UserColour:
                    Complement = value 
            return Complement

        Complement = ComplementaryRecommendations(Colours, UserColour)
        
        def AnalogousRecommendations(Colours, UserColour):
            Index = 0
            Analogous = []
            Complete = False
            while Index < (len(Colours) -1):
                if Colours[Index] == UserColour:
                    Analogous = [Colours[Index-1], Colours[Index], Colours[Index+1]]
                    if Index - 1 < 0:
                        Lower = abs(Index - 1)
                    if Index + 1 > len(Colours)-1:
                        Upper = (Index + 1) - (len(Colours)-1)
                    Complete = True
                if Complete == True:
                    break
                else:
                    Index += 1
            return Analogous
        
        def TriadRecommendations(Colours, UserColour):
            Index = 0
            Triad = []
            Complete = False
            ColourLength = len(Colours) - 1
            TriadIndex = int(ColourLength / 3)
            while Index < ColourLength:
                if Colours[Index] == UserColour:
                    Lower = Index - TriadIndex
                    Middle = Index
                    Upper = Index + TriadIndex
                    Triad = [Colours[Lower], Colours[Middle], Colours[Upper]]
                    if Lower < 0:
                        Lower = abs(Index - TriadIndex)
                    if Index + TriadIndex > ColourLength:
                        Upper = ColourLength - Index
                    Complete = True
                if Complete == True:
                    Triad = [Colours[Lower], Colours[Index], Colours[Upper]]
                    break
                else:
                    Index += 1
            return Triad
        
                             
################################################################################################### Radio Buttons
        RadioButtonFrame = Frame(MainFrame, bd=10, width=1350, height=1350, padx=20, relief=RIDGE)
        RadioButtonFrame.pack()
        Radio = IntVar()

        self.rbSimilarUsers = Radiobutton(RadioButtonFrame, text="What similar users like", font=("Courier New", 10), variable = Radio, value = 1, command = Selection)
        self.rbSimilarUsers.grid(row=0, column=0, sticky=W)
        self.rbComplementary = Radiobutton(RadioButtonFrame, text="Complementary Colours (High Colour Impact)", font=("Courier New", 10), variable = Radio, value=2, command = Selection)
        self.rbComplementary.grid(row=1, column=0, sticky=W)
        self.rbAnalogous = Radiobutton(RadioButtonFrame, text="Analogous Colours (Well-matched and easy to the eye)", font=("Courier New", 10), variable = Radio, value=3, command = Selection)
        self.rbAnalogous.grid(row=2, column=0, sticky=W)
        self.rbTriad = Radiobutton(RadioButtonFrame, text="Triad Colours (Harmonious while providing visual stimulation)", font=("Courier New", 10), variable = Radio, value=4, command = Selection)
        self.rbTriad.grid(row=3, column=0, sticky=W)
        
################################################################################################### Text Box
        TextFrame = Frame(MainFrame, bd=10, width=80, height=20, relief=RIDGE)
        TextFrame.pack(side=RIGHT)
        self.txtRecommendations = Text(TextFrame, font=("Courier New", 12, "bold"), width=80, height=20)
        self.txtRecommendations.grid(row=0, column=0, sticky=W)
        self.txtRecommendations.insert(END, "What similar users like:" + "\n")
        ReadAndRecommend()

        ButtonFrame = Frame(MainFrame, bd=10, width=1350, height=50, relief=RIDGE)
        ButtonFrame.pack(side=LEFT)
        self.btnBack = Button(ButtonFrame, text="Back", font=("Courier New", 15), command=PreviousWindow, width=25)
        self.btnBack.pack(side=BOTTOM)
        
if __name__ == "__main__":
    root = Tk()
    application = DataCollection(root)
    root.mainloop()
