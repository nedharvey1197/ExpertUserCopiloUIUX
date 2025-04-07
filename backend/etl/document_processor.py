"""
Document processor for extracting trial information from uploaded files.
Supports PDF, Word, and text documents.
"""
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import fitz  # PyMuPDF
from docx import Document
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processes uploaded documents to extract trial-related information."""

    def __init__(self):
        """Initialize document processor."""
        self.supported_extensions = {'.pdf', '.docx', '.doc', '.txt'}
        logger.info("DocumentProcessor initialized with supported extensions: %s", self.supported_extensions)

    def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process a document and extract trial information.

        Args:
            file_path: Path to the document

        Returns:
            Dict containing extracted information
        """
        logger.info(f"Starting document processing for: {file_path}")
        path = Path(file_path)

        if not path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.supported_extensions:
            logger.error(f"Unsupported file type: {path.suffix}")
            raise ValueError(f"Unsupported file type: {path.suffix}")

        try:
            logger.debug(f"Processing {path.suffix.lower()} file")
            if path.suffix.lower() == '.pdf':
                result = self._process_pdf(path)
            elif path.suffix.lower() in {'.docx', '.doc'}:
                result = self._process_word(path)
            else:  # .txt
                result = self._process_text(path)

            logger.debug(f"Document processing result: {result}")
            return result

        except Exception as e:
            logger.error(f"Error processing document {file_path}: {str(e)}", exc_info=True)
            raise

    def _process_pdf(self, path: Path) -> Dict[str, Any]:
        """Extract information from PDF document."""
        logger.debug(f"Processing PDF file: {path}")
        doc = fitz.open(str(path))
        text = ""

        try:
            logger.debug(f"PDF has {len(doc)} pages")
            for page_num, page in enumerate(doc, 1):
                logger.debug(f"Processing page {page_num}")
                text += page.get_text()
                logger.debug(f"Page {page_num} text length: {len(text)}")

            result = self._extract_trial_info(text)
            logger.debug(f"PDF processing result: {result}")
            return result

        finally:
            doc.close()
            logger.debug("PDF document closed")

    def _process_word(self, path: Path) -> Dict[str, Any]:
        """Extract information from Word document."""
        logger.debug(f"Processing Word file: {path}")
        doc = Document(path)
        text = "\n".join([p.text for p in doc.paragraphs])
        logger.debug(f"Word document text length: {len(text)}")

        result = self._extract_trial_info(text)
        logger.debug(f"Word processing result: {result}")
        return result

    def _process_text(self, path: Path) -> Dict[str, Any]:
        """Extract information from text file."""
        logger.debug(f"Processing text file: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        logger.debug(f"Text file length: {len(text)}")

        result = self._extract_trial_info(text)
        logger.debug(f"Text processing result: {result}")
        return result

    def _extract_trial_info(self, text: str) -> Dict[str, Any]:
        """Extract trial information from text."""
        logger.debug("Starting trial information extraction")

        # Extract key trial information using regex patterns
        patterns = {
            'trial_phase': r'Phase\s+([IVX]+)',
            'trial_type': r'(Interventional|Observational)',
            'primary_endpoint': r'Primary\s+Endpoint[s]?\s*:?\s*([^\.]+)',
            'secondary_endpoint': r'Secondary\s+Endpoint[s]?\s*:?\s*([^\.]+)',
            'sample_size': r'(\d+)\s+participants',
            'duration': r'(\d+)\s+(week|month|year)s?'
        }

        extracted_info = {}
        for key, pattern in patterns.items():
            logger.debug(f"Extracting {key} using pattern: {pattern}")
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_info[key] = match.group(1)
                logger.debug(f"Found {key}: {extracted_info[key]}")
            else:
                logger.debug(f"No match found for {key}")

        logger.debug(f"Extracted trial information: {extracted_info}")
        return extracted_info

    def enrich_trial_data(self, current_data: Dict[str, Any], document_path: str) -> Dict[str, Any]:
        """
        Enrich existing trial data with information from document.

        Args:
            current_data: Current trial information to enrich
            document_path: Path to the document to process

        Returns:
            Dict containing merged trial information
        """
        try:
            doc_data = self.process_document(document_path)

            # Merge data, preferring current data over document extraction
            enriched = {
                **doc_data,
                **current_data,
                "sources": {
                    **(current_data.get("sources", {})),
                    "document": {
                        "path": document_path,
                        "processed_at": doc_data["processed_at"],
                        "available": True
                    }
                }
            }

            return enriched

        except Exception as e:
            logger.error(f"Failed to enrich trial data from document {document_path}: {str(e)}")
            return {
                **current_data,
                "sources": {
                    **(current_data.get("sources", {})),
                    "document": {
                        "path": document_path,
                        "processed_at": datetime.utcnow().isoformat(),
                        "available": False,
                        "error": str(e)
                    }
                }
            }
