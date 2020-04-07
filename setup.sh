sudo apt-get update
sudo apt-get install python3-venv

python3 -m venv env
source env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
git update-index --skip-worktree config.json
git update-index --skip-worktree serverips.json
git update-index --skip-worktree prefixes.json