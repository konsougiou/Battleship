import requests

def initialize_host():
    return requests.get("http://127.0.0.1:8000/initialize")


def initialize_guest(key: int):
    return requests.get("http://127.0.0.1:8000/initialize", params={"key": key})


def send_grid(player: int, grid: list[list[int]], key: int):
    return requests.post("http://127.0.0.1:8000/setup", params={"player": player, "key": key}, json={"data": grid})


def ping_grid(player: int, key: int):
    return requests.get("http://127.0.0.1:8000/ping_setup", params={"player": player, "key": key})


def ping_initialize(key):
    return requests.get("http://127.0.0.1:8000/ping_initialize", params={"key": key})


def get_grid(player, key):
    return requests.get("http://127.0.0.1:8000/get_grid", params={"player": player, "key": key})


def fire(player, key, target):
    return requests.get("http://127.0.0.1:8000/fire", params={"player": player, "key": key, "x": target[0], "y": target[1]})


def ping_fire(key):
    return requests.get("http://127.0.0.1:8000/ping_fire", params={"key": key})
