import cx_Freeze

executables = [cx_Freeze.Executable("pygame_test1.py")]

cx_Freeze.setup(
    name="PsyqoSlither",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["apple.png","snakehead.png","fonts"]}},
    description = "Simple Snake Game",
    executables = executables,
    version = "0.1"
    )