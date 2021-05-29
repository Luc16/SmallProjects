import gspread
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *

gc = gspread.service_account(filename='gspread-314200-6ebce4156e1a.json')

sheet = gc.open("Teste")

names = ["the Millibit", "hello", "testing"]
emails = ["themillibit@gmail.com", "hello@gmail.com", "testing@gmail.com"]

sh = sheet.sheet1

for i in range(2, len(emails)+2):
    sh.update_cell(i, 1, names[i-2])
    sh.update_cell(i, 2, emails[i-2])

rule = ConditionalFormatRule(
    ranges=[GridRange.from_a1_range('C2:C', sh)],
    booleanRule=BooleanRule(
        condition=BooleanCondition('NUMBER_GREATER', ['500']),
        format=CellFormat(textFormat=TextFormat(bold=True), backgroundColor=Color(1,0,0))
    )
)
rules = get_conditional_format_rules(sh)
# rules.append(rule)
# rules.save()
