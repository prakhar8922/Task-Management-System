import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { tasksAPI, projectsAPI } from '../services/api';
import './Tasks.css';

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [searchParams] = useSearchParams();
  const projectFilter = searchParams.get('project');
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    project: projectFilter || '',
    status: 'todo',
    priority: 'medium',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProjects();
    fetchTasks();
  }, [projectFilter]);

  const fetchProjects = async () => {
    try {
      const response = await projectsAPI.list();
      setProjects(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    }
  };

  const fetchTasks = async () => {
    try {
      const params = projectFilter ? { project: projectFilter } : {};
      const response = await tasksAPI.list(params);
      setTasks(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await tasksAPI.create(formData);
      setShowModal(false);
      setFormData({ title: '', description: '', project: '', status: 'todo', priority: 'medium' });
      fetchTasks();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to create task');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await tasksAPI.delete(id);
      fetchTasks();
    } catch (error) {
      alert('Failed to delete task');
    }
  };

  if (loading) return <div className="loading">Loading tasks...</div>;

  return (
    <div className="tasks-page">
      <div className="page-header flex-between">
        <h1 className="page-title">Tasks</h1>
        <button onClick={() => setShowModal(true)} className="btn btn-primary">
          + New Task
        </button>
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <h2>Create New Task</h2>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label className="form-label">Title</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="form-label">Project</label>
                <select
                  className="form-select"
                  value={formData.project}
                  onChange={(e) => setFormData({ ...formData, project: e.target.value })}
                  required
                >
                  <option value="">Select a project</option>
                  {projects.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Status</label>
                  <select
                    className="form-select"
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="todo">To Do</option>
                    <option value="in_progress">In Progress</option>
                    <option value="review">Review</option>
                    <option value="done">Done</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Priority</label>
                  <select
                    className="form-select"
                    value={formData.priority}
                    onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label className="form-label">Description</label>
                <textarea
                  className="form-textarea"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div className="modal-actions">
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {tasks.length === 0 ? (
        <div className="empty-state">
          <p>No tasks yet. Create your first task to get started!</p>
        </div>
      ) : (
        <div className="tasks-grid">
          {tasks.map((task) => (
            <div key={task.id} className="task-card">
              <div className="task-header">
                <Link to={`/tasks/${task.id}`} className="task-title-link">
                  <h3>{task.title}</h3>
                </Link>
                <button onClick={() => handleDelete(task.id)} className="btn-icon">🗑️</button>
              </div>
              {task.description && <p className="task-description">{task.description}</p>}
              <div className="task-meta">
                <span className={`badge badge-${task.status === 'done' ? 'success' : task.status === 'in_progress' ? 'info' : 'warning'}`}>
                  {task.status}
                </span>
                <span className={`priority-${task.priority}`}>{task.priority}</span>
                {task.project_title && <span className="project-badge">{task.project_title}</span>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Tasks;
