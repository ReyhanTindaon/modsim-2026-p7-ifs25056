from flask import Blueprint, request, jsonify
from app.services.description_service import (
    create_description,
    get_all_descriptions,
    delete_description,
)

description_bp = Blueprint("description", __name__)

VALID_PLATFORMS = ["Tokopedia", "Shopee", "Lazada", "TikTok Shop", "Bukalapak", "Lainnya"]
VALID_TONES = ["formal", "santai", "persuasif"]


@description_bp.route("/descriptions/generate", methods=["POST"])
def generate():
    """POST /descriptions/generate - Generate deskripsi produk."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body harus berupa JSON"}), 400

    product_name = data.get("product_name", "").strip()
    features = data.get("features", [])
    platform = data.get("platform", "").strip()
    tone = data.get("tone", "").strip()

    if not product_name:
        return jsonify({"error": "product_name wajib diisi"}), 400
    if not features or not isinstance(features, list) or len(features) == 0:
        return jsonify({"error": "features wajib diisi dan berupa list"}), 400
    if not platform:
        return jsonify({"error": "platform wajib diisi"}), 400
    if not tone:
        return jsonify({"error": "tone wajib diisi"}), 400
    if tone not in VALID_TONES:
        return jsonify({"error": f"tone harus salah satu dari: {', '.join(VALID_TONES)}"}), 400

    try:
        result = create_description(product_name, features, platform, tone)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@description_bp.route("/descriptions", methods=["GET"])
def get_all():
    """GET /descriptions - Ambil semua deskripsi."""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=20, type=int)
    data = get_all_descriptions(page=page, per_page=per_page)
    return jsonify(data)


@description_bp.route("/descriptions/<int:description_id>", methods=["DELETE"])
def delete(description_id):
    """DELETE /descriptions/<id> - Hapus deskripsi."""
    result = delete_description(description_id)
    if result is None:
        return jsonify({"error": "Deskripsi tidak ditemukan"}), 404
    return jsonify({"message": f"Deskripsi dengan id {description_id} berhasil dihapus"}), 200
