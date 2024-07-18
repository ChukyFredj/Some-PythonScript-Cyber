import re

def get_metadata_with_regex(pdf_path):
    with open(pdf_path, 'rb') as file:
        content = file.read()
        
        metadata_patterns = {
            'Title': re.compile(rb'/Title\s*\(([^)]+)\)'),
            'Author': re.compile(rb'/Author\s*\(([^)]+)\)'),
            'Subject': re.compile(rb'/Subject\s*\(([^)]+)\)'),
            'Creator': re.compile(rb'/Creator\s*\(([^)]+)\)'),
            'Producer': re.compile(rb'/Producer\s*\(([^)]+)\)'),
            'CreationDate': re.compile(rb'/CreationDate\s*\(([^)]+)\)'),
            'ModDate': re.compile(rb'/ModDate\s*\(([^)]+)\)')
        }
        
        metadata = {}
        for key, pattern in metadata_patterns.items():
            match = pattern.search(content)
            if match:
                metadata[key] = match.group(1).decode('utf-8')
            else:
                metadata[key] = None
        
        return metadata

if __name__ == "__main__":
    pdf_path = 'ANONOPS_The_Press_Release.pdf'  # Remplacer par le chemin de votre fichier PDF
    metadata = get_metadata_with_regex(pdf_path)
    print("\nMétadonnées avec regex :")
    for key, value in metadata.items():
        print(f"{key}: {value}")
