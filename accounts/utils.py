def normalize_phone(phone):
    import re
    phone = re.sub('[^0-9]', '', phone)
    if phone.startswith('0'):
        phone = f'996{phone[1:]}'
    phone = f'+{phone}'
    return phone