"""
Leverage Calculator
Analyzes case strength and calculates negotiation leverage
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class LeverageAnalysis:
    """Leverage analysis result"""
    case_id: str
    overall_leverage_score: float  # 0-100
    leverage_factors: Dict[str, float]
    pressure_points: List[Dict[str, Any]]
    optimal_timing: Dict[str, Any]
    risk_to_opponent: str  # LOW, MEDIUM, HIGH, CRITICAL
    settlement_probability: float  # 0-1
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LeverageCalculator:
    """Calculates case leverage and strategic advantage"""

    def __init__(self):
        self.leverage_weights = {
            'violations': 0.25,
            'evidence_strength': 0.20,
            'legal_precedent': 0.15,
            'public_exposure': 0.15,
            'regulatory_risk': 0.15,
            'financial_impact': 0.10
        }

    def calculate_leverage(self, case_data: Dict[str, Any],
                          intelligence: Dict[str, Any]) -> LeverageAnalysis:
        """
        Calculate comprehensive leverage analysis

        Args:
            case_data: Case information
            intelligence: Intelligence report from research phase

        Returns:
            Complete leverage analysis
        """
        leverage_factors = {}

        # Calculate individual leverage factors
        leverage_factors['violations'] = self._calculate_violation_leverage(
            intelligence.get('violations', {})
        )

        leverage_factors['evidence_strength'] = self._calculate_evidence_leverage(
            intelligence.get('evidence', {})
        )

        leverage_factors['legal_precedent'] = self._calculate_precedent_leverage(
            case_data.get('legal_context', {})
        )

        leverage_factors['public_exposure'] = self._calculate_exposure_leverage(
            case_data.get('public_interest', 0)
        )

        leverage_factors['regulatory_risk'] = self._calculate_regulatory_leverage(
            intelligence.get('violations', {})
        )

        leverage_factors['financial_impact'] = self._calculate_financial_leverage(
            case_data.get('damages', 0),
            intelligence.get('violations', {})
        )

        # Calculate weighted overall score
        overall_score = sum(
            leverage_factors.get(factor, 0) * weight
            for factor, weight in self.leverage_weights.items()
        )

        # Identify pressure points
        pressure_points = self._identify_pressure_points(
            leverage_factors,
            intelligence
        )

        # Determine optimal timing
        optimal_timing = self._calculate_optimal_timing(
            leverage_factors,
            intelligence
        )

        # Assess risk to opponent
        risk_level = self._assess_opponent_risk(overall_score, leverage_factors)

        # Estimate settlement probability
        settlement_prob = self._estimate_settlement_probability(
            overall_score,
            leverage_factors
        )

        return LeverageAnalysis(
            case_id=case_data.get('case_id', 'unknown'),
            overall_leverage_score=overall_score,
            leverage_factors=leverage_factors,
            pressure_points=pressure_points,
            optimal_timing=optimal_timing,
            risk_to_opponent=risk_level,
            settlement_probability=settlement_prob,
            metadata={
                'calculation_date': datetime.now().isoformat(),
                'weights_used': self.leverage_weights
            }
        )

    def _calculate_violation_leverage(self, violations: Dict[str, Any]) -> float:
        """Calculate leverage from violations (0-100)"""
        if not violations:
            return 0.0

        score = 0.0

        # Critical violations add significant leverage
        critical = violations.get('critical_violations', 0)
        score += critical * 15

        # Major violations add moderate leverage
        major = violations.get('major_violations', 0)
        score += major * 8

        # Minor violations add some leverage
        minor = violations.get('minor_violations', 0)
        score += minor * 3

        # Open violations increase leverage
        open_violations = violations.get('open_violations', 0)
        score += open_violations * 5

        # Fines increase leverage
        fines = violations.get('total_fines', 0)
        score += (fines / 10000) * 10  # $10k = 10 points

        return min(score, 100.0)

    def _calculate_evidence_leverage(self, evidence: Dict[str, Any]) -> float:
        """Calculate leverage from evidence strength (0-100)"""
        if not evidence:
            return 0.0

        score = 0.0

        # Total evidence count
        total = evidence.get('total_evidence', 0)
        score += min(total * 5, 30)  # Max 30 points from volume

        # Verified evidence is more valuable
        verified = evidence.get('verified_evidence', 0)
        score += min(verified * 8, 40)  # Max 40 points from verified

        # Average relevance
        avg_relevance = evidence.get('average_relevance', 0)
        score += avg_relevance * 30  # Max 30 points from relevance

        return min(score, 100.0)

    def _calculate_precedent_leverage(self, legal_context: Dict[str, Any]) -> float:
        """Calculate leverage from legal precedents (0-100)"""
        # Simplified - in production, analyze actual case law
        favorable_precedents = legal_context.get('favorable_precedents', 0)
        average_settlement = legal_context.get('average_settlement', 0)

        score = 0.0
        score += min(favorable_precedents * 15, 60)
        score += min((average_settlement / 100000) * 10, 40)  # $100k = 10 points

        return min(score, 100.0)

    def _calculate_exposure_leverage(self, public_interest: float) -> float:
        """Calculate leverage from public/media exposure potential (0-100)"""
        # public_interest should be 0-10 scale
        return min(public_interest * 10, 100.0)

    def _calculate_regulatory_leverage(self, violations: Dict[str, Any]) -> float:
        """Calculate leverage from regulatory action risk (0-100)"""
        if not violations:
            return 0.0

        # More violations = more regulatory risk for opponent
        total_violations = violations.get('total_violations', 0)
        critical_violations = violations.get('critical_violations', 0)

        score = 0.0
        score += min(total_violations * 5, 50)
        score += critical_violations * 20

        return min(score, 100.0)

    def _calculate_financial_leverage(self, damages: float,
                                     violations: Dict[str, Any]) -> float:
        """Calculate leverage from financial impact (0-100)"""
        score = 0.0

        # Claimed damages
        score += min((damages / 100000) * 20, 50)  # $100k = 20 points, max 50

        # Potential fines
        fines = violations.get('total_fines', 0) if violations else 0
        score += min((fines / 50000) * 15, 50)  # $50k = 15 points, max 50

        return min(score, 100.0)

    def _identify_pressure_points(self, leverage_factors: Dict[str, float],
                                 intelligence: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify key pressure points for negotiation"""
        pressure_points = []

        # Sort leverage factors by strength
        sorted_factors = sorted(
            leverage_factors.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for factor, score in sorted_factors[:3]:  # Top 3 factors
            if score > 50:  # Only significant leverage points
                pressure_points.append({
                    'factor': factor,
                    'leverage_score': score,
                    'priority': 'HIGH' if score > 75 else 'MEDIUM',
                    'recommendation': self._get_pressure_point_recommendation(factor, score)
                })

        return pressure_points

    def _get_pressure_point_recommendation(self, factor: str, score: float) -> str:
        """Get tactical recommendation for pressure point"""
        recommendations = {
            'violations': 'Emphasize regulatory compliance failures and potential agency action',
            'evidence_strength': 'Present documentary evidence systematically to demonstrate case strength',
            'legal_precedent': 'Cite favorable precedents and settlement ranges',
            'public_exposure': 'Leverage media interest and public attention strategically',
            'regulatory_risk': 'Highlight potential for regulatory investigation and penalties',
            'financial_impact': 'Demonstrate full scope of damages and potential liability'
        }
        return recommendations.get(factor, 'Apply strategic pressure')

    def _calculate_optimal_timing(self, leverage_factors: Dict[str, float],
                                 intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate optimal timing for negotiations"""
        return {
            'immediate_action': leverage_factors.get('violations', 0) > 70,
            'recommended_phase': self._determine_negotiation_phase(leverage_factors),
            'timing_factors': {
                'regulatory_deadlines': 'Monitor for upcoming compliance deadlines',
                'media_cycles': 'Consider media attention timing',
                'financial_quarters': 'Target end of financial reporting periods'
            }
        }

    def _determine_negotiation_phase(self, leverage_factors: Dict[str, float]) -> str:
        """Determine recommended negotiation phase"""
        avg_leverage = sum(leverage_factors.values()) / len(leverage_factors)

        if avg_leverage > 70:
            return 'AGGRESSIVE - Immediate settlement demand'
        elif avg_leverage > 50:
            return 'ASSERTIVE - Structured negotiation with deadlines'
        else:
            return 'MEASURED - Information gathering and position building'

    def _assess_opponent_risk(self, overall_score: float,
                             leverage_factors: Dict[str, float]) -> str:
        """Assess risk level to opponent"""
        if overall_score > 75:
            return 'CRITICAL'
        elif overall_score > 60:
            return 'HIGH'
        elif overall_score > 40:
            return 'MEDIUM'
        else:
            return 'LOW'

    def _estimate_settlement_probability(self, overall_score: float,
                                        leverage_factors: Dict[str, float]) -> float:
        """Estimate probability of settlement (0-1)"""
        # Base probability on overall leverage
        base_prob = overall_score / 100

        # Adjust for evidence strength
        evidence_score = leverage_factors.get('evidence_strength', 0)
        if evidence_score > 70:
            base_prob += 0.1

        # Adjust for violations
        violation_score = leverage_factors.get('violations', 0)
        if violation_score > 70:
            base_prob += 0.15

        return min(base_prob, 0.95)  # Cap at 95%
