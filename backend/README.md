# Backend



apt install python3-pip
apt install python3.12-venv


python3 -m venv venv
source venv/bin/activate

pip3 install poetry
cd ai-assistant
poetry install 
pip3 install torch torchvision torchaudio
ollama create temp0:latest -f Modefile

pip install fastapi
apt install uvicorn
sudo apt-get install coreutils

pip install langchain_community

Скачиваем модель
curl -fsSL https://ollama.com/install.sh | sh

Проверить что fastapi работает
uvicorn app:app --host 0.0.0.0 --port 8000

Проверить что agent работает
python agent/main.py 

screen -l
screen -R
screen -ls
screen -S uvicorn_session
screen -XS uvicorn_session quit