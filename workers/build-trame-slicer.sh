set -o errexit

cd /workspace/

git clone --depth=1 https://github.com/KitwareMedical/trame-slicer.git
cd ./trame-slicer/

/workspace/Python-3.10.18/python -m venv ./.venv/
source ./.venv/bin/activate


pip install --upgrade pip
pip install --editable ./


wget https://github.com/KitwareMedical/trame-slicer/releases/download/v0.0.1/vtk_mrml-9.4.0-cp310-cp310-manylinux_2_35_x86_64.whl
pip install ./vtk_mrml-9.4.0-cp310-cp310-manylinux_2_35_x86_64.whl
