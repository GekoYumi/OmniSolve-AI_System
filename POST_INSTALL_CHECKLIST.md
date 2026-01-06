# OmniSolve 3.0 - Post-Installation Checklist

## Installation Verification

### ✅ Step 1: Verify Directory Structure

**Check Core directories exist:**
```bash
cd e:\AI_System\Core
dir
```

**Expected directories:**
- [ ] `agents/`
- [ ] `config/`
- [ ] `exceptions/`
- [ ] `logging/`
- [ ] `output/`
- [ ] `utils/`

**Expected files:**
- [ ] `orchestrator.py`
- [ ] `__init__.py`
- [ ] `OmniSolve_Orchestrator.py.old` (backup)

---

### ✅ Step 2: Install Dependencies

```bash
cd e:\AI_System
Runtime\python.exe -m pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed requests-2.31.0 aiofiles-23.2.1
```

**Verify installation:**
```bash
Runtime\python.exe -m pip list | findstr /I "requests aiofiles"
```

- [ ] `requests` package installed
- [ ] `aiofiles` package installed

---

### ✅ Step 3: Test Module Imports

**Test orchestrator import:**
```bash
Runtime\python.exe -c "from AI_System.Core import OmniSolveOrchestrator; print('✓ Orchestrator OK')"
```

**Test agents import:**
```bash
Runtime\python.exe -c "from AI_System.Core.agents import ArchitectAgent; print('✓ Agents OK')"
```

**Test config import:**
```bash
Runtime\python.exe -c "from AI_System.Core.config import config_loader; print('✓ Config OK')"
```

**Test logging import:**
```bash
Runtime\python.exe -c "from AI_System.Core.logging import get_logger; print('✓ Logging OK')"
```

**Test utils import:**
```bash
Runtime\python.exe -c "from AI_System.Core.utils import psi_generator; print('✓ Utils OK')"
```

**Results:**
- [ ] Orchestrator imports successfully
- [ ] Agents import successfully
- [ ] Config imports successfully
- [ ] Logging imports successfully
- [ ] Utils imports successfully
- [ ] `.github/copilot-instructions.md` present and linked from `README_v3.0.md`

---

### ✅ Step 4: Verify Persona Configurations

**Check Config files:**
```bash
cd e:\AI_System\Config
dir *.json
```

**Expected files:**
- [ ] `Architect.json`
- [ ] `Developer.json` (loads Steve.json)
- [ ] `Planner.json`
- [ ] `QA.json`

**Test persona loading:**
```bash
cd e:\AI_System
Runtime\python.exe -c "from AI_System.Core.config import config_loader; print(config_loader.load_persona('Architect')['name'])"
```

**Expected output:** `Architect`

- [ ] Personas load without errors

---

### ✅ Step 5: Test Individual Components

**Test PSI Generator:**
```bash
Runtime\python.exe -c "from AI_System.Core.utils import psi_generator; print(psi_generator.generate_psi('test_project')[:100])"
```

**Expected:** PSI string starting with "PROJECT STATE"

- [ ] PSI generator works

**Test Text Parsers:**
```bash
Runtime\python.exe -c "from AI_System.Core.utils import validate_python_syntax; is_valid, err = validate_python_syntax('print(123)'); print(f'Valid: {is_valid}')"
```

**Expected:** `Valid: True`

- [ ] Text parsers work

**Test File Manager:**
```bash
Runtime\python.exe -c "from AI_System.Core.output import file_manager; print(f'Projects dir: {file_manager.projects_dir}')"
```

**Expected:** Projects directory path

- [ ] File manager initialized

---

### ✅ Step 6: Verify Launcher Update

**Check launcher:**
```bash
type LAUNCH_OMNISOLVE.bat | findstr "3.0"
```

**Expected:** Line containing "OmniSolve 3.0"

```bash
type LAUNCH_OMNISOLVE.bat | findstr "orchestrator"
```

**Expected:** Line containing `python -m AI_System.Core.orchestrator`

- [ ] Launcher title updated
- [ ] Launcher command updated

---

## Functional Testing

### ✅ Step 7: First Test Run

**Start the system:**
```bash
LAUNCH_OMNISOLVE.bat
```

**Wait for:**
1. KoboldCPP to start (1-3 minutes for model loading)
2. "AI Engine is ONLINE!" message
3. OmniSolve orchestrator prompt

**When prompted:**
- Project Name: `test_hello`
- Development Request: `Create a simple Python script that prints "Hello World"`

**Expected behavior:**
- [ ] Orchestrator starts without errors
- [ ] Shows "OMNISOLVE v3.0 - REFACTORED ARCHITECTURE"
- [ ] Completes STEP 1: PSI generation
- [ ] Completes STEP 2: Architect designs files
- [ ] Completes STEP 3: Planner creates blueprint
- [ ] Completes STEP 4: Developer generates code
- [ ] Files written to `AI_System\Projects\test_hello\`
- [ ] Shows "PROJECT COMPLETE" summary

---

### ✅ Step 8: Verify Generated Output

**Check project directory:**
```bash
dir AI_System\Projects\test_hello
```

**Expected:**
- [ ] Directory exists
- [ ] Contains at least 1 .py file
- [ ] Files have content (not empty)

**Test generated code:**
```bash
cd AI_System\Projects\test_hello
..\..\Runtime\python.exe main.py
```

**Expected:**
- [ ] Code runs without syntax errors
- [ ] Produces expected output

---

### ✅ Step 9: Verify Logging

**Check log files created:**
```bash
dir AI_System\Logs\*20260105*
```

**Expected files:**
- [ ] `audit_*.jsonl` - JSON audit trail
- [ ] `orchestrator_*.log` - Main logs
- [ ] `agents_*.log` - Agent logs

**Check audit log content:**
```bash
type AI_System\Logs\audit_*.jsonl
```

**Expected:** JSON lines with events like:
- [ ] `project_start`
- [ ] `brain_query`
- [ ] `architect_complete`
- [ ] `developer_complete`
- [ ] `qa_passed`
- [ ] `file_written`
- [ ] `project_complete`

**Check orchestrator log:**
```bash
type AI_System\Logs\orchestrator_*.log | findstr "INFO"
```

**Expected:**
- [ ] Initialization messages
- [ ] Step completion messages
- [ ] File save confirmations

---

### ✅ Step 10: Test Caching

**Run same project again (within 5 minutes):**
1. Launch system
2. Use same project name: `test_hello`
3. Same or different task

**Check logs for:**
```bash
type AI_System\Logs\orchestrator_*.log | findstr "cache"
```

**Expected:**
- [ ] "Using cached PSI" message appears
- [ ] Second run faster than first (PSI cached)

---

## Performance Verification

### ✅ Step 11: Check Performance Metrics

**Measure PSI generation time:**

First run:
```bash
Runtime\python.exe -c "import time; from AI_System.Core.utils import psi_generator; start = time.time(); psi_generator.generate_psi('test_hello', use_cache=False); print(f'Time: {time.time()-start:.3f}s')"
```

Cached run:
```bash
Runtime\python.exe -c "import time; from AI_System.Core.utils import psi_generator; psi_generator.generate_psi('test_hello'); start = time.time(); psi_generator.generate_psi('test_hello'); print(f'Time: {time.time()-start:.3f}s')"
```

**Results:**
- [ ] First run: ~0.1-0.5s
- [ ] Cached run: ~0.001s (1000x faster)

---

## Error Handling Verification

### ✅ Step 12: Test Error Handling

**Test missing model:**
```bash
REM Temporarily rename model file
rename AI_System\Models\Llama-3-8B-Instruct-32k-v0.1.Q5_K_M.gguf test.bak
LAUNCH_OMNISOLVE.bat
```

**Expected:**
- [ ] Shows "[CRITICAL] Model not found" message
- [ ] Exits gracefully

```bash
REM Rename back
rename AI_System\Models\test.bak Llama-3-8B-Instruct-32k-v0.1.Q5_K_M.gguf
```

**Test missing persona:**
```bash
REM Temporarily rename persona
rename AI_System\Config\Architect.json Architect.bak
LAUNCH_OMNISOLVE.bat
```

**Expected:**
- [ ] Shows ConfigurationError
- [ ] Error logged to file
- [ ] Exits gracefully

```bash
REM Rename back
rename AI_System\Config\Architect.bak Architect.json
```

---

## Documentation Verification

### ✅ Step 13: Verify Documentation Files

**Check documentation exists:**
```bash
cd e:\AI_System
dir *.md
```

**Expected files:**
- [ ] `README_v3.0.md`
- [ ] `FILE_LIST_v3.0.md`
- [ ] `INSTALLATION_GUIDE.md`
- [ ] `REFACTORING_SUMMARY.md`
- [ ] `DIRECTORY_STRUCTURE.md`
- [ ] `POST_INSTALL_CHECKLIST.md` (this file)

**Check file sizes (approximate):**
- [ ] README ~50+ KB
- [ ] FILE_LIST ~70+ KB
- [ ] INSTALLATION ~40+ KB
- [ ] REFACTORING_SUMMARY ~50+ KB
- [ ] DIRECTORY_STRUCTURE ~30+ KB

---

## Advanced Testing

### ✅ Step 14: Test Complex Project

**Run with complex request:**
- Project Name: `calculator_app`
- Task: `Create a command-line calculator application with a menu system that supports addition, subtraction, multiplication, division, and square root operations. Include input validation and a quit option.`

**Expected:**
- [ ] Multiple files generated (3-5)
- [ ] All files pass QA
- [ ] No syntax errors
- [ ] Project runs successfully

---

### ✅ Step 15: Stress Test (Optional)

**Test with larger project:**
- Project Name: `todo_app`
- Task: `Create a complete to-do list application with SQLite database, CRUD operations (Create, Read, Update, Delete), command-line interface, and data persistence.`

**Monitor:**
- [ ] All agents complete successfully
- [ ] Logs capture all events
- [ ] No memory issues
- [ ] Files written correctly

---

## Configuration Verification

### ✅ Step 16: Test Environment Variables

**Set custom log level:**
```bash
set OMNISOLVE_LOG_LEVEL=DEBUG
LAUNCH_OMNISOLVE.bat
```

**Check logs:**
- [ ] More detailed DEBUG messages appear

**Set custom timeout:**
```bash
set OMNISOLVE_API_TIMEOUT=180
LAUNCH_OMNISOLVE.bat
```

**Expected:**
- [ ] System uses 180s timeout (check in error scenarios)

---

## Final Checklist

### System Health

- [ ] All modules import successfully
- [ ] All dependencies installed
- [ ] All persona files present
- [ ] Launcher updated correctly
- [ ] Old orchestrator backed up

### Functionality

- [ ] Can generate simple project
- [ ] Can generate complex project
- [ ] All agents work (Architect, Planner, Developer, QA)
- [ ] Files written to correct location
- [ ] Generated code is valid Python
- [ ] Generated code runs without errors

### Performance

- [ ] PSI caching works (99%+ faster)
- [ ] Persona caching works (95%+ faster)
- [ ] No performance degradation vs v2.4

### Logging & Monitoring

- [ ] Audit logs created (JSON format)
- [ ] Orchestrator logs created
- [ ] Agent logs created
- [ ] All events tracked
- [ ] Logs rotate correctly

### Error Handling

- [ ] Missing model detected
- [ ] Missing persona detected
- [ ] Syntax errors caught
- [ ] API errors handled gracefully
- [ ] All errors logged with context

### Documentation

- [ ] README comprehensive
- [ ] FILE_LIST complete
- [ ] INSTALLATION_GUIDE clear
- [ ] REFACTORING_SUMMARY accurate
- [ ] DIRECTORY_STRUCTURE helpful

---

## Troubleshooting Common Issues

### Issue: Import errors

**Solution:**
```bash
cd e:\
Runtime\python.exe -m AI_System.Core.orchestrator
```

### Issue: Missing dependencies

**Solution:**
```bash
cd e:\AI_System
Runtime\python.exe -m pip install --upgrade -r requirements.txt
```

### Issue: API timeout

**Solution:**
1. Check KoboldCPP is running
2. Increase timeout in `Core/config/constants.py`
3. Set `OMNISOLVE_API_TIMEOUT=300` environment variable

### Issue: Syntax errors in generated code

**Solution:**
1. Check QA agent is working
2. Review `Logs/agents_*.log` for QA feedback
3. Increase `DEFAULT_TEMPERATURE` in `Core/config/constants.py`

### Issue: Files not written

**Solution:**
1. Check `Logs/file_manager_*.log`
2. Verify permissions on `Projects/` directory
3. Review `Logs/orchestrator_*.log` for errors

---

## Success Criteria

✅ **All checks passed** = System is production-ready!

If any checks fail:
1. Review the specific section above
2. Check the troubleshooting guide
3. Review relevant log files
4. Consult `README_v3.0.md` for details

---

## Next Steps After Verification

1. **Read Documentation**: Familiarize yourself with new structure
2. **Customize Settings**: Adjust `Core/config/constants.py` as needed
3. **Try Real Projects**: Generate actual applications
4. **Monitor Logs**: Review audit trails regularly
5. **Optimize**: Enable parallel execution or async writes if needed

---

## Rollback Instructions (If Needed)

If something is critically broken:

```bash
cd e:\AI_System\Core

REM 1. Restore old orchestrator
del orchestrator.py
del __init__.py
ren OmniSolve_Orchestrator.py.old OmniSolve_Orchestrator.py

REM 2. Update launcher
notepad ..\..\LAUNCH_OMNISOLVE.bat
REM Change: python -m AI_System.Core.orchestrator
REM To: python AI_System\Core\OmniSolve_Orchestrator.py

REM 3. System will work as v2.4
```

Then report issues and restore when fixed.

---

**OmniSolve 3.0 Verification Complete! 🎉**

Date: _______________  
Verified by: _______________  
Status: ⬜ Passed  ⬜ Failed  ⬜ Partial  

Notes:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
