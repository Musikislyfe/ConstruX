"""
Task Distribution and Parallel Execution System
Coordinates parallel AI task execution with result aggregation
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid
from .base_ai import BaseAI, AIResponse, AICapability


@dataclass
class TaskResult:
    """Result from task execution"""
    task_id: str
    ai_model: str
    success: bool
    response: AIResponse
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'task_id': self.task_id,
            'ai_model': self.ai_model,
            'success': self.success,
            'response': self.response.to_dict(),
            'error': self.error
        }


class TaskDistributor:
    """Distributes and coordinates tasks across multiple AI models"""

    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.task_history: List[TaskResult] = []

    def distribute_tasks(self, tasks: Dict[str, Dict[str, Any]],
                        ai_models: Dict[str, BaseAI]) -> Dict[str, TaskResult]:
        """
        Distribute tasks to AI models in parallel

        Args:
            tasks: Dictionary of {model_name: task_config}
            ai_models: Dictionary of {model_name: AI_instance}

        Returns:
            Dictionary of {model_name: TaskResult}
        """
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_model = {}
            for model_name, task in tasks.items():
                if model_name not in ai_models:
                    print(f"Warning: Model {model_name} not available, skipping task")
                    continue

                ai = ai_models[model_name]

                # Add unique task ID
                task['id'] = str(uuid.uuid4())

                # Submit task
                future = executor.submit(self._execute_single_task, ai, task)
                future_to_model[future] = model_name

            # Collect results as they complete
            for future in as_completed(future_to_model):
                model_name = future_to_model[future]
                try:
                    result = future.result()
                    results[model_name] = result
                    self.task_history.append(result)
                except Exception as e:
                    error_result = TaskResult(
                        task_id="error",
                        ai_model=model_name,
                        success=False,
                        response=ai_models[model_name]._create_response(
                            task_id="error",
                            content="",
                            metadata={},
                            success=False,
                            error=str(e)
                        ),
                        error=str(e)
                    )
                    results[model_name] = error_result
                    self.task_history.append(error_result)

        return results

    def _execute_single_task(self, ai: BaseAI, task: Dict[str, Any]) -> TaskResult:
        """Execute a single task on an AI model"""
        try:
            # Validate task
            if not ai.validate_task(task):
                raise ValueError(f"Invalid task configuration for {ai.model_name}")

            # Execute task
            response = ai.execute_task(task)

            # Create result
            return TaskResult(
                task_id=task['id'],
                ai_model=ai.model_name,
                success=response.success,
                response=response,
                error=response.error
            )

        except Exception as e:
            # Create error result
            return TaskResult(
                task_id=task.get('id', 'unknown'),
                ai_model=ai.model_name,
                success=False,
                response=ai._create_response(
                    task_id=task.get('id', 'unknown'),
                    content="",
                    metadata={},
                    success=False,
                    error=str(e)
                ),
                error=str(e)
            )

    def get_successful_results(self, results: Dict[str, TaskResult]) -> Dict[str, TaskResult]:
        """Filter only successful results"""
        return {k: v for k, v in results.items() if v.success}

    def get_failed_results(self, results: Dict[str, TaskResult]) -> Dict[str, TaskResult]:
        """Filter only failed results"""
        return {k: v for k, v in results.items() if not v.success}

    def get_task_history(self) -> List[TaskResult]:
        """Get history of all executed tasks"""
        return self.task_history

    def synthesize_results(self, results: Dict[str, TaskResult]) -> Dict[str, Any]:
        """
        Synthesize results from multiple AI models into unified output

        Returns:
            Synthesized data structure with all results organized
        """
        synthesis = {
            'summary': {
                'total_tasks': len(results),
                'successful': len(self.get_successful_results(results)),
                'failed': len(self.get_failed_results(results)),
                'models_used': list(results.keys())
            },
            'results_by_model': {},
            'combined_insights': [],
            'errors': []
        }

        for model_name, result in results.items():
            synthesis['results_by_model'][model_name] = {
                'success': result.success,
                'content': result.response.content if result.success else None,
                'metadata': result.response.metadata,
                'error': result.error
            }

            if result.success:
                synthesis['combined_insights'].append({
                    'source': model_name,
                    'content': result.response.content
                })
            else:
                synthesis['errors'].append({
                    'source': model_name,
                    'error': result.error
                })

        return synthesis
