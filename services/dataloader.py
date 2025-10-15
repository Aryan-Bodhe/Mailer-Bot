import pandas as pd

class DataLoader():
    def __init__(self, excel_file):        
        self.data = pd.read_excel(excel_file)
        self.data.dropna(how='all')
        self.data.columns = self.data.columns.str.strip()
        self.validate_sheet()

    def validate_sheet(self):
        cols = self.data.columns
        if 'Mail' not in cols or 'Name' not in cols:
            raise pd.errors.DataError("'Mail' or 'Name' column missing in sheet.")
        
    def get_student_exam_data(self, exam_name: str):
        if exam_name.strip().lower() == 'all exams':
            return self.data[['Mail', 'Name'] + self.get_exam_names()]
        if exam_name not in self.data.columns:
            raise pd.errors.InvalidColumnName(f'Column {exam_name} not found in sheet.')
        return pd.concat([self.data['Mail'], self.data['Name'], self.data[exam_name]], axis=1)

    def get_head(self):
        return self.data.head()

    def get_student_names(self):
        return pd.concat([self.data['Mail'], self.data['Name']], axis=1)
    
    def get_exam_names(self):
        cols = self.data.columns.to_list()
        if "Name" in cols:
            cols.remove("Name")
        if "Mail" in cols:
            cols.remove("Mail")    
        if "Roll number" in cols:
            cols.remove("Roll number")

        # Remove columns where all values are 0 or NaN
        cols = [col for col in cols if not self.data[col].isna().all() and not (self.data[col].fillna(0) == 0).all()]
        return cols
        
