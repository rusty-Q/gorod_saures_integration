from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class LastReading:
    date: str
    value: str

@dataclass
class CurrentReading:
    value: Optional[str] = None
    source: str = "uk_gorod"
    date: Optional[str] = None
    input_field_name: Optional[str] = None
    tariffs: Optional[Dict[str, str]] = None
    saures_meter_id: Optional[int] = None
    saures_type: Optional[str] = None
    saures_unit: Optional[str] = None
    saures_state: Optional[str] = None
    update_time: Optional[str] = None
    matching_info: Optional[Dict] = None

@dataclass
class MeterReading:
    id: int
    meter_reading_id: str
    service: str
    serial_number: str
    serial_normalized: str
    next_verification_date: str
    last_reading: LastReading
    current_reading: CurrentReading
    askue_link: Optional[str] = None
    metadata: Dict = field(default_factory=dict)
    
    @classmethod
    def from_uk_gorod_html(cls, idx: int, meter_id: str, service: str, 
                          serial_number: str, **kwargs):
        return cls(
            id=idx,
            meter_reading_id=meter_id,
            service=service,
            serial_number=serial_number,
            serial_normalized=serial_number,  # Будет нормализовано позже
            next_verification_date=kwargs.get('next_verification', ''),
            last_reading=LastReading(
                date=kwargs.get('last_reading_date', ''),
                value=kwargs.get('last_reading_value', '')
            ),
            current_reading=CurrentReading(
                value=kwargs.get('current_value', ''),
                date=kwargs.get('current_reading_date'),
                input_field_name='InputValCnt',
                source='uk_gorod'
            ),
            askue_link=kwargs.get('askue_link')
        )
