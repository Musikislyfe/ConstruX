import express from 'express';
import { query } from '../database.js';
import { authenticateToken, authorizeRoles } from '../middleware/auth.js';

const router = express.Router();

// Get dashboard overview
router.get('/overview', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { projectId } = req.query;

    // Get overall stats
    const statsQuery = projectId
      ? 'SELECT * FROM dashboard_stats WHERE project_id = $1'
      : 'SELECT * FROM dashboard_stats';
    const statsParams = projectId ? [projectId] : [];

    const stats = await query(statsQuery, statsParams);

    // Get recent check-ins
    const recentCheckinsQuery = projectId
      ? `SELECT c.*, w.first_name, w.last_name, p.name as project_name
         FROM checkins c
         JOIN workers w ON c.worker_id = w.id
         JOIN projects p ON c.project_id = p.id
         WHERE c.project_id = $1
         ORDER BY c.checkin_time DESC
         LIMIT 10`
      : `SELECT c.*, w.first_name, w.last_name, p.name as project_name
         FROM checkins c
         JOIN workers w ON c.worker_id = w.id
         JOIN projects p ON c.project_id = p.id
         ORDER BY c.checkin_time DESC
         LIMIT 10`;

    const recentCheckins = await query(recentCheckinsQuery, projectId ? [projectId] : []);

    // Get task completion rate
    const taskStatsQuery = projectId
      ? `SELECT
           COUNT(*) as total_tasks,
           COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
           COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_tasks,
           COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_tasks
         FROM tasks
         WHERE project_id = $1`
      : `SELECT
           COUNT(*) as total_tasks,
           COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_tasks,
           COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_tasks,
           COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_tasks
         FROM tasks`;

    const taskStats = await query(taskStatsQuery, projectId ? [projectId] : []);

    // Get active workers count
    const activeWorkersQuery = projectId
      ? `SELECT COUNT(DISTINCT worker_id) as active_workers
         FROM checkins
         WHERE project_id = $1 AND checkout_time IS NULL`
      : `SELECT COUNT(DISTINCT worker_id) as active_workers
         FROM checkins
         WHERE checkout_time IS NULL`;

    const activeWorkers = await query(activeWorkersQuery, projectId ? [projectId] : []);

    // Get late check-ins count
    const lateCheckinsQuery = projectId
      ? `SELECT COUNT(*) as late_checkins
         FROM checkins
         WHERE project_id = $1 AND is_late = true AND checkin_time >= NOW() - INTERVAL '7 days'`
      : `SELECT COUNT(*) as late_checkins
         FROM checkins
         WHERE is_late = true AND checkin_time >= NOW() - INTERVAL '7 days'`;

    const lateCheckins = await query(lateCheckinsQuery, projectId ? [projectId] : []);

    // Get photo documentation stats
    const photoStatsQuery = projectId
      ? `SELECT
           COUNT(*) as total_photos,
           COUNT(CASE WHEN photo_type = 'before' THEN 1 END) as before_photos,
           COUNT(CASE WHEN photo_type = 'during' THEN 1 END) as during_photos,
           COUNT(CASE WHEN photo_type = 'after' THEN 1 END) as after_photos,
           COUNT(CASE WHEN ai_safety_flags IS NOT NULL AND array_length(ai_safety_flags, 1) > 0 THEN 1 END) as photos_with_safety_flags
         FROM photos ph
         JOIN tasks t ON ph.task_id = t.id
         WHERE t.project_id = $1`
      : `SELECT
           COUNT(*) as total_photos,
           COUNT(CASE WHEN photo_type = 'before' THEN 1 END) as before_photos,
           COUNT(CASE WHEN photo_type = 'during' THEN 1 END) as during_photos,
           COUNT(CASE WHEN photo_type = 'after' THEN 1 END) as after_photos,
           COUNT(CASE WHEN ai_safety_flags IS NOT NULL AND array_length(ai_safety_flags, 1) > 0 THEN 1 END) as photos_with_safety_flags
         FROM photos`;

    const photoStats = await query(photoStatsQuery, projectId ? [projectId] : []);

    res.json({
      projectStats: stats.rows,
      taskStats: taskStats.rows[0],
      activeWorkers: activeWorkers.rows[0].active_workers,
      lateCheckins: lateCheckins.rows[0].late_checkins,
      photoStats: photoStats.rows[0],
      recentCheckins: recentCheckins.rows
    });
  } catch (error) {
    console.error('Dashboard overview error:', error);
    res.status(500).json({ error: 'Failed to get dashboard data' });
  }
});

// Get time theft analytics
router.get('/time-theft', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { projectId, startDate, endDate } = req.query;

    let queryText = `
      SELECT
        w.id as worker_id,
        w.first_name,
        w.last_name,
        COUNT(*) as total_checkins,
        COUNT(CASE WHEN c.is_late THEN 1 END) as late_checkins,
        SUM(c.hours_worked) as total_hours,
        AVG(c.hours_worked) as avg_hours_per_shift,
        MIN(c.checkin_time::time) as earliest_checkin,
        MAX(c.checkin_time::time) as latest_checkin
      FROM workers w
      JOIN checkins c ON w.id = c.worker_id
      WHERE 1=1
    `;
    const params = [];

    if (projectId) {
      params.push(projectId);
      queryText += ` AND c.project_id = $${params.length}`;
    }

    if (startDate) {
      params.push(startDate);
      queryText += ` AND c.checkin_time >= $${params.length}`;
    }

    if (endDate) {
      params.push(endDate);
      queryText += ` AND c.checkin_time <= $${params.length}`;
    }

    queryText += ' GROUP BY w.id, w.first_name, w.last_name ORDER BY late_checkins DESC';

    const result = await query(queryText, params);

    res.json({
      analytics: result.rows,
      summary: {
        totalWorkers: result.rows.length,
        workersWithLateCheckins: result.rows.filter(w => w.late_checkins > 0).length,
        averageLateRate: result.rows.reduce((sum, w) => sum + (w.late_checkins / w.total_checkins), 0) / result.rows.length
      }
    });
  } catch (error) {
    console.error('Time theft analytics error:', error);
    res.status(500).json({ error: 'Failed to get time theft analytics' });
  }
});

// Get worker performance analytics
router.get('/worker-performance', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { workerId, startDate, endDate } = req.query;

    let queryText = `
      SELECT
        w.id,
        w.first_name,
        w.last_name,
        w.role,
        COUNT(DISTINCT ta.task_id) as tasks_assigned,
        COUNT(DISTINCT CASE WHEN t.status = 'completed' THEN t.id END) as tasks_completed,
        SUM(c.hours_worked) as total_hours,
        COUNT(DISTINCT c.id) as total_shifts,
        COUNT(ph.id) as photos_uploaded
      FROM workers w
      LEFT JOIN checkins c ON w.id = c.worker_id
      LEFT JOIN task_assignments ta ON w.id = ta.worker_id
      LEFT JOIN tasks t ON ta.task_id = t.id
      LEFT JOIN photos ph ON w.id = ph.worker_id
      WHERE 1=1
    `;
    const params = [];

    if (workerId) {
      params.push(workerId);
      queryText += ` AND w.id = $${params.length}`;
    }

    if (startDate) {
      params.push(startDate);
      queryText += ` AND c.checkin_time >= $${params.length}`;
    }

    if (endDate) {
      params.push(endDate);
      queryText += ` AND c.checkin_time <= $${params.length}`;
    }

    queryText += ' GROUP BY w.id, w.first_name, w.last_name, w.role ORDER BY tasks_completed DESC';

    const result = await query(queryText, params);

    res.json({
      workers: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Worker performance error:', error);
    res.status(500).json({ error: 'Failed to get worker performance data' });
  }
});

// Get cost analytics
router.get('/cost-analytics', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { projectId } = req.query;

    let queryText = `
      SELECT
        p.id as project_id,
        p.name as project_name,
        p.budget,
        SUM(c.hours_worked * w.hourly_rate) as actual_labor_cost,
        p.budget - SUM(c.hours_worked * w.hourly_rate) as budget_remaining,
        ((SUM(c.hours_worked * w.hourly_rate) / p.budget) * 100) as budget_used_percent,
        COUNT(DISTINCT w.id) as workers_on_project,
        SUM(c.hours_worked) as total_hours_worked
      FROM projects p
      LEFT JOIN checkins c ON p.id = c.project_id
      LEFT JOIN workers w ON c.worker_id = w.id
      WHERE p.status = 'active'
    `;
    const params = [];

    if (projectId) {
      params.push(projectId);
      queryText += ` AND p.id = $${params.length}`;
    }

    queryText += ' GROUP BY p.id, p.name, p.budget';

    const result = await query(queryText, params);

    res.json({
      projects: result.rows,
      totalBudget: result.rows.reduce((sum, p) => sum + parseFloat(p.budget || 0), 0),
      totalCost: result.rows.reduce((sum, p) => sum + parseFloat(p.actual_labor_cost || 0), 0)
    });
  } catch (error) {
    console.error('Cost analytics error:', error);
    res.status(500).json({ error: 'Failed to get cost analytics' });
  }
});

export default router;
