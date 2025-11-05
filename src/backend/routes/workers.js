import express from 'express';
import { query } from '../database.js';
import { authenticateToken, authorizeRoles } from '../middleware/auth.js';

const router = express.Router();

// Get all workers
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { isActive } = req.query;

    let queryText = `
      SELECT w.*, u.email, u.role as user_role,
        (SELECT COUNT(*) FROM task_assignments WHERE worker_id = w.id) as tasks_assigned,
        (SELECT COUNT(*) FROM checkins WHERE worker_id = w.id) as total_checkins,
        (SELECT SUM(hours_worked) FROM checkins WHERE worker_id = w.id) as total_hours
      FROM workers w
      LEFT JOIN users u ON w.user_id = u.id
      WHERE 1=1
    `;
    const params = [];

    if (isActive !== undefined) {
      params.push(isActive === 'true');
      queryText += ` AND w.is_active = $${params.length}`;
    }

    queryText += ' ORDER BY w.created_at DESC';

    const result = await query(queryText, params);

    res.json({
      workers: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get workers error:', error);
    res.status(500).json({ error: 'Failed to get workers' });
  }
});

// Get single worker
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT w.*, u.email, u.role as user_role,
        (SELECT json_agg(json_build_object(
          'id', t.id,
          'title', t.title,
          'status', t.status,
          'project_name', p.name
        ))
        FROM task_assignments ta
        JOIN tasks t ON ta.task_id = t.id
        JOIN projects p ON t.project_id = p.id
        WHERE ta.worker_id = w.id) as assigned_tasks,
        (SELECT COUNT(*) FROM checkins WHERE worker_id = w.id) as total_checkins,
        (SELECT SUM(hours_worked) FROM checkins WHERE worker_id = w.id) as total_hours,
        (SELECT COUNT(*) FROM photos WHERE worker_id = w.id) as photos_uploaded
      FROM workers w
      LEFT JOIN users u ON w.user_id = u.id
      WHERE w.id = $1`,
      [req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Worker not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get worker error:', error);
    res.status(500).json({ error: 'Failed to get worker' });
  }
});

// Create new worker
router.post('/', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const {
      userId,
      firstName,
      lastName,
      phone,
      role,
      hourlyRate
    } = req.body;

    if (!firstName || !lastName) {
      return res.status(400).json({ error: 'First name and last name are required' });
    }

    const result = await query(
      `INSERT INTO workers (user_id, first_name, last_name, phone, role, hourly_rate)
       VALUES ($1, $2, $3, $4, $5, $6)
       RETURNING *`,
      [userId || null, firstName, lastName, phone || null, role || null, hourlyRate || null]
    );

    res.status(201).json({
      message: 'Worker created successfully',
      worker: result.rows[0]
    });
  } catch (error) {
    console.error('Create worker error:', error);
    res.status(500).json({ error: 'Failed to create worker' });
  }
});

// Update worker
router.put('/:id', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const {
      firstName,
      lastName,
      phone,
      role,
      hourlyRate,
      isActive
    } = req.body;

    const updates = [];
    const params = [];
    let paramCount = 1;

    if (firstName !== undefined) {
      params.push(firstName);
      updates.push(`first_name = $${paramCount++}`);
    }
    if (lastName !== undefined) {
      params.push(lastName);
      updates.push(`last_name = $${paramCount++}`);
    }
    if (phone !== undefined) {
      params.push(phone);
      updates.push(`phone = $${paramCount++}`);
    }
    if (role !== undefined) {
      params.push(role);
      updates.push(`role = $${paramCount++}`);
    }
    if (hourlyRate !== undefined) {
      params.push(hourlyRate);
      updates.push(`hourly_rate = $${paramCount++}`);
    }
    if (isActive !== undefined) {
      params.push(isActive);
      updates.push(`is_active = $${paramCount++}`);
    }

    if (updates.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }

    params.push(req.params.id);
    const queryText = `UPDATE workers SET ${updates.join(', ')} WHERE id = $${paramCount} RETURNING *`;

    const result = await query(queryText, params);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Worker not found' });
    }

    res.json({
      message: 'Worker updated successfully',
      worker: result.rows[0]
    });
  } catch (error) {
    console.error('Update worker error:', error);
    res.status(500).json({ error: 'Failed to update worker' });
  }
});

// Delete worker
router.delete('/:id', authenticateToken, authorizeRoles('admin'), async (req, res) => {
  try {
    const result = await query('DELETE FROM workers WHERE id = $1 RETURNING id', [req.params.id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Worker not found' });
    }

    res.json({ message: 'Worker deleted successfully' });
  } catch (error) {
    console.error('Delete worker error:', error);
    res.status(500).json({ error: 'Failed to delete worker' });
  }
});

// Get worker's check-in history
router.get('/:id/checkins', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT c.*, p.name as project_name, p.address as project_address
       FROM checkins c
       JOIN projects p ON c.project_id = p.id
       WHERE c.worker_id = $1
       ORDER BY c.checkin_time DESC
       LIMIT 50`,
      [req.params.id]
    );

    res.json({
      checkins: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get worker checkins error:', error);
    res.status(500).json({ error: 'Failed to get worker checkins' });
  }
});

export default router;
