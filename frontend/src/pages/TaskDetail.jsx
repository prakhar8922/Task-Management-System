import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { tasksAPI, commentsAPI } from '../services/api';
import './TaskDetail.css';

const TaskDetail = () => {
  const { id } = useParams();
  const [task, setTask] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [taskRes, commentsRes] = await Promise.all([
        tasksAPI.get(id),
        commentsAPI.list(id),
      ]);
      setTask(taskRes.data);
      setComments(commentsRes.data.results || commentsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    setError('');
    try {
      await commentsAPI.create({ task: id, content: newComment });
      setNewComment('');
      fetchData();
    } catch (err) {
      setError('Failed to add comment');
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!task) return <div>Task not found</div>;

  return (
    <div className="task-detail">
      <Link to="/tasks" className="back-link">← Back to Tasks</Link>
      <div className="task-header">
        <h1 className="page-title">{task.title}</h1>
        <span className={`badge badge-${task.status === 'done' ? 'success' : task.status === 'in_progress' ? 'info' : 'warning'}`}>
          {task.status}
        </span>
      </div>
      
      {task.description && <p className="task-description">{task.description}</p>}
      
      <div className="task-info">
        <div className="info-item">
          <strong>Priority:</strong> <span className={`priority-${task.priority}`}>{task.priority}</span>
        </div>
        {task.project_detail && (
          <div className="info-item">
            <strong>Project:</strong> <Link to={`/projects/${task.project}`}>{task.project_detail.title}</Link>
          </div>
        )}
      </div>

      <div className="comments-section">
        <h2>Comments ({comments.length})</h2>
        <form onSubmit={handleAddComment} className="comment-form">
          <textarea
            className="form-textarea"
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Add a comment..."
            rows="3"
          />
          {error && <div className="error-message">{error}</div>}
          <button type="submit" className="btn btn-primary">Add Comment</button>
        </form>
        
        <div className="comments-list">
          {comments.map((comment) => (
            <div key={comment.id} className="comment-item">
              <div className="comment-header">
                <strong>{comment.author_detail?.email || 'User'}</strong>
                <span className="comment-date">
                  {new Date(comment.created_at).toLocaleDateString()}
                </span>
              </div>
              <p className="comment-content">{comment.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskDetail;
