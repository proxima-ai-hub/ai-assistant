import time
import requests

API_HOST = "localhost"
API_PORT = 8000


def generate_text(prompt):
    url = "http://localhost:8000/generateText/"
    data = {"prompt": prompt}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print('Error ', response.status_code)

def get_task_status(task_id):
    url = f"http://localhost:8000/task/{task_id['task_id']}"
    print('URL ', url)
    response = requests.get(url)
    if response.status_code == 200:
        result = response.json()
        print('Result: ', result)
        return result
    else:
        print('Error ', response.status_code)

def main():
    prompt = input("Enter the prompt: ")

    task_id = generate_text(prompt)
    while True:
        status = get_task_status(task_id)
        if "Task Pending" not in status:
            print(status)
            break
        time.sleep(2)


if __name__ == "__main__":
    main()
