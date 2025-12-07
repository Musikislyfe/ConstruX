"""
Mission Orchestrator
High-level orchestration of complete missions from start to finish
"""

from typing import Dict, Any
from ..core.ai_coordinator import AIJusticeLeague
from ..intelligence.research_coordinator import IntelligenceGathering
from ..analysis.strategic_analyzer import StrategicAnalysis
from ..execution.execution_coordinator import ExecutionCoordination
from ..utils.data_sync import DataSynchronizer
from ..utils.result_aggregator import ResultAggregator
from ..utils.export_utils import export_mission_results, create_report
from ..config.config_manager import ConfigManager


class MissionOrchestrator:
    """Orchestrates complete multi-AI missions from intelligence to execution"""

    def __init__(self, config: ConfigManager = None):
        """
        Initialize mission orchestrator

        Args:
            config: Configuration manager (will create default if not provided)
        """
        self.config = config or ConfigManager()

        # Initialize AI Justice League
        self.ai_league = AIJusticeLeague(
            self.config.get_framework_config()
        )

        # Initialize phase coordinators
        self.intelligence = IntelligenceGathering(self.ai_league)
        self.analysis = StrategicAnalysis(self.ai_league)
        self.execution = ExecutionCoordination(self.ai_league)

        # Initialize utilities
        self.data_sync = DataSynchronizer()
        self.aggregator = ResultAggregator()

    def execute_complete_mission(self, case_data: Dict[str, Any],
                                 export_dir: str = None) -> Dict[str, Any]:
        """
        Execute complete mission from intelligence gathering to execution planning

        Args:
            case_data: Case information and parameters
            export_dir: Optional directory to export results

        Returns:
            Complete mission results
        """
        case_id = case_data.get('case_id', 'mission_' + str(hash(str(case_data)))[:8])
        case_data['case_id'] = case_id

        print("\n" + "=" * 70)
        print("MULTI-AI JUSTICE LEAGUE - MISSION EXECUTION")
        print("=" * 70)
        print(f"\nCase ID: {case_id}")
        print(f"Mission: {case_data.get('mission_name', 'Justice Campaign')}\n")

        mission_results = {
            'case_id': case_id,
            'case_data': case_data
        }

        # Phase 1: Intelligence Gathering
        print("\n🔍 PHASE 1: INTELLIGENCE GATHERING")
        print("-" * 70)
        intelligence_report = self.intelligence.coordinate_research(case_data)
        mission_results['intelligence_report'] = intelligence_report

        # Sync intelligence data
        self.data_sync.sync_evidence(case_id, intelligence_report.get('evidence_collected', []))
        self.data_sync.sync_violations(case_id, intelligence_report.get('violations_identified', []))

        print(f"\n✓ Intelligence gathered from {len(intelligence_report.get('findings', {}))} AI models")
        print(f"✓ {len(intelligence_report.get('evidence_collected', []))} evidence items collected")
        print(f"✓ {len(intelligence_report.get('violations_identified', []))} violations identified")

        # Phase 2: Strategic Analysis
        print("\n\n🧠 PHASE 2: STRATEGIC ANALYSIS")
        print("-" * 70)
        strategic_analysis = self.analysis.coordinate_analysis(
            case_data,
            intelligence_report
        )
        mission_results['strategic_analysis'] = strategic_analysis

        # Sync analysis data
        self.data_sync.sync_analysis(case_id, strategic_analysis)

        leverage_score = strategic_analysis.get('leverage_analysis', {}).get('overall_leverage_score', 0)
        settlement_range = strategic_analysis.get('settlement_prediction', {}).get('predicted_range', {})

        print(f"\n✓ Leverage Score: {leverage_score:.1f}/100")
        print(f"✓ Settlement Range: ${settlement_range.get('low', 0):,.0f} - ${settlement_range.get('high', 0):,.0f}")
        print(f"✓ Strategic recommendations generated")

        # Phase 3: Execution Planning
        print("\n\n⚡ PHASE 3: EXECUTION PLANNING")
        print("-" * 70)
        execution_plan = self.execution.coordinate_deployment(
            case_data,
            strategic_analysis,
            intelligence_report
        )
        mission_results['execution_plan'] = execution_plan

        # Sync execution data
        self.data_sync.sync_execution(case_id, execution_plan)

        print(f"\n✓ {len(execution_plan.get('complaints', []))} complaints prepared")
        print(f"✓ Media strategy package created")
        print(f"✓ Negotiation framework established")
        print(f"✓ Campaign timeline generated")

        # Create executive summary
        print("\n\n📊 GENERATING EXECUTIVE SUMMARY")
        print("-" * 70)
        executive_summary = self.aggregator.create_executive_summary(mission_results)
        mission_results['executive_summary'] = executive_summary

        # Export results if directory provided
        if export_dir:
            print(f"\n\n💾 EXPORTING RESULTS TO: {export_dir}")
            print("-" * 70)

            # Export complete mission results
            export_mission_results(mission_results, export_dir)

            # Export execution packages
            self.execution.export_execution_package(
                execution_plan,
                f"{export_dir}/execution"
            )

            # Create human-readable report
            create_report(mission_results, f"{export_dir}/MISSION_REPORT.txt")

            print(f"✓ Results exported to {export_dir}")
            print(f"✓ Execution packages ready for deployment")
            print(f"✓ Mission report generated")

        # Final summary
        print("\n\n" + "=" * 70)
        print("MISSION EXECUTION COMPLETE")
        print("=" * 70)
        print(f"\n✓ Case ID: {case_id}")
        print(f"✓ All 3 phases completed successfully")
        print(f"✓ Leverage Score: {leverage_score:.1f}/100")
        print(f"✓ Settlement Target: ${settlement_range.get('mid', 0):,.0f}")
        print(f"✓ Ready for deployment")
        print("\n" + "=" * 70 + "\n")

        return mission_results

    def execute_intelligence_only(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute only intelligence gathering phase"""
        print("\n🔍 Executing Intelligence Gathering Phase...")
        return self.intelligence.coordinate_research(case_data)

    def execute_analysis_only(self, case_data: Dict[str, Any],
                             intelligence_report: Dict[str, Any]) -> Dict[str, Any]:
        """Execute only strategic analysis phase"""
        print("\n🧠 Executing Strategic Analysis Phase...")
        return self.analysis.coordinate_analysis(case_data, intelligence_report)

    def execute_execution_only(self, case_data: Dict[str, Any],
                              strategic_analysis: Dict[str, Any],
                              intelligence_report: Dict[str, Any]) -> Dict[str, Any]:
        """Execute only execution planning phase"""
        print("\n⚡ Executing Execution Planning Phase...")
        return self.execution.coordinate_deployment(
            case_data,
            strategic_analysis,
            intelligence_report
        )

    def get_mission_status(self, case_id: str) -> Dict[str, Any]:
        """Get status of a mission"""
        return self.data_sync.get_sync_status(case_id)

    def get_ai_capabilities(self) -> Dict[str, Any]:
        """Get capabilities of all AI models"""
        return self.ai_league.get_all_capabilities()
