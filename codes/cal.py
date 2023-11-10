import tkinter as tk
from tkinter import ttk
from tkinter import *

def calpy():
    def switch_tab(event):
        selected_tab = notebook.index(notebook.select())

    # Create the main window
    window = tk.Tk()
    window.title("Tabbed Interface")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(window)

    # Create and add tabs
    tab1 = tk.Frame(notebook)
    tab2 = tk.Frame(notebook)

    notebook.add(tab1, text="Calculator")
    notebook.add(tab2, text="Help")

    def sendtext(text):
        t.insert(tk.END, text)

    def evals():
        c=t.get(1.0,END)
        sol=eval(f'{c}')
        t.delete("1.0","end")
        t.insert(tk.END, sol)

    def clear():
        t.delete("1.0","end")

    t = Text(tab1, height=3, width=60)
    t.grid(row=0,column=0,columnspan=5)
    k=10
    for i in range(2,5):
        for j in range(0,3):
            k=k-1
            button=Button(tab1,text=k,height = 2, width = 9 ,command=lambda t=k: sendtext(t))
            button.grid(row=i,column=j,columnspan=1,pady=2,padx=3)
    n=0 
    airth=["+",'-','/','**','^','sqrt']
    for i in range(2,5):
        for j in range(3,5):
            button=Button(tab1,text=f"{airth[n]}",height = 2, width = 9 ,command=lambda t= f"{airth[n]}":sendtext(t))
            button.grid(row=i,column=j,columnspan=1)
            n=n+1
    button=Button(tab1,text=0,height = 2, width = 9, command=lambda t= 0:sendtext(t))
    button.grid(row=5,column=0,columnspan=1)

    button=Button(tab1,text='=',height = 2, width = 22, command=evals)
    button.grid(row=5,column=1,columnspan=2)

    button=Button(tab1,text='clr',height = 2, width = 22, command=clear)
    button.grid(row=5,column=3,columnspan=2)

    button = tk.Button(tab1, text='exit' ,command=window.destroy ,width=60,height=2)
    button.grid(row=6,column=0, columnspan=5)

    points_text = "1. clr: it will clear the text feild\n2. sqrt :it will provide the sqrt Ref sqrt of 36 is 6\
                    \n3. **: To get will give you Square(**2) or Cube(**3) or Quad(**4) and  so on"
    points_label = tk.Label(tab2, text=points_text, justify=tk.LEFT)
    points_label.grid(row=1, column=0, padx=20, pady=20)

    # Bind the tab switching event
    notebook.bind("<<NotebookTabChanged>>", switch_tab)

    # Grid layout for the notebook
    notebook.grid(row=0, column=0, sticky="nsew")

    # Make the notebook expand with the window
    window.grid_rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    # Start the Tkinter event loop
    window.mainloop()
