import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:5000";

function Comments() {
  const [comments, setComments] = useState([]);
  const [text, setText] = useState("");
  const [editId, setEditId] = useState(null);

  // Fetch comments
  const fetchComments = async () => {
    try {
      const res = await axios.get(`${API_URL}/comments`);
      setComments(res.data);
    } catch (err) {
      console.error("Error fetching comments:", err);
      alert("Could not fetch comments. Make sure backend is running!");
    }
  };

  useEffect(() => {
    fetchComments();
  }, []);

  // Add or Update comment
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await axios.put(`${API_URL}/comments/${editId}`, { text });
        setEditId(null);
      } else {
        await axios.post(`${API_URL}/comments`, { text });
      }
      setText("");
      fetchComments();
    } catch (err) {
      console.error("Error adding/updating comment:", err);
      alert("Could not add/update comment.");
    }
  };

  // Edit comment
  const handleEdit = (comment) => {
    setText(comment.text);
    setEditId(comment.id);
  };

  // Delete comment
  const handleDelete = async (id) => {
    try {
      await axios.delete(`${API_URL}/comments/${id}`);
      fetchComments();
    } catch (err) {
      console.error("Error deleting comment:", err);
      alert("Could not delete comment.");
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "20px auto" }}>
      <h2>Comments</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter comment"
          style={{ width: "70%" }}
          required
        />
        <button type="submit">{editId ? "Update" : "Add"}</button>
      </form>

      <ul>
        {comments.map((c) => (
          <li key={c.id} style={{ marginBottom: "8px" }}>
            {c.text}{" "}
            <button onClick={() => handleEdit(c)} style={{ marginRight: "4px" }}>
              Edit
            </button>
            <button onClick={() => handleDelete(c.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Comments;
