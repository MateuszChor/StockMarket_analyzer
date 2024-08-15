import requests
import time


def send_telegram_message(bot_token, chat_id, message_text):
    """
    Wysyła wiadomość na Telegram za pomocą bota.

    Args:
    - bot_token (str): Token API bota Telegram.
    - chat_id (str): ID czatu lub nazwa użytkownika czatu (np. @username).
    - message_text (str): Treść wiadomości do wysłania.
    """
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message_text,
    }
    try:
        response = requests.post(send_url, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")
        return None
    return response.json()



def send_message_to_group(bot_token, group_id, message_text):
    send_telegram_message(bot_token, group_id, message_text)


def send_telegram_message_one(bot_token, chat_id, message_text, last_sent_times):
    print(last_sent_times)
    """
    Wysyła wiadomość na Telegram za pomocą bota, ale tylko jeśli ostatnia wiadomość
    została wysłana więcej niż 15 minut temu.

    Args:
    - bot_token (str): Token API bota Telegram.
    - chat_id (str): ID czatu lub nazwa użytkownika czatu (np. @username).
    - message_text (str): Treść wiadomości do wysłania.
    """
    current_time = time.time()
    min_interval = 15 * 60  # 15 minut przeliczone na sekundy

    # Sprawdź, czy można wysłać wiadomość
    if chat_id in last_sent_times and current_time - last_sent_times[chat_id] < min_interval:
        print(f"Wiadomość nie została wysłana: Ostatnia wiadomość wysłana mniej niż 15 minut temu.")
        return {"error": "Wiadomość nie została wysłana, ponieważ ostatnia wiadomość była mniej niż 15 minut temu."}

    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {
        "chat_id": chat_id,
        "text": message_text,
    }
    response = requests.post(send_url, params=params)

    # Zapisz czas wysłania wiadomości
    last_sent_times[chat_id] = current_time
    return response.json()
