"""
File Parsing Utilities
Parse different document formats and extract text
"""

import os
from typing import Optional
from pathlib import Path

# PDF parsing
from PyPDF2 import PdfReader

# DOCX parsing
from docx import Document as DocxDocument

# CSV parsing
import csv


class FileParser:
    """Utility class for parsing different file formats"""
    
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """
        Parse PDF file and extract text
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def parse_docx(file_path: str) -> str:
        """
        Parse DOCX file and extract text
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text content
        """
        try:
            doc = DocxDocument(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def parse_txt(file_path: str) -> str:
        """
        Parse TXT/MD file and extract text
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            raise ValueError(f"Error parsing text file: {str(e)}")
    
    @staticmethod
    def parse_csv(file_path: str) -> str:
        """
        Parse CSV file and convert to text
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            CSV content as formatted text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                if not rows:
                    return ""
                
                # Format as text with headers
                text = []
                headers = rows[0]
                
                for row in rows[1:]:
                    row_text = ", ".join([f"{headers[i]}: {row[i]}" for i in range(len(row)) if i < len(headers)])
                    text.append(row_text)
                
                return "\n".join(text).strip()
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {str(e)}")
    
    @staticmethod
    def parse_file(file_path: str) -> str:
        """
        Auto-detect file type and parse accordingly
        
        Args:
            file_path: Path to file
            
        Returns:
            Extracted text content
            
        Raises:
            ValueError: If file type is not supported
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return FileParser.parse_pdf(file_path)
        elif ext == '.docx':
            return FileParser.parse_docx(file_path)
        elif ext in ['.txt', '.md']:
            return FileParser.parse_txt(file_path)
        elif ext == '.csv':
            return FileParser.parse_csv(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to split
        chunk_size: Maximum characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # If this is not the last chunk, try to break at a sentence or word boundary
        if end < text_length:
            # Look for sentence boundary (. ! ?)
            for i in range(end, max(start, end - 100), -1):
                if text[i] in '.!?\n':
                    end = i + 1
                    break
            else:
                # Look for word boundary
                for i in range(end, max(start, end - 50), -1):
                    if text[i].isspace():
                        end = i + 1
                        break
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        # Move start forward, accounting for overlap
        start = end - chunk_overlap if end < text_length else text_length
    
    return chunks

