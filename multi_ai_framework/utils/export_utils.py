"""
Export Utilities
Export mission results and create reports
"""

from typing import Dict, Any
from pathlib import Path
import json
from datetime import datetime


def export_mission_results(mission_results: Dict[str, Any], output_dir: str) -> bool:
    """
    Export complete mission results to directory

    Args:
        mission_results: Complete mission results
        output_dir: Output directory path

    Returns:
        Success status
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Export complete results as JSON
        with open(output_path / 'mission_results.json', 'w') as f:
            json.dump(mission_results, f, indent=2)

        # Export individual phases
        if 'research_phase' in mission_results:
            with open(output_path / 'research_phase.json', 'w') as f:
                json.dump(mission_results['research_phase'], f, indent=2)

        if 'analysis_phase' in mission_results:
            with open(output_path / 'analysis_phase.json', 'w') as f:
                json.dump(mission_results['analysis_phase'], f, indent=2)

        if 'execution_phase' in mission_results:
            with open(output_path / 'execution_phase.json', 'w') as f:
                json.dump(mission_results['execution_phase'], f, indent=2)

        return True

    except Exception as e:
        print(f"Error exporting mission results: {e}")
        return False


def create_report(mission_results: Dict[str, Any], output_path: str) -> bool:
    """
    Create human-readable mission report

    Args:
        mission_results: Complete mission results
        output_path: Output file path

    Returns:
        Success status
    """
    try:
        with open(output_path, 'w') as f:
            f.write("MULTI-AI JUSTICE LEAGUE MISSION REPORT\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            # Mission Summary
            summary = mission_results.get('mission_summary', {})
            f.write("MISSION SUMMARY\n")
            f.write("-" * 70 + "\n")
            f.write(f"Total Tasks: {summary.get('total_tasks', 0)}\n")
            f.write(f"Successful Tasks: {summary.get('successful_tasks', 0)}\n")
            f.write(f"Phases Completed: {summary.get('phases_completed', 0)}\n\n")

            # Research Phase
            if 'research_phase' in mission_results:
                f.write("INTELLIGENCE GATHERING PHASE\n")
                f.write("-" * 70 + "\n")
                research = mission_results['research_phase']
                research_summary = research.get('summary', {})
                f.write(f"Sources Consulted: {research_summary.get('models_used', [])}\n")
                f.write(f"Tasks Completed: {research_summary.get('total_tasks', 0)}\n")
                f.write(f"Successful: {research_summary.get('successful', 0)}\n\n")

            # Analysis Phase
            if 'analysis_phase' in mission_results:
                f.write("STRATEGIC ANALYSIS PHASE\n")
                f.write("-" * 70 + "\n")
                analysis = mission_results['analysis_phase']
                analysis_summary = analysis.get('summary', {})
                f.write(f"Analysis Tasks: {analysis_summary.get('total_tasks', 0)}\n")
                f.write(f"Successful: {analysis_summary.get('successful', 0)}\n\n")

            # Execution Phase
            if 'execution_phase' in mission_results:
                f.write("EXECUTION PLANNING PHASE\n")
                f.write("-" * 70 + "\n")
                execution = mission_results['execution_phase']
                execution_summary = execution.get('summary', {})
                f.write(f"Execution Tasks: {execution_summary.get('total_tasks', 0)}\n")
                f.write(f"Successful: {execution_summary.get('successful', 0)}\n\n")

            f.write("=" * 70 + "\n")
            f.write("END OF REPORT\n")

        return True

    except Exception as e:
        print(f"Error creating report: {e}")
        return False
