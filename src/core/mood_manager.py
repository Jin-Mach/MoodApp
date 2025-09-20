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

    @staticmethod
    def load_saved_mood() -> list[dict[str, str | int]]:
        try:
            saved_mood = []
            data_path = MoodManager.mood_data_path.joinpath("user_data.json")
            if data_path.exists() and data_path.stat().st_size > 0:
                with open(data_path, "r", encoding="utf-8") as file:
                    saved_mood = json.load(file)
            return saved_mood
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e)
            return saved_mood

    @staticmethod
    def format_data() -> list[tuple]:
        try:
            formated_data = []
            str_date = ""
            mood_data = MoodManager.load_saved_mood()
            for mood in mood_data:
                date = mood.get("datetime", "")
                if date:
                    date_time = datetime.datetime.fromisoformat(date)
                    str_date = date_time.strftime("%d.%m.%Y %H:%M")
                formated_data.append((str_date, mood.get("mood", ""), mood.get("note", "")))
            return formated_data
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e)
            return []

    @staticmethod
    def delete_saved_moods() -> None:
        try:
            mood_path = MoodManager.mood_data_path.joinpath("user_data.json")
            if mood_path.exists():
                mood_path.unlink()
        except Exception as e:
            error_handler = ErrorHandler()
            error_handler.write_show_exception(e)