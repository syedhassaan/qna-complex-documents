import boto3
import json
import os
import pypdf
import shutil


def analyze_invoice(file_path):
    # Create a Textract client
    textract_client = boto3.client("textract")

    # Read the file as bytes
    with open(file_path, "rb") as file:
        file_bytes = file.read()

    # Call AnalyzeExpense API
    response = textract_client.analyze_expense(Document={"Bytes": file_bytes})

    print("_response.keys():", response.keys())
    print("type(response): ", type(response))

    # print("response['ExpenseDocuments']:", response['ExpenseDocuments'])
    print("type(response['ExpenseDocuments']):", type(response["ExpenseDocuments"]))
    print("len(response['ExpenseDocuments']):", len(response["ExpenseDocuments"]))

    for document in response["ExpenseDocuments"]:
        print("----------------------------------------------------")
        # print("document: ", document)
        print("type(document): ", type(document))
        print("document.keys():", document.keys())

        print("----------------------------------------------------")
        print('document["LineItemGroups"]:', document["LineItemGroups"])
        print('len(document["LineItemGroups"]):', len(document["LineItemGroups"]))

        receipt_details = {}
        for field in document["SummaryFields"]:
            # print("===========================================")
            # print("field: ", field)
            # print("type(field): ", type(field))
            # print("field.keys(): ", field.keys())

            # Might be a good idea to not filter out anything.
            # if field["Type"]["Text"] in ("ADDRESS", "NAME", "INVOICE_RECEIPT_DATE", "AMOUNT_PAID", "SUBTOTAL", "TAX", "TOTAL", "VENDOR_PHONE", "OTHER"):
            # print("SUCCESS!")

            # if field.get("LabelDetection") != None:
            #     output_dict[field["LabelDetection"]["Text"]] = field["ValueDetection"]["Text"]
            # else:
            #    output_dict[field["Type"]["Text"]] = field["ValueDetection"]["Text"]

            if field["Type"]["Text"] not in receipt_details:
                receipt_details[field["Type"]["Text"]] = field["ValueDetection"]["Text"]

        items_dict = {}
        for group in document["LineItemGroups"]:
            print("type(group):", type(group))
            print("group.keys():", group.keys())
            print("len(group['LineItems']): ", len(group["LineItems"]))
            for line_item in group["LineItems"]:
                print("==========================================================")
                print("line_items: ", line_item)
                print("type(line_items): ", type(line_item))
                item_name = ""
                item_price = ""
                for line_item_exp_field in line_item["LineItemExpenseFields"]:
                    print("line_item_exp_field:", line_item_exp_field)
                    print("type(line_item_exp_field):", type(line_item_exp_field))

                    if line_item_exp_field["Type"]["Text"] == "ITEM":
                        # print(line_item_exp_field["Type"]["Text"], ":" , line_item_exp_field["ValueDetection"]["Text"])
                        item_name = line_item_exp_field["ValueDetection"]["Text"]
                        print("item_name: ", item_name)
                    elif line_item_exp_field["Type"]["Text"] == "PRICE":
                        item_price = line_item_exp_field["ValueDetection"]["Text"]
                        print("item_price: ", item_price)

                items_dict[item_name] = item_price

        receipt_details["items"] = items_dict

    return receipt_details


def write_to_file(data, file_name):
    print("file_name: ", file_name)
    # file_path = "..\output_data\\" + file_name + ".json"
    file_path = "..\Testcases_Invoices\\final_output\\" + file_name + ".json"
    # file_path = "test.json"
    # data = {"Name": "Hasan", "age": 14}
    with open(file_path, "a") as file:
        json.dump(data, file)
        file.write("\n\n")


def determine_num_pages(file):
    pdfFileObj = open(file, "rb")

    # creating a pdf reader object
    pdfReader = pypdf.PdfReader(pdfFileObj)

    print("# of pages:", len(pdfReader.pages))

    return len(pdfReader.pages)


def split_pdf(input_pdf_path):
    # Open the input PDF file
    pdf_paths = []
    os.mkdir("..\Testcases_Invoices\TestCases\\temp")
    with open(input_pdf_path, "rb") as input_pdf_file:
        pdf_reader = pypdf.PdfReader(input_pdf_file)

        # Loop through each page and save it as a separate PDF
        for page_num in range(len(pdf_reader.pages)):
            output_pdf_path = (
                f"..\Testcases_Invoices\TestCases\\temp\page_{page_num + 1}.pdf"
            )
            pdf_writer = pypdf.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_num])

            with open(output_pdf_path, "wb") as output_pdf_file:
                pdf_writer.write(output_pdf_file)

            pdf_paths.append(output_pdf_path)

    return pdf_paths


if __name__ == "__main__":
    # For processing a single file
    # Replace 'your_invoice.pdf' with the path to your invoice file
    # # invoice_file_path = '..\input_data\sample_invoice.png'
    invoice_file_path = "..\Testcases_Invoices\\TestCases\\Invoice221050915_Customer2203078_Modern Arab Enterprises.pdf"

    if ".pdf" in invoice_file_path:
        num_pages = determine_num_pages(invoice_file_path)

        if num_pages == 1:
            extracted_data = analyze_invoice(invoice_file_path)
            print("===========================================================")
            print(extracted_data)
            write_to_file(
                extracted_data, invoice_file_path.split("\\")[-1].split(".")[0]
            )

        elif num_pages >= 1:
            pdfs = split_pdf(invoice_file_path)
            print("pdfs: ", pdfs)
            extracted_data = []
            for pdf in pdfs:
                try:
                    extracted_data.append(analyze_invoice(pdf))
                except Exception as E:
                    print("Exception::", E)
            shutil.rmtree("..\Testcases_Invoices\TestCases\\temp")
    else:
        extracted_data = analyze_invoice(invoice_file_path)

    write_to_file(extracted_data, invoice_file_path.split("\\")[-1].split(".")[0])

    # For processing multiple files in a directory
    # Loop through the files in the directory
    # directory_path = "..\\Testcases_Invoices\\TestCases"
    # for filename in os.listdir(directory_path):
    #     if os.path.isfile(os.path.join(directory_path, filename)):
    #         # Process the file
    #         try:
    #             invoice_file_path = os.path.join(directory_path, filename)
    #             print("===========================================================")
    #             print(f"Processing file: {invoice_file_path}")

    #             if ".pdf" in invoice_file_path:
    #                 num_pages = determine_num_pages(invoice_file_path)
    #                 if num_pages == 1:
    #                     extracted_data = analyze_invoice(invoice_file_path)
    #                 elif num_pages >= 1:
    #                     pdfs = split_pdf(invoice_file_path)
    #                     print("pdfs: ", pdfs)
    #                     extracted_data = []
    #                     for pdf in pdfs:
    #                         extracted_data.append(analyze_invoice(pdf))
    #                     shutil.rmtree("..\Testcases_Invoices\TestCases\\temp")
    #             else:
    #                 extracted_data = analyze_invoice(invoice_file_path)

    #             print(extracted_data)
    #             write_to_file(
    #                 extracted_data, invoice_file_path.split("\\")[-1].split(".")[0]
    #             )

    #         except Exception as E:
    #             print("===========================================================")
    #             print("Exception::", E)

    #             try:
    #                 shutil.rmtree("..\Testcases_Invoices\TestCases\\temp")
    #             except Exception as e:
    #                 print("Exception::", E)
