"""Contains tests for creating and initializing custom Julia projects."""

import unittest
import os
from pysr import julia_helpers
from tempfile import TemporaryDirectory


class TestJuliaProject(unittest.TestCase):
    """Various tests for working with Julia projects."""

    def test_custom_shared_env(self):
        """Test that we can use PySR in a custom shared env."""
        with TemporaryDirectory() as tmpdir:
            # Create a temp depot to store julia packages (and our custom env)
            Main = julia_helpers.init_julia()
            if "JULIA_DEPOT_PATH" not in os.environ:
                old_env = None
                os.environ["JULIA_DEPOT_PATH"] = tmpdir
            else:
                old_env = os.environ["JULIA_DEPOT_PATH"]
                os.environ[
                    "JULIA_DEPOT_PATH"
                ] = f"{tmpdir}:{os.environ['JULIA_DEPOT_PATH']}"
            test_env_name = "@pysr_test_env"
            julia_helpers.install(julia_project=test_env_name)
            Main = julia_helpers.init_julia(julia_project=test_env_name)
            Main.eval("using SymbolicRegression")
            Main.eval("using Pkg")
            cur_project_dir = Main.eval("splitdir(dirname(Base.active_project()))[1]")
            potential_shared_project_dirs = Main.eval("Pkg.envdir(DEPOT_PATH[1])")
            self.assertEqual(cur_project_dir, potential_shared_project_dirs)
            Main.eval("pop!(DEPOT_PATH)")
            if old_env is None:
                del os.environ["JULIA_DEPOT_PATH"]
            else:
                os.environ["JULIA_DEPOT_PATH"] = old_env
