"""
Intelligence Gathering Coordinator
Orchestrates research across multiple AI models
"""

from typing import Dict, Any, List
from ..core.ai_coordinator import AIJusticeLeague
from .evidence_database import EvidenceDatabase, Evidence
from .violation_tracker import ViolationTracker, Violation
import uuid
from datetime import datetime


class IntelligenceGathering:
    """Coordinates intelligence gathering operations"""

    def __init__(self, ai_league: AIJusticeLeague):
        self.ai_league = ai_league
        self.evidence_db = EvidenceDatabase()
        self.violation_tracker = ViolationTracker()

    def coordinate_research(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate multi-AI research operation

        Returns:
            Synthesized intelligence report
        """
        print("🔍 Coordinating intelligence gathering across AI models...")

        # Execute distributed research
        research_results = self.ai_league.distribute_research(case_data)

        # Process and store findings
        intelligence_report = {
            'case_id': case_data.get('case_id', str(uuid.uuid4())),
            'research_date': datetime.now().isoformat(),
            'findings': {},
            'evidence_collected': [],
            'violations_identified': []
        }

        # Process each AI's research results
        for model_name, result in research_results.items():
            if result.success:
                intelligence_report['findings'][model_name] = {
                    'content': result.response.content,
                    'metadata': result.response.metadata
                }

                # Extract and store evidence
                evidence = self._extract_evidence(
                    case_data.get('case_id'),
                    model_name,
                    result.response.content
                )
                if evidence:
                    intelligence_report['evidence_collected'].extend(evidence)

                # Extract and store violations
                violations = self._extract_violations(
                    case_data.get('case_id'),
                    model_name,
                    result.response.content
                )
                if violations:
                    intelligence_report['violations_identified'].extend(violations)

        # Generate summary
        intelligence_report['summary'] = self._generate_intelligence_summary(
            intelligence_report
        )

        return intelligence_report

    def _extract_evidence(self, case_id: str, source: str,
                         content: str) -> List[Evidence]:
        """
        Extract evidence from AI research results
        This is a simplified version - in production, use more sophisticated NLP
        """
        evidence_list = []

        # Look for key evidence indicators
        evidence_keywords = [
            'violation', 'citation', 'complaint', 'inspection',
            'document', 'record', 'testimony', 'report'
        ]

        # Simple extraction - split by sentences
        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in evidence_keywords):
                evidence = Evidence(
                    id=str(uuid.uuid4()),
                    case_id=case_id,
                    evidence_type='research_finding',
                    description=sentence[:500],  # Truncate if too long
                    source=f"AI Research - {source}",
                    date_collected=datetime.now().isoformat(),
                    relevance_score=0.7,  # Default score
                    metadata={'ai_model': source, 'extraction_method': 'keyword'},
                    verified=False,
                    tags=[source, 'ai_research']
                )

                # Store in database
                self.evidence_db.add_evidence(evidence)
                evidence_list.append(evidence)

        return evidence_list

    def _extract_violations(self, case_id: str, source: str,
                          content: str) -> List[Violation]:
        """
        Extract violations from AI research results
        This is a simplified version - in production, use more sophisticated NLP
        """
        violations_list = []

        # Look for violation indicators
        violation_keywords = [
            'safety violation', 'building code', 'osha', 'ada violation',
            'non-compliance', 'citation', 'fine'
        ]

        sentences = content.split('.')
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in violation_keywords):
                # Determine severity based on keywords
                severity = 'minor'
                if any(word in sentence.lower() for word in ['critical', 'severe', 'serious']):
                    severity = 'critical'
                elif any(word in sentence.lower() for word in ['major', 'significant']):
                    severity = 'major'

                violation = Violation(
                    id=str(uuid.uuid4()),
                    case_id=case_id,
                    violation_type='identified_by_ai',
                    severity=severity,
                    description=sentence[:500],
                    location='To be determined',
                    date_reported=datetime.now().isoformat(),
                    status='open',
                    metadata={'ai_model': source, 'extraction_method': 'keyword'}
                )

                # Store in database
                self.violation_tracker.add_violation(violation)
                violations_list.append(violation)

        return violations_list

    def _generate_intelligence_summary(self,
                                      intelligence_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of intelligence findings"""
        return {
            'sources_consulted': len(intelligence_report['findings']),
            'evidence_items_collected': len(intelligence_report['evidence_collected']),
            'violations_identified': len(intelligence_report['violations_identified']),
            'research_completion_date': intelligence_report['research_date'],
            'key_findings': self._extract_key_findings(intelligence_report['findings'])
        }

    def _extract_key_findings(self, findings: Dict[str, Any]) -> List[str]:
        """Extract key findings from all AI research"""
        key_findings = []

        for model_name, finding in findings.items():
            content = finding.get('content', '')
            # Extract first substantive sentence as key finding
            sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 50]
            if sentences:
                key_findings.append(f"{model_name.upper()}: {sentences[0][:200]}...")

        return key_findings

    def get_intelligence_summary(self, case_id: str) -> Dict[str, Any]:
        """Get complete intelligence summary for a case"""
        evidence_summary = self.evidence_db.get_evidence_summary(case_id)
        violation_summary = self.violation_tracker.get_violation_summary(case_id)
        leverage_score = self.violation_tracker.calculate_leverage_score(case_id)

        return {
            'case_id': case_id,
            'evidence': evidence_summary,
            'violations': violation_summary,
            'leverage_score': leverage_score,
            'risk_assessment': self._assess_risk_level(leverage_score, violation_summary)
        }

    def _assess_risk_level(self, leverage_score: float,
                          violation_summary: Dict[str, Any]) -> str:
        """Assess overall risk level for opponent"""
        if leverage_score > 70 or violation_summary.get('critical_violations', 0) > 3:
            return 'HIGH'
        elif leverage_score > 40 or violation_summary.get('critical_violations', 0) > 0:
            return 'MEDIUM'
        else:
            return 'LOW'
