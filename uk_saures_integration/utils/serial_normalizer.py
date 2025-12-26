def normalize_serial_number(serial: str) -> str:
    """Удаляет лидирующие нули из серийного номера"""
    if not serial:
        return ""
    serial = str(serial).strip()
    if serial and all(c == '0' for c in serial):
        return "0"
    return serial.lstrip('0') or "0"
