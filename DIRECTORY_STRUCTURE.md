# OmniSolve 3.0 - Complete Directory Structure

## Root Structure

```
e:\
├── AI_System/                          # Main system directory
│   ├── Core/                           # ⭐ Refactored core modules
│   ├── Config/                         # Persona configurations
│   ├── Engine/                         # AI inference engine
│   ├── Logs/                           # System logs
│   ├── Models/                         # LLM model files
│   ├── Projects/                       # Generated projects output
│   ├── Runtime/                        # Python & Node.js runtime
│   ├── Saved_Agents/                   # Agent presets
│   ├── Saves/                          # Saved states
│   ├── Memory/                         # Vector store (future)
│   ├── Generated_Software/             # Legacy output folder
│   ├── SillyTavern/                    # SillyTavern integration
│   ├── requirements.txt                # ⭐ Python dependencies
│   ├── README_v3.0.md                  # ⭐ Complete documentation
│   ├── FILE_LIST_v3.0.md               # ⭐ File reference guide
│   ├── INSTALLATION_GUIDE.md           # ⭐ Setup instructions
│   └── REFACTORING_SUMMARY.md          # ⭐ Before/after comparison
├── docs/                               # System documentation
├── SillyTavern/                        # SillyTavern character data
├── Generated_Software/                 # Additional output
└── LAUNCH_OMNISOLVE.bat                # ⭐ Main launcher (updated)
```

⭐ = New or significantly modified in v3.0

---

## Core/ Directory (Detailed)

```
AI_System/Core/
│
├── __init__.py                         # ⭐ Package initialization
├── orchestrator.py                     # ⭐ Main orchestrator (entry point)
├── OmniSolve_Orchestrator.py.old       # 📦 Backup of original version
│
├── agents/                             # ⭐ Agent implementations
│   ├── __init__.py
│   ├── base_agent.py                   # Base class + parallel executor
│   ├── architect.py                    # File structure designer
│   ├── planner.py                      # Logic blueprint creator
│   ├── developer.py                    # Code generator (Steve)
│   └── qa.py                           # Code reviewer
│
├── config/                             # ⭐ Configuration management
│   ├── __init__.py
│   ├── constants.py                    # All constants & settings
│   └── config_loader.py                # Cached persona loader
│
├── exceptions/                         # ⭐ Custom exceptions
│   ├── __init__.py
│   └── errors.py                       # Exception hierarchy
│
├── logging/                            # ⭐ Structured logging
│   ├── __init__.py
│   └── logger.py                       # JSON audit + file logs
│
├── output/                             # ⭐ File management
│   ├── __init__.py
│   └── file_manager.py                 # Async writes + validation
│
├── utils/                              # ⭐ Utility functions
│   ├── __init__.py
│   ├── text_parsers.py                 # Optimized parsing
│   └── psi_generator.py                # Cached PSI generation
│
└── logging_module/                     # 🗑️ Legacy (can be deleted)
    └── __pycache__/
```

⭐ = New in v3.0  
📦 = Backup file  
🗑️ = Can be safely deleted  

---

## Config/ Directory

```
AI_System/Config/
├── Architect.json                      # Architect agent persona
├── Developer.json                      # Actually loads Steve.json
├── Planner.json                        # Planner agent persona
└── QA.json                             # QA agent persona
```

**Note**: Developer.json is internally mapped to load Steve.json (special case).

---

## Models/ Directory

```
AI_System/Models/
├── Llama-3-8B-Instruct-32k-v0.1.Q5_K_M.gguf
├── gemma-3-27b-it-abliterated.q4_k_m.gguf
├── deepseek-coder-7b-instruct-v1.5-Q5_K_M.gguf
└── DarkIdol-Llama-3.1-8B-Instruct-1.2-Uncensored.i1-Q4_K_S.gguf
```

Default model configured in LAUNCH_OMNISOLVE.bat: `Llama-3-8B-Instruct-32k-v0.1.Q5_K_M.gguf`

---

## Logs/ Directory (After First Run)

```
AI_System/Logs/
├── audit_20260105_123456.jsonl         # JSON audit trail (machine-readable)
├── orchestrator_20260105.log           # Main orchestrator logs
├── agents_20260105.log                 # Agent activity logs
├── file_manager_20260105.log           # File operations logs
├── psi_20260105.log                    # PSI generation logs
├── parsers_20260105.log                # Parsing activity logs
└── launcher_*.log                      # Legacy launcher logs
```

**Log Rotation**: Automatically rotates at 5MB, keeps 3-5 backups.

---

## Projects/ Directory (After Generation)

```
AI_System/Projects/
├── my_calculator/                      # Example project
│   ├── calculator.py                   # Generated code
│   └── main.py                         # Generated code
│
└── my_webapp/                          # Another project
    ├── app.py
    ├── routes.py
    └── models.py
```

Each project gets its own subdirectory.

---

## Runtime/ Directory

```
AI_System/Runtime/
├── python.exe                          # Embedded Python 3.14
├── pythonw.exe
├── python314.dll
├── python3.dll
├── vcruntime140.dll
├── vcruntime140_1.dll
├── node.exe                            # Embedded Node.js
├── npm.cmd
├── npx.cmd
├── get-pip.py                          # Pip installer
├── INSTALL_PIP.bat                     # Pip installation script
├── install_tools.bat
├── python314._pth                      # Python path config
│
├── Lib/                                # Python standard library
│   └── site-packages/                  # Installed packages
│       ├── requests/                   # ⭐ HTTP client
│       ├── aiofiles/                   # ⭐ Async file I/O
│       └── ...
│
├── Scripts/                            # Python scripts
│   ├── pip.exe
│   └── ...
│
└── node_modules/                       # Node.js packages
    └── ...
```

⭐ = Installed by requirements.txt

---

## Engine/ Directory

```
AI_System/Engine/
└── koboldcpp.exe                       # LLM inference engine
```

KoboldCPP provides the local API on port 5001.

---

## Documentation Files

```
AI_System/
├── README_v3.0.md                      # 📖 Complete system documentation (15+ pages)
├── FILE_LIST_v3.0.md                   # 📋 File reference guide (20+ pages)
├── INSTALLATION_GUIDE.md               # 🚀 Setup instructions (12+ pages)
├── REFACTORING_SUMMARY.md              # 📊 Before/after comparison (15+ pages)
└── DIRECTORY_STRUCTURE.md              # 🗂️ This file

docs/
├── 1.scope_and_goals.txt               # Original project scope
├── 2.architecture_and_continuation.txt # Architecture notes
├── 3.stateInterface_and_contextInjection.txt
├── 4.memory_and_retrieval.txt
└── 5.flow_and_lifecycle.txt
```

📖 = Main documentation  
📋 = Reference  
🚀 = Getting started  
📊 = Comparison  
🗂️ = This structure guide  

---

## File Count Summary

| Directory | Files | Purpose |
|-----------|-------|---------|
| `Core/` | 20 | ⭐ New modular architecture |
| `Core/agents/` | 5 | Agent implementations |
| `Core/config/` | 3 | Configuration management |
| `Core/exceptions/` | 2 | Error handling |
| `Core/logging/` | 2 | Logging system |
| `Core/output/` | 2 | File management |
| `Core/utils/` | 3 | Utility functions |
| `Config/` | 4 | Persona configurations |
| `Models/` | 4 | LLM model weights |
| `Engine/` | 1 | Inference engine |
| `Runtime/` | 100+ | Python & Node.js |
| `docs/` | 5 | Original documentation |
| **Documentation** | 5 | ⭐ New comprehensive guides |

**Total New Files Created**: 23 modules + 5 documentation files = **28 files**

---

## Key Files Quick Reference

### 🏃 Getting Started
1. `INSTALLATION_GUIDE.md` - Start here for setup
2. `LAUNCH_OMNISOLVE.bat` - Run this to launch
3. `README_v3.0.md` - Complete system overview
4. `.github/copilot-instructions.md` - Concise guidance for AI coding agents

### 🔧 Development
1. `Core/orchestrator.py` - Main entry point
2. `Core/agents/base_agent.py` - Agent base class
3. `Core/config/constants.py` - Settings to customize

### 📚 Reference
1. `FILE_LIST_v3.0.md` - What each file does
2. `REFACTORING_SUMMARY.md` - What changed from v2.4
3. `DIRECTORY_STRUCTURE.md` - This file (navigation)

### 🐛 Debugging
1. `Logs/orchestrator_*.log` - Main workflow logs
2. `Logs/audit_*.jsonl` - Machine-readable events
3. `Logs/agents_*.log` - Agent activity

### ⚙️ Configuration
1. `Config/*.json` - Agent personas
2. `Core/config/constants.py` - System constants
3. `requirements.txt` - Python dependencies

---

## Import Paths Reference

### Orchestrator
```python
from AI_System.Core import OmniSolveOrchestrator, main
```

### Agents
```python
from AI_System.Core.agents import (
    BaseAgent,
    ArchitectAgent,
    PlannerAgent,
    DeveloperAgent,
    QAAgent,
    ParallelAgentExecutor
)
```

### Configuration
```python
from AI_System.Core.config import (
    config_loader,
    API_URL,
    MAX_RETRIES,
    DEFAULT_TEMPERATURE
)
```

### Exceptions
```python
from AI_System.Core.exceptions import (
    OmniSolveError,
    ConfigurationError,
    BrainConnectionError,
    CodeGenerationError
)
```

### Logging
```python
from AI_System.Core.logging import get_logger, audit_log
```

### Output
```python
from AI_System.Core.output import file_manager
```

### Utilities
```python
from AI_System.Core.utils import (
    extract_json,
    extract_code,
    validate_python_syntax,
    psi_generator
)
```

---

## Navigation Tips

### Find a Feature
- **Constants/Settings**: `Core/config/constants.py`
- **Agent Logic**: `Core/agents/<agent_name>.py`
- **Error Types**: `Core/exceptions/errors.py`
- **Parsing Logic**: `Core/utils/text_parsers.py`
- **File Operations**: `Core/output/file_manager.py`
- **Logging Setup**: `Core/logging/logger.py`

### Add New Functionality
- **New Agent**: Create `Core/agents/myagent.py`
- **New Constant**: Add to `Core/config/constants.py`
- **New Exception**: Add to `Core/exceptions/errors.py`
- **New Utility**: Add to `Core/utils/`

### Debug Issues
1. Check `Logs/orchestrator_*.log` for high-level flow
2. Check `Logs/agents_*.log` for agent-specific issues
3. Check `Logs/audit_*.jsonl` for event timeline
4. Increase log level: Edit `Core/config/constants.py` → `LOG_LEVEL = "DEBUG"`

---

## Size Reference

| Directory | Approximate Size |
|-----------|------------------|
| `Core/` (code) | ~150 KB |
| `Models/` | ~4-25 GB (per model) |
| `Runtime/` | ~150 MB |
| `Engine/` | ~50 MB |
| `Logs/` | ~1-10 MB (rotates automatically) |
| `Projects/` | Varies (generated code) |
| **Documentation** | ~500 KB (plain text) |

---

## Backup Locations

| Original | Backup |
|----------|--------|
| `Core/OmniSolve_Orchestrator.py` | `Core/OmniSolve_Orchestrator.py.old` |

**Note**: All other files are new, no backups needed.

---

## Clean-Up Candidates

Can be safely deleted (legacy/unused):
- `Core/logging_module/` - Replaced by `Core/logging/`
- `Core/__pycache__/` - Python bytecode (auto-regenerates)
- `Generated_Software/` (root) - Duplicate of `AI_System/Generated_Software/`

---

**Use this file as a quick navigation guide for the OmniSolve 3.0 architecture!**
