"""
Constants and configuration values for OmniSolve.
All hardcoded values should be defined here for easy management.
"""
import os

# --- API CONFIGURATION ---
API_URL = os.getenv("OMNISOLVE_API_URL", "http://localhost:5001/api/v1/generate")
API_TIMEOUT = int(os.getenv("OMNISOLVE_API_TIMEOUT", "120"))  # seconds

# --- GENERATION PARAMETERS ---
DEFAULT_MAX_CONTEXT_LENGTH = 8192
DEFAULT_MAX_LENGTH = 2048
DEFAULT_TEMPERATURE = 0.3
RETRY_TEMPERATURE_INCREMENT = 0.1  # Increase temp on retry

# --- RETRY LOGIC ---
MAX_RETRIES = 3
RETRY_DELAY = 1.0  # seconds between retries

# --- PATHS ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECTS_DIR = os.path.join(ROOT_DIR, "Projects")
CONFIG_DIR = os.path.join(ROOT_DIR, "Config")
LOGS_DIR = os.path.join(ROOT_DIR, "Logs")
GENERATED_SOFTWARE_DIR = os.path.join(ROOT_DIR, "Generated_Software")

# --- STOP TOKENS ---
STOP_TOKENS = [
    "SYSTEM ROLE:",
    "[CURRENT TASK]",
    "[END]",
    "USER:",
    "ASSISTANT:"
]

# --- PSI CONFIGURATION ---
PSI_CACHE_TIMEOUT = 300  # Cache PSI for 5 minutes
PSI_MAX_FILES = 100  # Summarize if project has more files

# --- LOGGING ---
LOG_LEVEL = os.getenv("OMNISOLVE_LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
ENABLE_AUDIT_LOG = True

# --- PERSONA FILES ---
PERSONA_MAPPING = {
    "Architect": "Architect.json",
    "Planner": "Planner.json",
    "Developer": "Developer.json",  # Note: actually loads Steve.json
    "QA": "QA.json"
}
