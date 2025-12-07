"""
Settlement Negotiation Framework
Manages negotiation strategy, position tracking, and deal structuring
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class NegotiationFramework:
    """Settlement negotiation framework"""
    case_id: str
    opening_position: Dict[str, Any]
    target_settlement: Dict[str, Any]
    walkaway_point: Dict[str, Any]
    concession_strategy: Dict[str, Any]
    negotiation_phases: List[Dict[str, Any]]
    deal_terms: Dict[str, List[str]]
    pressure_tactics: List[Dict[str, Any]]
    contingency_plans: List[str]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SettlementNegotiator:
    """Manages settlement negotiation process"""

    def __init__(self):
        self.negotiation_history: List[Dict[str, Any]] = []

    def create_negotiation_framework(self, case_data: Dict[str, Any],
                                    strategic_analysis: Dict[str, Any]) -> NegotiationFramework:
        """
        Create comprehensive negotiation framework

        Args:
            case_data: Case information
            strategic_analysis: Strategic analysis with settlement predictions

        Returns:
            Complete negotiation framework
        """
        settlement_pred = strategic_analysis.get('settlement_prediction', {})
        leverage = strategic_analysis.get('leverage_analysis', {})

        # Define positions
        opening_position = self._define_opening_position(
            case_data,
            settlement_pred
        )

        target_settlement = self._define_target(settlement_pred)

        walkaway_point = self._define_walkaway(settlement_pred)

        # Create concession strategy
        concession_strategy = self._create_concession_strategy(
            opening_position,
            target_settlement,
            walkaway_point,
            leverage
        )

        # Define negotiation phases
        phases = self._define_negotiation_phases(leverage)

        # Structure deal terms
        deal_terms = self._structure_deal_terms(case_data, settlement_pred)

        # Identify pressure tactics
        pressure_tactics = self._identify_pressure_tactics(leverage)

        # Create contingency plans
        contingency_plans = self._create_contingency_plans(case_data, leverage)

        return NegotiationFramework(
            case_id=case_data.get('case_id', ''),
            opening_position=opening_position,
            target_settlement=target_settlement,
            walkaway_point=walkaway_point,
            concession_strategy=concession_strategy,
            negotiation_phases=phases,
            deal_terms=deal_terms,
            pressure_tactics=pressure_tactics,
            contingency_plans=contingency_plans,
            metadata={
                'leverage_score': leverage.get('overall_leverage_score', 0),
                'settlement_probability': settlement_pred.get('confidence_level', 0),
                'creation_date': datetime.now().isoformat()
            }
        )

    def _define_opening_position(self, case_data: Dict[str, Any],
                                settlement_pred: Dict[str, Any]) -> Dict[str, Any]:
        """Define opening negotiation position"""
        demand = settlement_pred.get('recommended_demand', 0)

        return {
            'monetary_demand': demand,
            'non_monetary_terms': [
                'Written acknowledgment of wrongdoing',
                'Policy changes to prevent recurrence',
                'Training for management on disability rights',
                'Neutral employment reference',
                'Removal of negative performance reviews',
                'Mutual non-disparagement',
                'Confidentiality (mutual)'
            ],
            'justification': 'Based on documented violations, comparable settlements, and legal exposure',
            'deadline': '21 days from presentation'
        }

    def _define_target(self, settlement_pred: Dict[str, Any]) -> Dict[str, Any]:
        """Define target settlement outcome"""
        predicted_range = settlement_pred.get('predicted_range', {})
        mid_point = predicted_range.get('mid', 0)

        return {
            'monetary_target': mid_point,
            'acceptable_terms': [
                'Settlement payment (full or structured)',
                'Neutral reference (required)',
                'Mutual release of claims',
                'Confidentiality terms',
                'Non-disparagement (mutual)'
            ],
            'timeline': 'Resolve within 60 days',
            'confidence': settlement_pred.get('confidence_level', 0.5)
        }

    def _define_walkaway(self, settlement_pred: Dict[str, Any]) -> Dict[str, Any]:
        """Define walkaway/floor position"""
        floor = settlement_pred.get('recommended_floor', 0)

        return {
            'minimum_acceptable': floor,
            'required_terms': [
                'Payment of at least floor amount',
                'Neutral employment reference',
                'Release of claims with fair consideration'
            ],
            'deal_breakers': [
                'Non-disclosure that prevents regulatory complaints',
                'Admission of fault by complainant',
                'Non-compete restrictions',
                'Waiver of statutory rights'
            ],
            'alternative': 'Proceed to litigation and regulatory process'
        }

    def _create_concession_strategy(self, opening: Dict[str, Any],
                                   target: Dict[str, Any],
                                   walkaway: Dict[str, Any],
                                   leverage: Dict[str, Any]) -> Dict[str, Any]:
        """Create strategic concession plan"""
        leverage_score = leverage.get('overall_leverage_score', 50)

        # High leverage = fewer/smaller concessions
        if leverage_score > 75:
            concession_rate = 0.05  # 5% per round
            max_rounds = 3
        elif leverage_score > 60:
            concession_rate = 0.08  # 8% per round
            max_rounds = 4
        else:
            concession_rate = 0.10  # 10% per round
            max_rounds = 5

        return {
            'concession_rate': concession_rate,
            'max_negotiation_rounds': max_rounds,
            'concession_schedule': self._create_concession_schedule(
                opening['monetary_demand'],
                target['monetary_target'],
                walkaway['minimum_acceptable'],
                concession_rate,
                max_rounds
            ),
            'non_monetary_concessions': [
                'Confidentiality scope can be negotiated',
                'Settlement structure (lump vs. payments) flexible',
                'Timing of payment negotiable',
                'Language of settlement agreement negotiable'
            ],
            'non_negotiable': [
                'Minimum monetary floor',
                'Neutral employment reference',
                'No admission of fault by complainant'
            ]
        }

    def _create_concession_schedule(self, opening: float, target: float,
                                   floor: float, rate: float,
                                   max_rounds: int) -> List[Dict[str, Any]]:
        """Create specific concession schedule"""
        schedule = []
        current_position = opening

        for round_num in range(1, max_rounds + 1):
            concession_amount = current_position * rate
            new_position = max(current_position - concession_amount, floor)

            schedule.append({
                'round': round_num,
                'position': new_position,
                'concession_amount': current_position - new_position,
                'rationale': self._get_concession_rationale(round_num, new_position, target),
                'require_reciprocal': round_num > 1  # After round 1, require counter-offer
            })

            current_position = new_position

            if new_position <= target:
                break

        return schedule

    def _get_concession_rationale(self, round_num: int, position: float,
                                 target: float) -> str:
        """Get rationale for concession"""
        if round_num == 1:
            return "Initial negotiation positioning"
        elif position > target:
            return "Moving toward middle ground, require substantial counter-offer"
        elif position == target:
            return "At target settlement point - final offer"
        else:
            return "Below target - approaching floor"

    def _define_negotiation_phases(self, leverage: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Define phases of negotiation"""
        return [
            {
                'phase': 'Opening',
                'duration': '1-2 weeks',
                'objectives': [
                    'Present demand with full justification',
                    'Demonstrate case strength',
                    'Set negotiation tone and timeline',
                    'Gauge opponent response'
                ],
                'tactics': [
                    'Present comprehensive evidence package',
                    'Cite comparable settlements',
                    'Emphasize regulatory complaints ready to file',
                    'Set firm response deadline'
                ]
            },
            {
                'phase': 'Information Exchange',
                'duration': '1-3 weeks',
                'objectives': [
                    'Assess opponent\'s position and constraints',
                    'Identify decision-makers',
                    'Understand their settlement authority',
                    'Probe for weaknesses in their position'
                ],
                'tactics': [
                    'Request their valuation and basis',
                    'Ask about decision-making process',
                    'Identify their key concerns',
                    'Maintain pressure through regulatory timeline'
                ]
            },
            {
                'phase': 'Active Negotiation',
                'duration': '2-4 weeks',
                'objectives': [
                    'Move toward target settlement',
                    'Structure deal terms',
                    'Build agreement framework',
                    'Resolve key obstacles'
                ],
                'tactics': [
                    'Strategic concessions tied to counter-offers',
                    'Package monetary and non-monetary terms',
                    'Create momentum toward resolution',
                    'Apply escalating pressure if stalled'
                ]
            },
            {
                'phase': 'Closing',
                'duration': '1-2 weeks',
                'objectives': [
                    'Finalize settlement amount',
                    'Draft settlement agreement',
                    'Address final concerns',
                    'Execute agreement'
                ],
                'tactics': [
                    'Make final offer if near target',
                    'Provide short deadline for acceptance',
                    'Prepare to walk away if needed',
                    'Document all agreed terms'
                ]
            }
        ]

    def _structure_deal_terms(self, case_data: Dict[str, Any],
                             settlement_pred: Dict[str, Any]) -> Dict[str, List[str]]:
        """Structure negotiable vs. non-negotiable terms"""
        return {
            'monetary_terms': [
                'Settlement amount',
                'Payment structure (lump sum vs. payments)',
                'Payment timing',
                'Tax treatment considerations',
                'Interest on delayed payment'
            ],
            'employment_terms': [
                'Neutral reference (non-negotiable)',
                'Reference letter content',
                'Removal of negative records',
                'Eligibility for rehire statement'
            ],
            'confidentiality_terms': [
                'Scope of confidentiality',
                'Exceptions (government agencies, taxes, advisors)',
                'Public disclosure limitations',
                'Social media restrictions'
            ],
            'future_conduct_terms': [
                'Mutual non-disparagement',
                'No-retaliation provisions',
                'Cooperation with investigations',
                'No-rehire provisions'
            ],
            'structural_terms': [
                'General release of claims',
                'Mutual release vs. unilateral',
                'Waiver of ADEA claims (if applicable)',
                'Dispute resolution for agreement',
                'Entire agreement clause'
            ]
        }

    def _identify_pressure_tactics(self, leverage: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify available pressure tactics"""
        tactics = []

        pressure_points = leverage.get('pressure_points', [])

        for point in pressure_points:
            factor = point.get('factor', '')
            score = point.get('leverage_score', 0)

            if factor == 'violations' and score > 60:
                tactics.append({
                    'tactic': 'Regulatory Filing Pressure',
                    'timing': 'If no response within deadline',
                    'action': 'File OSHA, EEOC, and other regulatory complaints',
                    'impact': 'Triggers investigations, increases defense costs'
                })

            if factor == 'public_exposure' and score > 50:
                tactics.append({
                    'tactic': 'Media Pressure',
                    'timing': 'If negotiations stall',
                    'action': 'Release information to media',
                    'impact': 'Reputational damage, public scrutiny'
                })

            if factor == 'regulatory_risk' and score > 60:
                tactics.append({
                    'tactic': 'Escalating Regulatory Action',
                    'timing': 'Progressive throughout negotiation',
                    'action': 'Follow up with agencies, provide additional evidence',
                    'impact': 'Increases likelihood of enforcement action'
                })

        # Always available tactics
        tactics.extend([
            {
                'tactic': 'Litigation Threat',
                'timing': 'If settlement negotiations fail',
                'action': 'File civil lawsuit',
                'impact': 'Discovery, depositions, trial risk, attorney fees'
            },
            {
                'tactic': 'Deadline Pressure',
                'timing': 'Throughout negotiation',
                'action': 'Impose and enforce response deadlines',
                'impact': 'Forces decision-making, prevents delay tactics'
            }
        ])

        return tactics

    def _create_contingency_plans(self, case_data: Dict[str, Any],
                                 leverage: Dict[str, Any]) -> List[str]:
        """Create contingency plans for different scenarios"""
        return [
            "If lowball offer: Reiterate evidence and comparable settlements, set short deadline for serious offer",
            "If no response: File regulatory complaints and send follow-up with final deadline",
            "If denial of liability: Present key evidence, offer to mediate with neutral third party",
            "If negotiations stall: Escalate pressure through regulatory and/or media channels",
            "If unreasonable demands: Walk away and proceed to litigation",
            "If good faith negotiation: Work toward mutual resolution within acceptable range",
            "If partial agreement: Document agreed terms, continue negotiating disputed issues",
            "If opponent requests mediation: Agree if within reasonable timeframe and they cover costs"
        ]

    def export_negotiation_framework(self, framework: NegotiationFramework,
                                   output_path: str):
        """Export negotiation framework to file"""
        import json

        with open(output_path, 'w') as f:
            json.dump(framework.to_dict(), f, indent=2)

        # Also create readable text version
        text_path = output_path.replace('.json', '.txt')
        with open(text_path, 'w') as f:
            f.write("SETTLEMENT NEGOTIATION FRAMEWORK\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Opening Position: ${framework.opening_position['monetary_demand']:,.0f}\n")
            f.write(f"Target Settlement: ${framework.target_settlement['monetary_target']:,.0f}\n")
            f.write(f"Walkaway Point: ${framework.walkaway_point['minimum_acceptable']:,.0f}\n\n")

            f.write("NEGOTIATION PHASES:\n")
            for phase in framework.negotiation_phases:
                f.write(f"\n{phase['phase']} ({phase['duration']})\n")
                f.write(f"Objectives: {', '.join(phase['objectives'])}\n")

            f.write("\n\nPRESSURE TACTICS:\n")
            for tactic in framework.pressure_tactics:
                f.write(f"\n- {tactic['tactic']}\n")
                f.write(f"  Timing: {tactic['timing']}\n")
                f.write(f"  Impact: {tactic['impact']}\n")
