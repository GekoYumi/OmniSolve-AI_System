"""
Structured logging with JSON and text output support.
Provides consistent logging across the OmniSolve system.
"""
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler

from ..config.constants import LOGS_DIR, LOG_LEVEL, LOG_FORMAT, ENABLE_AUDIT_LOG


class JSONFormatter(logging.Formatter):
    """Custom formatter that outputs logs as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as JSON.

        Args:
            record: The log record to format

        Returns:
            JSON string representation of the log
        """
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)

        # Add extra fields if present
        extra_fields = {k: v for k, v in record.__dict__.items()
                        if k not in ('name', 'msg', 'args', 'created', 'filename',
                                     'funcName', 'levelname', 'levelno', 'lineno',
                                     'module', 'msecs', 'message', 'pathname', 'process',
                                     'processName', 'relativeCreated', 'thread', 'threadName',
                                     'exc_info', 'exc_text', 'stack_info')}
        if extra_fields:
            log_data.update(extra_fields)

        return json.dumps(log_data)


class OmniSolveLogger:
    """Central logging manager for OmniSolve."""

    _instance: Optional['OmniSolveLogger'] = None
    _loggers: Dict[str, logging.Logger] = {}

    def __new__(cls):
        """Singleton pattern for logger manager."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the logger manager."""
        if self._initialized:
            return

        self._logs_dir = Path(LOGS_DIR)
        self._logs_dir.mkdir(exist_ok=True, parents=True)

        # Set up audit logger if enabled
        if ENABLE_AUDIT_LOG:
            self._setup_audit_logger()

        self._initialized = True

    def _setup_audit_logger(self) -> None:
        """Set up the audit logger with JSON formatting."""
        audit_logger = logging.getLogger('omnisolve.audit')
        audit_logger.setLevel(logging.INFO)
        audit_logger.propagate = False

        # Create audit log file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        audit_file = self._logs_dir / f'audit_{timestamp}.jsonl'

        # Rotating file handler for audit logs
        handler = RotatingFileHandler(
            audit_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        handler.setFormatter(JSONFormatter())
        audit_logger.addHandler(handler)

        self._loggers['audit'] = audit_logger

    def get_logger(self, name: str, log_to_file: bool = True) -> logging.Logger:
        """
        Get or create a logger with the specified name.

        Args:
            name: The logger name (typically module name)
            log_to_file: Whether to log to file in addition to console

        Returns:
            Configured logger instance
        """
        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(f'omnisolve.{name}')
        logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
        logger.propagate = False

        # Console handler with standard format
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

        # File handler with detailed format
        if log_to_file:
            timestamp = datetime.now().strftime('%Y%m%d')
            log_file = self._logs_dir / f'{name}_{timestamp}.log'

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=3
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
            logger.addHandler(file_handler)

        self._loggers[name] = logger
        return logger

    def audit_log(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Write an audit log entry.

        Args:
            event_type: Type of event (e.g., 'project_start', 'file_generated')
            data: Additional data to log
        """
        if 'audit' not in self._loggers:
            return

        audit_data = {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            **data
        }

        self._loggers['audit'].info(
            json.dumps(audit_data),
            extra={'event_type': event_type}
        )


# Global logger instance
logger_manager = OmniSolveLogger()


def get_logger(name: str) -> logging.Logger:
    """
    Convenience function to get a logger.

    Args:
        name: Logger name

    Returns:
        Configured logger
    """
    return logger_manager.get_logger(name)


def audit_log(event_type: str, **kwargs) -> None:
    """
    Convenience function for audit logging.

    Args:
        event_type: Type of event
        **kwargs: Additional data to log
    """
    logger_manager.audit_log(event_type, kwargs)
