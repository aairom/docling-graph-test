#!/bin/bash
# Git push script that excludes folders starting with underscore

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Git Push (Excluding _ folders)${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    echo -e "   Initialize with: ${GREEN}git init${NC}"
    exit 1
fi

# Check if .gitignore exists
if [ ! -f ".gitignore" ]; then
    echo -e "${YELLOW}⚠️  .gitignore not found, creating...${NC}"
    cat > .gitignore << 'EOF'
# Exclude folders starting with underscore
_*/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Logs
logs/
*.log

# Output files
output/
*.csv
*.html

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.bak
.cache/

# Environment variables
.env
.env.local
EOF
    echo -e "${GREEN}✓${NC} .gitignore created"
fi

# Show what will be excluded
echo -e "${BLUE}📁 Folders that will be excluded:${NC}"
find . -maxdepth 1 -type d -name "_*" ! -name ".git" | while read -r dir; do
    echo -e "   ${YELLOW}✗${NC} ${dir}"
done
echo ""

# Check for changes
if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    exit 0
fi

# Show status
echo -e "${BLUE}📊 Git status:${NC}"
git status --short
echo ""

# Ask for commit message
read -p "$(echo -e ${GREEN}Enter commit message:${NC} )" COMMIT_MSG

if [ -z "${COMMIT_MSG}" ]; then
    echo -e "${RED}❌ Commit message cannot be empty${NC}"
    exit 1
fi

# Add all files (respecting .gitignore)
echo -e "${BLUE}📦 Adding files...${NC}"
git add .

# Show what will be committed
echo ""
echo -e "${BLUE}📝 Files to be committed:${NC}"
git diff --cached --name-status | head -n 20
FILE_COUNT=$(git diff --cached --name-status | wc -l)
if [ "$FILE_COUNT" -gt 20 ]; then
    echo -e "${YELLOW}... and $((FILE_COUNT - 20)) more files${NC}"
fi
echo ""

# Confirm
read -p "$(echo -e ${YELLOW}Proceed with commit and push? [y/N]:${NC} )" -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}⚠️  Aborted${NC}"
    git reset
    exit 0
fi

# Commit
echo -e "${BLUE}💾 Committing...${NC}"
git commit -m "${COMMIT_MSG}"
echo -e "${GREEN}✓${NC} Committed"

# Get current branch
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push
echo ""
echo -e "${BLUE}🚀 Pushing to ${BRANCH}...${NC}"

if git push origin "${BRANCH}"; then
    echo -e "${GREEN}✓${NC} Pushed successfully to origin/${BRANCH}"
else
    echo -e "${RED}❌ Push failed${NC}"
    echo ""
    echo -e "${YELLOW}Possible solutions:${NC}"
    echo -e "  1. Set upstream: ${GREEN}git push -u origin ${BRANCH}${NC}"
    echo -e "  2. Check remote: ${GREEN}git remote -v${NC}"
    echo -e "  3. Add remote: ${GREEN}git remote add origin <url>${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Push Complete!${NC}"
echo -e "${GREEN}========================================${NC}"

# Made with Bob
