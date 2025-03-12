# GitHub Common Commands

## Git Configuration
```sh
# Set your name and email for commits
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Check your Git configuration
git config --list
```

## Repository Management
```sh
# Clone a repository
git clone repository_url

# Initialize a new Git repository
git init
```

## Working with Branches
```sh
# List all branches
git branch

# Create a new branch
git branch branch_name

# Switch to a branch
git checkout branch_name

# Create and switch to a new branch
git checkout -b branch_name

# Delete a branch
git branch -d branch_name
```

## Staging and Committing
```sh
# Check the status of the repository
git status

# Add a specific file to staging
git add file_name

# Add all files to staging
git add .

# Commit changes with a message
git commit -m "Your commit message"
```

## Pushing and Pulling
```sh
# Push a branch to GitHub
git push origin branch_name

# Pull the latest changes from GitHub
git pull origin branch_name
```

## Merging and Rebasing
```sh
# Merge a branch into the current branch
git merge branch_name

# Rebase the current branch onto another
git rebase branch_name
```

## Undoing Changes
```sh
# Undo changes in a file
git checkout -- file_name

# Reset the last commit (keep changes staged)
git reset --soft HEAD~1

# Reset the last commit (discard changes)
git reset --hard HEAD~1
```

## Working with Remote Repositories
```sh
# Add a remote repository
git remote add origin repository_url

# Show remote repositories
git remote -v
```

## Tags
```sh
# List all tags
git tag

# Create a new tag
git tag -a v1.0 -m "Version 1.0"

# Push tags to GitHub
git push origin --tags
```

## Cleaning Up
```sh
# Remove untracked files
git clean -f

# Remove untracked directories
git clean -fd
```