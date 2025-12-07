"""
Result Aggregator
Aggregates results from multiple AI models and analysis components
"""

from typing import Dict, Any, List
from collections import defaultdict


class ResultAggregator:
    """Aggregates and synthesizes results from multiple sources"""

    def __init__(self):
        self.results: Dict[str, List[Any]] = defaultdict(list)

    def add_result(self, category: str, result: Any):
        """Add a result to aggregation"""
        self.results[category].append(result)

    def aggregate_ai_responses(self, responses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aggregate responses from multiple AI models

        Args:
            responses: Dictionary of {model_name: response}

        Returns:
            Aggregated insights
        """
        aggregated = {
            'total_responses': len(responses),
            'successful_responses': 0,
            'failed_responses': 0,
            'insights_by_model': {},
            'common_themes': [],
            'unique_insights': []
        }

        for model_name, response in responses.items():
            if hasattr(response, 'success') and response.success:
                aggregated['successful_responses'] += 1
                aggregated['insights_by_model'][model_name] = {
                    'content_length': len(response.content) if hasattr(response, 'content') else 0,
                    'summary': self._summarize_content(
                        response.content if hasattr(response, 'content') else ""
                    )
                }
            else:
                aggregated['failed_responses'] += 1

        # Identify common themes (simplified - in production, use NLP)
        aggregated['common_themes'] = self._identify_common_themes(responses)

        return aggregated

    def aggregate_leverage_factors(self, factors: Dict[str, float]) -> Dict[str, Any]:
        """Aggregate leverage factor analysis"""
        sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)

        return {
            'total_factors': len(factors),
            'average_score': sum(factors.values()) / len(factors) if factors else 0,
            'top_factors': [
                {'factor': f, 'score': s}
                for f, s in sorted_factors[:3]
            ],
            'weak_factors': [
                {'factor': f, 'score': s}
                for f, s in sorted_factors[-2:]
            ]
        }

    def aggregate_evidence(self, evidence_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate evidence analysis"""
        total = len(evidence_list)
        verified = sum(1 for e in evidence_list if e.get('verified', False))

        by_type = defaultdict(int)
        total_relevance = 0

        for evidence in evidence_list:
            by_type[evidence.get('evidence_type', 'unknown')] += 1
            total_relevance += evidence.get('relevance_score', 0)

        return {
            'total_evidence': total,
            'verified_evidence': verified,
            'verification_rate': verified / total if total > 0 else 0,
            'average_relevance': total_relevance / total if total > 0 else 0,
            'evidence_by_type': dict(by_type),
            'evidence_strength': self._rate_evidence_strength(total, verified, total_relevance / total if total > 0 else 0)
        }

    def aggregate_violations(self, violations_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate violation analysis"""
        total = len(violations_list)

        by_severity = defaultdict(int)
        by_status = defaultdict(int)
        total_fines = 0

        for violation in violations_list:
            by_severity[violation.get('severity', 'unknown')] += 1
            by_status[violation.get('status', 'unknown')] += 1
            total_fines += violation.get('fine_amount', 0)

        return {
            'total_violations': total,
            'critical_violations': by_severity.get('critical', 0),
            'major_violations': by_severity.get('major', 0),
            'minor_violations': by_severity.get('minor', 0),
            'open_violations': by_status.get('open', 0),
            'total_fines': total_fines,
            'violations_by_severity': dict(by_severity),
            'violations_by_status': dict(by_status),
            'severity_distribution': self._calculate_distribution(by_severity)
        }

    def create_executive_summary(self, mission_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary from all mission results"""
        return {
            'mission_overview': {
                'case_id': mission_results.get('case_id', 'unknown'),
                'phases_completed': self._count_completed_phases(mission_results),
                'overall_success_rate': self._calculate_success_rate(mission_results)
            },
            'intelligence_summary': self._summarize_intelligence(
                mission_results.get('research_phase', {})
            ),
            'analysis_summary': self._summarize_analysis(
                mission_results.get('analysis_phase', {})
            ),
            'execution_summary': self._summarize_execution(
                mission_results.get('execution_phase', {})
            ),
            'key_findings': self._extract_key_findings(mission_results),
            'recommendations': self._generate_recommendations(mission_results)
        }

    def _summarize_content(self, content: str, max_length: int = 200) -> str:
        """Summarize content to max length"""
        if len(content) <= max_length:
            return content
        return content[:max_length] + "..."

    def _identify_common_themes(self, responses: Dict[str, Any]) -> List[str]:
        """Identify common themes across responses"""
        # Simplified theme identification
        # In production, use NLP/semantic analysis
        themes = []

        keywords = [
            'violation', 'discrimination', 'safety',
            'accommodation', 'retaliation', 'settlement'
        ]

        for keyword in keywords:
            count = 0
            for response in responses.values():
                content = response.content if hasattr(response, 'content') else ""
                if keyword.lower() in content.lower():
                    count += 1

            if count >= len(responses) / 2:  # Appears in at least half
                themes.append(keyword.title())

        return themes

    def _rate_evidence_strength(self, total: int, verified: int,
                               avg_relevance: float) -> str:
        """Rate overall evidence strength"""
        score = 0

        # Volume score
        if total > 20:
            score += 3
        elif total > 10:
            score += 2
        elif total > 5:
            score += 1

        # Verification score
        verification_rate = verified / total if total > 0 else 0
        if verification_rate > 0.7:
            score += 3
        elif verification_rate > 0.5:
            score += 2
        elif verification_rate > 0.3:
            score += 1

        # Relevance score
        if avg_relevance > 0.8:
            score += 3
        elif avg_relevance > 0.6:
            score += 2
        elif avg_relevance > 0.4:
            score += 1

        if score >= 7:
            return "EXCELLENT"
        elif score >= 5:
            return "STRONG"
        elif score >= 3:
            return "MODERATE"
        else:
            return "WEAK"

    def _calculate_distribution(self, by_category: Dict[str, int]) -> Dict[str, float]:
        """Calculate percentage distribution"""
        total = sum(by_category.values())
        if total == 0:
            return {}

        return {
            category: (count / total) * 100
            for category, count in by_category.items()
        }

    def _count_completed_phases(self, mission_results: Dict[str, Any]) -> int:
        """Count completed mission phases"""
        phases = ['research_phase', 'analysis_phase', 'execution_phase']
        return sum(1 for phase in phases if phase in mission_results)

    def _calculate_success_rate(self, mission_results: Dict[str, Any]) -> float:
        """Calculate overall success rate"""
        total_tasks = 0
        successful_tasks = 0

        for phase_key in ['research_phase', 'analysis_phase', 'execution_phase']:
            if phase_key in mission_results:
                phase = mission_results[phase_key]
                if 'summary' in phase:
                    total_tasks += phase['summary'].get('total_tasks', 0)
                    successful_tasks += phase['summary'].get('successful', 0)

        return successful_tasks / total_tasks if total_tasks > 0 else 0

    def _summarize_intelligence(self, research_phase: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize intelligence phase"""
        return {
            'sources_consulted': research_phase.get('summary', {}).get('models_used', []),
            'insights_gathered': research_phase.get('summary', {}).get('total_tasks', 0),
            'key_findings': research_phase.get('combined_insights', [])[:3]
        }

    def _summarize_analysis(self, analysis_phase: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize analysis phase"""
        return {
            'leverage_calculated': 'leverage_score' in analysis_phase,
            'settlement_modeled': 'settlement_prediction' in analysis_phase,
            'strategic_plan_created': 'strategic_recommendations' in analysis_phase
        }

    def _summarize_execution(self, execution_phase: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize execution phase"""
        return {
            'complaints_prepared': execution_phase.get('summary', {}).get('total_tasks', 0),
            'ready_for_deployment': execution_phase.get('summary', {}).get('successful', 0) > 0
        }

    def _extract_key_findings(self, mission_results: Dict[str, Any]) -> List[str]:
        """Extract key findings from mission"""
        findings = []

        # Add placeholder findings
        findings.append("Multi-AI coordination successfully completed")
        findings.append("Strategic analysis identified leverage points")
        findings.append("Execution package prepared and ready for deployment")

        return findings

    def _generate_recommendations(self, mission_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on results"""
        recommendations = []

        recommendations.append("Proceed with coordinated campaign deployment")
        recommendations.append("Monitor opponent response and adjust tactics")
        recommendations.append("Maintain pressure through multiple channels")

        return recommendations
