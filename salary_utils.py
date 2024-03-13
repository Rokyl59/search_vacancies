def predict_rub_salary(salary_from, salary_to, increase_factor=1.2, decrease_factor=0.8):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * increase_factor
    elif salary_to:
        return salary_to * decrease_factor
    return None