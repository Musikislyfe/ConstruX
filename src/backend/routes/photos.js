import express from 'express';
import multer from 'multer';
import path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { GoogleGenerativeAI } from '@google/generative-ai';
import fs from 'fs/promises';
import { query } from '../database.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const uniqueName = `${uuidv4()}${path.extname(file.originalname)}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: parseInt(process.env.MAX_FILE_SIZE) || 10 * 1024 * 1024 // 10MB default
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);

    if (extname && mimetype) {
      cb(null, true);
    } else {
      cb(new Error('Only image files are allowed'));
    }
  }
});

// Initialize Gemini AI (if API key is provided)
let genAI = null;
if (process.env.GEMINI_API_KEY) {
  genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
}

// Helper function to analyze photo with Gemini AI
async function analyzePhotoWithAI(imagePath, photoType) {
  if (!genAI) {
    return { analysis: 'AI analysis not configured', safetyFlags: [] };
  }

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' });

    // Read image file
    const imageData = await fs.readFile(imagePath);
    const base64Image = imageData.toString('base64');

    const prompt = `Analyze this construction site ${photoType} photo. Provide:
1. Quality assessment (good/fair/poor)
2. Safety concerns (list any PPE violations, hazards, or unsafe conditions)
3. Work status (what work is visible)
4. Materials visible
5. Any recommendations

Format your response as JSON with keys: quality, safety_concerns (array), work_status, materials (array), recommendations (array)`;

    const result = await model.generateContent([
      { inlineData: { mimeType: 'image/jpeg', data: base64Image } },
      prompt
    ]);

    const response = await result.response;
    const text = response.text();

    // Try to parse JSON response
    try {
      const jsonMatch = text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const analysis = JSON.parse(jsonMatch[0]);
        return {
          analysis: text,
          safetyFlags: analysis.safety_concerns || []
        };
      }
    } catch (e) {
      // If JSON parsing fails, return raw text
    }

    return {
      analysis: text,
      safetyFlags: []
    };
  } catch (error) {
    console.error('AI analysis error:', error);
    return {
      analysis: 'AI analysis failed: ' + error.message,
      safetyFlags: []
    };
  }
}

// Upload photo
router.post('/upload', authenticateToken, upload.single('photo'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { taskId, photoType, notes, analyzeWithAI = false } = req.body;

    if (!taskId || !photoType) {
      return res.status(400).json({ error: 'Task ID and photo type are required' });
    }

    if (!['before', 'during', 'after'].includes(photoType)) {
      return res.status(400).json({ error: 'Photo type must be before, during, or after' });
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

    // Create photo URL
    const photoUrl = `/uploads/${req.file.filename}`;

    // Analyze with AI if requested
    let aiAnalysis = null;
    let safetyFlags = [];

    if (analyzeWithAI === 'true' || analyzeWithAI === true) {
      const aiResult = await analyzePhotoWithAI(req.file.path, photoType);
      aiAnalysis = aiResult.analysis;
      safetyFlags = aiResult.safetyFlags;
    }

    // Save photo record
    const result = await query(
      `INSERT INTO photos (task_id, worker_id, photo_type, photo_url, notes, ai_analysis_result, ai_safety_flags)
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [taskId, workerId, photoType, photoUrl, notes || null, aiAnalysis, safetyFlags.length > 0 ? safetyFlags : null]
    );

    res.status(201).json({
      message: 'Photo uploaded successfully',
      photo: result.rows[0]
    });
  } catch (error) {
    console.error('Photo upload error:', error);
    res.status(500).json({ error: 'Photo upload failed' });
  }
});

// Get photos for a task
router.get('/task/:taskId', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT p.*, w.first_name, w.last_name
       FROM photos p
       JOIN workers w ON p.worker_id = w.id
       WHERE p.task_id = $1
       ORDER BY p.photo_type, p.uploaded_at`,
      [req.params.taskId]
    );

    // Group by photo type
    const grouped = {
      before: result.rows.filter(p => p.photo_type === 'before'),
      during: result.rows.filter(p => p.photo_type === 'during'),
      after: result.rows.filter(p => p.photo_type === 'after')
    };

    res.json({
      photos: result.rows,
      grouped,
      count: result.rows.length
    });
  } catch (error) {
    console.error('Get photos error:', error);
    res.status(500).json({ error: 'Failed to get photos' });
  }
});

// Get single photo
router.get('/:id', authenticateToken, async (req, res) => {
  try {
    const result = await query(
      `SELECT p.*, w.first_name, w.last_name, t.title as task_title
       FROM photos p
       JOIN workers w ON p.worker_id = w.id
       JOIN tasks t ON p.task_id = t.id
       WHERE p.id = $1`,
      [req.params.id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    res.json(result.rows[0]);
  } catch (error) {
    console.error('Get photo error:', error);
    res.status(500).json({ error: 'Failed to get photo' });
  }
});

// Analyze existing photo with AI
router.post('/:id/analyze', authenticateToken, async (req, res) => {
  try {
    const photoResult = await query(
      'SELECT * FROM photos WHERE id = $1',
      [req.params.id]
    );

    if (photoResult.rows.length === 0) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    const photo = photoResult.rows[0];
    const imagePath = path.join(process.cwd(), photo.photo_url.replace(/^\//, ''));

    const aiResult = await analyzePhotoWithAI(imagePath, photo.photo_type);

    // Update photo with AI analysis
    await query(
      'UPDATE photos SET ai_analysis_result = $1, ai_safety_flags = $2 WHERE id = $3',
      [aiResult.analysis, aiResult.safetyFlags.length > 0 ? aiResult.safetyFlags : null, req.params.id]
    );

    res.json({
      message: 'Photo analyzed successfully',
      analysis: aiResult.analysis,
      safetyFlags: aiResult.safetyFlags
    });
  } catch (error) {
    console.error('Photo analysis error:', error);
    res.status(500).json({ error: 'Photo analysis failed' });
  }
});

// Delete photo
router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const photoResult = await query(
      'SELECT photo_url FROM photos WHERE id = $1',
      [req.params.id]
    );

    if (photoResult.rows.length === 0) {
      return res.status(404).json({ error: 'Photo not found' });
    }

    const photo = photoResult.rows[0];

    // Delete from database
    await query('DELETE FROM photos WHERE id = $1', [req.params.id]);

    // Delete file from filesystem
    const filePath = path.join(process.cwd(), photo.photo_url.replace(/^\//, ''));
    try {
      await fs.unlink(filePath);
    } catch (e) {
      console.error('Failed to delete file:', e);
    }

    res.json({ message: 'Photo deleted successfully' });
  } catch (error) {
    console.error('Delete photo error:', error);
    res.status(500).json({ error: 'Failed to delete photo' });
  }
});

export default router;
