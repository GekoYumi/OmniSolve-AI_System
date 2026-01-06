"""
Project State Interface (PSI) generator with caching.
Generates directory trees representing current project state.
"""
import os
import time
from pathlib import Path
from typing import Optional, Dict

from ..config.constants import PROJECTS_DIR, PSI_CACHE_TIMEOUT, PSI_MAX_FILES
from ..exceptions.errors import ProjectError
from ..logging import get_logger

logger = get_logger('psi')


class PSIGenerator:
    """Generates and caches Project State Interface representations."""

    def __init__(self):
        """Initialize the PSI generator."""
        self._cache: Dict[str, tuple[str, float]] = {}  # project_name -> (psi, timestamp)
        self._projects_dir = Path(PROJECTS_DIR)

        # Ensure projects directory exists
        self._projects_dir.mkdir(exist_ok=True, parents=True)

    def generate_psi(
        self,
        project_name: str,
        use_cache: bool = True,
        max_depth: Optional[int] = None
    ) -> str:
        """
        Generate Project State Interface for a project.

        Args:
            project_name: Name of the project
            use_cache: Whether to use cached PSI if available
            max_depth: Maximum directory depth to traverse (None for unlimited)

        Returns:
            PSI string representation of the project structure

        Raises:
            ProjectError: If project path is invalid
        """
        # Check cache if enabled
        if use_cache and project_name in self._cache:
            cached_psi, timestamp = self._cache[project_name]
            age = time.time() - timestamp

            if age < PSI_CACHE_TIMEOUT:
                logger.debug(f"Using cached PSI for {project_name} (age: {age:.1f}s)")
                return cached_psi
            else:
                logger.debug(f"Cache expired for {project_name} (age: {age:.1f}s)")

        # Generate fresh PSI
        project_path = self._projects_dir / project_name

        # Check if project exists
        if not project_path.exists():
            logger.info(f"New project: {project_name}")
            psi = f"PROJECT STATE: New Project (Empty Directory)\nPath: {project_path}"
        else:
            logger.debug(f"Generating PSI for existing project: {project_name}")
            psi = self._generate_tree(project_path, project_name, max_depth)

        # Cache the result
        self._cache[project_name] = (psi, time.time())

        return psi

    def _generate_tree(
        self,
        project_path: Path,
        project_name: str,
        max_depth: Optional[int] = None
    ) -> str:
        """
        Generate directory tree representation.

        Args:
            project_path: Path to the project directory
            project_name: Name of the project
            max_depth: Maximum depth to traverse

        Returns:
            Tree representation as string
        """
        psi = f"PROJECT STATE ({project_name}):\n"
        psi += f"Location: {project_path}\n\n"

        file_count = 0
        dir_count = 0

        try:
            for root, dirs, files in os.walk(project_path):
                # Calculate current depth
                level = root.replace(str(project_path), '').count(os.sep)

                # Check depth limit
                if max_depth is not None and level >= max_depth:
                    dirs[:] = []  # Don't recurse deeper
                    continue

                # Skip common directories that shouldn't be in PSI
                dirs[:] = [d for d in dirs if d not in [
                    '__pycache__', '.git', '.venv', 'node_modules',
                    'venv', '.pytest_cache', '.mypy_cache'
                ]]

                indent = '  ' * level
                dir_name = os.path.basename(root)

                if level == 0:
                    psi += f"{dir_name}/\n"
                else:
                    psi += f"{indent}{dir_name}/\n"

                dir_count += len(dirs)

                # Add files
                for file in sorted(files):
                    psi += f"{indent}  {file}\n"
                    file_count += 1

                    # If too many files, summarize instead
                    if file_count > PSI_MAX_FILES:
                        psi += f"{indent}  ... ({file_count - PSI_MAX_FILES} more files)\n"
                        logger.warning(
                            f"Project {project_name} has {file_count} files, "
                            f"truncating PSI at {PSI_MAX_FILES}"
                        )
                        return psi + f"\nSummary: {dir_count} directories, {file_count}+ files"

            psi += f"\nSummary: {dir_count} directories, {file_count} files"

        except PermissionError as e:
            logger.error(f"Permission denied accessing {project_path}: {e}")
            raise ProjectError(f"Cannot access project directory: {project_path}", {'error': str(e)})
        except Exception as e:
            logger.error(f"Error generating PSI for {project_name}: {e}")
            raise ProjectError(f"Failed to generate PSI for {project_name}", {'error': str(e)})

        return psi

    def invalidate_cache(self, project_name: Optional[str] = None) -> None:
        """
        Invalidate PSI cache.

        Args:
            project_name: Specific project to invalidate, or None for all
        """
        if project_name is None:
            logger.debug("Invalidating all PSI cache")
            self._cache.clear()
        elif project_name in self._cache:
            logger.debug(f"Invalidating PSI cache for {project_name}")
            del self._cache[project_name]

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache statistics
        """
        return {
            'cached_projects': len(self._cache),
            'projects': list(self._cache.keys())
        }


# Global PSI generator instance
psi_generator = PSIGenerator()
