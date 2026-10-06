from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Reply keyboards
def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Create main menu keyboard."""
    keyboard = [
        [KeyboardButton(text="📊 Получить актуальный отчет")],
        [KeyboardButton(text="⚙️ Настройки парсинга")],
        [KeyboardButton(text="🔄 Синхронизировать БД")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Inline keyboards
def settings_inline_keyboard() -> InlineKeyboardMarkup:
    """Create settings inline keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="API", callback_data="source_api"),
         InlineKeyboardButton(text="JSON", callback_data="source_json")],
        [InlineKeyboardButton(text="Сохранить", callback_data="save_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def sync_inline_keyboard() -> InlineKeyboardMarkup:
    """Create synchronization inline keyboard."""
    keyboard = [
        [InlineKeyboardButton(text="Подтвердить синхронизацию", callback_data="confirm_sync")],
        [InlineKeyboardButton(text="Отмена", callback_data="cancel_sync")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Example usage
if __name__ == "__main__":
    # This would typically be called from handlers
    pass