"""
Complaint Generation System
Creates regulatory complaints, legal demands, and formal filings
"""

from typing import Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class ComplaintPackage:
    """Complete complaint package"""
    case_id: str
    complaint_type: str  # osha, ada, legal_demand, etc.
    title: str
    body: str
    supporting_facts: List[str]
    legal_basis: List[str]
    requested_relief: List[str]
    attachments: List[str]
    filing_instructions: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ComplaintGenerator:
    """Generates formatted complaints for various agencies and purposes"""

    def __init__(self):
        self.complaint_templates = {
            'osha': self._osha_template,
            'ada': self._ada_template,
            'eeoc': self._eeoc_template,
            'settlement_demand': self._settlement_demand_template,
            'regulatory': self._regulatory_template
        }

    def generate_complaints(self, case_data: Dict[str, Any],
                          strategic_analysis: Dict[str, Any],
                          ai_content: str = "") -> List[ComplaintPackage]:
        """
        Generate all appropriate complaints for a case

        Args:
            case_data: Case information
            strategic_analysis: Strategic analysis results
            ai_content: AI-generated complaint content

        Returns:
            List of complaint packages ready for filing
        """
        complaints = []

        # Determine which complaints to generate
        violation_types = self._identify_violation_types(case_data)

        for violation_type in violation_types:
            if violation_type in self.complaint_templates:
                complaint = self.complaint_templates[violation_type](
                    case_data,
                    strategic_analysis,
                    ai_content
                )
                complaints.append(complaint)

        # Always generate settlement demand
        settlement_demand = self._settlement_demand_template(
            case_data,
            strategic_analysis,
            ai_content
        )
        complaints.append(settlement_demand)

        return complaints

    def _identify_violation_types(self, case_data: Dict[str, Any]) -> List[str]:
        """Identify what types of complaints should be filed"""
        violations = []

        claim_types = case_data.get('claim_types', [])

        if 'safety_violations' in case_data.get('issues', []):
            violations.append('osha')

        if 'disability_discrimination' in claim_types:
            violations.append('ada')

        if any(claim in claim_types for claim in ['discrimination', 'harassment', 'retaliation']):
            violations.append('eeoc')

        violations.append('settlement_demand')

        return violations

    def _osha_template(self, case_data: Dict[str, Any],
                      strategic_analysis: Dict[str, Any],
                      ai_content: str) -> ComplaintPackage:
        """Generate OSHA complaint"""
        return ComplaintPackage(
            case_id=case_data.get('case_id', ''),
            complaint_type='osha',
            title=f"OSHA Safety Complaint - {case_data.get('location', '')}",
            body=self._generate_osha_body(case_data, ai_content),
            supporting_facts=self._extract_safety_facts(case_data),
            legal_basis=[
                "Occupational Safety and Health Act of 1970",
                "29 USC § 654 - General Duty Clause",
                "29 CFR 1910 - Occupational Safety Standards"
            ],
            requested_relief=[
                "Immediate workplace inspection",
                "Citation of safety violations",
                "Required remediation of hazards",
                "Protection from retaliation"
            ],
            attachments=self._list_safety_evidence(case_data),
            filing_instructions={
                'method': 'Online at osha.gov or phone 1-800-321-OSHA',
                'agency': 'Occupational Safety and Health Administration',
                'timeline': 'File immediately - no statute of limitations',
                'anonymity': 'Can request confidential complainant status'
            },
            metadata={
                'priority': 'HIGH',
                'estimated_impact': 'Regulatory investigation likely',
                'generation_date': datetime.now().isoformat()
            }
        )

    def _ada_template(self, case_data: Dict[str, Any],
                     strategic_analysis: Dict[str, Any],
                     ai_content: str) -> ComplaintPackage:
        """Generate ADA complaint"""
        return ComplaintPackage(
            case_id=case_data.get('case_id', ''),
            complaint_type='ada',
            title=f"ADA Discrimination Complaint - {case_data.get('complainant_name', 'Confidential')}",
            body=self._generate_ada_body(case_data, ai_content),
            supporting_facts=self._extract_ada_facts(case_data),
            legal_basis=[
                "Americans with Disabilities Act (ADA)",
                "42 USC § 12101 et seq.",
                "Rehabilitation Act of 1973 § 504",
                "Fair Employment and Housing Act (California)"
            ],
            requested_relief=[
                "Investigation of disability discrimination",
                "Accommodation compliance review",
                "Compensatory damages",
                "Policy changes and training"
            ],
            attachments=self._list_ada_evidence(case_data),
            filing_instructions={
                'method': 'File with EEOC and state DFEH/CRD',
                'timeline': '300 days from last discriminatory act',
                'dual_filing': 'EEOC automatically cross-files with state agency'
            },
            metadata={
                'priority': 'HIGH',
                'generation_date': datetime.now().isoformat()
            }
        )

    def _eeoc_template(self, case_data: Dict[str, Any],
                      strategic_analysis: Dict[str, Any],
                      ai_content: str) -> ComplaintPackage:
        """Generate EEOC complaint"""
        return ComplaintPackage(
            case_id=case_data.get('case_id', ''),
            complaint_type='eeoc',
            title=f"EEOC Charge of Discrimination",
            body=self._generate_eeoc_body(case_data, ai_content),
            supporting_facts=self._extract_eeoc_facts(case_data),
            legal_basis=[
                "Title VII of the Civil Rights Act of 1964",
                "Americans with Disabilities Act (ADA)",
                "Age Discrimination in Employment Act (ADEA)",
                "California Fair Employment and Housing Act"
            ],
            requested_relief=[
                "Full investigation of discrimination claims",
                "Reinstatement or front pay",
                "Back pay and lost benefits",
                "Compensatory and punitive damages",
                "Policy changes and training"
            ],
            attachments=self._list_employment_evidence(case_data),
            filing_instructions={
                'method': 'Online at eeoc.gov or in-person appointment',
                'timeline': '300 days from last discriminatory act (California)',
                'dual_filing': 'Automatically filed with state CRD'
            },
            metadata={
                'priority': 'CRITICAL',
                'generation_date': datetime.now().isoformat()
            }
        )

    def _settlement_demand_template(self, case_data: Dict[str, Any],
                                   strategic_analysis: Dict[str, Any],
                                   ai_content: str) -> ComplaintPackage:
        """Generate settlement demand letter"""
        settlement_pred = strategic_analysis.get('settlement_prediction', {})
        leverage = strategic_analysis.get('leverage_analysis', {})

        demand_amount = settlement_pred.get('recommended_demand', 0)

        return ComplaintPackage(
            case_id=case_data.get('case_id', ''),
            complaint_type='settlement_demand',
            title=f"Pre-Litigation Settlement Demand",
            body=self._generate_settlement_demand_body(
                case_data,
                strategic_analysis,
                demand_amount,
                ai_content
            ),
            supporting_facts=self._extract_all_facts(case_data),
            legal_basis=self._extract_legal_theories(case_data),
            requested_relief=[
                f"Settlement payment: ${demand_amount:,.0f}",
                "Written apology and acknowledgment",
                "Policy changes to prevent recurrence",
                "Neutral employment reference",
                "Non-disparagement agreement (mutual)",
                "Confidential settlement terms"
            ],
            attachments=self._list_all_evidence(case_data),
            filing_instructions={
                'delivery_method': 'Certified mail and email to legal counsel',
                'response_deadline': '21 days from receipt',
                'escalation': 'Regulatory filings and litigation if no response'
            },
            metadata={
                'priority': 'CRITICAL',
                'leverage_score': leverage.get('overall_leverage_score', 0),
                'settlement_probability': settlement_pred.get('confidence_level', 0),
                'generation_date': datetime.now().isoformat()
            }
        )

    def _regulatory_template(self, case_data: Dict[str, Any],
                           strategic_analysis: Dict[str, Any],
                           ai_content: str) -> ComplaintPackage:
        """Generate general regulatory complaint"""
        return ComplaintPackage(
            case_id=case_data.get('case_id', ''),
            complaint_type='regulatory',
            title=f"Regulatory Complaint - Multiple Violations",
            body=self._generate_regulatory_body(case_data, ai_content),
            supporting_facts=self._extract_all_facts(case_data),
            legal_basis=[
                "Applicable building codes",
                "Safety regulations",
                "Employment laws",
                "Disability rights statutes"
            ],
            requested_relief=[
                "Full investigation of violations",
                "Enforcement action against responsible parties",
                "Required remediation",
                "Protection from retaliation"
            ],
            attachments=self._list_all_evidence(case_data),
            filing_instructions={
                'agencies': 'Multiple - based on violation types',
                'coordination': 'Coordinate filing timing for maximum impact'
            },
            metadata={
                'priority': 'HIGH',
                'generation_date': datetime.now().isoformat()
            }
        )

    # Helper methods for generating complaint bodies
    def _generate_osha_body(self, case_data: Dict[str, Any], ai_content: str) -> str:
        if ai_content:
            return ai_content

        location = case_data.get('location', 'workplace')
        violations = case_data.get('safety_violations', [])

        body = f"""OSHA SAFETY COMPLAINT

Location: {location}
Date of Violations: {case_data.get('violation_dates', 'Ongoing')}

SAFETY HAZARDS IDENTIFIED:

"""
        for i, violation in enumerate(violations, 1):
            body += f"{i}. {violation}\n"

        body += """
These conditions create immediate danger to workers and violate OSHA safety standards.
I request immediate inspection and enforcement action.

I also request protection from retaliation under 29 USC § 660(c).
"""
        return body

    def _generate_ada_body(self, case_data: Dict[str, Any], ai_content: str) -> str:
        if ai_content:
            return ai_content

        return f"""ADA DISCRIMINATION COMPLAINT

I am filing this complaint regarding disability discrimination and failure to provide reasonable accommodations.

DISABILITY: {case_data.get('disability_type', 'Medical condition')}

DISCRIMINATION EXPERIENCED:
{case_data.get('discrimination_description', 'Discriminatory treatment based on disability')}

ACCOMMODATIONS REQUESTED BUT DENIED:
{case_data.get('denied_accommodations', 'Reasonable accommodations were requested but denied')}

ADVERSE ACTIONS TAKEN:
{case_data.get('adverse_actions', 'Termination and adverse treatment')}

This constitutes illegal disability discrimination under the ADA and California law.
"""

    def _generate_eeoc_body(self, case_data: Dict[str, Any], ai_content: str) -> str:
        if ai_content:
            return ai_content

        return f"""CHARGE OF DISCRIMINATION

COMPLAINANT: {case_data.get('complainant_name', 'Name on file')}
EMPLOYER: {case_data.get('employer_name', 'Employer name')}
BASIS: Disability, Retaliation

PARTICULARS:
I was employed as {case_data.get('position', 'employee')} from {case_data.get('employment_dates', 'dates on file')}.

I experienced discrimination based on my disability and was terminated in retaliation for requesting accommodations and reporting safety violations.

{case_data.get('discrimination_details', 'Detailed discrimination description')}

I request investigation and full relief including reinstatement, back pay, and damages.
"""

    def _generate_settlement_demand_body(self, case_data: Dict[str, Any],
                                       strategic_analysis: Dict[str, Any],
                                       demand_amount: float,
                                       ai_content: str) -> str:
        if ai_content:
            return ai_content

        leverage = strategic_analysis.get('leverage_analysis', {})
        pressure_points = leverage.get('pressure_points', [])

        body = f"""PRE-LITIGATION SETTLEMENT DEMAND

RE: {case_data.get('complainant_name', 'Claimant')} v. {case_data.get('employer_name', 'Employer')}

Dear Counsel,

This letter constitutes a formal settlement demand prior to litigation.

FACTUAL BACKGROUND:
{case_data.get('case_summary', 'Summary of facts')}

LEGAL VIOLATIONS:
"""
        for claim in case_data.get('claim_types', []):
            body += f"- {claim.replace('_', ' ').title()}\n"

        body += f"""
EVIDENCE:
We possess substantial evidence including documents, testimony, and regulatory violations.

KEY PRESSURE POINTS:
"""
        for pp in pressure_points[:3]:
            body += f"- {pp.get('factor', '').replace('_', ' ').title()}\n"

        body += f"""
DAMAGES AND SETTLEMENT DEMAND:
Based on the strength of our case and comparable settlements, we demand ${demand_amount:,.0f} to resolve all claims.

This demand is valid for 21 days. Failure to engage in good faith settlement negotiations will result in:
- Regulatory complaints with OSHA, EEOC, and other agencies
- Civil litigation seeking full damages
- Potential media exposure of violations

Please respond within 21 days to discuss resolution.

Respectfully,
[Attorney Name]
"""
        return body

    def _generate_regulatory_body(self, case_data: Dict[str, Any], ai_content: str) -> str:
        if ai_content:
            return ai_content

        return "Comprehensive regulatory complaint detailing all violations."

    # Helper methods for extracting facts and evidence
    def _extract_safety_facts(self, case_data: Dict[str, Any]) -> List[str]:
        return case_data.get('safety_violations', [])

    def _extract_ada_facts(self, case_data: Dict[str, Any]) -> List[str]:
        facts = []
        if case_data.get('disability_type'):
            facts.append(f"Disability: {case_data['disability_type']}")
        if case_data.get('denied_accommodations'):
            facts.append(f"Denied accommodations: {case_data['denied_accommodations']}")
        return facts

    def _extract_eeoc_facts(self, case_data: Dict[str, Any]) -> List[str]:
        return case_data.get('discrimination_facts', [])

    def _extract_all_facts(self, case_data: Dict[str, Any]) -> List[str]:
        facts = []
        facts.extend(self._extract_safety_facts(case_data))
        facts.extend(self._extract_ada_facts(case_data))
        facts.extend(self._extract_eeoc_facts(case_data))
        return facts

    def _extract_legal_theories(self, case_data: Dict[str, Any]) -> List[str]:
        theories = []
        for claim in case_data.get('claim_types', []):
            theories.append(claim.replace('_', ' ').title())
        return theories

    def _list_safety_evidence(self, case_data: Dict[str, Any]) -> List[str]:
        return case_data.get('safety_evidence', ['Violation photos', 'Inspection reports'])

    def _list_ada_evidence(self, case_data: Dict[str, Any]) -> List[str]:
        return case_data.get('ada_evidence', ['Medical documentation', 'Accommodation requests'])

    def _list_employment_evidence(self, case_data: Dict[str, Any]) -> List[str]:
        return case_data.get('employment_evidence', ['Email communications', 'Personnel file'])

    def _list_all_evidence(self, case_data: Dict[str, Any]) -> List[str]:
        evidence = []
        evidence.extend(self._list_safety_evidence(case_data))
        evidence.extend(self._list_ada_evidence(case_data))
        evidence.extend(self._list_employment_evidence(case_data))
        return list(set(evidence))  # Remove duplicates

    def export_complaint(self, complaint: ComplaintPackage, output_path: str):
        """Export complaint to file"""
        with open(output_path, 'w') as f:
            f.write(f"{complaint.title}\n")
            f.write("=" * len(complaint.title) + "\n\n")
            f.write(complaint.body)
            f.write(f"\n\nGenerated: {complaint.metadata.get('generation_date', '')}\n")

    def export_all_complaints(self, complaints: List[ComplaintPackage],
                             output_dir: str):
        """Export all complaints to directory"""
        from pathlib import Path
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for complaint in complaints:
            filename = f"{complaint.complaint_type}_complaint.txt"
            self.export_complaint(
                complaint,
                f"{output_dir}/{filename}"
            )

        # Export summary JSON
        summary = {
            'total_complaints': len(complaints),
            'complaint_types': [c.complaint_type for c in complaints],
            'complaints': [c.to_dict() for c in complaints]
        }

        with open(f"{output_dir}/complaints_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
