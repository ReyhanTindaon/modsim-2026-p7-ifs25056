import json
import re


def parse_description_response(result: str) -> str:
    """
    Ekstrak deskripsi produk dari respons LLM.
    LLM diharapkan mengembalikan JSON: {"description": "..."}
    Jika tidak bisa di-parse, kembalikan teks mentah.
    """
    try:
        content = result
        # Hapus markdown code fence
        content = re.sub(r"```json\s*|\s*```", "", content).strip()
        parsed = json.loads(content)
        return parsed.get("description", content)
    except Exception:
        # Fallback: kembalikan teks langsung
        return result.strip()
