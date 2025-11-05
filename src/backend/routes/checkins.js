import express from 'express';
import { query } from '../database.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

// Helper function to calculate distance between two GPS coordinates (Haversine formula)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371e3; // Earth's radius in meters
  const φ1 = (lat1 * Math.PI) / 180;
  const φ2 = (lat2 * Math.PI) / 180;
  const Δφ = ((lat2 - lat1) * Math.PI) / 180;
  const Δλ = ((lon2 - lon1) * Math.PI) / 180;

  const a =
    Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return R * c; // Distance in meters
}

// Check-in (Clock in)
router.post('/checkin', authenticateToken, async (req, res) => {
  try {
    const { projectId, gpsLat, gpsLng, photoUrl, scheduledTime } = req.body;

    if (!projectId || !gpsLat || !gpsLng) {
      return res.status(400).json({
        error: 'Project ID, GPS latitude, and GPS longitude are required'
      });
    }

    // Get worker ID
    const workerResult = await query(
      'SELECT id FROM workers WHERE user_id = $1',
      [req.user.id]
    );

    if (workerResult.rows.length === 0) {
      return res.status(404).json({ error: 'Worker profile not found' });
    }

    const workerId = workerResult.rows[0].id;

    // Get project location and geofence radius
    const projectResult = await query(
      'SELECT gps_latitude, gps_longitude, geofence_radius_meters FROM projects WHERE id = $1',
      [projectId]
    );

    if (projectResult.rows.length === 0) {
      return res.status(404).json({ error: 'Project not found' });
    }

    const project = projectResult.rows[0];

    // Verify GPS location is within geofence
    if (project.gps_latitude && project.gps_longitude) {
      const distance = calculateDistance(
        parseFloat(gpsLat),
        parseFloat(gpsLng),
        parseFloat(project.gps_latitude),
        parseFloat(project.gps_longitude)
      );

      const maxDistance = project.geofence_radius_meters || 100;

      if (distance > maxDistance) {
        return res.status(403).json({
          error: 'Check-in location outside geofence',
          distance: Math.round(distance),
          maxDistance: maxDistance,
          message: `You are ${Math.round(distance)}m away from the site. Must be within ${maxDistance}m.`
        });
      }
    }

    // Check if worker is already checked in
    const activeCheckin = await query(
      'SELECT id FROM checkins WHERE worker_id = $1 AND checkout_time IS NULL',
      [workerId]
    );

    if (activeCheckin.rows.length > 0) {
      return res.status(409).json({
        error: 'Already checked in',
        checkinId: activeCheckin.rows[0].id
      });
    }

    // Determine if late (if scheduled time provided)
    let isLate = false;
    if (scheduledTime) {
      const scheduled = new Date(scheduledTime);
      const now = new Date();
      isLate = now > scheduled;
    }

    // Create check-in record
    const result = await query(
      `INSERT INTO checkins (worker_id, project_id, checkin_time, checkin_gps_lat, checkin_gps_lng, checkin_photo_url, is_late)
       VALUES ($1, $2, NOW(), $3, $4, $5, $6)
       RETURNING *`,
      [workerId, projectId, gpsLat, gpsLng, photoUrl || null, isLate]
    );

    res.status(201).json({
      message: 'Checked in successfully',
      checkin: result.rows[0]
    });
  } catch (error) {
    console.error('Check-in error:', error);
    res.status(500).json({ error: 'Check-in failed' });
  }
});

// Check-out (Clock out)
router.post('/checkout', authenticateToken, async (req, res) => {
  try {
    const { gpsLat, gpsLng, photoUrl, notes } = req.body;

    if (!gpsLat || !gpsLng) {
      return res.status(400).json({
        error: 'GPS latitude and longitude are required'
      });
    }

    // Get worker ID
    const workerResult = await query(
      'SELECT id FROM workers WHERE user_id = $1',
      [req.user.id]
    );

    if (workerResult.rows.length === 0) {
      return res.status(404).json({ error: 'Worker profile not found' });
    }

    const workerId = workerResult.rows[0].id;

    // Get active check-in
    const checkinResult = await query(
      'SELECT * FROM checkins WHERE worker_id = $1 AND checkout_time IS NULL ORDER BY checkin_time DESC LIMIT 1',
      [workerId]
    );

    if (checkinResult.rows.length === 0) {
      return res.status(404).json({ error: 'No active check-in found' });
    }

    const checkin = checkinResult.rows[0];

    // Calculate hours worked
    const checkinTime = new Date(checkin.checkin_time);
    const checkoutTime = new Date();
    const hoursWorked = (checkoutTime - checkinTime) / (1000 * 60 * 60);

    // Update check-in record with checkout info
    const result = await query(
      `UPDATE checkins
       SET checkout_time = NOW(),
           checkout_gps_lat = $1,
           checkout_gps_lng = $2,
           checkout_photo_url = $3,
           hours_worked = $4,
           notes = $5
       WHERE id = $6
       RETURNING *`,
      [gpsLat, gpsLng, photoUrl || null, hoursWorked.toFixed(2), notes || null, checkin.id]
    );

    res.json({
      message: 'Checked out successfully',
      checkin: result.rows[0],
      hoursWorked: hoursWorked.toFixed(2)
    });
  } catch (error) {
    console.error('Check-out error:', error);
    res.status(500).json({ error: 'Check-out failed' });
  }
});

// Get all check-ins (with filters)
router.get('/', authenticateToken, async (req, res) => {
  try {
    const { projectId, workerId, startDate, endDate } = req.query;

    let queryText = `
      SELECT c.*, w.first_name, w.last_name, p.name as project_name
      FROM checkins c
      JOIN workers w ON c.worker_id = w.id
      JOIN projects p ON c.project_id = p.id
      WHERE 1=1
    `;
    const params = [];

    if (projectId) {
      params.push(projectId);
      queryText += ` AND c.project_id = $${params.length}`;
    }

    if (workerId) {
      params.push(workerId);
      queryText += ` AND c.worker_id = $${params.length}`;
    }

    if (startDate) {
      params.push(startDate);
      queryText += ` AND c.checkin_time >= $${params.length}`;
    }

    if (endDate) {
      params.push(endDate);
      queryText += ` AND c.checkin_time <= $${params.length}`;
    }

    queryText += ' ORDER BY c.checkin_time DESC LIMIT 100';

    const result = await query(queryText, params);

    res.json({
      checkins: result.rows,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get check-ins error:', error);
    res.status(500).json({ error: 'Failed to get check-ins' });
  }
});

// Get active check-in for current user
router.get('/active', authenticateToken, async (req, res) => {
  try {
    const workerResult = await query(
      'SELECT id FROM workers WHERE user_id = $1',
      [req.user.id]
    );

    if (workerResult.rows.length === 0) {
      return res.status(404).json({ error: 'Worker profile not found' });
    }

    const workerId = workerResult.rows[0].id;

    const result = await query(
      `SELECT c.*, p.name as project_name, p.address as project_address
       FROM checkins c
       JOIN projects p ON c.project_id = p.id
       WHERE c.worker_id = $1 AND c.checkout_time IS NULL
       ORDER BY c.checkin_time DESC
       LIMIT 1`,
      [workerId]
    );

    if (result.rows.length === 0) {
      return res.json({ active: false, checkin: null });
    }

    res.json({
      active: true,
      checkin: result.rows[0]
    });
  } catch (error) {
    console.error('Get active check-in error:', error);
    res.status(500).json({ error: 'Failed to get active check-in' });
  }
});

export default router;
