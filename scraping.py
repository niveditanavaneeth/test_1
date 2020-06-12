import requests
from bs4 import BeautifulSoup 
import xlsxwriter
import os

# import requests, bs4
url = 'https://www.espncricinfo.com/series/8050/scorecard/1053479/andhra-vs-himachal-pradesh-group-c-ranji-trophy-2016-17'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find(class_="table batsman")

# extract rows
rows = table.find_all(class_=["thead-light bg-light"])
rows_data = table.find_all("tbody");

#  row iteration
rows = iter(rows)
rows_data = iter(rows_data)

# creation of workbook
cwd = os.getcwd()
path = cwd + '\\tmp\\batsmendata.xlsx'
workbook = xlsxwriter.Workbook(path)
worksheet = workbook.add_worksheet()


header_1 = [td.text for td in next(rows).find_all('th') if td.text]
# print type(header_1) 

w_row = 0
w_column = 0

# write operation for header
for i in header_1:
    worksheet.write(w_row, w_column, header_1[w_column])
    w_column += 1 

w_row +=1
w_column = 0 

# write operation for data rows
for row in next(rows_data).find_all('tr'): 
    data = []
    for td1 in row.find_all('td'):
        if td1.text.encode("utf-8") != '':
            data.append(td1.text.encode("utf-8"))
            x = td1.text.encode("utf-8")
            # write operation
            worksheet.write(w_row, w_column, x.decode('utf-8').strip())

        w_column +=1

    w_column = 0
    if len(data) > 0:
        w_row += 1
    # print w_row , ' row count'
          
workbook.close()




# workbook.save("/tmp/batsmendata.xlsx")
# results = soup.find(id='ResultsContainer')
# # print (results.prettify());
# # job_elems = results.find_all('div', class_='Collapsible')
# job_elems_table = results.find_all('table', class_='table batsman')
# for job_elem in job_elems_table:
#     end='\n'*2
    # print(job_elem, end)

# 'C:/Users/nived/Desktop/scrapping/tmp/batsmendata.xlsx'
