from langchain_community.document_loaders import PyPDFLoader


from langchain_community.document_loaders import DirectoryLoader

# # Load PDFs from a directory
# directory_loader = DirectoryLoader('path/to/directory')
# documents = directory_loader.load()

# # Load a single PDF file
# pdf_loader = PyPDFLoader('path/to/pdf/file.pdf')
# document = pdf_loader.load()


loader = PyPDFLoader('./29_jan_morning.pdf')

doc= loader.load()
print(type(doc))
print(len(doc))

