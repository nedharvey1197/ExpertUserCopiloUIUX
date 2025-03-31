def load_parser(doc_path: str, overrides: dict) -> dict:
    """
    Loads and parses the document based on file extension or override.
    Returns raw text and document metadata.
    """
    from pathlib import Path
    from etl.utils.logger import log_event

    ext = Path(doc_path).suffix.lower()
    raw_text = "(not yet parsed)"

    if ext == ".pdf":
        raw_text = "[Stub] parsed PDF text"
    elif ext == ".txt":
        raw_text = "[Stub] parsed TXT content"
    elif ext in [".csv", ".tsv"]:
        raw_text = "[Stub] parsed CSV content"
    elif ext in [".docx"]:
        raw_text = "[Stub] parsed DOCX paragraphs"

    log_event("PARSE_COMPLETE", {"doc_path": str(doc_path), "ext": ext})
    return {"raw_text": raw_text, "meta": {"filename": str(doc_path), "ext": ext}}

