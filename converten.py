import LabelstudioToFonduer
from LabelstudioToFonduer.document_converter import DocumentConverter


documents_path = "/data/rxiv_publications_extracted"
output_path = "data/converted"

converter = DocumentConverter()

converter.convert(
    input_=documents_path, 
    output_path=output_path)


from LabelstudioToFonduer.document_converter import ConversionChecker

documents_path = "data/converted"

# project name is database name

converter = ConversionChecker(
        label_studio_url="139.6.160.19:8080",
        label_studio_api_key="3c6b5d7d1e140d894bcc0e9a1651b679fed906cf",
        fonduer_postgres_url="postgresql://postgres@fonduer-postgres-dev:5432/",
        project_name="biorxiv"
        )

converter.check(docs_path=documents_path)