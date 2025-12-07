"""
Data Synchronization
Synchronizes data across different components of the framework
"""

from typing import Dict, Any, List
import json
from datetime import datetime
from pathlib import Path


class DataSynchronizer:
    """Synchronizes data across framework components"""

    def __init__(self, sync_dir: str = "./data/sync"):
        self.sync_dir = Path(sync_dir)
        self.sync_dir.mkdir(parents=True, exist_ok=True)

    def sync_mission_data(self, case_id: str, data: Dict[str, Any]) -> bool:
        """
        Synchronize mission data to shared location

        Args:
            case_id: Case identifier
            data: Mission data to synchronize

        Returns:
            Success status
        """
        try:
            sync_file = self.sync_dir / f"{case_id}_sync.json"

            # Load existing data if present
            existing_data = {}
            if sync_file.exists():
                with open(sync_file, 'r') as f:
                    existing_data = json.load(f)

            # Merge new data
            existing_data.update(data)
            existing_data['last_sync'] = datetime.now().isoformat()

            # Save merged data
            with open(sync_file, 'w') as f:
                json.dump(existing_data, f, indent=2)

            return True

        except Exception as e:
            print(f"Error syncing data: {e}")
            return False

    def get_mission_data(self, case_id: str) -> Dict[str, Any]:
        """Get synchronized mission data"""
        sync_file = self.sync_dir / f"{case_id}_sync.json"

        if sync_file.exists():
            with open(sync_file, 'r') as f:
                return json.load(f)

        return {}

    def sync_evidence(self, case_id: str, evidence: List[Dict[str, Any]]) -> bool:
        """Synchronize evidence data"""
        return self.sync_mission_data(case_id, {'evidence': evidence})

    def sync_violations(self, case_id: str, violations: List[Dict[str, Any]]) -> bool:
        """Synchronize violation data"""
        return self.sync_mission_data(case_id, {'violations': violations})

    def sync_analysis(self, case_id: str, analysis: Dict[str, Any]) -> bool:
        """Synchronize analysis results"""
        return self.sync_mission_data(case_id, {'analysis': analysis})

    def sync_execution(self, case_id: str, execution: Dict[str, Any]) -> bool:
        """Synchronize execution results"""
        return self.sync_mission_data(case_id, {'execution': execution})

    def get_sync_status(self, case_id: str) -> Dict[str, Any]:
        """Get synchronization status"""
        data = self.get_mission_data(case_id)

        return {
            'case_id': case_id,
            'last_sync': data.get('last_sync', 'Never'),
            'components_synced': list(data.keys()),
            'has_evidence': 'evidence' in data,
            'has_violations': 'violations' in data,
            'has_analysis': 'analysis' in data,
            'has_execution': 'execution' in data
        }
