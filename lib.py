from deta import Deta
import os

d = Deta(os.getenv("DETA_PROJECT_KEY"))


FILES_DRIVE = d.Drive("Files")
FILES_BASE = d.Base("Files")
