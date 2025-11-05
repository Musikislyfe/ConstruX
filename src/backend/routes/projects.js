import express from 'express';
import { query } from '../database.js';
import { authenticateToken, authorizeRoles } from '../middleware/auth.js';

const router = express.Router();

// Get all projects
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { status } = req.query;

    let queryText = `
      SELECT p.*,
        (SELECT COUNT(*) FROM tasks WHERE project_id = p.id) as total_tasks,
        (SELECT COUNT(*) FROM tasks WHERE project_id = p.id AND status = 'completed') as completed_tasks,
        (SELECT COUNT(DISTINCT worker_id) FROM checkins WHERE project_id = p.id) as total_workers
      FROM projects p
      WHERE 1=1
    `;
    const params = [];

    if (status) {
      params.push(status);
      queryText += ` AND p.status = $${params.length}`;
    }

    queryText += ' ORDER BY p.created_at DESC';

    const result = await query(queryText, params);

    res.json({
      projects: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get projects error:', error);
    res.status(500).json({ error: 'Failed to get projects' });
  }
});

// Get single project
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT p.*,
        (SELECT COUNT(*) FROM tasks WHERE project_id = p.id) as total_tasks,
        (SELECT COUNT(*) FROM tasks WHERE project_id = p.id AND status = 'completed') as completed_tasks,
        (SELECT COUNT(*) FROM tasks WHERE project_id = p.id AND status = 'in_progress') as in_progress_tasks,
        (SELECT COUNT(DISTINCT worker_id) FROM checkins WHERE project_id = p.id) as total_workers,
        (SELECT SUM(hours_worked) FROM checkins WHERE project_id = p.id) as total_hours_worked,
        (SELECT COUNT(*) FROM photos ph JOIN tasks t ON ph.task_id = t.id WHERE t.project_id = p.id) as total_photos
      FROM projects p
      WHERE p.id = $1`,
      [req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Project not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get project error:', error);
    res.status(500).json({ error: 'Failed to get project' });
  }
});

// Create new project
router.post('/', authenticateToken, authorizeRoles('admin'), async (req, res) => {
  try {
    const {
      name,
      address,
      gpsLatitude,
      gpsLongitude,
      geofenceRadiusMeters = 100,
      startDate,
      estimatedCompletion,
      budget
    } = req.body;

    if (!name || !address) {
      return res.status(400).json({ error: 'Name and address are required' });
    }

    const result = await query(
      `INSERT INTO projects (name, address, gps_latitude, gps_longitude, geofence_radius_meters, start_date, estimated_completion, budget)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
       RETURNING *`,
      [
        name,
        address,
        gpsLatitude || null,
        gpsLongitude || null,
        geofenceRadiusMeters,
        startDate || null,
        estimatedCompletion || null,
        budget || null
      ]
    );

    res.status(201).json({
      message: 'Project created successfully',
      project: result.rows[0]
    });
  } catch (error) {
    console.error('Create project error:', error);
    res.status(500).json({ error: 'Failed to create project' });
  }
});

// Update project
router.put('/:id', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const {
      name,
      address,
      gpsLatitude,
      gpsLongitude,
      geofenceRadiusMeters,
      status,
      startDate,
      estimatedCompletion,
      budget
    } = req.body;

    const updates = [];
    const params = [];
    let paramCount = 1;

    if (name !== undefined) {
      params.push(name);
      updates.push(`name = $${paramCount++}`);
    }
    if (address !== undefined) {
      params.push(address);
      updates.push(`address = $${paramCount++}`);
    }
    if (gpsLatitude !== undefined) {
      params.push(gpsLatitude);
      updates.push(`gps_latitude = $${paramCount++}`);
    }
    if (gpsLongitude !== undefined) {
      params.push(gpsLongitude);
      updates.push(`gps_longitude = $${paramCount++}`);
    }
    if (geofenceRadiusMeters !== undefined) {
      params.push(geofenceRadiusMeters);
      updates.push(`geofence_radius_meters = $${paramCount++}`);
    }
    if (status !== undefined) {
      params.push(status);
      updates.push(`status = $${paramCount++}`);
    }
    if (startDate !== undefined) {
      params.push(startDate);
      updates.push(`start_date = $${paramCount++}`);
    }
    if (estimatedCompletion !== undefined) {
      params.push(estimatedCompletion);
      updates.push(`estimated_completion = $${paramCount++}`);
    }
    if (budget !== undefined) {
      params.push(budget);
      updates.push(`budget = $${paramCount++}`);
    }

    if (updates.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }

    params.push(req.params.id);
    const queryText = `UPDATE projects SET ${updates.join(', ')} WHERE id = $${paramCount} RETURNING *`;

    const result = await query(queryText, params);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Project not found' });
    }

    res.json({
      message: 'Project updated successfully',
      project: result.rows[0]
    });
  } catch (error) {
    console.error('Update project error:', error);
    res.status(500).json({ error: 'Failed to update project' });
  }
});

// Delete project
router.delete('/:id', authenticateToken, authorizeRoles('admin'), async (req, res) => {
  try {
    const result = await query('DELETE FROM projects WHERE id = $1 RETURNING id', [req.params.id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Project not found' });
    }

    res.json({ message: 'Project deleted successfully' });
  } catch (error) {
    console.error('Delete project error:', error);
    res.status(500).json({ error: 'Failed to delete project' });
  }
});

export default router;
