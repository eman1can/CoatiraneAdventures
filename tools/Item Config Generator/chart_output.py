chart_names = [
        'Monster Spawn Rates Per Floor',
        'Monster Spawn Rates Per Floor (Log)',
        'Metal Skewed Resource Drop Rates',
        'Gem Skewed Resource Drop Rates',
        'Hard Materials (Natural)',
        'Hard Materials (Alloys)',
        'Hard Materials (Metals)',
        'Gems',
        'Hard Materials (Metals & Gems)',
        'Hard Materials (Monster)',
        'All Hard Materials',
        'Soft Materials (Natural)',
        'Soft Materials (Monster)',
        'All Soft Materials',
        'All Materials']

excel_path = 'C:\\Users\\Zoe\\Code Projects\\PycharmProjects\\CoatiraneAdventures\\tools\\Item Config Generator\\output.xlsx'
picture_path = 'C:\\Users\\Zoe\\Pictures\\Coatirane Adventures Pictures\\Data Graphs\\'

# Open the excel and save all charts
from win32com.client import Dispatch

app = Dispatch("Excel.Application")
workbook = app.Workbooks.Open(Filename=excel_path)

name_index = 0
workbook.Sheets.Add(After=workbook.Sheets(chart_names[-1])).Name = 'Picture Sheet'
for sheet in workbook.Worksheets:
    print('Saving Pictures from sheet', sheet.Name)
    for chart in sheet.ChartObjects():
        print('Found Chart', chart.Name, '-', chart_names[name_index])
        chart.copyPicture()
        chart_object = workbook.ActiveSheet.ChartObjects().Add(0, 0, 1920, 1080)
        chart_object.Chart.Paste()
        chart_object.Chart.Export(Filename=picture_path + f'{name_index} ' + chart_names[name_index] + '.png')
        chart_object.Delete()
        name_index += 1
workbook.ActiveSheet.Delete()
workbook.Close(SaveChanges=False, Filename=excel_path)
