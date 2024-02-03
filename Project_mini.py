import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageTk

data = pd.read_excel('Project_dataset.xlsx')

class MLGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Central University Of Karnataka Result Analysis ")
        self.root.attributes('-fullscreen', True)

        # Loading the university logo image
        self.logo_image = Image.open('Central_University_of_Karnataka.png')   
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Configure ttk Styles For Each Components 
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 14), padding=5)   # Okay Buttons 
        self.style.configure('TCombobox', font=('Arial', 14), padding=5)     # For Buttons and options 
        self.style.configure('Heading.TLabel', font=('Times New Roman', 30 , 'bold'))    # For Headings 

        # Customize dropdown item appearance
        self.style.configure('Custom.TCombobox', font=('Arial', 14), padding=5)

        self.create_widgets()

    def create_widgets(self):

         # Logo   Importing logo and resizing it 
        max_logo_width = self.root.winfo_screenwidth() // 2  # width as needed
        max_logo_height = self.root.winfo_screenheight() // 4  # height as needed

        self.logo_image.thumbnail((max_logo_width, max_logo_height), Image.ANTIALIAS)     # For Thimbnail of image 
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        logo_label = ttk.Label(self.root, image=self.logo_photo)
        logo_label.pack(pady=30) 


        # Heading
        heading_label = ttk.Label(self.root, text="Welcome To Central University Of Karnataka", style='Heading.TLabel')
        heading_label.pack(pady=10)
        heading_label = ttk.Label(self.root, text="Student Academic Performance Analysis Portal", style='Heading.TLabel')
        heading_label.pack(pady=20)

        # Dropdown menu
        options = ["Show Top 10 Students", "Show Complete Result","Passed Students", "Failed Students","Show Topper Result" , 
                   "Pass Percentage", "Fail Percentage", "1st Division with Distinction", 
                   "1st Division", "2nd Division", "Marks Distribution Plot", "Result Plot"
                   ]
        self.selected_option = tk.StringVar()
        self.dropdown = ttk.Combobox(self.root, textvariable=self.selected_option, values=options, style='TCombobox')
        self.dropdown.set("Select Option")
        self.dropdown.pack(pady=30)
        self.dropdown.config(font=('Arial', 14))

        # Okay button
        self.okay_button = ttk.Button(self.root, text="Okay", command=self.handle_okay, style='TButton')   
        self.okay_button.pack(pady=10)

    def handle_okay(self):
        selected_option = self.selected_option.get()

        if selected_option == "Show Top 10 Students":
            result = self.get_top_10()
            self.show_result(result)
        elif selected_option == "Show Topper Result":
            result = self.get_topper()
            self.show_result(result)
        elif selected_option == "Show Complete Result":
            result = self.get_complete_result()
            self.show_result(result)
        elif selected_option == "Pass Percentage":
            result = self.get_pass_percentage()
            self.show_result(result)
        elif selected_option == "Fail Percentage":
            result = self.get_fail_percentage()
            self.show_result(result)
        elif selected_option == "1st Division with Distinction":
            result = self.get_division_result(75, float('inf'), '1st Division with Distinction')
            self.show_result(result)
        elif selected_option == "1st Division":
            result = self.get_division_result(60, 74, '1st Division')
            self.show_result(result)
        elif selected_option == "2nd Division":
            result = self.get_division_result(50, 59, '2nd Division')
            self.show_result(result)
        elif selected_option == "Marks Distribution Plot":
            self.plot_marks_distribution()
        elif selected_option == "Result Plot":
            self.plot_result_distribution()
        elif selected_option == "Passed Students":
            result = self.get_passed_students()
            self.show_result(result)
        elif selected_option == "Failed Students":
            result = self.get_failed_students()
            self.show_result(result)

    def get_topper(self):
        topper = data[data['REMARKS'] == 'PASS'].loc[data['PERCENTAGE'].idxmax()]
        return topper

    def get_top_10(self):
        top_10 = data[data['REMARKS'] == 'PASS'].nlargest(10, 'PERCENTAGE')
        return top_10

    def get_complete_result(self):
        return data 

    def get_pass_percentage(self):
        pass_percentage = (data['REMARKS'] == 'PASS').mean() * 100
        return f"Pass Percentage: {pass_percentage:.2f}%"  

    def get_fail_percentage(self):
        fail_percentage = (data['REMARKS'] == 'FAIL').mean() * 100
        return f"Fail Percentage: {fail_percentage:.2f}%"

    def get_division_result(self, lower_limit, upper_limit, division_name):
        division_result = data[(data['PERCENTAGE'] >= lower_limit) & (data['PERCENTAGE'] <= upper_limit) & (data['REMARKS'] == 'PASS')]
        division_result['Division'] = division_name
        return division_result

    def get_passed_students(self):
        passed_students = data[data['REMARKS'] == 'PASS']
        return passed_students

    def get_failed_students(self):
        failed_students = data[data['REMARKS'] == 'FAIL']
        return failed_students

    def plot_marks_distribution(self):
        sns.histplot(data['PERCENTAGE'])
        plt.title('Marks Distribution')
        plt.xlabel('Percentage')
        plt.show()

    def plot_result_distribution(self):
        data['REMARKS'].value_counts().plot(kind='pie', autopct='%.2f', figsize=(8, 8))
        plt.title('Result Plot')
        plt.ylabel('')
        plt.show()


        # Till Here 

    def show_result(self, result):
        result_str = result.to_string() if isinstance(result, pd.DataFrame) else str(result)
        result_window = tk.Toplevel(self.root)
        result_window.title("Result")
        result_text = tk.Text(result_window, wrap="none", height=250, width=350)
        result_text.insert("0.3", result_str)
        result_text.pack()
        result_button = ttk.Button(result_window, text="Close", command=result_window.destroy, style='TButton')
        result_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MLGUI(root)
    root.mainloop()


