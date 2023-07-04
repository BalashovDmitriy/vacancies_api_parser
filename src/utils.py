def format_salary(value):
    if value is None:
        return "не указана"
    else:
        if value['from']:
            if value['to']:
                return f"от {value['from']} до {value['to']} {value['currency']}"
            else:
                return f"от {value['from']} {value['currency']}"
        else:
            if value['to']:
                return f"до {value['to']} {value['currency']}"