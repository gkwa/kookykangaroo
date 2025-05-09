"""Logger module for KookyKangaroo."""

import rich.console


class Logger:
    """Simple logger that outputs to stderr."""

    LEVELS = {"ERROR": 0, "WARNING": 1, "INFO": 2, "DEBUG": 3, "TRACE": 4}

    def __init__(self) -> None:
        """Initialize the logger."""
        self.console = rich.console.Console(stderr=True)
        self.level = "ERROR"  # Default level

    def set_level(self, level: str) -> None:
        """Set the logging level."""
        if level in self.LEVELS:
            self.level = level

    def _should_log(self, level: str) -> bool:
        """Check if the message should be logged based on level."""
        return self.LEVELS.get(level, 0) <= self.LEVELS.get(self.level, 0)

    def error(self, message: str) -> None:
        """Log an error message."""
        if self._should_log("ERROR"):
            self.console.print(f"ERROR: {message}", style="bold red")

    def warning(self, message: str) -> None:
        """Log a warning message."""
        if self._should_log("WARNING"):
            self.console.print(f"WARNING: {message}", style="yellow")

    def info(self, message: str) -> None:
        """Log an info message."""
        if self._should_log("INFO"):
            self.console.print(f"INFO: {message}", style="blue")

    def debug(self, message: str) -> None:
        """Log a debug message."""
        if self._should_log("DEBUG"):
            self.console.print(f"DEBUG: {message}", style="dim")

    def trace(self, message: str) -> None:
        """Log a trace message."""
        if self._should_log("TRACE"):
            self.console.print(f"TRACE: {message}", style="dim cyan")


_logger_instance = None


def get_logger() -> Logger:
    """Get the logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger()
    return _logger_instance
