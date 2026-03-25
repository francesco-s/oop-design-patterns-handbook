// Product interface
interface Document {
    String create();
}

// Concrete Products
class PDFDocument implements Document {
    @Override
    public String create() {
        return "PDF document created";
    }
}

class WordDocument implements Document {
    @Override
    public String create() {
        return "Word document created";
    }
}

class TextDocument implements Document {
    @Override
    public String create() {
        return "Text document created";
    }
}

// Creator (Factory) class
class DocumentCreator {
    public static Document createDocument(String docType) {
        // Factory method to create documents based on type
        switch (docType.toLowerCase()) {
            case "pdf":
                return new PDFDocument();
            case "word":
                return new WordDocument();
            case "text":
                return new TextDocument();
            default:
                throw new IllegalArgumentException("Document type '" + docType + "' not supported");
        }
    }
}

public class DocumentFactory {
    public static void main(String[] args) {
        // Create different document types using the factory
        String[] docTypes = {"pdf", "word", "text"};
        
        for (String type : docTypes) {
            Document document = DocumentCreator.createDocument(type);
            System.out.println(document.create());
        }
        
        // Try with an invalid type (will throw an exception)
        try {
            Document document = DocumentCreator.createDocument("excel");
            System.out.println(document.create());
        } catch (IllegalArgumentException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}