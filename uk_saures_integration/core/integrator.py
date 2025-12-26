from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.meter_reading import MeterReading, CurrentReading
from .uk_gorod_client import UkGorodClient
from .saures_client import SauresClient
from ..utils.config import ConfigLoader

class DataIntegrator:
    def __init__(self, config_path: str = None):
        self.config_loader = ConfigLoader(config_path)
        self.uk_client = UkGorodClient()
        self.saures_client = SauresClient()
        
    def collect_and_integrate_data(self) -> List[MeterReading]:
        """Основной метод сбора и интеграции данных"""
        try:
            # 1. Загрузка конфигурации
            uk_config = self.config_loader.load_service_config('uk_gorod')
            saures_config = self.config_loader.load_service_config('saures')
            
            print("="*60)
            print("🏠 СБОР ДАННЫХ С UK_GOROD")
            print("="*60)
            
            # 2. Аутентификация и получение данных с UK_GOROD
            if not self.uk_client.authenticate(uk_config.login, uk_config.password):
                raise Exception("Ошибка аутентификации в UK_GOROD")
            
            uk_readings = self.uk_client.get_meter_readings()
            print(f"✅ Получено счетчиков с UK_GOROD: {len(uk_readings)}")
            
            print("\n" + "="*60)
            print("📡 ПОДКЛЮЧЕНИЕ К SAURES API")
            print("="*60)
            
            # 3. Аутентификация и получение данных с Saures
            saures_auth = self.saures_client.authenticate(
                saures_config.login, 
                saures_config.password
            )
            
            objects = self.saures_client.get_user_objects(saures_auth['sid'])
            if not objects:
                raise Exception("Нет доступных объектов в Saures")
            
            object_id = objects[0]['id']
            print(f"✅ Используем объект Saures ID: {object_id}")
            
            saures_meters = self.saures_client.get_object_meters(saures_auth['sid'], object_id)
            print(f"✅ Получено счетчиков с Saures: {len(saures_meters)}")
            
            # 4. Интеграция данных
            print("\n" + "="*60)
            print("🔄 ИНТЕГРАЦИЯ ДАННЫХ")
            print("="*60)
            
            updated_count = self._integrate_readings(uk_readings, saures_meters, object_id)
            print(f"✅ Обновлено показаний: {updated_count}/{len(uk_readings)}")
            
            # 5. Добавление метаданных
            for reading in uk_readings:
                reading.metadata = {
                    'saures_sync': reading.current_reading.source == 'saures_api',
                    'sync_time': datetime.now().isoformat(),
                    'object_id': object_id if reading.current_reading.source == 'saures_api' else None
                }
            
            return uk_readings
            
        except Exception as e:
            raise Exception(f"Ошибка интеграции данных: {e}")
    
    def _integrate_readings(self, uk_readings: List[MeterReading], 
                          saures_meters: Dict[str, Dict[str, Any]], 
                          object_id: int) -> int:
        """Интеграция показаний из Saures в данные UK_GOROD"""
        updated_count = 0
        
        for reading in uk_readings:
            if reading.serial_normalized in saures_meters:
                saures_data = saures_meters[reading.serial_normalized]
                values = saures_data['values']
                type_number = saures_data['type']['number']
                
                # Обновляем текущие показания
                reading.current_reading.source = 'saures_api'
                reading.current_reading.saures_meter_id = saures_data['meter_id']
                reading.current_reading.saures_type = saures_data['type']['name']
                reading.current_reading.saures_unit = saures_data['unit']
                reading.current_reading.saures_state = saures_data['state']['name']
                reading.current_reading.update_time = datetime.now().isoformat()
                
                # Обработка различных типов счетчиков
                if type_number == 8:  # Электричество (T1, T2, T3)
                    if len(values) >= 3:
                        total = sum(values)
                        reading.current_reading.value = f"{total:.2f}"
                        reading.current_reading.tariffs = {
                            'T1': f"{values[0]:.2f}",
                            'T2': f"{values[1]:.2f}",
                            'T3': f"{values[2]:.2f}"
                        }
                    else:
                        reading.current_reading.value = f"{sum(values):.2f}"
                else:
                    if values:
                        reading.current_reading.value = f"{values[-1]:.2f}"
                    else:
                        reading.current_reading.value = "0.00"
                
                # Сохраняем информацию о сопоставлении
                reading.current_reading.matching_info = {
                    'uk_serial_original': reading.serial_number,
                    'uk_serial_normalized': reading.serial_normalized,
                    'saures_serial_original': saures_data['original_sn'],
                    'saures_serial_normalized': saures_data['normalized_sn']
                }
                
                updated_count += 1
                
                print(f"    ✓ {reading.service}:")
                print(f"      SN: {reading.serial_number} → {reading.serial_normalized}")
                print(f"      Значение: {reading.current_reading.value}")
            
            else:
                print(f"    ✗ {reading.service}:")
                print(f"      SN: {reading.serial_number} → {reading.serial_normalized}")
                print(f"      Не найден в Saures")
        
        return updated_count
