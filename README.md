# UK-Saures Integration

Библиотека для интеграции данных счетчиков из UK_GOROD и Saures API.

## Установка

```bash
pip install -e .
```

## Использование
### Как библиотека
```python
from uk_saures_integration import DataIntegrator

# Создаем интегратор
integrator = DataIntegrator()

# Собираем и интегрируем данные
readings = integrator.collect_and_integrate_data()

# Работаем с результатами
for reading in readings:
    print(f"{reading.service}: {reading.current_reading.value}")
```
### Как CLI инструмент
```bash
# Запуск интеграции
uk-saures-integrate

# Или через Python
python -m uk_saures_integration.cli
```
### Конфигурация ```secrets.yaml```
```yaml
services:
  - name: uk_gorod
    login: ваш_email@mail.ru
    password: ваш_пароль
  
  - name: saures
    login: ваш_email@saures.ru
    password: ваш_пароль_saures
```
