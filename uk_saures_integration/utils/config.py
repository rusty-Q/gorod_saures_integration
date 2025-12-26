import yaml
import os
from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class ServiceConfig:
    name: str
    login: str
    password: str

class ConfigLoader:
    def __init__(self, config_path: str = None):
        if config_path is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.config_path = os.path.join(script_dir, '../../secrets.yaml')
        else:
            self.config_path = config_path
    
    def load_service_config(self, service_name: str) -> ServiceConfig:
        """Загружает конфигурацию для указанного сервиса"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                secrets = yaml.safe_load(f)
            
            for service in secrets.get('services', []):
                if service.get('name') == service_name:
                    return ServiceConfig(
                        name=service_name,
                        login=service['login'],
                        password=service['password']
                    )
            
            raise ValueError(f"Сервис '{service_name}' не найден в конфиге")
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл конфигурации не найден: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Ошибка парсинга YAML: {e}")
