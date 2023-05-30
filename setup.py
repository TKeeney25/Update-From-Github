from cx_Freeze import setup, Executable
directory_table = [
    ("ProgramMenuFolder", "TARGETDIR", "."),
    ("MyProgramMenu", "ProgramMenuFolder", "MYPROG~1|My Program"),
]

msi_data = {
    "ProgId": [
        ("Prog.Id", None, None, "This is a description", "IconId", None),
    ],
    "Icon": [
        ("IconId", "./data/images/icon.ico")
    ]
}
bdist_msi_options = {
    "data": msi_data
}


setup(
    name='TickerTracker',
    version='0.1.0',
    author='Tyler Keeney',
    author_email='tyler.a.keeney@gmail.com',
    description='Program that yields useful csv data from a list of funds',
    executables=[Executable("updater.py", icon='./data/images/icon.ico', target_name='TickerTracker-0.1.0')],
    options={
        "build_exe": {
            "excludes": ['tkinter', 'unittest'],
            "include_msvcr": True
        },
        "bdist_msi": bdist_msi_options
    }
)
