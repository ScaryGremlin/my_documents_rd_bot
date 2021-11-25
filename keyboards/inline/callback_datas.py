from aiogram.utils.callback_data import CallbackData

main_callback = CallbackData("mainmenu", "action")
office_detail_callback = CallbackData("office_detail_menu", "action", "queue_id")
backtotop_callback = CallbackData("backtotopmenu", "action")
cancel_callback = CallbackData("cancelmenu", "action")
calendar_callback = CallbackData("calendar", "act", "year", "month", "day")
time_calendar_callback = CallbackData("time_calendar", "action", "time")
unsubscribe_callback = CallbackData("unsubscribemenu", "action")
type_window_callback = CallbackData("typewindowmenu", "action", "type_window")
