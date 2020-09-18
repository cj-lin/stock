conda create -yn stock -c quantopian --file requirements.txt
conda activate stock
python -m ipykernel install --user --name stock --display-name "Python (stock)"
