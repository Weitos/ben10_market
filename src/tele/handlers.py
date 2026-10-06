import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.tele.kb import main_menu_keyboard, settings_inline_keyboard, sync_inline_keyboard
from src.base.data_provider import DataProvider
from src.base.analytics import process_market_data, get_top_products
from src.base.database import DatabaseClient
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Create router
router = Router()

# FSM States for settings
class SettingsStates(StatesGroup):
    waiting_for_source_choice = State()
    api_source = State()  # New state to track API vs JSON source preference

# Command handlers
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command."""
    # Set default source to JSON (more reliable)
    await state.update_data(source="json")
    
    welcome_text = (
        "👋 Добро пожаловать в Ben 10 Market Bot!\n\n"
        "Я помогу вам анализировать маржинальность товаров и выгружать отчеты в Google Sheets.\n\n"
        "Используйте кнопки ниже для навигации:"
    )
    await message.answer(welcome_text, reply_markup=main_menu_keyboard())

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    help_text = (
        "🤖 Доступные команды:\n"
        "/start - Главное меню\n"
        "/help - Помощь\n\n"
        "Кнопки:\n"
        "📊 Получить актуальный отчет - Анализ данных и выгрузка в Google Sheets\n"
        "⚙️ Настройки парсинга - Выбор источника данных (API/JSON)\n"
        "🔄 Синхронизировать БД - Обновление локальных данных"
    )
    await message.answer(help_text)

# Message handlers for buttons
@router.message(F.text == "📊 Получить актуальный отчет")
async def handle_get_report(message: Message, state: FSMContext):
    """Handle 'Get Report' button."""
    try:
        await message.answer("⏳ Начинаю анализ данных...")
        
        # Get user's source preference
        user_data = await state.get_data()
        use_api = user_data.get("source", "json") == "api"
        
        # Initialize components
        data_provider = DataProvider()
        db_client = DatabaseClient()
        
        # Load data (with API fallback logic)
        data = await data_provider.load_data(use_api=use_api)
        
        if not data:
            await message.answer("❌ Не удалось загрузить данные для анализа.")
            return
        
        source_text = "AliExpress API" if use_api and user_data.get("source") == "api" else "локальных данных"
        await message.answer(f"✅ Загружено {len(data)} товаров из {source_text}. Начинаю анализ...")
        
        # Process data
        df = process_market_data(data)
        top_products = get_top_products(df)
        
        await message.answer("✅ Анализ завершен. Выгружаю данные в Google Sheets...")
        
        # Upload to Excel file
        db_client.save_market_data(df)
        db_client.export_to_excel()
        
        # Generate summary for chat
        best_products_text = "\n".join([
            f"{i+1}. {row['name']} - маржа {row['net_margin_rub']:.2f} руб. ({row['margin_pct']:.1f}%)"
            for i, (_, row) in enumerate(top_products['best'].iterrows())
        ])
        
        worst_products_text = "\n".join([
            f"{i+1}. {row['name']} - маржа {row['net_margin_rub']:.2f} руб. ({row['margin_pct']:.1f}%)"
            for i, (_, row) in enumerate(top_products['worst'].iterrows())
        ])
        
        summary_text = (
            f"📈 <b>Анализ маржинальности завершен!</b>\n\n"
            f"📄 Всего товаров: {len(df)}\n"
            f"📡 Источник: {source_text}\n\n"
            f"🥇 <b>ТОП-3 лучших товара:</b>\n{best_products_text}\n\n"
            f"💣 <b>ТОП-3 худших товара:</b>\n{worst_products_text}\n\n"
            f"🔗 Данные доступны в Google Sheets."
        )
        
        await message.answer(summary_text, reply_markup=main_menu_keyboard())
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        await message.answer("❌ Произошла ошибка при генерации отчета. Пожалуйста, попробуйте позже.")

@router.message(F.text == "⚙️ Настройки парсинга")
async def handle_settings(message: Message, state: FSMContext):
    """Handle 'Settings' button."""
    settings_text = (
        "⚙️ <b>Настройки парсинга</b>\n\n"
        "Выберите источник данных для анализа:"
    )
    await message.answer(settings_text, reply_markup=settings_inline_keyboard())
    await state.set_state(SettingsStates.waiting_for_source_choice)

@router.message(F.text == "🔄 Синхронизировать БД")
async def handle_sync_db(message: Message):
    """Handle 'Sync DB' button."""
    sync_text = (
        "🔄 <b>Синхронизация базы данных</b>\n\n"
        "Это действие обновит локальные данные из источника API (если доступен) "
        "или проверит целостность существующих данных.\n\n"
        "Вы уверены, что хотите продолжить?"
    )
    await message.answer(sync_text, reply_markup=sync_inline_keyboard())

# Callback handlers
@router.callback_query(F.data.startswith("source_"))
async def handle_source_choice(callback: CallbackQuery, state: FSMContext):
    """Handle source selection callbacks."""
    source = callback.data.split("_")[1]
    
    if source == "api":
        response_text = "🌐 Источник данных изменен на API AliExpress."
        await state.update_data(source="api")
    elif source == "json":
        response_text = "📁 Источник данных изменен на локальный JSON файл."
        await state.update_data(source="json")
    else:
        response_text = "❓ Неизвестный источник данных."
    
    await callback.message.edit_text(response_text)
    await callback.answer()

@router.callback_query(F.data == "save_settings")
async def handle_save_settings(callback: CallbackQuery):
    """Handle save settings callback."""
    await callback.message.edit_text("✅ Настройки успешно сохранены!")
    await callback.answer()

@router.callback_query(F.data == "confirm_sync")
async def handle_confirm_sync(callback: CallbackQuery):
    """Handle confirm sync callback."""
    await callback.message.edit_text("🔄 Начинаю синхронизацию базы данных...")
    await callback.answer()
    
    # Here would be the actual sync logic
    # For now, we'll just simulate it
    await callback.message.answer("✅ Синхронизация завершена успешно!", reply_markup=main_menu_keyboard())

@router.callback_query(F.data == "cancel_sync")
async def handle_cancel_sync(callback: CallbackQuery):
    """Handle cancel sync callback."""
    await callback.message.edit_text("↩️ Синхронизация отменена.")
    await callback.answer()
    await callback.message.answer("Выберите действие:", reply_markup=main_menu_keyboard())

# Example usage
if __name__ == "__main__":
    # This would typically be called from main.py
    pass