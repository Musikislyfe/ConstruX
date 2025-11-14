# 🔧 Bid Reverse Engine™

An interactive React application for on-site apartment renovation assessments. This tool implements a recursive assessment system that helps contractors and property managers generate professional bid estimates based on comprehensive property evaluations.

## 🌟 Features

### 📋 Multi-Tab Assessment Interface

1. **Intake Tab** - Project Information & Client Signals
   - Property details (address, unit, square footage)
   - Initial scope request (Emergency, Tenant-Ready, Full Reno, Code Compliance)
   - Manager's pain points (Failed inspection, Tenant complaints, etc.)
   - Budget signals (Just functional, Do it right, Want the best)
   - Timeline pressure indicators with cost multipliers

2. **Structural Tab** - Weighted Structural Assessment
   - Foundation scoring (3.0x weight)
   - Walls condition (2.5x weight)
   - Floors assessment (2.0x weight)
   - Ceiling evaluation (1.5x weight)
   - Roof/Water damage (3.5x weight)
   - Real-time structural risk calculation

3. **Systems Tab** - Critical Systems Evaluation
   - Electrical system (age, condition, code compliance)
   - Plumbing infrastructure
   - HVAC systems
   - Fire safety equipment
   - Automated urgency scoring

4. **Hazards Tab** - Environmental & Compliance Risks
   - Lead paint detection ($3,500 remediation cost)
   - Asbestos presence ($10,000 remediation cost)
   - Mold issues ($5,000 remediation cost)
   - Code violations ($2,000 correction cost)
   - ADA compliance gaps ($15,000 upgrade cost)
   - Site logistics assessment (access, staging, power, restrictions)

5. **Results Tab** - Professional Bid Generation
   - Three bid scenarios (Quick Fix, Comprehensive, Premium)
   - Priority item ranking by criticality
   - Detailed cost breakdowns with markup percentages
   - Timeline estimates
   - One-click professional report generation

### 🧮 Intelligent Calculation Engine

- **Base Cost Calculation**: Automatically adjusts per-square-foot pricing based on overall condition score
  - Low condition (< 30): $125/sqft
  - Medium condition (30-60): $225/sqft
  - High condition (> 60): $375/sqft

- **Risk Multipliers**:
  - High structural risk (+35%)
  - High systems urgency (+25%)
  - Hazards present (+20%)
  - ASAP timeline (+30%)

- **Scenario Generation**:
  - Quick Fix: 30% of adjusted cost, 5-10 days
  - Comprehensive: 100% of adjusted cost, 3-4 weeks (Recommended)
  - Premium: 150% of adjusted cost, 6-8 weeks

### 📱 Mobile-Optimized Design

- Fully responsive layout for phones and tablets
- Touch-friendly interface elements
- Optimized for on-site field use
- Works offline once loaded
- No zoom on iOS form inputs

### 📄 Professional Report Generation

One-click copy-to-clipboard functionality generates formatted assessment reports including:
- Executive summary with key metrics
- Critical findings and priorities
- Recommended approach with investment details
- Professional formatting ready for client presentation

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ installed
- npm or yarn package manager

### Installation

```bash
# Navigate to the app directory
cd bid-reverse-engine

# Install dependencies
npm install

# Start development server
npm run dev
```

The app will open automatically at `http://localhost:3000`

### Building for Production

```bash
# Create optimized production build
npm run build

# Preview production build
npm run preview
```

The production files will be in the `dist/` directory.

## 📖 Usage Guide

### Step 1: Project Intake
1. Enter property details (address, unit number, square footage)
2. Select the initial scope request
3. Identify the manager's primary pain point
4. Capture budget signals and timeline requirements

### Step 2: Structural Assessment
1. Use sliders to score each structural element (0 = Perfect, 10 = Failed)
2. The system automatically applies weighted calculations
3. Review the real-time structural risk score

### Step 3: Systems Evaluation
1. For each system (Electrical, Plumbing, HVAC, Fire Safety):
   - Enter the age in years
   - Rate the current condition (0-10)
   - Mark code compliance status
2. Monitor the automated urgency score

### Step 4: Hazards & Logistics
1. Toggle presence of environmental hazards
2. Set site logistics parameters (access, staging area)
3. Note power availability and time restrictions
4. Review calculated hazard remediation costs

### Step 5: Generate Bid
1. Navigate to the Results tab
2. Click "Generate Bid Analysis"
3. Review all three bid scenarios
4. Check priority items (critical items highlighted in red)
5. Copy the professional report to clipboard
6. Share with client or use for proposal development

## 🎯 Use Cases

- **On-Site Property Assessments**: Use during walkthrough inspections to capture real-time data
- **Bid Preparation**: Generate three-tier pricing options instantly
- **Client Presentations**: Professional reports ready to share
- **Risk Assessment**: Identify critical issues before committing to fixed pricing
- **Portfolio Management**: Track condition metrics across multiple properties
- **Insurance Claims**: Document pre/post conditions with systematic scoring

## 🛠️ Technical Stack

- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **CSS Modules** - Scoped component styling
- **Local State Management** - useState hooks for reactive UI

## 📂 Project Structure

```
bid-reverse-engine/
├── src/
│   ├── components/
│   │   ├── BidReverseEngine.jsx    # Main component
│   │   └── BidReverseEngine.css    # Component styles
│   ├── main.jsx                     # App entry point
│   └── index.css                    # Global styles
├── index.html                       # HTML template
├── vite.config.js                   # Vite configuration
├── package.json                     # Dependencies
└── README.md                        # Documentation
```

## 🔧 Customization

### Adjusting Cost Calculations

Edit the calculation functions in `BidReverseEngine.jsx`:

```javascript
// Modify base costs per square foot
const baseCost = projectInfo.sqft * 125; // Adjust multiplier

// Adjust risk multipliers
if (structuralRisk > 50) multiplier += 0.35; // Modify threshold or percentage
```

### Changing Hazard Costs

Update the `calculateHazardCost()` function:

```javascript
if (hazards.leadPaint) cost += 3500; // Adjust remediation costs
```

### Modifying Scenario Percentages

Adjust the scenario calculations:

```javascript
const quickFix = {
  cost: Math.round(adjustedCost * 0.3), // Change percentage
  timeline: '5-10 days',               // Update timeline
  markup: 25                           // Adjust markup
};
```

## 📊 Calculation Examples

### Example 1: Standard Tenant-Ready Unit

**Input:**
- Square footage: 850 sqft
- Structural scores: Low (avg 2/10)
- Systems: Moderate age, good condition
- No hazards
- Normal timeline

**Output:**
- Condition Score: ~25
- Base Cost: $106,250 (850 × $125)
- Quick Fix: ~$31,875
- Comprehensive: ~$106,250
- Premium: ~$159,375

### Example 2: High-Risk Renovation

**Input:**
- Square footage: 1,200 sqft
- Structural scores: High (avg 8/10)
- Systems: Non-compliant electrical/plumbing
- Asbestos + lead paint detected
- ASAP timeline

**Output:**
- Condition Score: ~75
- Base Cost: $450,000 (1,200 × $375)
- Additional Hazards: +$13,500
- Risk Multiplier: 1.9x
- Comprehensive: ~$868,500

## 🤝 Contributing

This is a proprietary tool for ConstruX operations. For internal improvements:

1. Create a feature branch
2. Make your changes
3. Test thoroughly on mobile devices
4. Submit for review

## 📱 Deployment Options

### Option 1: Static Hosting (Recommended for Mobile)
- Netlify: Deploy from git with automatic builds
- Vercel: Zero-config deployment
- GitHub Pages: Free hosting with custom domain support

### Option 2: Self-Hosted
- Build and deploy to your own server
- Serve from the `dist/` directory
- Configure HTTPS for secure access

### Option 3: Progressive Web App (PWA)
- Add service worker for offline capability
- Enable "Add to Home Screen" on mobile devices
- Works like a native app

## 📄 License

Copyright © 2024 ConstruX. All rights reserved.

## 🆘 Support

For issues or questions:
- Check existing issues in the repository
- Create a new issue with detailed description
- Include screenshots for UI-related problems
- Specify device/browser for mobile issues

## 🔮 Future Enhancements

- [ ] Photo upload capability for documentation
- [ ] Data persistence with localStorage
- [ ] Export to PDF functionality
- [ ] Historical project comparison
- [ ] Integration with estimation software
- [ ] Multi-language support
- [ ] Custom branding options
- [ ] Email report functionality

---

**Built with ⚡ by ConstruX for efficient field operations**
