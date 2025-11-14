import Initialise
import Scripts.GUI as start
from datetime import datetime

print(f"{datetime.now()}: Initialising")
print(f"{datetime.now()}: ⬇️ Downloading required packages")
Initialise.install_requirements()
print(f"{datetime.now()}: ✅ Downloaded required packages")

print(f"{datetime.now()}: Starting main app")
start.gui()