from flask import Blueprint, request, jsonify
from .database import db
from .models import Comment

api = Blueprint("api", __name__)

# Health check
@api.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "Backend is running"})


# CREATE a comment
@api.route("/comments", methods=["POST"])
def create_comment():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    comment = Comment(text=text)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"id": comment.id, "text": comment.text}), 201


# READ all comments
@api.route("/comments", methods=["GET"])
def get_comments():
    comments = Comment.query.all()
    return jsonify(
        [{"id": c.id, "text": c.text} for c in comments]
    ), 200


# UPDATE a comment
@api.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    data = request.get_json()

    comment.text = data.get("text", comment.text)
    db.session.commit()

    return jsonify({"id": comment.id, "text": comment.text}), 200


# DELETE a comment
@api.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted"}), 200
