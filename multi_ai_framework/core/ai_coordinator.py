"""
AI Justice League Coordinator
Main orchestration class for multi-AI coordination
"""

from typing import Dict, Any, List, Optional
from .base_ai import BaseAI, AICapability
from .ai_implementations import ClaudeAI, GeminiAI, DeepSeekAI, ChatGPTAI
from .task_distributor import TaskDistributor, TaskResult


class AIJusticeLeague:
    """
    Multi-AI Coordination Framework
    Orchestrates Claude, Gemini, DeepSeek, and ChatGPT for complex missions
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AI Justice League

        Args:
            config: Configuration dictionary with API keys and settings
        """
        self.config = config or {}

        # Initialize AI models
        self.claude = ClaudeAI(
            api_key=self.config.get('anthropic_api_key'),
            config=self.config.get('claude_config', {})
        )

        self.gemini = GeminiAI(
            api_key=self.config.get('google_api_key'),
            config=self.config.get('gemini_config', {})
        )

        self.deepseek = DeepSeekAI(
            api_key=self.config.get('deepseek_api_key'),
            config=self.config.get('deepseek_config', {})
        )

        self.chatgpt = ChatGPTAI(
            api_key=self.config.get('openai_api_key'),
            config=self.config.get('chatgpt_config', {})
        )

        # Create model registry
        self.models: Dict[str, BaseAI] = {
            'claude': self.claude,
            'gemini': self.gemini,
            'deepseek': self.deepseek,
            'chatgpt': self.chatgpt
        }

        # Initialize task distributor
        self.distributor = TaskDistributor(
            max_workers=self.config.get('max_workers', 4)
        )

    def coordinate_mission(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Coordinate a complete mission across all AI models

        Args:
            case_data: Mission/case data to process

        Returns:
            Synthesized results from all AI models
        """
        # Phase 1: Intelligence Gathering
        print("🔍 Phase 1: Intelligence Gathering...")
        research_results = self.distribute_research(case_data)

        # Phase 2: Strategic Analysis
        print("🧠 Phase 2: Strategic Analysis...")
        analysis_results = self.distribute_analysis(case_data, research_results)

        # Phase 3: Execution Planning
        print("⚡ Phase 3: Execution Planning...")
        execution_results = self.distribute_execution(case_data, analysis_results)

        # Synthesize all results
        return self.synthesize_mission_results(
            research_results,
            analysis_results,
            execution_results
        )

    def distribute_research(self, case_data: Dict[str, Any]) -> Dict[str, TaskResult]:
        """
        Phase 1: Distribute research tasks across AI models

        - Gemini: Real-time data gathering
        - DeepSeek: Legal precedent analysis
        - ChatGPT: Regulatory procedures
        - Claude: Narrative framework
        """
        tasks = {
            'gemini': {
                'prompt': f"""
                Conduct real-time research on the following case:
                {case_data.get('summary', '')}

                Focus on:
                - Building violations and safety records
                - Recent regulatory actions
                - Public records and databases
                - Current status of any violations

                Provide detailed findings with sources.
                """,
                'model': 'gemini-2.0-flash-exp'
            },
            'deepseek': {
                'prompt': f"""
                Analyze legal precedents related to:
                {case_data.get('legal_issues', '')}

                Focus on:
                - Similar cases and outcomes
                - Settlement ranges and patterns
                - Key legal arguments that succeeded
                - Jurisdiction-specific considerations

                Provide strategic legal analysis.
                """,
                'model': 'deepseek-chat'
            },
            'chatgpt': {
                'prompt': f"""
                Map regulatory procedures for:
                {case_data.get('regulatory_context', '')}

                Focus on:
                - Filing requirements and deadlines
                - Proper documentation formats
                - Regulatory agency contacts
                - Procedural best practices

                Provide actionable procedural guidance.
                """,
                'model': 'gpt-4'
            },
            'claude': {
                'prompt': f"""
                Develop narrative framework for:
                {case_data.get('human_story', '')}

                Focus on:
                - Human impact and story arc
                - Key emotional and factual elements
                - Strategic messaging themes
                - Narrative consistency across channels

                Provide compelling narrative structure.
                """,
                'model': 'claude-sonnet-4-5-20250929'
            }
        }

        return self.distributor.distribute_tasks(tasks, self.models)

    def distribute_analysis(self, case_data: Dict[str, Any],
                          research_results: Dict[str, TaskResult]) -> Dict[str, TaskResult]:
        """
        Phase 2: Distribute strategic analysis tasks

        - DeepSeek: Risk assessment and modeling
        - Claude: Leverage calculation
        - ChatGPT: Communication strategy
        - Gemini: Market analysis
        """
        # Extract research insights for context
        research_context = self._extract_research_context(research_results)

        tasks = {
            'deepseek': {
                'prompt': f"""
                Model opponent exposure and risk based on:

                Case Data: {case_data.get('summary', '')}
                Research Findings: {research_context}

                Analyze:
                - Opponent's legal vulnerabilities
                - Potential liability ranges
                - Risk factors for opponent
                - Defensive strategies they might employ

                Provide quantitative risk assessment.
                """,
                'model': 'deepseek-chat'
            },
            'claude': {
                'prompt': f"""
                Calculate leverage points based on:

                Case Data: {case_data.get('summary', '')}
                Research Findings: {research_context}

                Identify:
                - Maximum leverage points
                - Settlement optimization strategies
                - Negotiation pressure points
                - Strategic timing considerations

                Provide tactical leverage analysis.
                """,
                'model': 'claude-sonnet-4-5-20250929'
            },
            'chatgpt': {
                'prompt': f"""
                Optimize communication strategy for:

                Case Data: {case_data.get('summary', '')}
                Research Findings: {research_context}

                Develop:
                - Key messaging for different audiences
                - Media strategy recommendations
                - Stakeholder communication plan
                - Crisis communication protocols

                Provide comprehensive communication framework.
                """,
                'model': 'gpt-4'
            },
            'gemini': {
                'prompt': f"""
                Research current settlement trends for:

                Case Type: {case_data.get('case_type', '')}
                Jurisdiction: {case_data.get('jurisdiction', '')}

                Analyze:
                - Recent settlement amounts
                - Industry benchmarks
                - Trending legal strategies
                - Market conditions affecting settlements

                Provide current market intelligence.
                """,
                'model': 'gemini-2.0-flash-exp'
            }
        }

        return self.distributor.distribute_tasks(tasks, self.models)

    def distribute_execution(self, case_data: Dict[str, Any],
                           analysis_results: Dict[str, TaskResult]) -> Dict[str, TaskResult]:
        """
        Phase 3: Distribute execution planning tasks

        - Claude: Complaint drafting
        - ChatGPT: Media package preparation
        - DeepSeek: Settlement framework
        - Gemini: Timeline coordination
        """
        analysis_context = self._extract_analysis_context(analysis_results)

        tasks = {
            'claude': {
                'prompt': f"""
                Draft comprehensive complaint based on:

                Case Data: {case_data.get('summary', '')}
                Strategic Analysis: {analysis_context}

                Include:
                - Statement of facts
                - Legal claims and theories
                - Requested relief
                - Supporting documentation requirements

                Provide complete complaint framework.
                """,
                'model': 'claude-sonnet-4-5-20250929',
                'max_tokens': 8000
            },
            'chatgpt': {
                'prompt': f"""
                Prepare media strategy package for:

                Case Data: {case_data.get('summary', '')}
                Strategic Analysis: {analysis_context}

                Create:
                - Press release draft
                - Media talking points
                - FAQ for press inquiries
                - Social media strategy

                Provide complete media coordination package.
                """,
                'model': 'gpt-4'
            },
            'deepseek': {
                'prompt': f"""
                Develop settlement framework based on:

                Case Data: {case_data.get('summary', '')}
                Strategic Analysis: {analysis_context}

                Structure:
                - Settlement range and justification
                - Non-monetary terms to request
                - Negotiation strategy and phases
                - Deal-breaker identification

                Provide comprehensive settlement strategy.
                """,
                'model': 'deepseek-chat'
            },
            'gemini': {
                'prompt': f"""
                Create coordinated timeline for:

                Case Data: {case_data.get('summary', '')}
                Strategic Analysis: {analysis_context}

                Map:
                - Filing deadlines and milestones
                - Media coordination timing
                - Negotiation windows
                - Escalation triggers and timing

                Provide detailed coordination timeline.
                """,
                'model': 'gemini-2.0-flash-exp'
            }
        }

        return self.distributor.distribute_tasks(tasks, self.models)

    def _extract_research_context(self, results: Dict[str, TaskResult]) -> str:
        """Extract key insights from research phase"""
        context_parts = []
        for model_name, result in results.items():
            if result.success:
                context_parts.append(f"{model_name.upper()}: {result.response.content[:500]}...")
        return "\n\n".join(context_parts)

    def _extract_analysis_context(self, results: Dict[str, TaskResult]) -> str:
        """Extract key insights from analysis phase"""
        context_parts = []
        for model_name, result in results.items():
            if result.success:
                context_parts.append(f"{model_name.upper()}: {result.response.content[:500]}...")
        return "\n\n".join(context_parts)

    def synthesize_mission_results(self, research: Dict[str, TaskResult],
                                  analysis: Dict[str, TaskResult],
                                  execution: Dict[str, TaskResult]) -> Dict[str, Any]:
        """Synthesize all mission phase results"""
        return {
            'research_phase': self.distributor.synthesize_results(research),
            'analysis_phase': self.distributor.synthesize_results(analysis),
            'execution_phase': self.distributor.synthesize_results(execution),
            'mission_summary': {
                'total_tasks': len(research) + len(analysis) + len(execution),
                'successful_tasks': (
                    len(self.distributor.get_successful_results(research)) +
                    len(self.distributor.get_successful_results(analysis)) +
                    len(self.distributor.get_successful_results(execution))
                ),
                'phases_completed': 3
            }
        }

    def get_model_by_capability(self, capability: AICapability) -> List[BaseAI]:
        """Find AI models that have specific capability"""
        return [ai for ai in self.models.values() if ai.has_capability(capability)]

    def get_all_capabilities(self) -> Dict[str, List[AICapability]]:
        """Get capabilities map for all models"""
        return {
            name: ai.get_capabilities()
            for name, ai in self.models.items()
        }
