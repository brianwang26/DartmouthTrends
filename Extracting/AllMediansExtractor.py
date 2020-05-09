import requests
import lxml.html as lh
import pandas as pd

termsW = [str(i)+"w" for i in range(11,21)]
termsS = [str(i)+"s" for i in range(11,20)]
termsX = [str(i)+"x" for i in range(11,20)]
termsF = [str(i)+"f" for i in range(11,20)]
allTerms = termsW + termsS + termsX + termsF

def scrapeMedians(term):
    # Looking at 20W medians from ORC page
    url= "http://www.dartmouth.edu/reg/transcript/medians/" + str(term) + ".html"
    print(url)

    # Create "page" to handle the contents of website
    page = requests.get(url)

    # Use "document" to store contents of website
    document = lh.fromstring(page.content)

    # Parse data stored between </tr>'s of HTML (to scrape from HTML table)
    table_elements = document.xpath('//tr')

    # Perform sanity check to make sure number of columns in first 5 rows of table are the same (should be 4)
    print([len(row) for row in table_elements[:5]])

    # Parse data stored between </tr>'s of HTML (to scrape from HTML table)
    table_elements = document.xpath('//tr')

    # Create a list called table that will hold all our data
    table =[]

    # ColNum will keep track of which column in the table we are looking at
    colNum=0

    # For each column, store the first element (titles of the columns) and an empty list in "table"
    for firstRow in table_elements[0]:
        colNum += 1
        name = firstRow.text_content()
        name = name.replace(" ", "")
        print('%d:"%s"' % (colNum, name)) # print column index and title of column for a sanity check
        table.append((name, []))

    # Since first row is the header, data is stored on the second row onwards
    for rowNum in range(1, len(table_elements)):

        thisRow = table_elements[rowNum]   # thisRow stores all columns in current row

        # Ensures that rows have 4 columns
        if len(thisRow) != 4:
            break

        colNum = 0   # colNum keeps track of column as we traverse this row

        # Iterate through each element of current row
        for elem in thisRow:
            data = elem.text_content()
            try:
                data = int(data)
            except:
                data = data.replace(" ", "")
                pass
            table[colNum][1].append(data)  # Append the data to the list of this current column
            colNum += 1   # Increment i for the next column

    Dict = {title: column for (title, column) in table}
    df = pd.DataFrame(Dict)
    return(df)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)

frames = []
for term in allTerms:
    frames.append(scrapeMedians(term))

result = pd.concat(frames)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(result)

result.to_csv("data/rawData.csv", index=False)
