import cx_Freeze

executables = [cx_Freeze.Executable("astar.py")]

cx_Freeze.setup(
    name="TEST",
    options={"build_exe": {"packages":["pygame"]}},
    executables = executables
    )