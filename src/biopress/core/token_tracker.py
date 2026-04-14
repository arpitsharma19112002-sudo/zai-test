"""Token tracking for cost optimization."""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import time


class OperationType(Enum):
    """Types of operations that can use tokens."""
    TEMPLATE_LOOKUP = "template"  # 0 tokens - predefined templates
    SYMPY_COMPUTE = "sympy"      # 0 tokens - SymPy math
    LLM_VALIDATION = "llm"       # Uses tokens - L2 validation
    LLM_TRANSLATION = "translate" # Uses tokens - translation
    LLM_NEW_CONTENT = "new"       # Uses tokens - new content generation
    LLM_MIMIC = "mimic"          # Uses tokens - pattern mimic


LLM_COST_PER_1K = {"input": 0.001, "output": 0.002}


@dataclass
class TokenUsage:
    """Token usage for a single operation."""
    operation: OperationType
    input_tokens: int = 0
    output_tokens: int = 0
    duration_ms: float = 0.0


@dataclass
class TokenReport:
    """Token usage report for a generation session."""
    operations: list[TokenUsage] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    questions_generated: int = 0
    
    @property
    def total_input_tokens(self) -> int:
        return sum(op.input_tokens for op in self.operations)
    
    @property
    def total_output_tokens(self) -> int:
        return sum(op.output_tokens for op in self.operations)
    
    @property
    def total_tokens(self) -> int:
        return self.total_input_tokens + self.total_output_tokens
    
    @property
    def zero_token_operations(self) -> int:
        return sum(
            1 for op in self.operations 
            if op.operation in (OperationType.TEMPLATE_LOOKUP, OperationType.SYMPY_COMPUTE)
        )
    
    @property
    def llm_operations(self) -> int:
        return sum(
            1 for op in self.operations 
            if op.operation in (
                OperationType.LLM_VALIDATION,
                OperationType.LLM_TRANSLATION,
                OperationType.LLM_NEW_CONTENT,
                OperationType.LLM_MIMIC,
            )
        )
    
    @property
    def zero_token_percentage(self) -> float:
        total_ops = len(self.operations)
        if total_ops == 0:
            return 100.0
        return (self.zero_token_operations / total_ops) * 100
    
    @property
    def estimated_cost(self) -> float:
        """Estimated cost in USD."""
        input_cost = (self.total_input_tokens / 1000) * LLM_COST_PER_1K["input"]
        output_cost = (self.total_output_tokens / 1000) * LLM_COST_PER_1K["output"]
        return input_cost + output_cost
    
    def add_operation(self, op: TokenUsage) -> None:
        self.operations.append(op)
    
    def finalize(self, questions_generated: int = 0) -> None:
        self.end_time = time.time()
        self.questions_generated = questions_generated
    
    def format_report(self) -> str:
        """Format the report as a string."""
        
        lines = [
            "=" * 50,
            "TOKEN USAGE REPORT",
            "=" * 50,
            f"Questions Generated: {self.questions_generated}",
            f"Total Operations: {len(self.operations)}",
            f"Zero-Token Operations: {self.zero_token_operations}",
            f"LLM Operations: {self.llm_operations}",
            f"Zero-Token Percentage: {self.zero_token_percentage:.1f}%",
            "",
            f"Input Tokens: {self.total_input_tokens:,}",
            f"Output Tokens: {self.total_output_tokens:,}",
            f"Total Tokens: {self.total_tokens:,}",
            f"Estimated Cost: ${self.estimated_cost:.4f}",
            "",
            "Breakdown:",
        ]
        
        for op in self.operations:
            op_type = op.operation.value
            lines.append(f"  - {op_type}: {op.input_tokens + op.output_tokens} tokens")
        
        lines.append("=" * 50)
        return "\n".join(lines)


import threading

class TokenTracker:
    """Track token usage across generation operations with thread safety."""
    
    _instance: Optional['TokenTracker'] = None
    _lock = threading.Lock()
    
    def __init__(self) -> None:
        self._current_report: Optional[TokenReport] = None
        self._op_lock = threading.Lock()
    
    @classmethod
    def get_instance(cls) -> 'TokenTracker':
        """Get the global token tracker instance with thread safety."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = TokenTracker()
        return cls._instance
    
    def start_tracking(self) -> TokenReport:
        """Start a new tracking session."""
        with self._op_lock:
            self._current_report = TokenReport()
            return self._current_report
    
    def get_current_report(self) -> Optional[TokenReport]:
        """Get the current report."""
        return self._current_report
    
    def record_operation(
        self,
        operation: OperationType,
        input_tokens: int = 0,
        output_tokens: int = 0,
        duration_ms: float = 0.0,
    ) -> None:
        """Record an operation's token usage."""
        with self._op_lock:
            if self._current_report is None:
                self._current_report = TokenReport()
            
            usage = TokenUsage(
                operation=operation,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                duration_ms=duration_ms,
            )
            self._current_report.add_operation(usage)
    
    def record_template_lookup(self, count: int = 1) -> None:
        """Record template lookup (0 tokens)."""
        for _ in range(count):
            self.record_operation(OperationType.TEMPLATE_LOOKUP, 0, 0)
    
    def record_sympy_compute(self, count: int = 1) -> None:
        """Record SymPy computation (0 tokens)."""
        for _ in range(count):
            self.record_operation(OperationType.SYMPY_COMPUTE, 0, 0)
    
    def record_llm_validation(
        self,
        input_tokens: int,
        output_tokens: int,
        duration_ms: float = 0.0,
    ) -> None:
        """Record LLM validation call."""
        self.record_operation(
            OperationType.LLM_VALIDATION,
            input_tokens,
            output_tokens,
            duration_ms,
        )
    
    def record_llm_translation(
        self,
        input_tokens: int,
        output_tokens: int,
        duration_ms: float = 0.0,
    ) -> None:
        """Record LLM translation call."""
        self.record_operation(
            OperationType.LLM_TRANSLATION,
            input_tokens,
            output_tokens,
            duration_ms,
        )
    
    def finalize(
        self,
        questions_generated: int = 0,
    ) -> TokenReport:
        """Finalize the current tracking session."""
        with self._op_lock:
            if self._current_report:
                self._current_report.finalize(questions_generated)
                report = self._current_report
                self._current_report = None
                return report
            return TokenReport()
    
    def reset(self) -> None:
        """Reset the tracker."""
        with self._op_lock:
            self._current_report = None


def get_token_tracker() -> TokenTracker:
    """Helper to get the global token tracker instance."""
    return TokenTracker.get_instance()