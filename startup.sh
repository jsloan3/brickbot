tmux kill-session -t brickbot &>/dev/null
tmux new-session -d -s brickbot "source .venv/bin/activate; python main.py"
tmux a -t brickbot
