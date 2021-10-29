from git import Repo
from models import Repository


username = "Jacobamv"
password = "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"
name = input("Repo_name")
name2 = input("Enter name again")

if name != name2:
    print("Names don't match")
    exit()

full_local_path = "a/{name}"


repo = Repository(
    path = full_local_path,
)