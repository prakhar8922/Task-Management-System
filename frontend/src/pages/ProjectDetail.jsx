import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { projectsAPI, tasksAPI } from '../services/api';
import './ProjectDetail.css';

const ProjectDetail = () => {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const [projectRes, tasksRes] = await Promise.all([
        projectsAPI.get(id),
        tasksAPI.list({ project: id }),
      ]);
      setProject(projectRes.data);
      setTasks(tasksRes.data.results || tasksRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!project) return <div>Project not found</div>;

  return (
    <div className="project-detail">
      <Link to="/projects" className="back-link">← Back to Projects</Link>
      <div className="project-header">
        <h1 className="page-title">{project.title}</h1>
        <Link to={`/tasks?project=${id}`} className="btn btn-primary">
          + Add Task
        </Link>
      </div>
      <p className="project-description">{project.description || 'No description'}</p>

      <div className="tasks-section">
        <h2>Tasks ({tasks.length})</h2>
        {tasks.length === 0 ? (
          <div className="empty-state">No tasks in this project yet.</div>
        ) : (
          <div className="tasks-list">
            {tasks.map((task) => (
              <Link key={task.id} to={`/tasks/${task.id}`} className="task-item">
                <div className="task-item-header">
                  <h3>{task.title}</h3>
                  <span className={`badge badge-${task.status === 'done' ? 'success' : task.status === 'in_progress' ? 'info' : 'warning'}`}>
                    {task.status}
                  </span>
                </div>
                {task.description && <p className="task-description">{task.description}</p>}
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectDetail;
