import os
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


SUPERJOB_TOWN_CODE = 4
SUPERJOB_CATALOGUE_ID = 48

VACANCIES_PER_PAGE = 100

HH_AREA_CODE = '1'
SEARCH_PERIOD_DAYS = '30'

SALARY_INCREASE_FACTOR = 1.2
SALARY_DECREASE_FACTOR = 0.8


def predict_rub_salary_for_superJob(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * SALARY_INCREASE_FACTOR
    elif salary_to:
        return salary_to * SALARY_DECREASE_FACTOR
    return None


def get_average_salary_sj(language, headers):
    page = 0
    more_pages = True
    vacancies_found = 0
    vacancies_processed = 0
    total_salary = 0

    while more_pages:
        params = {
            'town': SUPERJOB_TOWN_CODE,
            'catalogues': SUPERJOB_CATALOGUE_ID,
            'keyword': f'Программист {language}',
            'page': page,
            'count': VACANCIES_PER_PAGE
        }
        response = requests.get(
            'https://api.superjob.ru/2.0/vacancies/',
            headers=headers,
            params=params
        )
        response.raise_for_status()
        data = response.json()
        vacancies = data.get('objects')
        more_pages = data.get('more')

        for vacancy in vacancies:
            if vacancy.get('currency') == 'rub':
                salary_from = vacancy.get('payment_from')
                salary_to = vacancy.get('payment_to')
                predicted_salary = predict_rub_salary_for_superJob(
                    salary_from,
                    salary_to
                )
                if predicted_salary:
                    vacancies_processed += 1
                    total_salary += predicted_salary

        vacancies_found += len(vacancies)
        page += 1

    average_salary = total_salary / vacancies_processed if vacancies_processed else 0
    return {
        'vacancies_found': vacancies_found,
        'vacancies_processed': vacancies_processed,
        'average_salary': int(average_salary)
    }


def predict_rub_salary(vacancy):
    salary_info = vacancy.get('salary')
    if not salary_info or salary_info.get('currency') != 'RUR':
        return None
    if salary_info['from'] and salary_info['to']:
        return (salary_info['from'] + salary_info['to']) / 2
    elif salary_info['from']:
        return salary_info['from'] * SALARY_INCREASE_FACTOR
    elif salary_info['to']:
        return salary_info['to'] * SALARY_DECREASE_FACTOR
    return None


def get_vacancies_info_hh(language):
    page = 0
    pages_number = 1
    vacancies_info = {
        'vacancies_found': 0,
        'vacancies_processed': 0,
        'average_salary': 0
    }
    while page < pages_number:
        params = {
            'text': f'программист {language}',
            'area': HH_AREA_CODE,
            'period': SEARCH_PERIOD_DAYS,
            'page': page,
            'per_page': VACANCIES_PER_PAGE
        }
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        vacancies_page = response.json()

        vacancies_processed = 0
        total_salary = 0
        for vacancy in vacancies_page['items']:
            predicted_salary = predict_rub_salary(vacancy)
            if predicted_salary:
                total_salary += predicted_salary
                vacancies_processed += 1

        vacancies_info['vacancies_found'] += vacancies_page['found']
        vacancies_info['vacancies_processed'] += vacancies_processed
        old_total = vacancies_info['average_salary'] * (vacancies_info['vacancies_processed'] - vacancies_processed)
        new_total = old_total + total_salary
        if vacancies_info['vacancies_processed'] > 0:
            vacancies_info['average_salary'] = int(new_total / vacancies_info['vacancies_processed'])

        pages_number = vacancies_page['pages']
        page += 1
    return vacancies_info


def print_statistics_table(statistics, source_name):
    table_data = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        ]
    ]
    for language, stats in statistics.items():
        table_data.append([
            language,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ])
    table = AsciiTable(table_data, source_name)
    print(table.table)


if __name__ == "__main__":
    load_dotenv()
    sj_api_key = os.getenv('SJ_API_KEY')
    languages = [
        'Python',
        'Java',
        'JavaScript',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'Go',
        'Scala',
        'Swift',
        'TypeScript'
    ]
    sj_headers = {'X-Api-App-Id': sj_api_key}

    sj_statistics = {}
    for language in languages:
        sj_statistics[language] = get_average_salary_sj(language, sj_headers)

    print_statistics_table(
        sj_statistics,
        "Статистика по сайту SuperJob Moscow"
    )

    hh_statistics = {}
    for language in languages:
        hh_statistics[language] = get_vacancies_info_hh(language)

    print_statistics_table(
        hh_statistics,
        "Статистика по сайту HeadHunter, Moscow"
    )
