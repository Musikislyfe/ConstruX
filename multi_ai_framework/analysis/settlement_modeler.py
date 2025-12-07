"""
Settlement Prediction and Modeling
Models settlement ranges and negotiation strategies
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import statistics


@dataclass
class SettlementPrediction:
    """Settlement prediction model results"""
    case_id: str
    predicted_range: Dict[str, float]  # low, mid, high
    confidence_level: float  # 0-1
    comparable_cases: List[Dict[str, Any]]
    factors_affecting_value: Dict[str, float]
    recommended_demand: float
    recommended_floor: float
    negotiation_strategy: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SettlementModeler:
    """Predicts settlement values and models negotiation scenarios"""

    def __init__(self):
        self.value_multipliers = {
            'wrongful_termination': {'base': 50000, 'max': 500000},
            'disability_discrimination': {'base': 75000, 'max': 750000},
            'harassment': {'base': 60000, 'max': 600000},
            'retaliation': {'base': 45000, 'max': 450000},
            'wage_claims': {'base': 'calculated', 'max': 300000}
        }

    def model_settlement(self, case_data: Dict[str, Any],
                        leverage_analysis: Dict[str, Any]) -> SettlementPrediction:
        """
        Model settlement prediction

        Args:
            case_data: Case information including claims and damages
            leverage_analysis: Leverage analysis results

        Returns:
            Settlement prediction with ranges and strategy
        """
        # Calculate base value
        base_value = self._calculate_base_value(case_data)

        # Apply leverage multipliers
        leverage_score = leverage_analysis.get('overall_leverage_score', 50)
        leverage_multiplier = self._calculate_leverage_multiplier(leverage_score)

        # Calculate predicted range
        predicted_range = {
            'low': base_value * 0.5 * leverage_multiplier,
            'mid': base_value * leverage_multiplier,
            'high': base_value * 1.5 * leverage_multiplier
        }

        # Find comparable cases
        comparable_cases = self._find_comparable_cases(case_data)

        # Calculate confidence level
        confidence = self._calculate_confidence(
            leverage_analysis,
            len(comparable_cases)
        )

        # Identify value factors
        value_factors = self._identify_value_factors(
            case_data,
            leverage_analysis
        )

        # Calculate recommended demand and floor
        recommended_demand = self._calculate_demand(
            predicted_range['high'],
            leverage_score
        )

        recommended_floor = self._calculate_floor(
            predicted_range['low'],
            case_data
        )

        # Determine negotiation strategy
        strategy = self._determine_negotiation_strategy(
            leverage_score,
            confidence,
            predicted_range
        )

        return SettlementPrediction(
            case_id=case_data.get('case_id', 'unknown'),
            predicted_range=predicted_range,
            confidence_level=confidence,
            comparable_cases=comparable_cases,
            factors_affecting_value=value_factors,
            recommended_demand=recommended_demand,
            recommended_floor=recommended_floor,
            negotiation_strategy=strategy,
            metadata={
                'base_value': base_value,
                'leverage_multiplier': leverage_multiplier,
                'leverage_score': leverage_score
            }
        )

    def _calculate_base_value(self, case_data: Dict[str, Any]) -> float:
        """Calculate base settlement value"""
        claim_types = case_data.get('claim_types', [])
        economic_damages = case_data.get('economic_damages', 0)

        # Start with economic damages
        base_value = economic_damages

        # Add claim type values
        for claim_type in claim_types:
            if claim_type in self.value_multipliers:
                claim_base = self.value_multipliers[claim_type]['base']
                if isinstance(claim_base, (int, float)):
                    base_value += claim_base

        # Add emotional distress damages
        emotional_distress = case_data.get('emotional_distress_severity', 0)  # 0-10 scale
        base_value += emotional_distress * 10000  # $10k per severity point

        # Add punitive damages potential
        if case_data.get('punitive_damages_viable', False):
            base_value *= 1.5

        return max(base_value, 25000)  # Minimum base value

    def _calculate_leverage_multiplier(self, leverage_score: float) -> float:
        """Calculate multiplier based on leverage score"""
        # Convert 0-100 score to 0.5-2.0 multiplier
        # 50 = 1.0x, 100 = 2.0x, 0 = 0.5x
        return 0.5 + (leverage_score / 100) * 1.5

    def _find_comparable_cases(self, case_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find comparable case settlements
        In production, this would query a database of actual settlements
        """
        # Placeholder comparable cases
        claim_types = case_data.get('claim_types', [])
        jurisdiction = case_data.get('jurisdiction', 'unknown')

        comparables = []

        # Simulated comparable data
        if 'wrongful_termination' in claim_types:
            comparables.append({
                'case_name': 'Similar Case 2023',
                'jurisdiction': jurisdiction,
                'settlement_amount': 175000,
                'claim_types': ['wrongful_termination', 'disability_discrimination'],
                'similarity_score': 0.85
            })

        if 'disability_discrimination' in claim_types:
            comparables.append({
                'case_name': 'ADA Case 2022',
                'jurisdiction': jurisdiction,
                'settlement_amount': 250000,
                'claim_types': ['disability_discrimination'],
                'similarity_score': 0.78
            })

        return comparables

    def _calculate_confidence(self, leverage_analysis: Dict[str, Any],
                            comparable_count: int) -> float:
        """Calculate confidence level in prediction (0-1)"""
        confidence = 0.5  # Base confidence

        # More evidence increases confidence
        evidence_strength = leverage_analysis.get('leverage_factors', {}).get('evidence_strength', 0)
        confidence += (evidence_strength / 100) * 0.2

        # More comparable cases increase confidence
        confidence += min(comparable_count * 0.1, 0.2)

        # Higher overall leverage increases confidence
        leverage_score = leverage_analysis.get('overall_leverage_score', 50)
        if leverage_score > 70:
            confidence += 0.1

        return min(confidence, 0.95)  # Cap at 95%

    def _identify_value_factors(self, case_data: Dict[str, Any],
                               leverage_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Identify factors affecting case value"""
        factors = {}

        # Economic damages factor
        economic = case_data.get('economic_damages', 0)
        if economic > 0:
            factors['economic_damages'] = min((economic / 100000) * 20, 30)

        # Evidence strength
        evidence_score = leverage_analysis.get('leverage_factors', {}).get('evidence_strength', 0)
        factors['evidence_strength'] = evidence_score * 0.25

        # Violations impact
        violation_score = leverage_analysis.get('leverage_factors', {}).get('violations', 0)
        factors['violations_impact'] = violation_score * 0.30

        # Emotional distress
        emotional = case_data.get('emotional_distress_severity', 0)
        factors['emotional_distress'] = emotional * 2.5

        # Public interest/exposure
        exposure = leverage_analysis.get('leverage_factors', {}).get('public_exposure', 0)
        factors['public_exposure'] = exposure * 0.15

        return factors

    def _calculate_demand(self, high_estimate: float, leverage_score: float) -> float:
        """Calculate recommended initial demand"""
        # Start higher when leverage is strong
        if leverage_score > 75:
            return high_estimate * 1.4
        elif leverage_score > 60:
            return high_estimate * 1.3
        elif leverage_score > 45:
            return high_estimate * 1.2
        else:
            return high_estimate * 1.1

    def _calculate_floor(self, low_estimate: float, case_data: Dict[str, Any]) -> float:
        """Calculate recommended settlement floor (minimum acceptable)"""
        # Floor should cover at minimum economic damages + something for time/effort
        economic_damages = case_data.get('economic_damages', 0)
        floor = max(low_estimate * 0.8, economic_damages + 15000)

        return floor

    def _determine_negotiation_strategy(self, leverage_score: float,
                                       confidence: float,
                                       predicted_range: Dict[str, float]) -> str:
        """Determine recommended negotiation strategy"""
        if leverage_score > 75 and confidence > 0.7:
            return """AGGRESSIVE ANCHORING:
- Lead with high demand backed by evidence
- Set tight negotiation timeline
- Emphasize regulatory/media risks
- Minimal initial concessions"""

        elif leverage_score > 60 and confidence > 0.6:
            return """PRINCIPLED NEGOTIATION:
- Present justified demand with comparables
- Structured negotiation phases
- Evidence-based concessions only
- Multiple pressure points"""

        elif leverage_score > 45:
            return """COLLABORATIVE APPROACH:
- Reasonable opening position
- Focus on mutual resolution
- Gradual concession strategy
- Emphasize cost of litigation"""

        else:
            return """EXPLORATORY NEGOTIATION:
- Gather information on opponent's position
- Build leverage through discovery
- Flexible positioning
- Keep options open"""

    def model_negotiation_scenarios(self, settlement_prediction: SettlementPrediction,
                                   concession_rate: float = 0.1) -> List[Dict[str, Any]]:
        """
        Model different negotiation scenarios

        Args:
            settlement_prediction: Base settlement prediction
            concession_rate: Concession rate per round (default 10%)

        Returns:
            List of scenario outcomes
        """
        scenarios = []

        initial_demand = settlement_prediction.recommended_demand
        floor = settlement_prediction.recommended_floor

        # Scenario 1: Quick settlement
        scenarios.append({
            'scenario': 'Quick Settlement',
            'rounds': 2,
            'final_amount': initial_demand * 0.85,
            'probability': 0.3,
            'timeline': '2-4 weeks'
        })

        # Scenario 2: Standard negotiation
        scenarios.append({
            'scenario': 'Standard Negotiation',
            'rounds': 4,
            'final_amount': settlement_prediction.predicted_range['mid'],
            'probability': 0.5,
            'timeline': '6-12 weeks'
        })

        # Scenario 3: Extended negotiation
        scenarios.append({
            'scenario': 'Extended Negotiation',
            'rounds': 6,
            'final_amount': settlement_prediction.predicted_range['mid'] * 0.9,
            'probability': 0.15,
            'timeline': '3-6 months'
        })

        # Scenario 4: Trial risk
        scenarios.append({
            'scenario': 'Trial',
            'rounds': 0,
            'final_amount': settlement_prediction.predicted_range['high'] * 1.2,
            'probability': 0.05,
            'timeline': '12-24 months'
        })

        return scenarios
