import json
import pathlib

import requests

from src.utilities.error_handler import ErrorHandler


# noinspection PyBroadException
class FilesProvider:

    @staticmethod
    def check_json_files() -> bool:
        status = False
        try:
            required_files = ["app_config.json"]
            raw_url = "https://raw.githubusercontent.com/Jin-Mach/MoodApp/refs/heads/main/config/"
            files_path = pathlib.Path(__file__).parents[2].joinpath("config")
            files_path.mkdir(parents=True, exist_ok=True)
            for file in required_files:
                file_path = files_path.joinpath(file)
                if not file_path.exists() or file_path.stat().st_size == 0:
                    json_file = requests.get(f"{raw_url}{file}", timeout=5)
                    with open(files_path.joinpath(file), "w", encoding="utf-8") as raw_json:
                        raw_json.write(json_file.text)
                else:
                    try:
                        with open(file_path, "r", encoding="utf-8") as test_file:
                            json.load(test_file)
                    except:
                        json_file = requests.get(f"{raw_url}{file}", timeout=5)
                        with open(files_path.joinpath(file), "w", encoding="utf-8") as raw_json:
                            raw_json.write(json_file.text)
            status = True
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e, continue_visible=False, cancel_visible=True)
        return status

    @staticmethod
    def check_icons() -> bool:
        status = False
        try:
            required_files = ["neutralMoodButton_icon.png", "sadMoodButton_icon.png", "smileMoodButton_icon.png"]
            raw_url = "https://raw.githubusercontent.com/Jin-Mach/MoodApp/main/icons/"
            files_path = pathlib.Path(__file__).parents[2].joinpath("icons")
            files_path.mkdir(parents=True, exist_ok=True)
            for file in required_files:
                file_path = files_path.joinpath(file)
                if not file_path.exists() or file_path.stat().st_size == 0:
                    icon_file = requests.get(f"{raw_url}{file}", timeout=5)
                    with open(file_path, "wb") as raw_icon:
                        raw_icon.write(icon_file.content)
            status = True
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e, continue_visible=False, cancel_visible=True)
        return status