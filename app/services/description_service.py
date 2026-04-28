import json
from app.extensions import SessionLocal
from app.models.product_request import ProductRequest
from app.models.description import Description
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_description_response


def create_description(product_name: str, features: list, platform: str, tone: str):
    """Generate deskripsi produk via LLM dan simpan ke database."""
    session = SessionLocal()
    try:
        features_str = ", ".join(features)
        tone_map = {
            "formal": "bahasa formal dan profesional",
            "santai": "bahasa santai dan akrab",
            "persuasif": "bahasa persuasif dan menarik",
        }
        tone_desc = tone_map.get(tone, tone)

        prompt = f"""
Buatkan deskripsi produk e-commerce untuk platform {platform} dalam format JSON.

Produk: {product_name}
Fitur utama: {features_str}
Gaya bahasa: {tone_desc}

Balas HANYA dengan JSON berikut (tanpa teks lain):
{{
    "description": "<deskripsi produk siap pakai>"
}}
"""
        raw = generate_from_llm(prompt)
        content = parse_description_response(raw)

        # Simpan request
        req = ProductRequest(
            product_name=product_name,
            features=json.dumps(features, ensure_ascii=False),
            platform=platform,
            tone=tone,
        )
        session.add(req)
        session.commit()

        # Simpan deskripsi
        desc = Description(content=content, request_id=req.id)
        session.add(desc)
        session.commit()

        return {
            "id": desc.id,
            "product_name": product_name,
            "platform": platform,
            "tone": tone,
            "features": features,
            "content": content,
            "request_id": req.id,
            "created_at": desc.created_at.isoformat(),
        }

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_descriptions(page: int = 1, per_page: int = 20):
    """Ambil semua deskripsi dengan pagination."""
    session = SessionLocal()
    try:
        query = session.query(Description)
        total = query.count()
        items = (
            query.order_by(Description.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        data = []
        for d in items:
            req = session.query(ProductRequest).get(d.request_id)
            data.append({
                "id": d.id,
                "content": d.content,
                "request_id": d.request_id,
                "product_name": req.product_name if req else None,
                "platform": req.platform if req else None,
                "tone": req.tone if req else None,
                "features": json.loads(req.features) if req else [],
                "created_at": d.created_at.isoformat(),
            })

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if per_page > 0 else 0,
            "data": data,
        }
    finally:
        session.close()


def delete_description(description_id: int):
    """Hapus deskripsi berdasarkan ID."""
    session = SessionLocal()
    try:
        desc = session.query(Description).filter(Description.id == description_id).first()
        if not desc:
            return None
        session.delete(desc)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
