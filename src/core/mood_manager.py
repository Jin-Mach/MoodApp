import datetime
import json
import pathlib

from src.utilities.error_handler import ErrorHandler


class MoodManager:
    mood_data_path = pathlib.Path(__file__).parents[2].joinpath("data")
    mood_data_path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_current_mood(mood: int, note: str) -> None:
        try:
            json_data = []
            current_datetime = datetime.datetime.now().isoformat()
            new_data = {
                "datetime": current_datetime,
                "mood": mood,
                "note": note
            }
            if MoodManager.mood_data_path.joinpath("user_data.json").exists():
                try:
                    with open(MoodManager.mood_data_path.joinpath("user_data.json"), "r", encoding="utf-8") as data:
                        json_data = json.load(data)
                except json.JSONDecodeError:
                    json_data = []
            json_data.append(new_data)
            with open(MoodManager.mood_data_path.joinpath("user_data.json"), "w", encoding="utf-8") as file:
                json.dump(json_data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e)