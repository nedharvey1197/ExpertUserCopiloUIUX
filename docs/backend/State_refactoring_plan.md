### 🎯 Cursor-AI Implementation Package: Session State Integration (Copilot V0)

---

## 🔍 Goal

Unify backend Copilot session state management across file upload and enrichment using the `CopilotSessionState` model. Integrate structured logging of `5Ws` and enrichment metadata for V0 functionality.

---

## 🧠 Embedded Session Reference Block

### ✅ What steps have already been completed?

- Defined `CopilotSessionState` model in `models/session_state.py`
- Implemented `update_session_state(session_id, update_dict)` in `state_updater.py`
- Created `/copilot/session` endpoint to return session_id
- Captured session_id in frontend and passed through `/upload_file`
- Refactored `run_pipeline()` to:
  - Extract file preview
  - Run 5Ws extraction
  - Patch session state
- Deferred all frontend session hydration logic (to be handled via Cursor)

### ✅ Components & Files Affected:

- `copilot.py`
- `pipeline_runner.py`
- `fivews_initializer.py`
- `state_updater.py`
- `models/session_state.py`
- (Frontend only uses `session_id` — no session sync yet)

### ✅ Implementation Challenges Addressed:

- Introduced schema-governed patching
- Modularized update logic after pipeline steps
- Delayed FE state complexity to avoid premature coupling
- Error-safe state updates using nested schema patterns

---

## 🔧 FILE-BY-FILE INSTRUCTIONS

### 🔄 `copilot.py`

**Intent:** Accept `session_id`, save file, trigger pipeline, patch state.

```python
# 🔁 Replace upload_file with:
@router.post("/upload_file")
async def upload_file(
    session_id: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        filename = file.filename
        file_location = UPLOAD_DIR / f"{session_id}_{filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Run enrichment pipeline (auto-patches state)
        run_pipeline(session_id=session_id, file_path=file_location)

        return {
            "session_id": session_id,
            "status": "File uploaded and enrichment started"
        }

    except Exception as e:
        update_session_state(session_id, {"enrichment": {"status": "error", "errors": str(e)}})
        raise HTTPException(status_code=500, detail=str(e))
```

**Requires Import:**

```python
from utils.pipeline_runner import run_pipeline
from utils.state_updater import update_session_state
```

---

### 🔄 `pipeline_runner.py`

**Intent:** Load text, extract 5Ws, update session state.

```python
from utils.state_updater import update_session_state
from logic.fivews_initializer import extract_5ws_from_text


def run_pipeline(session_id: int, file_path: Path):
    from PyPDF2 import PdfReader
    from pathlib import Path

    preview = ""
    try:
        reader = PdfReader(str(file_path))
        preview = "\n".join([p.extract_text() or "" for p in reader.pages])
    except Exception as e:
        preview = f"(Error extracting preview: {e})"

    fivews = extract_5ws_from_text(preview)

    update_session_state(session_id, {
        "enrichment": {
            "file_uploaded": file_path.name,
            "file_preview": preview[:500],
            "5ws_extracted": fivews,
            "status": "complete"
        }
    })
```

---

### 🔄 `fivews_initializer.py`

**Intent:** Extract 5Ws from unstructured text using regex mapping.

```python
def extract_5ws_from_text(text: str) -> dict:
    from pathlib import Path
    import json
    import re

    MAPPING_PATH = Path(__file__).parent / "../assets/synopsis_mapping.json"
    with open(MAPPING_PATH, "r") as f:
        MAPPINGS = json.load(f)

    result = {}
    for category, rules in MAPPINGS.items():
        result[category] = "Unknown"
        for rule in rules:
            if re.search(rule["pattern"], text, re.IGNORECASE):
                result[category] = rule["value"].replace("{MATCH}", re.search(rule["pattern"], text).group())
                break

    return result
```

---

### ✅ `state_updater.py`

No changes needed, already supports structured updates like:

```python
update_session_state(session_id, {"enrichment": {"file_uploaded": "example.pdf"}})
```

---

## ✅ INSTRUCTIONS FOR CURSOR.AI COMPOSER

You will:

1. Replace `upload_file()` in `copilot.py`
2. Replace `run_pipeline()` in `pipeline_runner.py`
3. Replace `fivews_initializer.py` content with `extract_5ws_from_text()` logic
4. Confirm that:
   - Session creation (`/copilot/session`) still works
   - FE sends `session_id` from StageOneIntake
   - Enrichment preview & 5Ws are correctly injected into `copilot.sessions.state`

Test with:

```bash
curl -X POST -F "session_id=123" -F "file=@example.pdf" http://localhost:8000/copilot/upload_file
```

---

## 📦 Outcome

You will now:

- Persist enrichment summaries into structured state
- Build toward intelligent 5Ws → Synopsis evolution
- Support future logic using the same parametric session state model

---

Ping me when you're ready to test or run into any Composer-AI implementation snags. I’ll remain on standby as technical supervisor.

Onward. ✨
