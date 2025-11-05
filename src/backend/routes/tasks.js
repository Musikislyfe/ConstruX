import express from 'express';
import { query } from '../database.js';
import { authenticateToken, authorizeRoles } from '../middleware/auth.js';

const router = express.Router();

// Get all tasks
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { projectId, status, workerId } = req.query;

    let queryText = `
      SELECT t.*, p.name as project_name,
        (SELECT COUNT(*) FROM photos WHERE task_id = t.id) as photo_count,
        (SELECT json_agg(json_build_object('id', w.id, 'first_name', w.first_name, 'last_name', w.last_name))
         FROM task_assignments ta
         JOIN workers w ON ta.worker_id = w.id
         WHERE ta.task_id = t.id) as assigned_workers
      FROM tasks t
      JOIN projects p ON t.project_id = p.id
      WHERE 1=1
    `;
    const params = [];

    if (projectId) {
      params.push(projectId);
      queryText += ` AND t.project_id = $${params.length}`;
    }

    if (status) {
      params.push(status);
      queryText += ` AND t.status = $${params.length}`;
    }

    if (workerId) {
      params.push(workerId);
      queryText += ` AND EXISTS (SELECT 1 FROM task_assignments WHERE task_id = t.id AND worker_id = $${params.length})`;
    }

    queryText += ' ORDER BY t.created_at DESC';

    const result = await query(queryText, params);

    res.json({
      tasks: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get tasks error:', error);
    res.status(500).json({ error: 'Failed to get tasks' });
  }
});

// Get single task
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT t.*, p.name as project_name, p.address as project_address,
        (SELECT json_agg(json_build_object(
          'id', ph.id,
          'photo_type', ph.photo_type,
          'photo_url', ph.photo_url,
          'uploaded_at', ph.uploaded_at,
          'worker_name', w.first_name || ' ' || w.last_name
        ) ORDER BY ph.uploaded_at)
        FROM photos ph
        JOIN workers w ON ph.worker_id = w.id
        WHERE ph.task_id = t.id) as photos,
        (SELECT json_agg(json_build_object('id', w.id, 'first_name', w.first_name, 'last_name', w.last_name))
         FROM task_assignments ta
         JOIN workers w ON ta.worker_id = w.id
         WHERE ta.task_id = t.id) as assigned_workers
      FROM tasks t
      JOIN projects p ON t.project_id = p.id
      WHERE t.id = $1`,
      [req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get task error:', error);
    res.status(500).json({ error: 'Failed to get task' });
  }
});

// Create new task
router.post('/', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const {
      projectId,
      title,
      description,
      location,
      priority = 'medium',
      estimatedHours,
      dueDate,
      assignedWorkers = []
    } = req.body;

    if (!projectId || !title) {
      return res.status(400).json({ error: 'Project ID and title are required' });
    }

    // Create task
    const taskResult = await query(
      `INSERT INTO tasks (project_id, title, description, location, priority, estimated_hours, due_date)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [projectId, title, description || null, location || null, priority, estimatedHours || null, dueDate || null]
    );

    const task = taskResult.rows[0];

    // Assign workers
    if (assignedWorkers.length > 0) {
      for (const workerId of assignedWorkers) {
        await query(
          'INSERT INTO task_assignments (task_id, worker_id) VALUES ($1, $2)',
          [task.id, workerId]
        );
      }
    }

    res.status(201).json({
      message: 'Task created successfully',
      task
    });
  } catch (error) {
    console.error('Create task error:', error);
    res.status(500).json({ error: 'Failed to create task' });
  }
});

// Update task
router.put('/:id', authenticateToken, async (req, res) => {
  try {
    const {
      title,
      description,
      location,
      status,
      priority,
      estimatedHours,
      actualHours,
      dueDate
    } = req.body;

    const updates = [];
    const params = [];
    let paramCount = 1;

    if (title !== undefined) {
      params.push(title);
      updates.push(`title = $${paramCount++}`);
    }
    if (description !== undefined) {
      params.push(description);
      updates.push(`description = $${paramCount++}`);
    }
    if (location !== undefined) {
      params.push(location);
      updates.push(`location = $${paramCount++}`);
    }
    if (status !== undefined) {
      params.push(status);
      updates.push(`status = $${paramCount++}`);
      if (status === 'completed') {
        updates.push(`completed_at = NOW()`);
      }
    }
    if (priority !== undefined) {
      params.push(priority);
      updates.push(`priority = $${paramCount++}`);
    }
    if (estimatedHours !== undefined) {
      params.push(estimatedHours);
      updates.push(`estimated_hours = $${paramCount++}`);
    }
    if (actualHours !== undefined) {
      params.push(actualHours);
      updates.push(`actual_hours = $${paramCount++}`);
    }
    if (dueDate !== undefined) {
      params.push(dueDate);
      updates.push(`due_date = $${paramCount++}`);
    }

    if (updates.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }

    params.push(req.params.id);
    const queryText = `UPDATE tasks SET ${updates.join(', ')} WHERE id = $${paramCount} RETURNING *`;

    const result = await query(queryText, params);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }

    res.json({
      message: 'Task updated successfully',
      task: result.rows[0]
    });
  } catch (error) {
    console.error('Update task error:', error);
    res.status(500).json({ error: 'Failed to update task' });
  }
});

// Delete task
router.delete('/:id', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const result = await query('DELETE FROM tasks WHERE id = $1 RETURNING id', [req.params.id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }

    res.json({ message: 'Task deleted successfully' });
  } catch (error) {
    console.error('Delete task error:', error);
    res.status(500).json({ error: 'Failed to delete task' });
  }
});

// Assign worker to task
router.post('/:id/assign', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { workerId } = req.body;

    if (!workerId) {
      return res.status(400).json({ error: 'Worker ID is required' });
    }

    await query(
      'INSERT INTO task_assignments (task_id, worker_id) VALUES ($1, $2) ON CONFLICT DO NOTHING',
      [req.params.id, workerId]
    );

    res.json({ message: 'Worker assigned to task successfully' });
  } catch (error) {
    console.error('Assign worker error:', error);
    res.status(500).json({ error: 'Failed to assign worker' });
  }
});

// Unassign worker from task
router.post('/:id/unassign', authenticateToken, authorizeRoles('admin', 'supervisor'), async (req, res) => {
  try {
    const { workerId } = req.body;

    if (!workerId) {
      return res.status(400).json({ error: 'Worker ID is required' });
    }

    await query(
      'DELETE FROM task_assignments WHERE task_id = $1 AND worker_id = $2',
      [req.params.id, workerId]
    );

    res.json({ message: 'Worker unassigned from task successfully' });
  } catch (error) {
    console.error('Unassign worker error:', error);
    res.status(500).json({ error: 'Failed to unassign worker' });
  }
});

export default router;
