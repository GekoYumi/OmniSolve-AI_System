"""
OmniSolve Orchestrator - Refactored Version 3.0
Coordinates AI agents to generate software projects.
"""
import sys
import time

from .agents import (
    ArchitectAgent,
    PlannerAgent,
    DeveloperAgent,
    QAAgent
)
from .config import MAX_RETRIES
from .exceptions import (
    OmniSolveError,
    CodeGenerationError,
)
from .logging import get_logger, audit_log
from .output import file_manager
from .utils import psi_generator

logger = get_logger('orchestrator')


class OmniSolveOrchestrator:
    """
    Main orchestrator for the OmniSolve system.
    Coordinates agents to design and generate software projects.
    """

    def __init__(self):
        """Initialize the orchestrator and all agents."""
        logger.info("Initializing OmniSolve Orchestrator v3.0")

        # Initialize agents
        self.architect = ArchitectAgent()
        self.planner = PlannerAgent()
        self.developer = DeveloperAgent()
        self.qa = QAAgent()

        logger.info("All agents initialized successfully")

    def run(self, project_name: str, task: str) -> bool:
        """
        Execute the full development workflow.

        Args:
            project_name: Name of the project to create/modify
            task: Development task description

        Returns:
            True if successful, False otherwise
        """
        start_time = time.time()

        logger.info("=" * 60)
        logger.info("OMNISOLVE v3.0 - REFACTORED ARCHITECTURE")
        logger.info("=" * 60)
        logger.info(f"Project: {project_name}")
        logger.info(f"Task: {task}")
        logger.info("=" * 60)

        audit_log(
            'project_start',
            project_name=project_name,
            task=task,
            timestamp=time.time()
        )

        try:
            # Step 1: Generate PSI (cached)
            logger.info("\n[STEP 1] Generating Project State Interface...")
            psi = psi_generator.generate_psi(project_name, use_cache=True)
            logger.info(f"PSI generated ({len(psi)} chars)")

            # Step 2: Architect designs file structure
            logger.info("\n[STEP 2] ARCHITECT: Designing file structure...")
            file_list = self.architect.process(task, {
                'psi': psi,
                'project_name': project_name
            })

            logger.info(f"Architecture complete: {len(file_list)} files planned")
            for file_entry in file_list:
                logger.info(f"  - {file_entry['path']}")

            # Step 3: Planner creates logic blueprint
            logger.info("\n[STEP 3] PLANNER: Creating logic blueprint...")
            blueprint = self.planner.process(task, {
                'psi': psi,
                'file_list': file_list,
                'project_name': project_name
            })

            logger.info(f"Blueprint complete ({len(blueprint)} chars)")

            # Step 4: Developer generates code for each file
            logger.info("\n[STEP 4] DEVELOPER (Steve): Generating code...")

            files_written = 0
            files_failed = 0

            for i, file_entry in enumerate(file_list, 1):
                file_path = file_entry['path']
                logger.info(f"\n  [{i}/{len(file_list)}] Working on: {file_path}")

                success = self._generate_and_validate_file(
                    project_name,
                    file_path,
                    task,
                    psi,
                    blueprint
                )

                if success:
                    files_written += 1
                else:
                    files_failed += 1

            # Summary
            elapsed_time = time.time() - start_time
            logger.info(f"\n{'='*60}")
            logger.info("PROJECT COMPLETE")
            logger.info(f"{'='*60}")
            logger.info(f"Files written: {files_written}/{len(file_list)}")
            logger.info(f"Files failed: {files_failed}/{len(file_list)}")
            logger.info(f"Time elapsed: {elapsed_time:.1f}s")
            logger.info(f"{'='*60}")

            audit_log(
                'project_complete',
                project_name=project_name,
                files_written=files_written,
                files_failed=files_failed,
                elapsed_time=elapsed_time,
                success=files_failed == 0
            )

            return files_failed == 0

        except OmniSolveError as e:
            logger.error(f"OmniSolve error: {e}")
            if e.details:
                logger.error(f"Details: {e.details}")

            audit_log(
                'project_failed',
                project_name=project_name,
                error=str(e),
                error_type=type(e).__name__
            )
            return False

        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)

            audit_log(
                'project_failed',
                project_name=project_name,
                error=str(e),
                error_type='unexpected'
            )
            return False

    def _generate_and_validate_file(
        self,
        project_name: str,
        file_path: str,
        task: str,
        psi: str,
        blueprint: str
    ) -> bool:
        """
        Generate code for a single file with retry logic and QA validation.

        Args:
            project_name: Name of the project
            file_path: Path to the file to generate
            task: Original task description
            psi: Project state interface
            blueprint: Logic blueprint from planner

        Returns:
            True if file was successfully generated and validated
        """
        context = {
            'psi': psi,
            'blueprint': blueprint,
            'file_path': file_path,
            'project_name': project_name
        }

        previous_code = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                logger.info(f"    Attempt {attempt}/{MAX_RETRIES}...")

                # Generate code
                if attempt == 1:
                    code = self.developer.process(task, context)
                else:
                    # Regenerate with feedback
                    feedback = "Previous attempt failed validation. Generate better code."
                    code = self.developer.regenerate_with_feedback(
                        task,
                        context,
                        feedback,
                        previous_code
                    )

                previous_code = code

                # Quick syntax check first
                is_valid, syntax_error = self.qa.quick_validate(code, file_path)
                if not is_valid:
                    logger.warning(f"    Syntax error: {syntax_error}")
                    if attempt < MAX_RETRIES:
                        continue
                    else:
                        logger.error(f"    Max retries exhausted for {file_path}")
                        return False

                # Full QA review
                logger.info("    Submitting to QA for review...")
                passed, review = self.qa.process("Review code", {
                    'code': code,
                    'file_path': file_path,
                    'project_name': project_name
                })

                if passed:
                    # Write the file
                    logger.info("    [PASS] QA passed, writing file...")
                    written_path = file_manager.write_file(
                        project_name,
                        file_path,
                        code,
                        validate=True
                    )
                    logger.info(f"    [PASS] File saved: {written_path}")
                    return True
                else:
                    logger.warning(f"    [FAIL] QA rejected: {review[:100]}...")
                    if attempt < MAX_RETRIES:
                        logger.info("    Retrying...")
                    else:
                        logger.error(f"    Max retries exhausted for {file_path}")
                        return False

            except CodeGenerationError as e:
                logger.error(f"    Code generation failed: {e}")
                if attempt >= MAX_RETRIES:
                    return False

            except Exception as e:
                logger.error(f"    Unexpected error: {e}", exc_info=True)
                if attempt >= MAX_RETRIES:
                    return False

        return False


def main():
    """Main entry point for the orchestrator."""
    try:
        # Get user input
        print("\n" + "=" * 60)
        print("OMNISOLVE 3.0 - REFACTORED ARCHITECTURE")
        print("=" * 60)

        project_name = input("\nProject Name: ").strip()
        if not project_name:
            print("Error: Project name cannot be empty")
            return 1

        task = input("Development Request: ").strip()
        if not task:
            print("Error: Task cannot be empty")
            return 1

        # Create and run orchestrator
        orchestrator = OmniSolveOrchestrator()
        success = orchestrator.run(project_name, task)

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nFatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
