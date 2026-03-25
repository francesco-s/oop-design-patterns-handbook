from abc import ABC, abstractmethod

# Product interface
class Document(ABC):
    @abstractmethod
    def create(self):
        pass

# Concrete Products
class PDFDocument(Document):
    def create(self):
        return "PDF document created"

class WordDocument(Document):
    def create(self):
        return "Word document created"

class TextDocument(Document):
    def create(self):
        return "Text document created"

# Creator (Factory) class
class DocumentCreator:
    @staticmethod
    def create_document(doc_type):
        """Factory method to create documents based on type."""
        if doc_type == "pdf":
            return PDFDocument()
        elif doc_type == "word":
            return WordDocument()
        elif doc_type == "text":
            return TextDocument()
        else:
            raise ValueError(f"Document type '{doc_type}' not supported")


if __name__ == "__main__":
    # Create different document types using the factory
    for doc_type in ["pdf", "word", "text"]:
        document = DocumentCreator.create_document(doc_type)
        print(document.create())
    
    # Try with an invalid type (will raise an exception)
    try:
        document = DocumentCreator.create_document("excel")
        print(document.create())
    except ValueError as e:
        print(f"Error: {e}")