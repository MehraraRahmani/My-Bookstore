from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from db import Database
from ttkthemes import ThemedStyle

db = Database("bookstore.db")

class Root(Tk):


    
    def __init__(self):
        super().__init__()
        self.title("My Fancy Bookstore")
        self.geometry("600x350")
        #Initilize UI
        self.create_widgets()
      
        
        #Populate list
        self.populate_list()
        
        self.selected_item = 0
        
                
    def create_widgets(self):
        #Title
        self.title_text = StringVar()
        title_label = ttk.Label(self, text="Title")
        title_label.grid(row=0, column=0)
        self.title_entry = ttk.Entry(self , textvariable=self.title_text)
        self.title_entry.grid(row=0, column=1)
        #Author
        self.author_text = StringVar()
        author_label = ttk.Label(self, text="Author")
        author_label.grid(row=0, column=2)
        self.author_entry = ttk.Entry(self , textvariable=self.author_text)
        self.author_entry.grid(row=0, column=3)
        #Year
        self.year_text = StringVar()
        year_label = ttk.Label(self, text="Year")
        year_label.grid(row=1, column=0)
        self.year_entry = ttk.Entry(self , textvariable=self.year_text)
        self.year_entry.grid(row=1, column=1)
        #ISBN
        self.isbn_text = StringVar()
        isbn_label = ttk.Label(self, text="ISBN")
        isbn_label.grid(row=1, column=2)
        self.isbn_entry = ttk.Entry(self , textvariable=self.isbn_text)
        self.isbn_entry.grid(row=1, column=3)
        
        #Books list
        self.books_list = Listbox(self, height=8 , width=50)
        self.books_list.grid(row=3, column=0, columnspan=3 , rowspan=6, padx=20, pady=20)
        #scrollbar
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.grid(row=3 , column=3 , rowspan=6, sticky="WNS", pady=20)
        
        # bind selected item
        self.books_list.bind('<<ListboxSelect>>', self.select_book)
        
        #connect listbox and scrollbar
        self.books_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.books_list.yview)
        
        #Buttons
        self.add_button = ttk.Button(self, text="Add Book", command=self.add_book)
        self.add_button.grid(row=2, column=0, pady=20)
        
        self.remove_button = ttk.Button(self, text="Remove Book", command=self.remove_book)
        self.remove_button.grid(row=2, column=1, pady=20)
        
        self.update_button = ttk.Button(self, text="Update Book", command=self.update_book)
        self.update_button.grid(row=2, column=2, pady=20)
        
        self.search_button = ttk.Button(self, text="Search Books", command=self.search_books)
        self.search_button.grid(row=2, column=3, pady=20)
        
    def populate_list(self , rows=None):
        #clear list
        self.books_list.delete(0 , END)
        if rows == None :
            rows = db.fetch()
        for row in rows:
            self.books_list.insert(END, row)

    
    def add_book(self):
        #check if any field is empty show an error to user.
        
        #insert book to database
        db.insert(self.title_text.get() , self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        #clear fields + populate list
        self.clear_fields()
        self.populate_list()
        
    def select_book(self , event):
        widget = event.widget
        self.selected_item=widget.get(ANCHOR)
        #add slscted item to enteries
        self.clear_fields()
        self.title_entry.insert(0, self.selected_item[1])
        self.author_entry.insert(0, self.selected_item[2])
        self.year_entry.insert(0, self.selected_item[3])
        self.isbn_entry.insert(0, self.selected_item[4])
        
    def remove_book(self):
        db.remove(self.selected_item[0])
        #clear fields + populate list
        self.clear_fields()
        self.populate_list()
        
    def update_book(self):
        db.update(self.selected_item[0], self.title_text.get() , self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.populate_list()
        
    def search_books(self):
        rows = db.search(self.title_text.get() , self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.populate_list(rows)
        
    def clear_fields(self):
        self.title_entry.delete(0, END)
        self.author_entry.delete(0, END)
        self.year_entry.delete(0, END)
        self.isbn_entry.delete(0, END)
    


root = Root() 
root.resizable(True, True)
style = ThemedStyle(root)
style.set_theme("radiance") 
root.mainloop()