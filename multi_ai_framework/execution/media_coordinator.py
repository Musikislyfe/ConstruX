"""
Media Strategy Coordinator
Manages media outreach, press releases, and public relations strategy
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class MediaPackage:
    """Complete media strategy package"""
    case_id: str
    press_release: str
    talking_points: List[str]
    faq: Dict[str, str]
    social_media_strategy: Dict[str, Any]
    media_contacts: List[Dict[str, str]]
    timing_strategy: Dict[str, str]
    risk_assessment: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MediaCoordinator:
    """Coordinates media and public relations strategy"""

    def __init__(self):
        self.media_templates = {
            'press_release': self._create_press_release,
            'social_media': self._create_social_strategy,
            'crisis_response': self._create_crisis_response
        }

    def prepare_media_strategy(self, case_data: Dict[str, Any],
                              strategic_analysis: Dict[str, Any],
                              ai_content: str = "") -> MediaPackage:
        """
        Prepare comprehensive media strategy package

        Args:
            case_data: Case information
            strategic_analysis: Strategic analysis results
            ai_content: AI-generated media content

        Returns:
            Complete media package
        """
        leverage = strategic_analysis.get('leverage_analysis', {})
        public_interest_score = leverage.get('leverage_factors', {}).get('public_exposure', 0)

        # Generate press release
        press_release = self._create_press_release(case_data, strategic_analysis, ai_content)

        # Create talking points
        talking_points = self._create_talking_points(case_data, strategic_analysis)

        # Generate FAQ
        faq = self._create_faq(case_data)

        # Develop social media strategy
        social_strategy = self._create_social_strategy(
            case_data,
            public_interest_score
        )

        # Identify media contacts
        media_contacts = self._identify_media_contacts(case_data)

        # Create timing strategy
        timing_strategy = self._create_timing_strategy(
            case_data,
            strategic_analysis
        )

        # Assess media risks
        risk_assessment = self._assess_media_risks(case_data, strategic_analysis)

        return MediaPackage(
            case_id=case_data.get('case_id', ''),
            press_release=press_release,
            talking_points=talking_points,
            faq=faq,
            social_media_strategy=social_strategy,
            media_contacts=media_contacts,
            timing_strategy=timing_strategy,
            risk_assessment=risk_assessment,
            metadata={
                'public_interest_score': public_interest_score,
                'recommended_approach': self._determine_media_approach(public_interest_score),
                'generation_date': datetime.now().isoformat()
            }
        )

    def _create_press_release(self, case_data: Dict[str, Any],
                            strategic_analysis: Dict[str, Any],
                            ai_content: str) -> str:
        """Create press release"""
        if ai_content:
            return ai_content

        complainant = case_data.get('complainant_name', 'Individual')
        employer = case_data.get('employer_name', 'Employer')
        location = case_data.get('location', 'Location')

        press_release = f"""FOR IMMEDIATE RELEASE
{datetime.now().strftime('%B %d, %Y')}

{complainant} Files Discrimination and Safety Complaints Against {employer}

{location} - {complainant} has filed formal complaints with multiple regulatory agencies alleging disability discrimination, safety violations, and wrongful termination against {employer}.

BACKGROUND:
{case_data.get('case_summary', 'Worker experienced discrimination and unsafe working conditions.')}

KEY ALLEGATIONS:
"""
        for claim in case_data.get('claim_types', []):
            press_release += f"• {claim.replace('_', ' ').title()}\n"

        violations = strategic_analysis.get('leverage_analysis', {}).get('leverage_factors', {})

        press_release += f"""
SAFETY VIOLATIONS:
Regulatory complaints detail multiple building safety violations and OSHA violations at the facility.

REGULATORY ACTION:
Complaints have been filed with:
• Occupational Safety and Health Administration (OSHA)
• Equal Employment Opportunity Commission (EEOC)
• California Civil Rights Department

STATEMENT:
"{case_data.get('complainant_statement', 'I am standing up for my rights and the safety of all workers.')}"

CONTACT:
[Attorney Name]
[Law Firm]
[Phone]
[Email]

###
"""
        return press_release

    def _create_talking_points(self, case_data: Dict[str, Any],
                             strategic_analysis: Dict[str, Any]) -> List[str]:
        """Create media talking points"""
        talking_points = [
            f"This case involves serious disability discrimination and safety violations",
            f"Multiple regulatory complaints have been filed with appropriate agencies",
            f"The complainant exhausted all internal remedies before filing externally",
            f"We have substantial evidence supporting all claims",
            f"This is about protecting worker rights and workplace safety"
        ]

        # Add leverage-specific talking points
        leverage_factors = strategic_analysis.get('leverage_analysis', {}).get('leverage_factors', {})

        if leverage_factors.get('violations', 0) > 60:
            talking_points.append(
                "Documented building safety violations put all workers at risk"
            )

        if 'disability_discrimination' in case_data.get('claim_types', []):
            talking_points.append(
                "Reasonable accommodations were requested and wrongfully denied"
            )

        if leverage_factors.get('regulatory_risk', 0) > 60:
            talking_points.append(
                "Regulatory investigations are expected based on the evidence"
            )

        return talking_points

    def _create_faq(self, case_data: Dict[str, Any]) -> Dict[str, str]:
        """Create FAQ for media inquiries"""
        return {
            "What are the main allegations?":
                f"Disability discrimination, wrongful termination, and workplace safety violations.",

            "What agencies are investigating?":
                "OSHA, EEOC, and California Civil Rights Department have received complaints.",

            "What is being requested?":
                "Full investigation, remediation of safety hazards, and compensation for damages.",

            "Did the worker complain internally first?":
                "Yes, internal complaints were made and were met with retaliation.",

            "What makes this case significant?":
                "It highlights the intersection of disability rights and workplace safety.",

            "Is there a settlement demand?":
                "A pre-litigation settlement demand has been presented to the employer.",

            "What happens next?":
                "We are awaiting regulatory agency action and employer response to settlement demand.",

            "Are other workers affected?":
                "The safety violations potentially affect all workers at the facility."
        }

    def _create_social_strategy(self, case_data: Dict[str, Any],
                               public_interest_score: float) -> Dict[str, Any]:
        """Create social media strategy"""
        strategy = {
            'approach': 'measured' if public_interest_score < 50 else 'active',
            'platforms': [],
            'posting_schedule': {},
            'hashtags': [],
            'content_themes': []
        }

        if public_interest_score > 40:
            strategy['platforms'] = ['Twitter/X', 'LinkedIn']
            strategy['hashtags'] = [
                '#WorkerRights',
                '#DisabilityRights',
                '#WorkplaceSafety',
                '#EmploymentLaw'
            ]
            strategy['content_themes'] = [
                'Worker protection',
                'Disability accommodation',
                'Workplace safety',
                'Legal accountability'
            ]

        if public_interest_score > 70:
            strategy['platforms'].append('Facebook')
            strategy['approach'] = 'aggressive'
            strategy['posting_schedule'] = {
                'initial': 'Post press release and key facts',
                'day_2-7': 'Share relevant statistics and legal information',
                'ongoing': 'Update on regulatory responses and case progress'
            }

        return strategy

    def _identify_media_contacts(self, case_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Identify relevant media contacts"""
        contacts = [
            {
                'outlet': 'Local News Stations',
                'focus': 'Local workplace issues',
                'priority': 'HIGH'
            },
            {
                'outlet': 'Labor and Employment Media',
                'focus': 'Worker rights stories',
                'priority': 'MEDIUM'
            },
            {
                'outlet': 'Disability Rights Media',
                'focus': 'ADA and disability issues',
                'priority': 'MEDIUM'
            }
        ]

        # Add specific outlet recommendations based on case
        if case_data.get('location'):
            contacts.insert(0, {
                'outlet': f"{case_data['location']} Local Press",
                'focus': 'Local business accountability',
                'priority': 'HIGH'
            })

        return contacts

    def _create_timing_strategy(self, case_data: Dict[str, Any],
                               strategic_analysis: Dict[str, Any]) -> Dict[str, str]:
        """Create media timing strategy"""
        return {
            'initial_release': 'Coordinate with regulatory complaint filing',
            'follow_up': 'Update media when agencies respond or investigate',
            'settlement_news': 'Coordinate with legal team before any settlement announcements',
            'optimal_timing': 'Weekday mornings for maximum pickup',
            'avoid': 'Major news event days, holidays, late Fridays'
        }

    def _assess_media_risks(self, case_data: Dict[str, Any],
                          strategic_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks of media strategy"""
        risks = {
            'reputational_risk_to_opponent': 'HIGH',
            'potential_responses': [
                'Employer may issue denial statement',
                'Employer may attempt damage control',
                'Employer may seek to discredit complainant'
            ],
            'mitigation_strategies': [
                'Stick to documented facts only',
                'Maintain professional tone',
                'Emphasize regulatory validation',
                'Avoid inflammatory language',
                'Prepare for counter-narrative'
            ],
            'legal_considerations': [
                'Avoid defamatory statements',
                'Verify all facts before public release',
                'Coordinate with legal counsel',
                'Preserve confidentiality where required'
            ]
        }

        return risks

    def _determine_media_approach(self, public_interest_score: float) -> str:
        """Determine recommended media approach"""
        if public_interest_score > 70:
            return "ACTIVE: Proactive media outreach and sustained coverage"
        elif public_interest_score > 50:
            return "MODERATE: Strategic media placement when advantageous"
        elif public_interest_score > 30:
            return "REACTIVE: Respond to inquiries, limited proactive outreach"
        else:
            return "MINIMAL: Focus on regulatory channels, avoid media"

    def export_media_package(self, media_package: MediaPackage, output_dir: str):
        """Export media package to files"""
        from pathlib import Path
        import json

        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Export press release
        with open(f"{output_dir}/press_release.txt", 'w') as f:
            f.write(media_package.press_release)

        # Export talking points
        with open(f"{output_dir}/talking_points.txt", 'w') as f:
            f.write("MEDIA TALKING POINTS\n")
            f.write("=" * 50 + "\n\n")
            for i, point in enumerate(media_package.talking_points, 1):
                f.write(f"{i}. {point}\n\n")

        # Export FAQ
        with open(f"{output_dir}/media_faq.txt", 'w') as f:
            f.write("MEDIA FAQ\n")
            f.write("=" * 50 + "\n\n")
            for question, answer in media_package.faq.items():
                f.write(f"Q: {question}\n")
                f.write(f"A: {answer}\n\n")

        # Export complete package as JSON
        with open(f"{output_dir}/media_package.json", 'w') as f:
            json.dump(media_package.to_dict(), f, indent=2)
