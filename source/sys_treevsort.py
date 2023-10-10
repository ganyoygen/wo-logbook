import tkinter as tk
from tkinter import ttk

def sort_treeview(tree, col, descending):
    # Function to sort the Treeview by column
    data = [(tree.set(item, col), item) for item in tree.get_children('')]
    # data.sort(key=lambda t: int(t[0]), reverse=descending) # Fixme: hanya sort number, selain itu gagal
    data.sort(reverse=descending)
    for index, (val, item) in enumerate(data):
        tree.move(item, '', index)
    tree.heading(col, command=lambda: sort_treeview(tree, col, not descending))

if __name__ == "__main__":
    parent = tk.Tk()
    parent.title("Sortable Treeview Example")

    # Create a Treeview widget with columns
    columns = ("Name", "Age", "Country")
    tree = ttk.Treeview(parent, columns=columns, show="headings")

    # Configure column headings and sorting functionality
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_treeview(tree, c, False))
        tree.column(col, width=100)

    # Insert data into the Treeview
    data = [("Taliesin Megaira", 35, "USA"),
            ("Fionn Teofilo", 28, "UK"),
            ("Ata Caishen", 45, "France"),
            ("Marina Evie", 38, "Spain"),
            ("Xanthe Eligio", 32, "France"),
            ("Fausta Tone", 30, "Australia"),
            ("Yawan Idane", 42, "Mongolia"),
            ("Rolph Noah", 30, "South Africa")]

    for item in data:
        tree.insert('', 'end', values=item)
    tree.pack()
    parent.mainloop()