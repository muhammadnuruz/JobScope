from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterState(StatesGroup):
    phone_number = State()
    location = State()
    photo = State()
    done = State()


class SearchCompanyState(StatesGroup):
    waiting_for_query = State()
    waiting_for_amount = State()


class TaskCreateState(StatesGroup):
    waiting_for_employee = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_deadline = State()
    waiting_for_reward = State()
    waiting_for_penalty = State()


class NearbyUserState(StatesGroup):
    waiting_for_location = State()
