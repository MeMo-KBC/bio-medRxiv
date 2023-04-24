import LabelstudioToFonduer
from LabelstudioToFonduer.document_converter import DocumentConverter


documents_path = "/data/rxiv_publications_extracted"
output_path = "data/converted"

converter = DocumentConverter()

converter.convert(
    input_=documents_path, 
    output_path=output_path)