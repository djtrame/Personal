import cx_Freeze

executables = [cx_Freeze.Executable("psyqo_tank2.py")]

cx_Freeze.setup(
    name="PsyqoTank",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["boom.wav","explosion.wav","fonts"]}},
    description = "Simple Tank Game",
    executables = executables,
    version = "0.1"
    )