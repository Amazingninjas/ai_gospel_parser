
import requests
from bs4 import BeautifulSoup
import os

def download_robertson_grammar():
    """
    Downloads Robertson's Grammar from Archive.org and saves it as a clean text file.
    """
    print("Downloading Robertson's Grammar...")
    archive_url = "https://archive.org/details/grammarofgreekne00robe_2"
    
    try:
        response = requests.get(archive_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # --- DEBUG ---
        for link in soup.find_all('a'):
            print(f"Link found: {link.get('href')} -> {link.get_text(strip=True)}")
        # --- END DEBUG ---

        # Look for a link to a full text version
        text_link = soup.find('a', string=lambda t: t and 'full text' in t.lower())
        
        if text_link:
            text_url = "https://archive.org" + text_link['href']
            print(f"Found full text link: {text_url}")
            text_response = requests.get(text_url)
            text_response.raise_for_status()
            
            # The text on archive.org is often in a <pre> tag
            text_soup = BeautifulSoup(text_response.content, 'html.parser')
            pre_tag = text_soup.find('pre')
            if pre_tag:
                clean_text = pre_tag.get_text()
                output_path = '/home/justin/ai-projects/ai_gospel_parser/reference_texts/robertson_grammar/robertson_grammar.txt'
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(clean_text)
                print(f"Robertson's Grammar downloaded and saved to {output_path}")
                return

    except requests.exceptions.RequestException as e:
        print(f"Could not download Robertson's Grammar: {e}")

    print("Could not find a clean plain text version of Robertson's Grammar.")

def download_moulton_milligan():
    """
    Downloads Moulton-Milligan from Archive.org.
    It will try to find a plain text version, otherwise it will note the PDF for later OCR.
    """
    print("Downloading Moulton-Milligan...")
    archive_url = "https://archive.org/details/vocabularyofgree00mouluoft"
    
    try:
        response = requests.get(archive_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # --- DEBUG ---
        for link in soup.find_all('a'):
            print(f"Link found: {link.get('href')} -> {link.get_text(strip=True)}")
        # --- END DEBUG ---
        
        # Look for a link to a full text version
        text_link = soup.find('a', string=lambda t: t and 'full text' in t.lower())
        
        if text_link:
            text_url = "https://archive.org" + text_link['href']
            print(f"Found full text link: {text_url}")
            text_response = requests.get(text_url)
            text_response.raise_for_status()
            
            # The text on archive.org is often in a <pre> tag
            text_soup = BeautifulSoup(text_response.content, 'html.parser')
            pre_tag = text_soup.find('pre')
            if pre_tag:
                clean_text = pre_tag.get_text()
                output_path = '/home/justin/ai-projects/ai_gospel_parser/reference_texts/moulton_milligan/moulton_milligan_vocab.txt'
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(clean_text)
                print(f"Moulton-Milligan downloaded and saved to {output_path}")
                return

    except requests.exceptions.RequestException as e:
        print(f"Could not access {archive_url}: {e}")

    # If plain text download fails, fallback to noting the PDF
    print("Could not find a clean plain text version of Moulton-Milligan.")
    print("Noting PDF for later OCR.")
    
    metadata_path = '/home/justin/ai-projects/ai_gospel_parser/reference_texts/moulton_milligan/metadata.json'
    metadata = {
        "source": "https://archive.org/download/vocabularyofgree00mouluoft/vocabularyofgree00mouluoft.pdf",
        "needs_ocr": True,
        "notes": "PDF downloaded, requires OCR to extract plain text."
    }
    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    with open(metadata_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(metadata, f, indent=4)
    print(f"Metadata updated in {metadata_path}")


if __name__ == "__main__":
    download_robertson_grammar()
    download_moulton_milligan()
