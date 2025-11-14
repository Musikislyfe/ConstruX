import React, { useState, useEffect } from 'react';
import './BidReverseEngine.css';

const BidReverseEngine = () => {
  // State management
  const [projectInfo, setProjectInfo] = useState({
    address: '',
    unit: '',
    manager: '',
    date: new Date().toISOString().split('T')[0],
    sqft: 1000,
    scope: '',
    painPoint: '',
    budgetSignal: '',
    timeline: ''
  });

  const [structuralScores, setStructuralScores] = useState({
    foundation: 0,
    walls: 0,
    floors: 0,
    ceiling: 0,
    roofWater: 0
  });

  const [systemScores, setSystemScores] = useState({
    electrical: { age: 0, condition: 0, compliance: false },
    plumbing: { age: 0, condition: 0, compliance: false },
    hvac: { age: 0, condition: 0, compliance: false },
    fireSafety: { age: 0, condition: 0, compliance: false }
  });

  const [hazards, setHazards] = useState({
    leadPaint: false,
    asbestos: false,
    mold: false,
    codeViolations: false,
    adaCompliance: false
  });

  const [logistics, setLogistics] = useState({
    access: 'easy',
    staging: 'good',
    power: true,
    restrictions: false
  });

  const [bidResults, setBidResults] = useState(null);
  const [activeTab, setActiveTab] = useState('intake');

  // Calculation weights
  const structuralWeights = {
    foundation: 3.0,
    walls: 2.5,
    floors: 2.0,
    ceiling: 1.5,
    roofWater: 3.5
  };

  // Calculate scores
  const calculateStructuralRisk = () => {
    let totalRisk = 0;
    Object.keys(structuralScores).forEach(key => {
      totalRisk += structuralScores[key] * structuralWeights[key];
    });
    return totalRisk;
  };

  const calculateSystemsUrgency = () => {
    let totalUrgency = 0;
    Object.values(systemScores).forEach(system => {
      totalUrgency += (10 - system.condition) + (system.age > 20 ? 5 : 0) + (!system.compliance ? 10 : 0);
    });
    return totalUrgency;
  };

  const calculateHazardCost = () => {
    let cost = 0;
    if (hazards.leadPaint) cost += 3500;
    if (hazards.asbestos) cost += 10000;
    if (hazards.mold) cost += 5000;
    if (hazards.codeViolations) cost += 2000;
    if (hazards.adaCompliance) cost += 15000;
    return cost;
  };

  const calculateBid = () => {
    const structuralRisk = calculateStructuralRisk();
    const systemsUrgency = calculateSystemsUrgency();
    const hazardCost = calculateHazardCost();

    // Base cost calculation
    const conditionScore = (structuralRisk + systemsUrgency) / 2;
    let baseCost;
    if (conditionScore < 30) {
      baseCost = projectInfo.sqft * 125;
    } else if (conditionScore < 60) {
      baseCost = projectInfo.sqft * 225;
    } else {
      baseCost = projectInfo.sqft * 375;
    }

    // Risk multiplier
    let multiplier = 1.0;
    if (structuralRisk > 50) multiplier += 0.35;
    if (systemsUrgency > 60) multiplier += 0.25;
    if (hazardCost > 0) multiplier += 0.20;
    if (projectInfo.timeline === 'asap') multiplier += 0.30;

    const adjustedCost = baseCost * multiplier + hazardCost;

    // Generate three scenarios
    const quickFix = {
      cost: Math.round(adjustedCost * 0.3),
      timeline: '5-10 days',
      markup: 25,
      scope: 'Address top 3 priority items only'
    };

    const comprehensive = {
      cost: Math.round(adjustedCost),
      timeline: '3-4 weeks',
      markup: 35,
      scope: 'All systems to code'
    };

    const premium = {
      cost: Math.round(adjustedCost * 1.5),
      timeline: '6-8 weeks',
      markup: 45,
      scope: 'Full upgrade + improvements'
    };

    // Priority items
    const priorities = [
      { item: 'Structural repairs', score: structuralRisk, critical: structuralRisk > 60 },
      { item: 'Electrical updates', score: systemScores.electrical.condition === 0 ? 80 : 40, critical: !systemScores.electrical.compliance },
      { item: 'Plumbing repairs', score: systemScores.plumbing.condition === 0 ? 70 : 30, critical: !systemScores.plumbing.compliance },
      { item: 'HVAC service', score: systemScores.hvac.age > 15 ? 60 : 20, critical: false },
      { item: 'Hazard remediation', score: hazardCost > 0 ? 90 : 0, critical: hazardCost > 5000 }
    ].sort((a, b) => b.score - a.score);

    setBidResults({
      quickFix,
      comprehensive,
      premium,
      priorities: priorities.filter(p => p.score > 0),
      structuralRisk,
      systemsUrgency,
      hazardCost,
      conditionScore
    });
  };

  const generateReport = () => {
    if (!bidResults) return '';

    return `PROFESSIONAL ASSESSMENT - ${projectInfo.address} Unit ${projectInfo.unit}

Date: ${projectInfo.date}
Manager: ${projectInfo.manager}

EXECUTIVE SUMMARY:
- Structural Integrity: ${(100 - (bidResults.structuralRisk * 2)).toFixed(0)}% sound
- Systems Status: ${(100 - (bidResults.systemsUrgency * 1.25)).toFixed(0)}% functional
- Code Compliance: ${bidResults.priorities.filter(p => p.critical).length} items flagged
- Square Footage: ${projectInfo.sqft} sq ft

CRITICAL FINDINGS:
${bidResults.priorities.slice(0, 3).map((p, i) => `${i + 1}. ${p.item}${p.critical ? ' (IMMEDIATE ATTENTION REQUIRED)' : ''}`).join('\n')}

RECOMMENDED APPROACH: Comprehensive Plan
Investment: $${bidResults.comprehensive.cost.toLocaleString()}
Timeline: ${bidResults.comprehensive.timeline}
Warranty: 24 months on all work

This quote is valid for 14 days. A 30% deposit secures your start date.`;
  };

  // Tab content components
  const IntakeTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Project Information</h2>

      <div className="grid grid-cols-2 gap-4">
        <input
          placeholder="Property Address"
          value={projectInfo.address}
          onChange={(e) => setProjectInfo({...projectInfo, address: e.target.value})}
          className="input-field"
        />
        <input
          placeholder="Unit #"
          value={projectInfo.unit}
          onChange={(e) => setProjectInfo({...projectInfo, unit: e.target.value})}
          className="input-field"
        />
        <input
          placeholder="Manager Name"
          value={projectInfo.manager}
          onChange={(e) => setProjectInfo({...projectInfo, manager: e.target.value})}
          className="input-field"
        />
        <input
          type="date"
          value={projectInfo.date}
          onChange={(e) => setProjectInfo({...projectInfo, date: e.target.value})}
          className="input-field"
        />
        <input
          type="number"
          placeholder="Square Footage"
          value={projectInfo.sqft}
          onChange={(e) => setProjectInfo({...projectInfo, sqft: parseInt(e.target.value) || 0})}
          className="input-field"
        />
      </div>

      <div className="space-y-3">
        <div>
          <h3 className="font-semibold mb-2">Initial Scope Request</h3>
          <div className="grid grid-cols-2 gap-2">
            {['Emergency', 'Tenant-Ready', 'Full Reno', 'Code Compliance'].map(scope => (
              <button
                key={scope}
                onClick={() => setProjectInfo({...projectInfo, scope})}
                className={`btn-option ${projectInfo.scope === scope ? 'btn-option-active' : ''}`}
              >
                {scope}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h3 className="font-semibold mb-2">Manager's Pain Point</h3>
          <div className="grid grid-cols-2 gap-2">
            {['Failed inspection', 'Tenant complaints', 'Property sale', 'Insurance', 'Preventive'].map(pain => (
              <button
                key={pain}
                onClick={() => setProjectInfo({...projectInfo, painPoint: pain})}
                className={`btn-option text-sm ${projectInfo.painPoint === pain ? 'btn-option-active' : ''}`}
              >
                {pain}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h3 className="font-semibold mb-2">Budget Signal</h3>
          <div className="grid grid-cols-3 gap-2">
            {[
              {value: 'low', label: 'Just functional'},
              {value: 'medium', label: 'Do it right'},
              {value: 'high', label: 'Want the best'}
            ].map(budget => (
              <button
                key={budget.value}
                onClick={() => setProjectInfo({...projectInfo, budgetSignal: budget.value})}
                className={`btn-option text-sm ${projectInfo.budgetSignal === budget.value ? 'btn-option-active' : ''}`}
              >
                {budget.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <h3 className="font-semibold mb-2">Timeline Pressure</h3>
          <div className="grid grid-cols-3 gap-2">
            {[
              {value: 'asap', label: 'ASAP (+30%)'},
              {value: 'normal', label: '30 days'},
              {value: 'flexible', label: 'Flexible'}
            ].map(time => (
              <button
                key={time.value}
                onClick={() => setProjectInfo({...projectInfo, timeline: time.value})}
                className={`btn-option text-sm ${projectInfo.timeline === time.value ? 'btn-option-active' : ''}`}
              >
                {time.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  const StructuralTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Structural Assessment</h2>

      {Object.entries(structuralScores).map(([key, value]) => (
        <div key={key} className="space-y-2">
          <div className="flex justify-between items-center">
            <label className="font-semibold capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</label>
            <span className="text-sm text-gray-600">Weight: {structuralWeights[key]}x</span>
          </div>
          <input
            type="range"
            min="0"
            max="10"
            value={value}
            onChange={(e) => setStructuralScores({...structuralScores, [key]: parseInt(e.target.value)})}
            className="slider"
          />
          <div className="flex justify-between text-sm">
            <span>Perfect (0)</span>
            <span className="font-bold">Score: {value}</span>
            <span>Failed (10)</span>
          </div>
        </div>
      ))}

      <div className="summary-box">
        <p className="font-semibold">Structural Risk Score: {calculateStructuralRisk().toFixed(1)}</p>
        <p className="text-sm text-gray-600 mt-1">
          {calculateStructuralRisk() < 30 ? 'Low Risk' : calculateStructuralRisk() < 60 ? 'Medium Risk' : 'High Risk'}
        </p>
      </div>
    </div>
  );

  const SystemsTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Systems Assessment</h2>

      {Object.entries(systemScores).map(([system, data]) => (
        <div key={system} className="system-card">
          <h3 className="font-semibold capitalize">{system.replace(/([A-Z])/g, ' $1').trim()}</h3>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-sm">Age (years)</label>
              <input
                type="number"
                value={data.age}
                onChange={(e) => setSystemScores({
                  ...systemScores,
                  [system]: {...data, age: parseInt(e.target.value) || 0}
                })}
                className="input-field-small"
              />
            </div>

            <div>
              <label className="text-sm">Condition (0-10)</label>
              <input
                type="number"
                min="0"
                max="10"
                value={data.condition}
                onChange={(e) => setSystemScores({
                  ...systemScores,
                  [system]: {...data, condition: parseInt(e.target.value) || 0}
                })}
                className="input-field-small"
              />
            </div>

            <div>
              <label className="text-sm">Compliant?</label>
              <button
                onClick={() => setSystemScores({
                  ...systemScores,
                  [system]: {...data, compliance: !data.compliance}
                })}
                className={`compliance-btn ${data.compliance ? 'compliance-yes' : 'compliance-no'}`}
              >
                {data.compliance ? 'Yes' : 'No'}
              </button>
            </div>
          </div>
        </div>
      ))}

      <div className="summary-box">
        <p className="font-semibold">Systems Urgency Score: {calculateSystemsUrgency()}</p>
        <p className="text-sm text-gray-600 mt-1">
          {calculateSystemsUrgency() < 40 ? 'Low Priority' : calculateSystemsUrgency() < 80 ? 'Medium Priority' : 'High Priority'}
        </p>
      </div>
    </div>
  );

  const HazardsTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Hazards & Compliance</h2>

      <div className="space-y-3">
        {Object.entries(hazards).map(([hazard, value]) => (
          <div key={hazard} className="hazard-item">
            <label className="font-semibold capitalize">
              {hazard.replace(/([A-Z])/g, ' $1').trim()}
            </label>
            <button
              onClick={() => setHazards({...hazards, [hazard]: !value})}
              className={`hazard-btn ${value ? 'hazard-present' : 'hazard-absent'}`}
            >
              {value ? 'Present' : 'Not Found'}
            </button>
          </div>
        ))}
      </div>

      <div className="mt-4 space-y-3">
        <h3 className="font-semibold">Site Logistics</h3>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="text-sm">Access</label>
            <select
              value={logistics.access}
              onChange={(e) => setLogistics({...logistics, access: e.target.value})}
              className="select-field"
            >
              <option value="easy">Easy</option>
              <option value="moderate">Moderate</option>
              <option value="difficult">Difficult</option>
            </select>
          </div>

          <div>
            <label className="text-sm">Staging Area</label>
            <select
              value={logistics.staging}
              onChange={(e) => setLogistics({...logistics, staging: e.target.value})}
              className="select-field"
            >
              <option value="good">Good</option>
              <option value="limited">Limited</option>
              <option value="none">None</option>
            </select>
          </div>
        </div>

        <div className="flex gap-4">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={logistics.power}
              onChange={(e) => setLogistics({...logistics, power: e.target.checked})}
              className="checkbox"
            />
            Power Available
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={logistics.restrictions}
              onChange={(e) => setLogistics({...logistics, restrictions: e.target.checked})}
              className="checkbox"
            />
            Time Restrictions
          </label>
        </div>
      </div>

      <div className="summary-box">
        <p className="font-semibold">Additional Hazard Costs: ${calculateHazardCost().toLocaleString()}</p>
      </div>
    </div>
  );

  const ResultsTab = () => (
    <div className="space-y-4">
      <h2 className="text-xl font-bold mb-4">Bid Analysis Results</h2>

      {!bidResults ? (
        <div className="text-center py-8">
          <button
            onClick={calculateBid}
            className="btn-generate"
          >
            Generate Bid Analysis
          </button>
        </div>
      ) : (
        <>
          <div className="metrics-grid">
            <div>
              <p className="text-sm text-gray-600">Structural Risk</p>
              <p className="text-lg font-semibold">{bidResults.structuralRisk.toFixed(1)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Systems Urgency</p>
              <p className="text-lg font-semibold">{bidResults.systemsUrgency}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Hazard Costs</p>
              <p className="text-lg font-semibold">${bidResults.hazardCost.toLocaleString()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Overall Condition</p>
              <p className="text-lg font-semibold">{bidResults.conditionScore.toFixed(1)}</p>
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="font-semibold">Priority Items</h3>
            {bidResults.priorities.map((priority, index) => (
              <div key={index} className={`priority-item ${priority.critical ? 'priority-critical' : ''}`}>
                <div className="flex justify-between">
                  <span className="font-medium">{priority.item}</span>
                  <span className={`text-sm ${priority.critical ? 'text-red-600' : ''}`}>
                    {priority.critical ? 'CRITICAL' : `Priority: ${priority.score}`}
                  </span>
                </div>
              </div>
            ))}
          </div>

          <div className="space-y-4">
            <h3 className="font-semibold">Bid Scenarios</h3>

            <div className="scenario-card scenario-quick">
              <h4 className="scenario-title">Scenario A - Quick Fix</h4>
              <p className="text-sm text-gray-600 mt-1">{bidResults.quickFix.scope}</p>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <div>
                  <p className="text-xs text-gray-500">Cost</p>
                  <p className="font-bold">${bidResults.quickFix.cost.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Timeline</p>
                  <p className="font-bold">{bidResults.quickFix.timeline}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Markup</p>
                  <p className="font-bold">{bidResults.quickFix.markup}%</p>
                </div>
              </div>
            </div>

            <div className="scenario-card scenario-comprehensive">
              <h4 className="scenario-title">Scenario B - Comprehensive (Recommended)</h4>
              <p className="text-sm text-gray-600 mt-1">{bidResults.comprehensive.scope}</p>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <div>
                  <p className="text-xs text-gray-500">Cost</p>
                  <p className="font-bold">${bidResults.comprehensive.cost.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Timeline</p>
                  <p className="font-bold">{bidResults.comprehensive.timeline}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Markup</p>
                  <p className="font-bold">{bidResults.comprehensive.markup}%</p>
                </div>
              </div>
            </div>

            <div className="scenario-card scenario-premium">
              <h4 className="scenario-title">Scenario C - Premium Renovation</h4>
              <p className="text-sm text-gray-600 mt-1">{bidResults.premium.scope}</p>
              <div className="grid grid-cols-3 gap-2 mt-2">
                <div>
                  <p className="text-xs text-gray-500">Cost</p>
                  <p className="font-bold">${bidResults.premium.cost.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Timeline</p>
                  <p className="font-bold">{bidResults.premium.timeline}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500">Markup</p>
                  <p className="font-bold">{bidResults.premium.markup}%</p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-6 space-y-3">
            <button
              onClick={() => {
                const report = generateReport();
                navigator.clipboard.writeText(report);
                alert('Report copied to clipboard!');
              }}
              className="btn-action btn-action-primary"
            >
              Copy Professional Report
            </button>

            <button
              onClick={() => calculateBid()}
              className="btn-action btn-action-secondary"
            >
              Recalculate
            </button>
          </div>
        </>
      )}
    </div>
  );

  return (
    <div className="app-container">
      <h1 className="app-title">🔧 BID REVERSE ENGINE™</h1>

      <div className="tab-bar">
        {['intake', 'structural', 'systems', 'hazards', 'results'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`tab-btn ${activeTab === tab ? 'tab-btn-active' : ''}`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="content-area">
        {activeTab === 'intake' && <IntakeTab />}
        {activeTab === 'structural' && <StructuralTab />}
        {activeTab === 'systems' && <SystemsTab />}
        {activeTab === 'hazards' && <HazardsTab />}
        {activeTab === 'results' && <ResultsTab />}
      </div>

      <div className="footer">
        <span>Progress: {Object.values(projectInfo).filter(v => v).length + Object.values(structuralScores).filter(v => v > 0).length} fields completed</span>
        <span>© 2024 Bid Reverse Engine</span>
      </div>
    </div>
  );
};

export default BidReverseEngine;
