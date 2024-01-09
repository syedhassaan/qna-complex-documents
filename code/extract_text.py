import pypdf

# file = "..\input_data\\Dutch.pdf"
file = "..\Testcases_Invoices\\TestCases\\21-0867 INV.pdf"
pdfFileObj = open(file, "rb")

# creating a pdf reader object
pdfReader = pypdf.PdfReader(pdfFileObj)

print(len(pdfReader.pages))

final_string = ""
i = 0
for page in pdfReader.pages:
    # creating a page object
    i += 1
    print("Page #", i)
    pageObj = page

    # extracting text from page
    text = pageObj.extract_text()
    print(text)

    final_string += text

    # break

file_name = file.split("\\")[-1].split(".")[0]
print("file_name: ", file_name)
file_path = "..\output_data\\" + file_name + ".txt"
print("file_path: ", file_path)
with open(file_path, "w", encoding="utf-8") as file:
    file.write(final_string)
