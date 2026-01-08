import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { projectsAPI, tasksAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    projects: 0,
    tasks: 0,
    tasksTodo: 0,
    tasksInProgress: 0,
  });
  const [recentProjects, setRecentProjects] = useState([]);
  const [recentTasks, setRecentTasks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [projectsRes, tasksRes] = await Promise.all([
        projectsAPI.list(),
        tasksAPI.list(),
      ]);

      const projects = projectsRes.data.results || projectsRes.data;
      const tasks = tasksRes.data.results || tasksRes.data;

      setStats({
        projects: projects.length,
        tasks: tasks.length,
        tasksTodo: tasks.filter(t => t.status === 'todo').length,
        tasksInProgress: tasks.filter(t => t.status === 'in_progress').length,
      });

      setRecentProjects(projects.slice(0, 5));
      setRecentTasks(tasks.slice(0, 5));
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1 className="page-title">Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📁</div>
          <div className="stat-content">
            <div className="stat-value">{stats.projects}</div>
            <div className="stat-label">Projects</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <div className="stat-value">{stats.tasks}</div>
            <div className="stat-label">Total Tasks</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📋</div>
          <div className="stat-content">
            <div className="stat-value">{stats.tasksTodo}</div>
            <div className="stat-label">To Do</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔄</div>
          <div className="stat-content">
            <div className="stat-value">{stats.tasksInProgress}</div>
            <div className="stat-label">In Progress</div>
          </div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <div className="card-header flex-between">
            <h2 className="card-title">Recent Projects</h2>
            <Link to="/projects" className="btn btn-secondary btn-sm">
              View All
            </Link>
          </div>
          <div className="card-body">
            {recentProjects.length === 0 ? (
              <p className="text-secondary">No projects yet. <Link to="/projects">Create one</Link></p>
            ) : (
              <ul className="list">
                {recentProjects.map((project) => (
                  <li key={project.id} className="list-item">
                    <Link to={`/projects/${project.id}`} className="list-link">
                      <div className="list-title">{project.title}</div>
                      <div className="list-meta">{project.task_count || 0} tasks</div>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header flex-between">
            <h2 className="card-title">Recent Tasks</h2>
            <Link to="/tasks" className="btn btn-secondary btn-sm">
              View All
            </Link>
          </div>
          <div className="card-body">
            {recentTasks.length === 0 ? (
              <p className="text-secondary">No tasks yet. <Link to="/tasks">Create one</Link></p>
            ) : (
              <ul className="list">
                {recentTasks.map((task) => (
                  <li key={task.id} className="list-item">
                    <Link to={`/tasks/${task.id}`} className="list-link">
                      <div className="list-title">{task.title}</div>
                      <div className="list-meta">
                        <span className={`status-${task.status}`}>{task.status}</span>
                        {task.project_title && <span> • {task.project_title}</span>}
                      </div>
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
