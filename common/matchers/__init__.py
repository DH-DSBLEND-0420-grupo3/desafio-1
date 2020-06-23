import numpy as np
import re

def match_pattern(text, amenity_pattern):
    if text is not np.nan:
        m = re.search(amenity_pattern, text, re.I)
        if m is not None:
            return 1
    return 0

### returns number of rooms
def match_rooms(text):
    if text is not np.nan:
        regex = r'([0-9]+)\s+(amb\s|amb\.|ambiente)'
        m = re.search(regex, text, re.I)
        if m is not None:
            return np.int(m.group(1))
    return np.nan

### returns floor number
def match_floor(text):
    if text is not np.nan:
        if 'planta baja' in text:
            return 0
        regex = r'(1°|2°|3°|4°|5°|6°|2do|3er|primer|segundo|tercer|septimo|decimo)\spiso'
        m = re.search(regex, text, re.I)
        if m is not None:
            piso = m.group(1).lower()
            if piso in ['1°', 'primer']:
                return 1
            elif piso in ['2°', '2do', 'segundo']:
                return 2
            elif piso in ['3°', '3er', 'tercer']:
                return 3
            elif piso in ['septimo']:
                return 7
            elif piso in ['decimo']:
                return 10
            else:
                return np.int(piso.replace('°', ''))
    return np.nan

### returns 1 if there is a match else 0
def match_amenity_pileta(text):
    return match_pattern(text, "pileta|swimming pool|piscina|picina|pisina|jacuzzi|jacuzi")

### returns 1 if there is a match else 0
def match_amenity_parrilla(text):
    return match_pattern(text, "parrilla|parrila|orno de barro|barbecue|asador")

### returns 1 if there is a match else 0
def match_amenity_quincho(text):
    return match_pattern(text, "quincho")

### returns 1 if there is a match else 0
def match_amenity_patio(text):
    return match_pattern(text, "patio|jardin|jardín|con parque|parque con|lindo parque|parque compartido|parque arbolado")

### returns 1 if there is a match else 0
def match_amenity_cochera(text):
    return match_pattern(text, "cochera|garage")

### returns 1 if there is a match else 0
def match_amenity_balcon(text):
    return match_pattern(text, "balcon|balcón")

### returns value in meters2 or nan
def match_coveredm2(text):
    if text is not np.nan:
        regex = [
            r'(\d[0-9\.,]+)\s+m2\s+cub',
            r'metros\s+cubiertos\s*:?(\d[0-9\.,]+)',
            r'superficie\sedificada\s*:?\s*(\d[0-9\.,]+)',
            r'sup\.\scub\s*:?\s*(\d[0-9\.,]+)',
            r'sup\.\scubierta\s*:?\s*(\d[0-9\.,]+)',
            r'superficie\s+cubierta\s*:?\s*(\d[0-9\.,]+)',
        ]
        for pattern in regex:
            m = re.search(pattern, text, re.I)
            if m is not None:
                sup = m.group(1).strip(',')
                sup = sup.replace('.', '').replace(',', '.')
                if sup == '':
                    return np.nan
                return np.int(float(sup))
    return np.nan

### returns value in meters2 or nan
def match_totalm2(text):
    if text is not np.nan:
        regex = [
            r'(\d[0-9\.,]+)\s+m2\s+tot',
            r'metros\s+totales\s*:?\s*(\d[0-9\.,]+)',
            r'(\d[0-9\.,]+)\smtrs\stot',
            r'sup\.?\s+terreno\s*:?\s*(\d[0-9\.,]+)',
            r'sup\.?\s+total\s*:?\s*(\d[0-9\.,]+)',
            r'sup\.?\s+total\s+terreno\s*:?\s*(\d[0-9\.,]+)',
            r'sup\.?\s+total\s+del\s+terreno\s*:?\s*(\d[0-9\.,]+)',
            r'superficie\s+terreno\s*:?\s*(\d[0-9\.,]+)',
            r'superficie\s+total\s*:?\s*(\d[0-9\.,]+)',
            r'terreno\s*:?\s*(\d[0-9\.,]+)\s*mt',
            r'terreno\s*:?\s*(\d[0-9\.,]+),',
            r'(\d[0-9\.,]+)\s+m2\s+de\s+terreno',
            r'(\d[0-9\.,]+)\s+mts?\s+de\s+terreno',
        ]
        for pattern in regex:
            m = re.search(pattern, text, re.I)
            if m is not None:
                sup = m.group(1)
                sup = sup.replace('.', '').replace(',', '.')
                return np.nan if sup == '' else np.int(float(sup))
    return np.nan

### returns price, currency or nan, nan
def match_price_title(text):
    regex = r'^\s*(\$|u\$d|usd)\s*([0-9\.,]+).+en\sventa'
    m = re.search(regex, text, re.I)
    if m is None:
        return np.nan, np.nan
    currency = 'ARS' if m.group(1) == '$' else 'USD'
    price    = np.float64(m.group(2).replace('.', '').replace(',', '.'))
    return currency, price

### returns price, currency or nan, nan
def match_price_description(text):
    if text is not np.nan:    
        regex = r'(vendo\scasa|valor\sde\sventa|valor:|vendo|valor|precio\ses\sde|precio\sde)\s+(\$|u\$d|usd)\s*([0-9\.,]+)'
        m = re.search(regex, text, re.I)
        if m is not None:
            currency = 'ARS' if m.group(2) == '$' else 'USD'
            price    = m.group(3).strip('.')
            if len(price) > 0:
                return currency, np.float64(price.replace('.', '').replace(',', '.'))
    return np.nan, np.nan