import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DB_PATH = os.path.join(BASE_DIR, "college.db")

ANTHROPIC_MODEL = "claude-sonnet-4-6"