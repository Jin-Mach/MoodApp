from src.utilities.files_provider import FilesProvider
from src.utilities.support_provider import SupportProvider


def app_init() -> bool:
    init_ok = False
    if SupportProvider.check_internet_connection():
        init_methods = [FilesProvider.check_json_files(), FilesProvider.check_icons()]
        if all(init_methods):
            init_ok = True
    return init_ok