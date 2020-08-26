#!/usr/bin/python3

import re

prefix_to_country = {
	'2A': ('GB-SCT', 'EU'),
	'2D': ('IM', 'EU'),
	'2E': ('GB-ENG', 'EU'),
	'2I': ('GB-NIR', 'EU'),
	'2J': ('JE', 'EU'),
	'2M': ('GB-SCT', 'EU'),
	'2U': ('GG', 'EU'),
	'2W': ('GB-WLS', 'EU'),
	'3A': ('MC', 'EU'),
	'3B6': ('MU', 'AF'),
	'3B7': ('MU', 'AF'),
	'3B8': ('MU', 'AF'),
	'3B9': ('MU', 'AF'),
	'3C': ('GQ', 'AF'),
	'3D2': ('FJ', 'OC'),
	'3DA': ('SZ', 'AF'),
	'3E': ('PA', 'NA'),
	'3F': ('PA', 'NA'),
	'3G': ('CL', 'SA'),
	'3H': ('CN', 'AS'),
	'3I': ('CN', 'AS'),
	'3J': ('CN', 'AS'),
	'3K': ('CN', 'AS'),
	'3L': ('CN', 'AS'),
	'3M': ('CN', 'AS'),
	'3N': ('CN', 'AS'),
	'3O': ('CN', 'AS'),
	'3P': ('CN', 'AS'),
	'3Q': ('CN', 'AS'),
	'3R': ('CN', 'AS'),
	'3S': ('CN', 'AS'),
	'3T': ('CN', 'AS'),
	'3U': ('CN', 'AS'),
	'3V': ('TN', 'AF'),
	'3W': ('VN', 'AS'),
	'3X': ('GN', 'AF'),
	'3Y': ('AQ', 'SA'),
	'3Z': ('PL', 'EU'),
	'4A': ('MX', 'NA'),
	'4B': ('MX', 'NA'),
	'4C': ('MX', 'NA'),
	'4D': ('PH', 'OC'),
	'4E': ('PH', 'OC'),
	'4F': ('PH', 'OC'),
	'4G': ('PH', 'OC'),
	'4H': ('PH', 'OC'),
	'4I': ('PH', 'OC'),
	'4J': ('AZ', 'AS'),
	'4K': ('AZ', 'AS'),
	'4L': ('GE', 'AS'),
	'4M': ('VE', 'SA'),
	'4M0': ('VE', 'NA'),
	'4O': ('ME', 'EU'),
	'4P': ('LK', 'AS'),
	'4Q': ('LK', 'AS'),
	'4R': ('LK', 'AS'),
	'4S': ('LK', 'AS'),
	'4T': ('PE', 'SA'),
	'4V': ('HT', 'NA'),
	'4W': ('TL', 'OC'),
	'4X': ('IL', 'AS'),
	'4Z': ('IL', 'AS'),
	'5A': ('LY', 'AF'),
	'5B': ('CY', 'AS'),
	'5C': ('MA', 'AF'),
	'5D': ('MA', 'AF'),
	'5E': ('MA', 'AF'),
	'5F': ('MA', 'AF'),
	'5G': ('MA', 'AF'),
	'5H': ('TZ', 'AF'),
	'5I': ('TZ', 'AF'),
	'5J': ('CO', 'SA'),
	'5J0': ('CO', 'NA'),
	'5K': ('CO', 'SA'),
	'5K0': ('CO', 'NA'),
	'5L': ('LR', 'AF'),
	'5M': ('LR', 'AF'),
	'5N': ('NG', 'AF'),
	'5O': ('NG', 'AF'),
	'5P': ('DK', 'EU'),
	'5Q': ('DK', 'EU'),
	'5R': ('MG', 'AF'),
	'5S': ('MG', 'AF'),
	'5T': ('MR', 'AF'),
	'5U': ('NE', 'AF'),
	'5V': ('TG', 'AF'),
	'5W': ('WS', 'OC'),
	'5X': ('UG', 'AF'),
	'5Y': ('KE', 'AF'),
	'5Z': ('KE', 'AF'),
	'6A': ('EG', 'AF'),
	'6B': ('EG', 'AF'),
	'6C': ('SY', 'AS'),
	'6D': ('MX', 'NA'),
	'6E': ('MX', 'NA'),
	'6F': ('MX', 'NA'),
	'6G': ('MX', 'NA'),
	'6H': ('MX', 'NA'),
	'6I': ('MX', 'NA'),
	'6J': ('MX', 'NA'),
	'6K': ('KR', 'AS'),
	'6L': ('KR', 'AS'),
	'6M': ('KR', 'AS'),
	'6N': ('KR', 'AS'),
	'6O': ('SO', 'AF'),
	'6P': ('PK', 'AS'),
	'6Q': ('PK', 'AS'),
	'6R': ('PK', 'AS'),
	'6S': ('PK', 'AS'),
	'6T': ('SD', 'AF'),
	'6U': ('SD', 'AF'),
	'6V': ('SN', 'AF'),
	'6W': ('SN', 'AF'),
	'6X': ('MG', 'AF'),
	'6Y': ('JM', 'NA'),
	'6Z': ('LR', 'AF'),
	'7A': ('ID', 'OC'),
	'7B': ('ID', 'OC'),
	'7C': ('ID', 'OC'),
	'7D': ('ID', 'OC'),
	'7E': ('ID', 'OC'),
	'7F': ('ID', 'OC'),
	'7G': ('ID', 'OC'),
	'7H': ('ID', 'OC'),
	'7I': ('ID', 'OC'),
	'7J': ('JP', 'AS'),
	'7K': ('JP', 'AS'),
	'7L': ('JP', 'AS'),
	'7M': ('JP', 'AS'),
	'7N': ('JP', 'AS'),
	'7O': ('YE', 'AS'),
	'7P': ('LS', 'AF'),
	'7Q': ('MW', 'AF'),
	'7R': ('DZ', 'AF'),
	'7S': ('SE', 'EU'),
	'7T': ('DZ', 'AF'),
	'7U': ('DZ', 'AF'),
	'7V': ('DZ', 'AF'),
	'7W': ('DZ', 'AF'),
	'7X': ('DZ', 'AF'),
	'7Y': ('DZ', 'AF'),
	'7Z': ('SA', 'AS'),
	'8A': ('ID', 'OC'),
	'8B': ('ID', 'OC'),
	'8C': ('ID', 'OC'),
	'8D': ('ID', 'OC'),
	'8E': ('ID', 'OC'),
	'8F': ('ID', 'OC'),
	'8G': ('ID', 'OC'),
	'8H': ('ID', 'OC'),
	'8I': ('ID', 'OC'),
	'8J': ('JP', 'AS'),
	'8K': ('JP', 'AS'),
	'8L': ('JP', 'AS'),
	'8M': ('JP', 'AS'),
	'8N': ('JP', 'AS'),
	'8O': ('BW', 'AF'),
	'8P': ('BB', 'NA'),
	'8Q': ('MV', 'AS'),
	'8R': ('GY', 'SA'),
	'8S': ('SE', 'EU'),
	'8T': ('IN', 'AS'),
	'8U': ('IN', 'AS'),
	'8V': ('IN', 'AS'),
	'8W': ('IN', 'AS'),
	'8X': ('IN', 'AS'),
	'8Y': ('IN', 'AS'),
	'8Z': ('SA', 'AS'),
	'9A': ('HR', 'EU'),
	'9B': ('IR', 'AS'),
	'9C': ('IR', 'AS'),
	'9D': ('IR', 'AS'),
	'9E': ('ET', 'AF'),
	'9F': ('ET', 'AF'),
	'9G': ('GH', 'AF'),
	'9H': ('MT', 'EU'),
	'9I': ('ZM', 'AF'),
	'9J': ('ZM', 'AF'),
	'9K': ('KW', 'AS'),
	'9L': ('SL', 'AF'),
	'9M': ('MY', 'AS'),
	'9M6': ('MY', 'OC'),
	'9M8': ('MY', 'OC'),
	'9N': ('NP', 'AS'),
	'9O': ('CD', 'AF'),
	'9P': ('CD', 'AF'),
	'9Q': ('CD', 'AF'),
	'9R': ('CD', 'AF'),
	'9S': ('CD', 'AF'),
	'9T': ('CD', 'AF'),
	'9U': ('BI', 'AF'),
	'9V': ('SG', 'AS'),
	'9W': ('MY', 'AS'),
	'9W6': ('MY', 'OC'),
	'9W8': ('MY', 'OC'),
	'9X': ('RW', 'AF'),
	'9Y': ('TT', 'SA'),
	'9Z': ('TT', 'SA'),
	'A': ('US', 'NA'),
	'A2': ('BW', 'AF'),
	'A3': ('TO', 'OC'),
	'A4': ('OM', 'AS'),
	'A5': ('BT', 'AS'),
	'A6': ('AE', 'AS'),
	'A7': ('QA', 'AS'),
	'A8': ('LR', 'AF'),
	'A9': ('BH', 'AS'),
	'AH0': ('GU', 'OC'),
	'AH1': ('US', 'OC'),
	'AH2': ('GU', 'OC'),
	'AH3': ('US', 'OC'),
	'AH4': ('US', 'OC'),
	'AH5': ('US', 'OC'),
	'AH6': ('US', 'OC'),
	'AH7': ('US', 'OC'),
	'AH8': ('AS', 'OC'),
	'AH9': ('US', 'OC'),
	'AM': ('ES', 'EU'),
	'AM8': ('ES', 'AF'),
	'AM9': ('ES', 'AF'),
	'AN': ('ES', 'EU'),
	'AN8': ('ES', 'AF'),
	'AN9': ('ES', 'AF'),
	'AO': ('ES', 'EU'),
	'AO8': ('ES', 'AF'),
	'AO9': ('ES', 'AF'),
	'AP': ('PK', 'AS'),
	'AQ': ('PK', 'AS'),
	'AR': ('PK', 'AS'),
	'AS': ('PK', 'AS'),
	'AT': ('IN', 'AS'),
	'AU': ('IN', 'AS'),
	'AV': ('IN', 'AS'),
	'AW': ('IN', 'AS'),
	'AX': ('AU', 'OC'),
	'AX0': ('AQ', 'SA'),
	'AX9': ('NF', 'OC'),
	'AX9C': ('CC', 'OC'),
	'AX9L': ('AU', 'OC'),
	'AX9M': ('AU', 'OC'),
	'AX9W': ('AU', 'OC'),
	'AX9X': ('CX', 'OC'),
	'AX9Y': ('CC', 'OC'),
	'AX9Z': ('AU', 'OC'),
	'AY': ('AR', 'SA'),
	'AY1Z': ('AQ', 'SA'),
	'AY2Z': ('AQ', 'SA'),
	'AY3Z': ('AQ', 'SA'),
	'AY4Z': ('AQ', 'SA'),
	'AY5Z': ('AQ', 'SA'),
	'AY6Z': ('AQ', 'SA'),
	'AY7Z': ('AQ', 'SA'),
	'AY8Z': ('AQ', 'SA'),
	'AY9Z': ('AQ', 'SA'),
	'AZ': ('AR', 'SA'),
	'B': ('CN', 'AS'),
	'BM': ('TW', 'AS'),
	'BN': ('TW', 'AS'),
	'BO': ('TW', 'AS'),
	'BP': ('TW', 'AS'),
	'BQ': ('TW', 'AS'),
	'BU': ('TW', 'AS'),
	'BV': ('TW', 'AS'),
	'BW': ('TW', 'AS'),
	'BX': ('TW', 'AS'),
	'C2': ('NR', 'OC'),
	'C3': ('AD', 'EU'),
	'C4': ('CY', 'AS'),
	'C5': ('GM', 'AF'),
	'C6': ('BS', 'NA'),
	'C8': ('MZ', 'AF'),
	'C9': ('MZ', 'AF'),
	'CA': ('CL', 'SA'),
	'CB': ('CL', 'SA'),
	'CC': ('CL', 'SA'),
	'CD': ('CL', 'SA'),
	'CE': ('CL', 'SA'),
	'CE9': ('AQ', 'SA'),
	'CF': ('CA', 'NA'),
	'CG': ('CA', 'NA'),
	'CH1': ('CA', 'NA'),
	'CH2': ('CA', 'NA'),
	'CI0': ('CA', 'NA'),
	'CI1': ('CA', 'NA'),
	'CI2': ('CA', 'NA'),
	'CJ': ('CA', 'NA'),
	'CK': ('CA', 'NA'),
	'CL': ('CU', 'NA'),
	'CM': ('CU', 'NA'),
	'CN': ('MA', 'AF'),
	'CO': ('CU', 'NA'),
	'CP': ('BO', 'SA'),
	'CQ': ('PT', 'EU'),
	'CQ2': ('PT', 'AF'),
	'CQ3': ('PT', 'AF'),
	'CQ9': ('PT', 'AF'),
	'CR': ('PT', 'EU'),
	'CR3': ('PT', 'AF'),
	'CR9': ('PT', 'AF'),
	'CS': ('PT', 'EU'),
	'CS3': ('PT', 'AF'),
	'CS9': ('PT', 'AF'),
	'CT': ('PT', 'EU'),
	'CT3': ('PT', 'AF'),
	'CT9': ('PT', 'AF'),
	'CU': ('PT', 'EU'),
	'CV': ('UY', 'SA'),
	'CW': ('UY', 'SA'),
	'CX': ('UY', 'SA'),
	'CY0': ('CA', 'NA'),
	'CY1': ('CA', 'NA'),
	'CY2': ('CA', 'NA'),
	'CY9': ('US', 'NA'),
	'CZ0': ('CA', 'NA'),
	'CZ1': ('CA', 'NA'),
	'CZ2': ('CA', 'NA'),
	'D': ('DE', 'EU'),
	'D2': ('AO', 'AF'),
	'D3': ('AO', 'AF'),
	'D4': ('CV', 'AF'),
	'D5': ('LR', 'AF'),
	'D6': ('KM', 'AF'),
	'D7': ('KR', 'AS'),
	'D8': ('KR', 'AS'),
	'D9': ('KR', 'AS'),
	'DS': ('KR', 'AS'),
	'DT': ('KR', 'AS'),
	'DU': ('PH', 'OC'),
	'DV': ('PH', 'OC'),
	'DW': ('PH', 'OC'),
	'DX': ('PH', 'OC'),
	'DY': ('PH', 'OC'),
	'DZ': ('PH', 'OC'),
	'E': ('ES', 'EU'),
	'E2': ('TH', 'AS'),
	'E3': ('ER', 'AF'),
	'E4': ('PS', 'AS'),
	'E5': ('CK', 'OC'),
	'E6': ('NU', 'OC'),
	'E7': ('BA', 'EU'),
	'EA8': ('ES', 'AF'),
	'EA9': ('ES', 'AF'),
	'EB8': ('ES', 'AF'),
	'EB9': ('ES', 'AF'),
	'EC8': ('ES', 'AF'),
	'EC9': ('ES', 'AF'),
	'ED8': ('ES', 'AF'),
	'ED9': ('ES', 'AF'),
	'EE8': ('ES', 'AF'),
	'EE9': ('ES', 'AF'),
	'EF8': ('ES', 'AF'),
	'EF9': ('ES', 'AF'),
	'EG8': ('ES', 'AF'),
	'EG9': ('ES', 'AF'),
	'EH8': ('ES', 'AF'),
	'EH9': ('ES', 'AF'),
	'EI': ('IE', 'EU'),
	'EJ': ('IE', 'EU'),
	'EK': ('AM', 'AS'),
	'EL': ('LR', 'AF'),
	'EM': ('UA', 'EU'),
	'EN': ('UA', 'EU'),
	'EO': ('UA', 'EU'),
	'EP': ('IR', 'AS'),
	'EQ': ('IR', 'AS'),
	'ER': ('MD', 'EU'),
	'ES': ('EE', 'EU'),
	'ET': ('ET', 'AF'),
	'EU': ('BY', 'EU'),
	'EV': ('BY', 'EU'),
	'EW': ('BY', 'EU'),
	'EX': ('KG', 'AS'),
	'EY': ('TJ', 'AS'),
	'EZ': ('TM', 'AS'),
	'F': ('FR', 'EU'),
	'FG': ('GP', 'NA'),
	'FH': ('YT', 'AF'),
	'FJ': ('FR', 'NA'),
	'FK': ('NC', 'OC'),
	'FM': ('MQ', 'NA'),
	'FO': ('PF', 'OC'),
	'FP': ('FR', 'NA'),
	'FR': ('FR', 'AF'),
	'FT': ('FR', 'AF'),
	'FT0X': ('TF', 'AF'),
	'FT0Y': ('AQ', 'SA'),
	'FT0Z': ('TF', 'AF'),
	'FT1Y': ('AQ', 'SA'),
	'FT1Z': ('TF', 'AF'),
	'FT2X': ('TF', 'AF'),
	'FT2Y': ('AQ', 'SA'),
	'FT2Z': ('TF', 'AF'),
	'FT3Y': ('AQ', 'SA'),
	'FT3Z': ('TF', 'AF'),
	'FT4X': ('TF', 'AF'),
	'FT4Y': ('AQ', 'SA'),
	'FT4Z': ('TF', 'AF'),
	'FT5X': ('TF', 'AF'),
	'FT5Y': ('AQ', 'SA'),
	'FT5Z': ('TF', 'AF'),
	'FT6Y': ('AQ', 'SA'),
	'FT6Z': ('TF', 'AF'),
	'FT7Y': ('AQ', 'SA'),
	'FT7Z': ('TF', 'AF'),
	'FT8X': ('TF', 'AF'),
	'FT8Y': ('AQ', 'SA'),
	'FT8Z': ('TF', 'AF'),
	'FW': ('WF', 'OC'),
	'FY': ('GF', 'SA'),
	'G': ('GB-ENG', 'EU'),
	'GC': ('GB-WLS', 'EU'),
	'GD': ('IM', 'EU'),
	'GH': ('JE', 'EU'),
	'GI': ('GB-NIR', 'EU'),
	'GJ': ('JE', 'EU'),
	'GM': ('GB-SCT', 'EU'),
	'GN': ('GB-NIR', 'EU'),
	'GP': ('GG', 'EU'),
	'GS': ('GB-SCT', 'EU'),
	'GT': ('IM', 'EU'),
	'GU': ('GG', 'EU'),
	'GW': ('GB-WLS', 'EU'),
	'H2': ('CY', 'AS'),
	'H3': ('PA', 'NA'),
	'H4': ('SB', 'OC'),
	'H5': ('ZA', 'AF'),
	'H6': ('NI', 'NA'),
	'H7': ('NI', 'NA'),
	'H8': ('PA', 'NA'),
	'H9': ('PA', 'NA'),
	'HA': ('HU', 'EU'),
	'HB': ('CH', 'EU'),
	'HB0': ('LI', 'EU'),
	'HC': ('EC', 'SA'),
	'HD': ('EC', 'SA'),
	'HE': ('CH', 'EU'),
	'HE0': ('LI', 'EU'),
	'HF': ('PL', 'EU'),
	'HG': ('HU', 'EU'),
	'HH': ('HT', 'NA'),
	'HI': ('DO', 'NA'),
	'HJ': ('CO', 'SA'),
	'HJ0': ('CO', 'NA'),
	'HJ0M': ('CO', 'SA'),
	'HK': ('CO', 'SA'),
	'HK0': ('CO', 'NA'),
	'HK0M': ('CO', 'SA'),
	'HL': ('KR', 'AS'),
	'HN': ('IQ', 'AS'),
	'HO': ('PA', 'NA'),
	'HP': ('PA', 'NA'),
	'HQ': ('HN', 'NA'),
	'HR': ('HN', 'NA'),
	'HS': ('TH', 'AS'),
	'HT': ('NI', 'NA'),
	'HU': ('SV', 'NA'),
	'HV': ('VA', 'EU'),
	'HW': ('FR', 'EU'),
	'HX': ('FR', 'EU'),
	'HY': ('FR', 'EU'),
	'HZ': ('SA', 'AS'),
	'I': ('IT', 'EU'),
	'IG9': ('IT', 'AF'),
	'IH9': ('IT', 'AF'),
	'J': ('JP', 'AS'),
	'J2': ('DJ', 'AF'),
	'J3': ('GD', 'NA'),
	'J4': ('GR', 'EU'),
	'J5': ('GW', 'AF'),
	'J6': ('LC', 'NA'),
	'J7': ('DM', 'NA'),
	'J8': ('VC', 'NA'),
	'JD1': ('JP', 'AS'),
	'JT': ('MN', 'AS'),
	'JU': ('MN', 'AS'),
	'JV': ('MN', 'AS'),
	'JW': ('NO', 'EU'),
	'JX': ('NO', 'EU'),
	'JY': ('JO', 'AS'),
	'K': ('US', 'NA'),
	'KH0': ('GU', 'OC'),
	'KH1': ('US', 'OC'),
	'KH2': ('GU', 'OC'),
	'KH3': ('US', 'OC'),
	'KH4': ('US', 'OC'),
	'KH5': ('US', 'OC'),
	'KH6': ('US', 'OC'),
	'KH7': ('US', 'OC'),
	'KH8': ('AS', 'OC'),
	'KH9': ('US', 'OC'),
	'KL9K': ('KR', 'AS'),
	'KP2': ('VI', 'NA'),
	'KP3': ('PR', 'NA'),
	'KP4': ('PR', 'NA'),
	'KP5': ('PR', 'NA'),
	'L1': ('AR', 'SA'),
	'L2': ('AR', 'SA'),
	'L3': ('AR', 'SA'),
	'L4': ('AR', 'SA'),
	'L5': ('AR', 'SA'),
	'L6': ('AR', 'SA'),
	'L7': ('AR', 'SA'),
	'L8': ('AR', 'SA'),
	'L9': ('AR', 'SA'),
	'LA': ('NO', 'EU'),
	'LB': ('NO', 'EU'),
	'LC': ('NO', 'EU'),
	'LD': ('NO', 'EU'),
	'LE': ('NO', 'EU'),
	'LF': ('NO', 'EU'),
	'LG': ('NO', 'EU'),
	'LH': ('NO', 'EU'),
	'LI': ('NO', 'EU'),
	'LJ': ('NO', 'EU'),
	'LK': ('NO', 'EU'),
	'LL': ('NO', 'EU'),
	'LM': ('NO', 'EU'),
	'LN': ('NO', 'EU'),
	'LO': ('AR', 'SA'),
	'LP': ('AR', 'SA'),
	'LQ': ('AR', 'SA'),
	'LR': ('AR', 'SA'),
	'LS': ('AR', 'SA'),
	'LT': ('AR', 'SA'),
	'LU': ('AR', 'SA'),
	'LU1Z': ('AQ', 'SA'),
	'LU2Z': ('AQ', 'SA'),
	'LU3Z': ('AQ', 'SA'),
	'LU4Z': ('AQ', 'SA'),
	'LU5Z': ('AQ', 'SA'),
	'LU6Z': ('AQ', 'SA'),
	'LU7Z': ('AQ', 'SA'),
	'LU8Z': ('AQ', 'SA'),
	'LU9Z': ('AQ', 'SA'),
	'LV': ('AR', 'SA'),
	'LW': ('AR', 'SA'),
	'LX': ('LU', 'EU'),
	'LY': ('LT', 'EU'),
	'LZ': ('BG', 'EU'),
	'M': ('GB-ENG', 'EU'),
	'MA': ('GB-SCT', 'EU'),
	'MC': ('GB-WLS', 'EU'),
	'MD': ('IM', 'EU'),
	'MH': ('JE', 'EU'),
	'MI': ('GB-NIR', 'EU'),
	'MJ': ('JE', 'EU'),
	'MM': ('GB-SCT', 'EU'),
	'MN': ('GB-NIR', 'EU'),
	'MP': ('GG', 'EU'),
	'MS': ('GB-SCT', 'EU'),
	'MT': ('IM', 'EU'),
	'MU': ('GG', 'EU'),
	'MW': ('GB-WLS', 'EU'),
	'N': ('US', 'NA'),
	'NH0': ('GU', 'OC'),
	'NH1': ('US', 'OC'),
	'NH2': ('GU', 'OC'),
	'NH3': ('US', 'OC'),
	'NH4': ('US', 'OC'),
	'NH5': ('US', 'OC'),
	'NH6': ('US', 'OC'),
	'NH7': ('US', 'OC'),
	'NH8': ('AS', 'OC'),
	'NH9': ('US', 'OC'),
	'NLD': ('KW', 'AS'),
	'NP2': ('VI', 'NA'),
	'NP3': ('PR', 'NA'),
	'NP4': ('PR', 'NA'),
	'NP5': ('PR', 'NA'),
	'OA': ('PE', 'SA'),
	'OB': ('PE', 'SA'),
	'OC': ('PE', 'SA'),
	'OD': ('LB', 'AS'),
	'OE': ('AT', 'EU'),
	'OF': ('FI', 'EU'),
	'OF0': ('AX', 'EU'),
	'OG': ('FI', 'EU'),
	'OG0': ('AX', 'EU'),
	'OH': ('FI', 'EU'),
	'OH0': ('AX', 'EU'),
	'OI': ('FI', 'EU'),
	'OI0': ('AX', 'EU'),
	'OJ': ('FI', 'EU'),
	'OK': ('CZ', 'EU'),
	'OL': ('CZ', 'EU'),
	'OM': ('SK', 'EU'),
	'ON': ('BE', 'EU'),
	'OO': ('BE', 'EU'),
	'OP': ('BE', 'EU'),
	'OQ': ('BE', 'EU'),
	'OR': ('BE', 'EU'),
	'OS': ('BE', 'EU'),
	'OT': ('BE', 'EU'),
	'OU': ('DK', 'EU'),
	'OV': ('DK', 'EU'),
	'OW': ('FO', 'EU'),
	'OX': ('GL', 'NA'),
	'OY': ('FO', 'EU'),
	'OZ': ('DK', 'EU'),
	'P2': ('PG', 'OC'),
	'P3': ('CY', 'AS'),
	'P4': ('AW', 'SA'),
	'P5': ('KP', 'AS'),
	'P6': ('KP', 'AS'),
	'P7': ('KP', 'AS'),
	'P8': ('KP', 'AS'),
	'P9': ('KP', 'AS'),
	'PA': ('NL', 'EU'),
	'PB': ('NL', 'EU'),
	'PC': ('NL', 'EU'),
	'PD': ('NL', 'EU'),
	'PE': ('NL', 'EU'),
	'PF': ('NL', 'EU'),
	'PG': ('NL', 'EU'),
	'PH': ('NL', 'EU'),
	'PI': ('NL', 'EU'),
	'PJ0': ('SX', 'NA'),
	'PJ2': ('CW', 'SA'),
	'PJ4': ('NL', 'SA'),
	'PJ5': ('NL', 'NA'),
	'PJ6': ('NL', 'NA'),
	'PJ7': ('SX', 'NA'),
	'PJ8': ('SX', 'NA'),
	'PK': ('ID', 'OC'),
	'PL': ('ID', 'OC'),
	'PM': ('ID', 'OC'),
	'PN': ('ID', 'OC'),
	'PO': ('ID', 'OC'),
	'PP': ('BR', 'SA'),
	'PQ': ('BR', 'SA'),
	'PR': ('BR', 'SA'),
	'PS': ('BR', 'SA'),
	'PT': ('BR', 'SA'),
	'PU': ('BR', 'SA'),
	'PV': ('BR', 'SA'),
	'PW': ('BR', 'SA'),
	'PX': ('BR', 'SA'),
	'PY': ('BR', 'SA'),
	'PZ': ('SR', 'SA'),
	'R': ('RU', 'EU'),
	'R0': ('RU', 'AS'),
	'R8': ('RU', 'AS'),
	'R8F': ('RU', 'EU'),
	'R8G': ('RU', 'EU'),
	'R8X': ('RU', 'EU'),
	'R9': ('RU', 'AS'),
	'R9F': ('RU', 'EU'),
	'R9G': ('RU', 'EU'),
	'R9X': ('RU', 'EU'),
	'RA0': ('RU', 'AS'),
	'RA8': ('RU', 'AS'),
	'RA8F': ('RU', 'EU'),
	'RA8G': ('RU', 'EU'),
	'RA8X': ('RU', 'EU'),
	'RA9': ('RU', 'AS'),
	'RA9F': ('RU', 'EU'),
	'RA9G': ('RU', 'EU'),
	'RA9X': ('RU', 'EU'),
	'RC0': ('RU', 'AS'),
	'RC8': ('RU', 'AS'),
	'RC8F': ('RU', 'EU'),
	'RC8G': ('RU', 'EU'),
	'RC8X': ('RU', 'EU'),
	'RC9': ('RU', 'AS'),
	'RC9F': ('RU', 'EU'),
	'RC9G': ('RU', 'EU'),
	'RC9X': ('RU', 'EU'),
	'RD0': ('RU', 'AS'),
	'RD8': ('RU', 'AS'),
	'RD8F': ('RU', 'EU'),
	'RD8G': ('RU', 'EU'),
	'RD8X': ('RU', 'EU'),
	'RD9': ('RU', 'AS'),
	'RD9F': ('RU', 'EU'),
	'RD9G': ('RU', 'EU'),
	'RD9X': ('RU', 'EU'),
	'RE0': ('RU', 'AS'),
	'RE8': ('RU', 'AS'),
	'RE8F': ('RU', 'EU'),
	'RE8G': ('RU', 'EU'),
	'RE8X': ('RU', 'EU'),
	'RE9': ('RU', 'AS'),
	'RE9F': ('RU', 'EU'),
	'RE9G': ('RU', 'EU'),
	'RE9X': ('RU', 'EU'),
	'RF0': ('RU', 'AS'),
	'RF8': ('RU', 'AS'),
	'RF8F': ('RU', 'EU'),
	'RF8G': ('RU', 'EU'),
	'RF8X': ('RU', 'EU'),
	'RF9': ('RU', 'AS'),
	'RF9F': ('RU', 'EU'),
	'RF9G': ('RU', 'EU'),
	'RF9X': ('RU', 'EU'),
	'RG0': ('RU', 'AS'),
	'RG8': ('RU', 'AS'),
	'RG8F': ('RU', 'EU'),
	'RG8G': ('RU', 'EU'),
	'RG8X': ('RU', 'EU'),
	'RG9': ('RU', 'AS'),
	'RG9F': ('RU', 'EU'),
	'RG9G': ('RU', 'EU'),
	'RG9X': ('RU', 'EU'),
	'RI0': ('RU', 'AS'),
	'RI1AN': ('AQ', 'SA'),
	'RI8': ('RU', 'AS'),
	'RI8X': ('RU', 'EU'),
	'RI9': ('RU', 'AS'),
	'RI9X': ('RU', 'EU'),
	'RJ0': ('RU', 'AS'),
	'RJ8': ('RU', 'AS'),
	'RJ8F': ('RU', 'EU'),
	'RJ8G': ('RU', 'EU'),
	'RJ8X': ('RU', 'EU'),
	'RJ9': ('RU', 'AS'),
	'RJ9F': ('RU', 'EU'),
	'RJ9G': ('RU', 'EU'),
	'RJ9X': ('RU', 'EU'),
	'RK0': ('RU', 'AS'),
	'RK8': ('RU', 'AS'),
	'RK8F': ('RU', 'EU'),
	'RK8G': ('RU', 'EU'),
	'RK8X': ('RU', 'EU'),
	'RK9': ('RU', 'AS'),
	'RK9F': ('RU', 'EU'),
	'RK9G': ('RU', 'EU'),
	'RK9X': ('RU', 'EU'),
	'RL0': ('RU', 'AS'),
	'RL8': ('RU', 'AS'),
	'RL8F': ('RU', 'EU'),
	'RL8G': ('RU', 'EU'),
	'RL8X': ('RU', 'EU'),
	'RL9': ('RU', 'AS'),
	'RL9F': ('RU', 'EU'),
	'RL9G': ('RU', 'EU'),
	'RL9X': ('RU', 'EU'),
	'RM0': ('RU', 'AS'),
	'RM8': ('RU', 'AS'),
	'RM8F': ('RU', 'EU'),
	'RM8G': ('RU', 'EU'),
	'RM8X': ('RU', 'EU'),
	'RM9': ('RU', 'AS'),
	'RM9F': ('RU', 'EU'),
	'RM9G': ('RU', 'EU'),
	'RM9X': ('RU', 'EU'),
	'RN0': ('RU', 'AS'),
	'RN8': ('RU', 'AS'),
	'RN8F': ('RU', 'EU'),
	'RN8G': ('RU', 'EU'),
	'RN8X': ('RU', 'EU'),
	'RN9': ('RU', 'AS'),
	'RN9F': ('RU', 'EU'),
	'RN9G': ('RU', 'EU'),
	'RN9X': ('RU', 'EU'),
	'RO0': ('RU', 'AS'),
	'RO8': ('RU', 'AS'),
	'RO8F': ('RU', 'EU'),
	'RO8G': ('RU', 'EU'),
	'RO8X': ('RU', 'EU'),
	'RO9': ('RU', 'AS'),
	'RO9F': ('RU', 'EU'),
	'RO9G': ('RU', 'EU'),
	'RO9X': ('RU', 'EU'),
	'RQ0': ('RU', 'AS'),
	'RQ8': ('RU', 'AS'),
	'RQ8F': ('RU', 'EU'),
	'RQ8G': ('RU', 'EU'),
	'RQ8X': ('RU', 'EU'),
	'RQ9': ('RU', 'AS'),
	'RQ9F': ('RU', 'EU'),
	'RQ9G': ('RU', 'EU'),
	'RQ9X': ('RU', 'EU'),
	'RT0': ('RU', 'AS'),
	'RT8': ('RU', 'AS'),
	'RT8F': ('RU', 'EU'),
	'RT8G': ('RU', 'EU'),
	'RT8X': ('RU', 'EU'),
	'RT9': ('RU', 'AS'),
	'RT9F': ('RU', 'EU'),
	'RT9G': ('RU', 'EU'),
	'RT9X': ('RU', 'EU'),
	'RU0': ('RU', 'AS'),
	'RU8': ('RU', 'AS'),
	'RU8F': ('RU', 'EU'),
	'RU8G': ('RU', 'EU'),
	'RU8X': ('RU', 'EU'),
	'RU9': ('RU', 'AS'),
	'RU9F': ('RU', 'EU'),
	'RU9G': ('RU', 'EU'),
	'RU9X': ('RU', 'EU'),
	'RV0': ('RU', 'AS'),
	'RV8': ('RU', 'AS'),
	'RV8F': ('RU', 'EU'),
	'RV8G': ('RU', 'EU'),
	'RV8X': ('RU', 'EU'),
	'RV9': ('RU', 'AS'),
	'RV9F': ('RU', 'EU'),
	'RV9G': ('RU', 'EU'),
	'RV9X': ('RU', 'EU'),
	'RW0': ('RU', 'AS'),
	'RW8': ('RU', 'AS'),
	'RW8F': ('RU', 'EU'),
	'RW8G': ('RU', 'EU'),
	'RW8X': ('RU', 'EU'),
	'RW9': ('RU', 'AS'),
	'RW9F': ('RU', 'EU'),
	'RW9G': ('RU', 'EU'),
	'RW9X': ('RU', 'EU'),
	'RX0': ('RU', 'AS'),
	'RX8': ('RU', 'AS'),
	'RX8F': ('RU', 'EU'),
	'RX8G': ('RU', 'EU'),
	'RX8X': ('RU', 'EU'),
	'RX9': ('RU', 'AS'),
	'RX9F': ('RU', 'EU'),
	'RX9G': ('RU', 'EU'),
	'RX9X': ('RU', 'EU'),
	'RY0': ('RU', 'AS'),
	'RY8': ('RU', 'AS'),
	'RY8F': ('RU', 'EU'),
	'RY8G': ('RU', 'EU'),
	'RY8X': ('RU', 'EU'),
	'RY9': ('RU', 'AS'),
	'RY9F': ('RU', 'EU'),
	'RY9G': ('RU', 'EU'),
	'RY9X': ('RU', 'EU'),
	'RZ0': ('RU', 'AS'),
	'RZ8': ('RU', 'AS'),
	'RZ8F': ('RU', 'EU'),
	'RZ8G': ('RU', 'EU'),
	'RZ8X': ('RU', 'EU'),
	'RZ9': ('RU', 'AS'),
	'RZ9F': ('RU', 'EU'),
	'RZ9G': ('RU', 'EU'),
	'RZ9X': ('RU', 'EU'),
	'S0': ('EH', 'AF'),
	'S2': ('BD', 'AS'),
	'S3': ('BD', 'AS'),
	'S4': ('ZA', 'AF'),
	'S5': ('SI', 'EU'),
	'S6': ('SG', 'AS'),
	'S7': ('SC', 'AF'),
	'S8': ('ZA', 'AF'),
	'S9': ('ST', 'AF'),
	'SA': ('SE', 'EU'),
	'SB': ('SE', 'EU'),
	'SC': ('SE', 'EU'),
	'SD': ('SE', 'EU'),
	'SE': ('SE', 'EU'),
	'SF': ('SE', 'EU'),
	'SG': ('SE', 'EU'),
	'SH': ('SE', 'EU'),
	'SI': ('SE', 'EU'),
	'SJ': ('SE', 'EU'),
	'SK': ('SE', 'EU'),
	'SL': ('SE', 'EU'),
	'SM': ('SE', 'EU'),
	'SN': ('PL', 'EU'),
	'SO': ('PL', 'EU'),
	'SP': ('PL', 'EU'),
	'SQ': ('PL', 'EU'),
	'SR': ('PL', 'EU'),
	'SS': ('EG', 'AF'),
	'ST': ('SD', 'AF'),
	'SU': ('EG', 'AF'),
	'SV': ('GR', 'EU'),
	'SW': ('GR', 'EU'),
	'SX': ('GR', 'EU'),
	'SY': ('GR', 'EU'),
	'SZ': ('GR', 'EU'),
	'T2': ('TV', 'OC'),
	'T30': ('KI', 'OC'),
	'T31': ('KI', 'OC'),
	'T32': ('KI', 'OC'),
	'T33': ('KI', 'OC'),
	'T4': ('CU', 'NA'),
	'T5': ('SO', 'AF'),
	'T6': ('AF', 'AS'),
	'T7': ('SM', 'EU'),
	'T8': ('PW', 'OC'),
	'TA': ('TR', 'AS'),
	'TA1': ('TR', 'EU'),
	'TB': ('TR', 'AS'),
	'TB1': ('TR', 'EU'),
	'TC': ('TR', 'AS'),
	'TC1': ('TR', 'EU'),
	'TD': ('GT', 'NA'),
	'TE': ('CR', 'NA'),
	'TF': ('IS', 'EU'),
	'TG': ('GT', 'NA'),
	'TH': ('FR', 'EU'),
	'TI': ('CR', 'NA'),
	'TJ': ('CM', 'AF'),
	'TK': ('FR', 'EU'),
	'TL': ('CF', 'AF'),
	'TM': ('FR', 'EU'),
	'TN': ('CG', 'AF'),
	'TP': ('FR', 'EU'),
	'TQ': ('FR', 'EU'),
	'TR': ('GA', 'AF'),
	'TS': ('TN', 'AF'),
	'TT': ('TD', 'AF'),
	'TU': ('CI', 'AF'),
	'TV': ('FR', 'EU'),
	'TW': ('WF', 'OC'),
	'TY': ('BJ', 'AF'),
	'TZ': ('ML', 'AF'),
	'U': ('RU', 'EU'),
	'U0': ('RU', 'AS'),
	'U5': ('UA', 'EU'),
	'U8': ('RU', 'AS'),
	'U8F': ('RU', 'EU'),
	'U8G': ('RU', 'EU'),
	'U8X': ('RU', 'EU'),
	'U9': ('RU', 'AS'),
	'U9F': ('RU', 'EU'),
	'U9G': ('RU', 'EU'),
	'U9X': ('RU', 'EU'),
	'UA0': ('RU', 'AS'),
	'UA8': ('RU', 'AS'),
	'UA8F': ('RU', 'EU'),
	'UA8G': ('RU', 'EU'),
	'UA8X': ('RU', 'EU'),
	'UA9': ('RU', 'AS'),
	'UA9F': ('RU', 'EU'),
	'UA9G': ('RU', 'EU'),
	'UA9X': ('RU', 'EU'),
	'UB0': ('RU', 'AS'),
	'UB8': ('RU', 'AS'),
	'UB8F': ('RU', 'EU'),
	'UB8G': ('RU', 'EU'),
	'UB8X': ('RU', 'EU'),
	'UB9': ('RU', 'AS'),
	'UB9F': ('RU', 'EU'),
	'UB9G': ('RU', 'EU'),
	'UB9X': ('RU', 'EU'),
	'UC0': ('RU', 'AS'),
	'UC8': ('RU', 'AS'),
	'UC8F': ('RU', 'EU'),
	'UC8G': ('RU', 'EU'),
	'UC8X': ('RU', 'EU'),
	'UC9': ('RU', 'AS'),
	'UC9F': ('RU', 'EU'),
	'UC9G': ('RU', 'EU'),
	'UC9X': ('RU', 'EU'),
	'UD0': ('RU', 'AS'),
	'UD8': ('RU', 'AS'),
	'UD8F': ('RU', 'EU'),
	'UD8G': ('RU', 'EU'),
	'UD8X': ('RU', 'EU'),
	'UD9': ('RU', 'AS'),
	'UD9F': ('RU', 'EU'),
	'UD9G': ('RU', 'EU'),
	'UD9X': ('RU', 'EU'),
	'UE0': ('RU', 'AS'),
	'UE8': ('RU', 'AS'),
	'UE8F': ('RU', 'EU'),
	'UE8G': ('RU', 'EU'),
	'UE8X': ('RU', 'EU'),
	'UE9': ('RU', 'AS'),
	'UE9F': ('RU', 'EU'),
	'UE9G': ('RU', 'EU'),
	'UE9X': ('RU', 'EU'),
	'UF0': ('RU', 'AS'),
	'UF8': ('RU', 'AS'),
	'UF8F': ('RU', 'EU'),
	'UF8G': ('RU', 'EU'),
	'UF8X': ('RU', 'EU'),
	'UF9': ('RU', 'AS'),
	'UF9F': ('RU', 'EU'),
	'UF9G': ('RU', 'EU'),
	'UF9X': ('RU', 'EU'),
	'UG0': ('RU', 'AS'),
	'UG8': ('RU', 'AS'),
	'UG8F': ('RU', 'EU'),
	'UG8G': ('RU', 'EU'),
	'UG8X': ('RU', 'EU'),
	'UG9': ('RU', 'AS'),
	'UG9F': ('RU', 'EU'),
	'UG9G': ('RU', 'EU'),
	'UG9X': ('RU', 'EU'),
	'UH0': ('RU', 'AS'),
	'UH8': ('RU', 'AS'),
	'UH8F': ('RU', 'EU'),
	'UH8G': ('RU', 'EU'),
	'UH8X': ('RU', 'EU'),
	'UH9': ('RU', 'AS'),
	'UH9F': ('RU', 'EU'),
	'UH9G': ('RU', 'EU'),
	'UH9X': ('RU', 'EU'),
	'UI0': ('RU', 'AS'),
	'UI8': ('RU', 'AS'),
	'UI8F': ('RU', 'EU'),
	'UI8G': ('RU', 'EU'),
	'UI8X': ('RU', 'EU'),
	'UI9': ('RU', 'AS'),
	'UI9F': ('RU', 'EU'),
	'UI9G': ('RU', 'EU'),
	'UI9X': ('RU', 'EU'),
	'UJ': ('UZ', 'AS'),
	'UK': ('UZ', 'AS'),
	'UL': ('UZ', 'AS'),
	'UM': ('UZ', 'AS'),
	'UN': ('KZ', 'AS'),
	'UO': ('KZ', 'AS'),
	'UP': ('KZ', 'AS'),
	'UQ': ('KZ', 'AS'),
	'UR': ('UA', 'EU'),
	'US': ('UA', 'EU'),
	'UT': ('UA', 'EU'),
	'UU': ('UA', 'EU'),
	'UV': ('UA', 'EU'),
	'UW': ('UA', 'EU'),
	'UX': ('UA', 'EU'),
	'UY': ('UA', 'EU'),
	'UZ': ('UA', 'EU'),
	'V2': ('AG', 'NA'),
	'V3': ('BZ', 'NA'),
	'V4': ('KN', 'NA'),
	'V5': ('NA', 'AF'),
	'V6': ('FM', 'OC'),
	'V7': ('MH', 'OC'),
	'V8': ('BN', 'OC'),
	'V9': ('ZA', 'AF'),
	'VA': ('CA', 'NA'),
	'VB': ('CA', 'NA'),
	'VC': ('CA', 'NA'),
	'VD1': ('CA', 'NA'),
	'VD2': ('CA', 'NA'),
	'VE': ('CA', 'NA'),
	'VF0': ('CA', 'NA'),
	'VF1': ('CA', 'NA'),
	'VF2': ('CA', 'NA'),
	'VG': ('CA', 'NA'),
	'VH': ('AU', 'OC'),
	'VH9': ('NF', 'OC'),
	'VH9C': ('CC', 'OC'),
	'VH9L': ('AU', 'OC'),
	'VH9M': ('AU', 'OC'),
	'VH9W': ('AU', 'OC'),
	'VH9X': ('CX', 'OC'),
	'VH9Y': ('CC', 'OC'),
	'VH9Z': ('AU', 'OC'),
	'VI': ('AU', 'OC'),
	'VI0': ('AQ', 'SA'),
	'VI9': ('NF', 'OC'),
	'VI9C': ('CC', 'OC'),
	'VI9L': ('AU', 'OC'),
	'VI9M': ('AU', 'OC'),
	'VI9W': ('AU', 'OC'),
	'VI9X': ('CX', 'OC'),
	'VI9Y': ('CC', 'OC'),
	'VI9Z': ('AU', 'OC'),
	'VJ': ('AU', 'OC'),
	'VJ9': ('NF', 'OC'),
	'VJ9C': ('CC', 'OC'),
	'VJ9L': ('AU', 'OC'),
	'VJ9M': ('AU', 'OC'),
	'VJ9W': ('AU', 'OC'),
	'VJ9X': ('CX', 'OC'),
	'VJ9Y': ('CC', 'OC'),
	'VJ9Z': ('AU', 'OC'),
	'VK': ('AU', 'OC'),
	'VK0': ('AQ', 'SA'),
	'VK9': ('NF', 'OC'),
	'VK9C': ('CC', 'OC'),
	'VK9FC': ('CC', 'OC'),
	'VK9FL': ('AU', 'OC'),
	'VK9FW': ('AU', 'OC'),
	'VK9FX': ('CX', 'OC'),
	'VK9KC': ('CC', 'OC'),
	'VK9KX': ('CX', 'OC'),
	'VK9L': ('AU', 'OC'),
	'VK9M': ('AU', 'OC'),
	'VK9W': ('AU', 'OC'),
	'VK9X': ('CX', 'OC'),
	'VK9Y': ('CC', 'OC'),
	'VK9Z': ('AU', 'OC'),
	'VK9ZY': ('CC', 'OC'),
	'VL': ('AU', 'OC'),
	'VL9': ('NF', 'OC'),
	'VL9C': ('CC', 'OC'),
	'VL9L': ('AU', 'OC'),
	'VL9M': ('AU', 'OC'),
	'VL9W': ('AU', 'OC'),
	'VL9X': ('CX', 'OC'),
	'VL9Y': ('CC', 'OC'),
	'VL9Z': ('AU', 'OC'),
	'VM': ('AU', 'OC'),
	'VM9': ('NF', 'OC'),
	'VM9C': ('CC', 'OC'),
	'VM9L': ('AU', 'OC'),
	'VM9M': ('AU', 'OC'),
	'VM9W': ('AU', 'OC'),
	'VM9X': ('CX', 'OC'),
	'VM9Y': ('CC', 'OC'),
	'VM9Z': ('AU', 'OC'),
	'VN': ('AU', 'OC'),
	'VN9': ('NF', 'OC'),
	'VN9C': ('CC', 'OC'),
	'VN9L': ('AU', 'OC'),
	'VN9M': ('AU', 'OC'),
	'VN9W': ('AU', 'OC'),
	'VN9X': ('CX', 'OC'),
	'VN9Y': ('CC', 'OC'),
	'VN9Z': ('AU', 'OC'),
	'VO1': ('CA', 'NA'),
	'VO2': ('CA', 'NA'),
	'VP2E': ('AI', 'NA'),
	'VP2M': ('MS', 'NA'),
	'VP2V': ('VG', 'NA'),
	'VP5': ('TC', 'NA'),
	'VP6': ('GB', 'OC'),
	'VP8': ('FK', 'SA'),
	'VP9': ('BM', 'NA'),
	'VQ5': ('TC', 'NA'),
	'VQ9': ('GB', 'AF'),
	'VR': ('HK', 'AS'),
	'VT': ('IN', 'AS'),
	'VU': ('IN', 'AS'),
	'VV': ('IN', 'AS'),
	'VW': ('IN', 'AS'),
	'VX': ('CA', 'NA'),
	'VY0': ('CA', 'NA'),
	'VY1': ('CA', 'NA'),
	'VY2': ('CA', 'NA'),
	'VY9': ('CA', 'NA'),
	'VZ': ('AU', 'OC'),
	'VZ9': ('NF', 'OC'),
	'VZ9C': ('CC', 'OC'),
	'VZ9L': ('AU', 'OC'),
	'VZ9M': ('AU', 'OC'),
	'VZ9W': ('AU', 'OC'),
	'VZ9X': ('CX', 'OC'),
	'VZ9Y': ('CC', 'OC'),
	'VZ9Z': ('AU', 'OC'),
	'W': ('US', 'NA'),
	'WH0': ('GU', 'OC'),
	'WH1': ('US', 'OC'),
	'WH2': ('GU', 'OC'),
	'WH3': ('US', 'OC'),
	'WH4': ('US', 'OC'),
	'WH5': ('US', 'OC'),
	'WH6': ('US', 'OC'),
	'WH7': ('US', 'OC'),
	'WH8': ('AS', 'OC'),
	'WH9': ('US', 'OC'),
	'WP2': ('VI', 'NA'),
	'WP3': ('PR', 'NA'),
	'WP4': ('PR', 'NA'),
	'WP5': ('PR', 'NA'),
	'XA': ('MX', 'NA'),
	'XB': ('MX', 'NA'),
	'XC': ('MX', 'NA'),
	'XD': ('MX', 'NA'),
	'XE': ('MX', 'NA'),
	'XF': ('MX', 'NA'),
	'XG': ('MX', 'NA'),
	'XH': ('MX', 'NA'),
	'XI': ('MX', 'NA'),
	'XJ1': ('CA', 'NA'),
	'XJ2': ('CA', 'NA'),
	'XK0': ('CA', 'NA'),
	'XK1': ('CA', 'NA'),
	'XK2': ('CA', 'NA'),
	'XL': ('CA', 'NA'),
	'XM': ('CA', 'NA'),
	'XN1': ('CA', 'NA'),
	'XN2': ('CA', 'NA'),
	'XO0': ('CA', 'NA'),
	'XO1': ('CA', 'NA'),
	'XO2': ('CA', 'NA'),
	'XP': ('GL', 'NA'),
	'XQ': ('CL', 'SA'),
	'XR': ('CL', 'SA'),
	'XR9': ('AQ', 'SA'),
	'XS': ('CN', 'AS'),
	'XT': ('BF', 'AF'),
	'XU': ('KH', 'AS'),
	'XV': ('VN', 'AS'),
	'XW': ('LA', 'AS'),
	'XX9': ('MO', 'AS'),
	'XY': ('MM', 'AS'),
	'XZ': ('MM', 'AS'),
	'Y2': ('DE', 'EU'),
	'Y3': ('DE', 'EU'),
	'Y4': ('DE', 'EU'),
	'Y5': ('DE', 'EU'),
	'Y6': ('DE', 'EU'),
	'Y7': ('DE', 'EU'),
	'Y8': ('DE', 'EU'),
	'Y9': ('DE', 'EU'),
	'YA': ('AF', 'AS'),
	'YB': ('ID', 'OC'),
	'YC': ('ID', 'OC'),
	'YD': ('ID', 'OC'),
	'YE': ('ID', 'OC'),
	'YF': ('ID', 'OC'),
	'YG': ('ID', 'OC'),
	'YH': ('ID', 'OC'),
	'YI': ('IQ', 'AS'),
	'YJ': ('VU', 'OC'),
	'YK': ('SY', 'AS'),
	'YL': ('LV', 'EU'),
	'YM': ('TR', 'AS'),
	'YM1': ('TR', 'EU'),
	'YN': ('NI', 'NA'),
	'YO': ('RO', 'EU'),
	'YP': ('RO', 'EU'),
	'YQ': ('RO', 'EU'),
	'YR': ('RO', 'EU'),
	'YS': ('SV', 'NA'),
	'YT': ('RS', 'EU'),
	'YU': ('RS', 'EU'),
	'YV': ('VE', 'SA'),
	'YV0': ('VE', 'NA'),
	'YW': ('VE', 'SA'),
	'YW0': ('VE', 'NA'),
	'YX': ('VE', 'SA'),
	'YX0': ('VE', 'NA'),
	'YY': ('VE', 'SA'),
	'YY0': ('VE', 'NA'),
	'Z2': ('ZW', 'AF'),
	'Z3': ('MK', 'EU'),
	'Z6': ('XK', 'EU'),
	'Z8': ('SS', 'AF'),
	'ZA': ('AL', 'EU'),
	'ZB': ('GI', 'EU'),
	'ZC4': ('GB', 'AS'),
	'ZD7': ('SH', 'AF'),
	'ZD8': ('SH', 'AF'),
	'ZD9': ('SH', 'AF'),
	'ZF': ('KY', 'NA'),
	'ZG': ('GI', 'EU'),
	'ZK': ('NZ', 'OC'),
	'ZK3': ('TK', 'OC'),
	'ZL': ('NZ', 'OC'),
	'ZL5': ('AQ', 'SA'),
	'ZL50': ('NZ', 'OC'),
	'ZM': ('NZ', 'OC'),
	'ZM5': ('AQ', 'SA'),
	'ZP': ('PY', 'SA'),
	'ZR': ('ZA', 'AF'),
	'ZS': ('ZA', 'AF'),
	'ZS7': ('AQ', 'SA'),
	'ZT': ('ZA', 'AF'),
	'ZU': ('ZA', 'AF'),
	'ZV': ('BR', 'SA'),
	'ZW': ('BR', 'SA'),
	'ZX': ('BR', 'SA'),
	'ZY': ('BR', 'SA'),
	'ZZ': ('BR', 'SA'),
}


country_names = {
	'AD': 'Andorra',
	'AE': 'United Arab Emirates',
	'AF': 'Afghanistan',
	'AG': 'Antigua & Barbuda',
	'AI': 'Anguilla',
	'AL': 'Albania',
	'AM': 'Armenia',
	'AO': 'Angola',
	'AQ': 'Antarctica',
	'AR': 'Argentina',
	'AS': 'American Samoa',
	'AT': 'Austria',
	'AU': 'Australia',
	'AW': 'Aruba',
	'AX': 'Åland Islands',
	'AZ': 'Azerbaijan',
	'BA': 'Bosnia',
	'BB': 'Barbados',
	'BD': 'Bangladesh',
	'BE': 'Belgium',
	'BF': 'Burkina Faso',
	'BG': 'Bulgaria',
	'BH': 'Bahrain',
	'BI': 'Burundi',
	'BJ': 'Benin',
	'BL': 'St. Barthélemy',
	'BM': 'Bermuda',
	'BN': 'Brunei',
	'BO': 'Bolivia',
	'BQ': 'Caribbean Netherlands',
	'BR': 'Brazil',
	'BS': 'Bahamas',
	'BT': 'Bhutan',
	'BV': 'Bouvet Island',
	'BW': 'Botswana',
	'BY': 'Belarus',
	'BZ': 'Belize',
	'CA': 'Canada',
	'CC': 'Cocos (Keeling) Islands',
	'CD': 'Congo - Kinshasa',
	'CF': 'Central African Republic',
	'CG': 'Congo - Brazzaville',
	'CH': 'Switzerland',
	'CI': 'Côte d’Ivoire',
	'CK': 'Cook Islands',
	'CL': 'Chile',
	'CM': 'Cameroon',
	'CN': 'China',
	'CO': 'Colombia',
	'CR': 'Costa Rica',
	'CU': 'Cuba',
	'CV': 'Cape Verde',
	'CW': 'Curaçao',
	'CX': 'Christmas Island',
	'CY': 'Cyprus',
	'CZ': 'Czechia',
	'DE': 'Germany',
	'DJ': 'Djibouti',
	'DK': 'Denmark',
	'DM': 'Dominica',
	'DO': 'Dominican Republic',
	'DZ': 'Algeria',
	'EC': 'Ecuador',
	'EE': 'Estonia',
	'EG': 'Egypt',
	'EH': 'Western Sahara',
	'ER': 'Eritrea',
	'ES': 'Spain',
	'ET': 'Ethiopia',
	'FI': 'Finland',
	'FJ': 'Fiji',
	'FK': 'Falkland Islands',
	'FM': 'Micronesia',
	'FO': 'Faroe Islands',
	'FR': 'France',
	'GA': 'Gabon',
	'GB': 'UK',
	'GD': 'Grenada',
	'GE': 'Georgia',
	'GF': 'French Guiana',
	'GG': 'Guernsey',
	'GH': 'Ghana',
	'GI': 'Gibraltar',
	'GL': 'Greenland',
	'GM': 'Gambia',
	'GN': 'Guinea',
	'GP': 'Guadeloupe',
	'GQ': 'Equatorial Guinea',
	'GR': 'Greece',
	'GS': 'South Georgia & South Sandwich Islands',
	'GT': 'Guatemala',
	'GU': 'Guam',
	'GW': 'Guinea-Bissau',
	'GY': 'Guyana',
	'HK': 'Hong Kong',
	'HM': 'Heard & McDonald Islands',
	'HN': 'Honduras',
	'HR': 'Croatia',
	'HT': 'Haiti',
	'HU': 'Hungary',
	'ID': 'Indonesia',
	'IE': 'Ireland',
	'IL': 'Israel',
	'IM': 'Isle of Man',
	'IN': 'India',
	'IO': 'British Indian Ocean Territory',
	'IQ': 'Iraq',
	'IR': 'Iran',
	'IS': 'Iceland',
	'IT': 'Italy',
	'JE': 'Jersey',
	'JM': 'Jamaica',
	'JO': 'Jordan',
	'JP': 'Japan',
	'KE': 'Kenya',
	'KG': 'Kyrgyzstan',
	'KH': 'Cambodia',
	'KI': 'Kiribati',
	'KM': 'Comoros',
	'KN': 'St. Kitts & Nevis',
	'KP': 'North Korea',
	'KR': 'South Korea',
	'KW': 'Kuwait',
	'KY': 'Cayman Islands',
	'KZ': 'Kazakhstan',
	'LA': 'Laos',
	'LB': 'Lebanon',
	'LC': 'St. Lucia',
	'LI': 'Liechtenstein',
	'LK': 'Sri Lanka',
	'LR': 'Liberia',
	'LS': 'Lesotho',
	'LT': 'Lithuania',
	'LU': 'Luxembourg',
	'LV': 'Latvia',
	'LY': 'Libya',
	'MA': 'Morocco',
	'MC': 'Monaco',
	'MD': 'Moldova',
	'ME': 'Montenegro',
	'MF': 'St. Martin',
	'MG': 'Madagascar',
	'MH': 'Marshall Islands',
	'MK': 'Macedonia',
	'ML': 'Mali',
	'MM': 'Myanmar',
	'MN': 'Mongolia',
	'MO': 'Macau',
	'MP': 'Northern Mariana Islands',
	'MQ': 'Martinique',
	'MR': 'Mauritania',
	'MS': 'Montserrat',
	'MT': 'Malta',
	'MU': 'Mauritius',
	'MV': 'Maldives',
	'MW': 'Malawi',
	'MX': 'Mexico',
	'MY': 'Malaysia',
	'MZ': 'Mozambique',
	'NA': 'Namibia',
	'NC': 'New Caledonia',
	'NE': 'Niger',
	'NF': 'Norfolk Island',
	'NG': 'Nigeria',
	'NI': 'Nicaragua',
	'NL': 'Netherlands',
	'NO': 'Norway',
	'NP': 'Nepal',
	'NR': 'Nauru',
	'NU': 'Niue',
	'NZ': 'New Zealand',
	'OM': 'Oman',
	'PA': 'Panama',
	'PE': 'Peru',
	'PF': 'French Polynesia',
	'PG': 'Papua New Guinea',
	'PH': 'Philippines',
	'PK': 'Pakistan',
	'PL': 'Poland',
	'PM': 'St. Pierre & Miquelon',
	'PN': 'Pitcairn Islands',
	'PR': 'Puerto Rico',
	'PS': 'Palestine',
	'PT': 'Portugal',
	'PW': 'Palau',
	'PY': 'Paraguay',
	'QA': 'Qatar',
	'RE': 'Réunion',
	'RO': 'Romania',
	'RS': 'Serbia',
	'RU': 'Russia',
	'RW': 'Rwanda',
	'SA': 'Saudi Arabia',
	'SB': 'Solomon Islands',
	'SC': 'Seychelles',
	'SD': 'Sudan',
	'SE': 'Sweden',
	'SG': 'Singapore',
	'SH': 'St. Helena',
	'SI': 'Slovenia',
	'SJ': 'Svalbard & Jan Mayen',
	'SK': 'Slovakia',
	'SL': 'Sierra Leone',
	'SM': 'San Marino',
	'SN': 'Senegal',
	'SO': 'Somalia',
	'SR': 'Suriname',
	'SS': 'South Sudan',
	'ST': 'São Tomé & Príncipe',
	'SV': 'El Salvador',
	'SX': 'Sint Maarten',
	'SY': 'Syria',
	'SZ': 'Swaziland',
	'TC': 'Turks & Caicos Islands',
	'TD': 'Chad',
	'TF': 'French Southern Territories',
	'TG': 'Togo',
	'TH': 'Thailand',
	'TJ': 'Tajikistan',
	'TK': 'Tokelau',
	'TL': 'Timor-Leste',
	'TM': 'Turkmenistan',
	'TN': 'Tunisia',
	'TO': 'Tonga',
	'TR': 'Turkey',
	'TT': 'Trinidad & Tobago',
	'TV': 'Tuvalu',
	'TW': 'Taiwan',
	'TZ': 'Tanzania',
	'UA': 'Ukraine',
	'UG': 'Uganda',
	'UM': 'U.S. Outlying Islands',
	'US': 'USA',
	'UY': 'Uruguay',
	'UZ': 'Uzbekistan',
	'VA': 'Vatican City',
	'VC': 'St. Vincent & Grenadines',
	'VE': 'Venezuela',
	'VG': 'British Virgin Islands',
	'VI': 'U.S. Virgin Islands',
	'VN': 'Vietnam',
	'VU': 'Vanuatu',
	'WF': 'Wallis & Futuna',
	'WS': 'Samoa',
	'YE': 'Yemen',
	'YT': 'Mayotte',
	'ZA': 'South Africa',
	'ZM': 'Zambia',
	'ZW': 'Zimbabwe',
	'GB-SCT': 'Scotland',
	'GB-ENG': 'England',
	'GB-NIR': 'Northern Ireland',
	'GB-WLS': 'Wales',
	'XK': 'Kosovo',
}

continent_names = {
	'AF': 'Africa',
	'AN': 'Antarctica',
	'AS': 'Asia',
	'EU': 'Europe',
	'NA': 'North America',
	'SA': 'South America',
	'OC': 'Oceania',
}

country_coordinates = {
	'AD': (42.5, 1.6),
	'AE': (24.0, 54.0),
	'AF': (33.0, 65.0),
	'AG': (17.05, -61.8),
	'AI': (18.25, -63.1667),
	'AL': (41.0, 20.0),
	'AM': (40.0, 45.0),
	'AN': (12.25, -68.75),
	'AO': (-12.5, 18.5),
	'AQ': (-90.0, 0.0),
	'AR': (-34.0, -64.0),
	'AS': (-14.3333, -170.0),
	'AT': (47.3333, 13.3333),
	'AU': (-27.0, 133.0),
	'AW': (12.5, -69.9667),
	'AX': (60.29, 20.09),
	'AZ': (40.5, 47.5),
	'BA': (44.0, 18.0),
	'BB': (13.1667, -59.5333),
	'BD': (24.0, 90.0),
	'BE': (50.8333, 4.0),
	'BF': (13.0, -2.0),
	'BG': (43.0, 25.0),
	'BH': (26.0, 50.55),
	'BI': (-3.5, 30.0),
	'BJ': (9.5, 2.25),
	'BM': (32.3333, -64.75),
	'BN': (4.5, 114.6667),
	'BO': (-17.0, -65.0),
	'BR': (-10.0, -55.0),
	'BS': (24.25, -76.0),
	'BT': (27.5, 90.5),
	'BV': (-54.4333, 3.4),
	'BW': (-22.0, 24.0),
	'BY': (53.0, 28.0),
	'BZ': (17.25, -88.75),
	'CA': (60.0, -95.0),
	'CC': (-12.5, 96.8333),
	'CD': (0.0, 25.0),
	'CF': (7.0, 21.0),
	'CG': (-1.0, 15.0),
	'CH': (47.0, 8.0),
	'CI': (8.0, -5.0),
	'CK': (-21.2333, -159.7667),
	'CL': (-30.0, -71.0),
	'CM': (6.0, 12.0),
	'CN': (35.0, 105.0),
	'CO': (4.0, -72.0),
	'CR': (10.0, -84.0),
	'CU': (21.5, -80.0),
	'CV': (16.0, -24.0),
	'CW': (12.1836, -68.9663),
	'CX': (-10.5, 105.6667),
	'CY': (35.0, 33.0),
	'CZ': (49.75, 15.5),
	'DE': (51.0, 9.0),
	'DJ': (11.5, 43.0),
	'DK': (56.0, 10.0),
	'DM': (15.4167, -61.3333),
	'DO': (19.0, -70.6667),
	'DZ': (28.0, 3.0),
	'EC': (-2.0, -77.5),
	'EE': (59.0, 26.0),
	'EG': (27.0, 30.0),
	'EH': (24.5, -13.0),
	'ER': (15.0, 39.0),
	'ES': (40.0, -4.0),
	'ET': (8.0, 38.0),
	'FI': (64.0, 26.0),
	'FJ': (-18.0, 175.0),
	'FK': (-51.75, -59.0),
	'FM': (6.9167, 158.25),
	'FO': (62.0, -7.0),
	'FR': (46.0, 2.0),
	'GA': (-1.0, 11.75),
	'GB': (54.0, -2.0),
	'GB-ENG': (52, -1),
	'GB-NIR': (54, -6),
	'GB-SCT': (56, -4),
	'GB-WLS': (51, -4),
	'GD': (12.1167, -61.6667),
	'GE': (42.0, 43.5),
	'GF': (4.0, -53.0),
	'GG': (49.5, -2.56),
	'GH': (8.0, -2.0),
	'GI': (36.1833, -5.3667),
	'GL': (72.0, -40.0),
	'GM': (13.4667, -16.5667),
	'GN': (11.0, -10.0),
	'GP': (16.25, -61.5833),
	'GQ': (2.0, 10.0),
	'GR': (39.0, 22.0),
	'GS': (-54.5, -37.0),
	'GT': (15.5, -90.25),
	'GU': (13.4667, 144.7833),
	'GW': (12.0, -15.0),
	'GY': (5.0, -59.0),
	'HK': (22.25, 114.1667),
	'HM': (-53.1, 72.5167),
	'HN': (15.0, -86.5),
	'HR': (45.1667, 15.5),
	'HT': (19.0, -72.4167),
	'HU': (47.0, 20.0),
	'ID': (-5.0, 120.0),
	'IE': (53.0, -8.0),
	'IL': (31.5, 34.75),
	'IM': (54.23, -4.55),
	'IN': (20.0, 77.0),
	'IO': (-6.0, 71.5),
	'IQ': (33.0, 44.0),
	'IR': (32.0, 53.0),
	'IS': (65.0, -18.0),
	'IT': (42.8333, 12.8333),
	'JE': (49.21, -2.13),
	'JM': (18.25, -77.5),
	'JO': (31.0, 36.0),
	'JP': (36.0, 138.0),
	'KE': (1.0, 38.0),
	'KG': (41.0, 75.0),
	'KH': (13.0, 105.0),
	'KI': (1.4167, 173.0),
	'KM': (-12.1667, 44.25),
	'KN': (17.3333, -62.75),
	'KP': (40.0, 127.0),
	'KR': (37.0, 127.5),
	'KW': (29.3375, 47.6581),
	'KY': (19.5, -80.5),
	'KZ': (48.0, 68.0),
	'LA': (18.0, 105.0),
	'LB': (33.8333, 35.8333),
	'LC': (13.8833, -61.1333),
	'LI': (47.1667, 9.5333),
	'LK': (7.0, 81.0),
	'LR': (6.5, -9.5),
	'LS': (-29.5, 28.5),
	'LT': (56.0, 24.0),
	'LU': (49.75, 6.1667),
	'LV': (57.0, 25.0),
	'LY': (25.0, 17.0),
	'MA': (32.0, -5.0),
	'MC': (43.7333, 7.4),
	'MD': (47.0, 29.0),
	'ME': (42.0, 19.0),
	'MG': (-20.0, 47.0),
	'MH': (9.0, 168.0),
	'MK': (41.8333, 22.0),
	'ML': (17.0, -4.0),
	'MM': (22.0, 98.0),
	'MN': (46.0, 105.0),
	'MO': (22.1667, 113.55),
	'MP': (15.2, 145.75),
	'MQ': (14.6667, -61.0),
	'MR': (20.0, -12.0),
	'MS': (16.75, -62.2),
	'MT': (35.8333, 14.5833),
	'MU': (-20.2833, 57.55),
	'MV': (3.25, 73.0),
	'MW': (-13.5, 34.0),
	'MX': (23.0, -102.0),
	'MY': (2.5, 112.5),
	'MZ': (-18.25, 35.0),
	'NA': (-22.0, 17.0),
	'NC': (-21.5, 165.5),
	'NE': (16.0, 8.0),
	'NF': (-29.0333, 167.95),
	'NG': (10.0, 8.0),
	'NI': (13.0, -85.0),
	'NL': (52.5, 5.75),
	'NO': (62.0, 10.0),
	'NP': (28.0, 84.0),
	'NR': (-0.5333, 166.9167),
	'NU': (-19.0333, -169.8667),
	'NZ': (-41.0, 174.0),
	'OM': (21.0, 57.0),
	'PA': (9.0, -80.0),
	'PE': (-10.0, -76.0),
	'PF': (-15.0, -140.0),
	'PG': (-6.0, 147.0),
	'PH': (13.0, 122.0),
	'PK': (30.0, 70.0),
	'PL': (52.0, 20.0),
	'PM': (46.8333, -56.3333),
	'PN': (-24.7, -127.4),
	'PR': (18.25, -66.5),
	'PS': (32.0, 35.25),
	'PT': (39.5, -8.0),
	'PW': (7.5, 134.5),
	'PY': (-23.0, -58.0),
	'QA': (25.5, 51.25),
	'RE': (-21.1, 55.6),
	'RO': (46.0, 25.0),
	'RS': (44.0, 21.0),
	'RU': (60.0, 100.0),
	'RW': (-2.0, 30.0),
	'SA': (25.0, 45.0),
	'SB': (-8.0, 159.0),
	'SC': (-4.5833, 55.6667),
	'SD': (15.0, 30.0),
	'SE': (62.0, 15.0),
	'SG': (1.3667, 103.8),
	'SH': (-15.9333, -5.7),
	'SI': (46.0, 15.0),
	'SJ': (78.0, 20.0),
	'SK': (48.6667, 19.5),
	'SL': (8.5, -11.5),
	'SM': (43.7667, 12.4167),
	'SN': (14.0, -14.0),
	'SO': (10.0, 49.0),
	'SR': (4.0, -56.0),
	'SS': (8.0, 30.0),
	'ST': (1.0, 7.0),
	'SV': (13.8333, -88.9167),
	'SX': (18.0436, -63.0528),
	'SY': (35.0, 38.0),
	'SZ': (-26.5, 31.5),
	'TC': (21.75, -71.5833),
	'TD': (15.0, 19.0),
	'TF': (-43.0, 67.0),
	'TG': (8.0, 1.1667),
	'TH': (15.0, 100.0),
	'TJ': (39.0, 71.0),
	'TK': (-9.0, -172.0),
	'TL': (-8.55, 125.5167),
	'TM': (40.0, 60.0),
	'TN': (34.0, 9.0),
	'TO': (-20.0, -175.0),
	'TR': (39.0, 35.0),
	'TT': (11.0, -61.0),
	'TV': (-8.0, 178.0),
	'TW': (23.5, 121.0),
	'TZ': (-6.0, 35.0),
	'UA': (49.0, 32.0),
	'UG': (1.0, 32.0),
	'UM': (19.2833, 166.6),
	'US': (38.0, -97.0),
	'UY': (-33.0, -56.0),
	'UZ': (41.0, 64.0),
	'VA': (41.9, 12.45),
	'VC': (13.25, -61.2),
	'VE': (8.0, -66.0),
	'VG': (18.5, -64.5),
	'VI': (18.3333, -64.8333),
	'VN': (16.0, 106.0),
	'VU': (-16.0, 167.0),
	'WF': (-13.3, -176.2),
	'WS': (-13.5833, -172.3333),
	'XK': (42.611, 20.83),
	'YE': (15.0, 48.0),
	'YT': (-12.8333, 45.1667),
	'ZA': (-29.0, 24.0),
	'ZM': (-15.0, 30.0),
	'ZW': (-20.0, 30.0)
}

class Country(object):
	def __init__(self, callsign):
		callsign = callsign.upper()
		while callsign:
			if callsign in prefix_to_country:
				self.iso, continent_abbr = prefix_to_country[callsign]
			callsign = callsign[:-1]
		self.name = country_names[self.iso]
		self.continent = continent_names[continent_abbr]
		self.lat, self.lon = country_coordinates[self.iso]

	def __repr__(self):
		return "<Country: '%s'>" % self

	def __str__(self):
		return "%s, %s" % (self.name, self.continent)

	def translate(self, t):
		# little hack to allow pymysql to treat this like a str
		return self.callsign.translate(t)

class Callsign(object):
	def __init__(self, callsign):
		self.callsign = callsign.upper()
		self.plain_callsign = self.callsign

		suffix_regex = r"/(MM|AM|M|P)$"
		sm = re.search(suffix_regex, self.callsign)
		if sm:
			self.suffix = sm.group(0).replace('/', '')
		else:
			self.suffix = None
		callsign_without_suffix = re.sub(suffix_regex, '', self.callsign)

		if '/' in callsign_without_suffix:
			self.int_prefix = callsign_without_suffix.split('/')[0]
			self.plain_callsign = callsign_without_suffix.split('/')[1]
			self.roaming_country = Country(self.int_prefix)
		else:
			self.plain_callsign = callsign_without_suffix
			self.int_prefix = None
			self.roaming_country = None
		self.country = Country(self.plain_callsign)

	def __repr__(self):
		return "<Callsign: '%s'>" % self.callsign

	def __str__(self):
		return self.callsign

	def translate(self, t):
		# little hack to allow pymysql to treat this like a str
		return self.callsign.translate(t)
