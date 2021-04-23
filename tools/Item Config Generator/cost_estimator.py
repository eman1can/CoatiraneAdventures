import pandas
from pandas import ExcelWriter

file = open('Counters.txt', 'r', encoding='utf-8')
data = eval(file.read())
file.close()

overview = [['Floor Number', 'Minimum Movements', 'Maximum Movements', 'Average Movements', 'Minimum Encounters', 'Maximum Encounters', 'Average Encounters']]
sheets = {}
for floor_index, floor_data in data.items():
    overview.append([floor_index + 1])
    floor_data_name = f'Floor {floor_index + 1} Spawns and Drops'
    sheets[floor_data_name] = []
    for key in ['Minimum Movements', 'Maximum Movements', 'Average Movements', 'Minimum Encounters', 'Maximum Encounters', 'Average Encounters']:
        overview[floor_index + 1].append(floor_data.pop(key))
    drop_items = floor_data.pop('Drop Items')
    sheets[floor_data_name].append(['Monster Name', 'Minimum Spawns', 'Maximum Spawns', 'Average Spawns'])
    for monster, monster_data in floor_data.items():
        sheets[floor_data_name].append([monster, *monster_data.values()])
    drop_item_by_id = {}
    for run in drop_items:
        for drop_item, drop_count in run.items():
            drop_item_name = drop_item.replace('_', ' ').title()
            if drop_item_name in drop_item_by_id:
                drop_item_by_id[drop_item_name].append(drop_count)
            else:
                drop_item_by_id[drop_item_name] = [drop_count]
    sheets[floor_data_name].append(['Drop Item Name', 'Minimum Drops', 'Maximum Drops', 'Average Drops'])
    for key, value in drop_item_by_id.items():
        sheets[floor_data_name].append([key, min(value), max(value), sum(value) / 1000])
    sheets[floor_data_name] = pandas.DataFrame(sheets[floor_data_name][1:], columns=sheets[floor_data_name][0])
writer = ExcelWriter('drop_amount.xlsx')
df = pandas.DataFrame(overview[1:], columns=overview[0])
df.to_excel(writer, sheet_name='Overview', index=False)
for name, dataframe in sheets.items():
    dataframe.to_excel(writer, sheet_name=name, index=False)
writer.close()
