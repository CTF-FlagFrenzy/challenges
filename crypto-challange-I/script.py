#!/usr/bin/env python3
from dotenv import load_dotenv
import os

load_dotenv()

teamkey = os.getenv("TEAMKEY")
challangeKey = os.getenv("CHALLANGEKEY")
print(f"Team key: {teamkey}")
print(f"Challange key: {challangeKey}")

print("Running startup script...")
# Add your startup logic here
