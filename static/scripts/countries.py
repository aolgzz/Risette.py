#===================================================================#
#                                                                   #
#    A script that displays the country name and flag               #
#    according to the initials of the country.                      #
#                                                                   #
#-------------------------------------------------------------------#
#                                                                   #
#    Arturo Olivares                                                #
#                                                                   #
#   Copyright (C) 2023 Arturo Olivares                              #
#   GNU GPLv3                                                       #
#                                                                   #
#===================================================================#

from browser import document

countries = {
  "DZ": {"name": "Algeria", "flag": "🇩🇿"},
  "AR": {"name": "Argentina", "flag": "🇦🇷"},
  "AU": {"name": "Australia", "flag": "🇦🇺"},
  "AT": {"name": "Austria", "flag": "🇦🇹"},
  "AZ": {"name": "Azerbaijan", "flag": "🇦🇿"},
  "BH": {"name": "Bahrain", "flag": "🇧🇭"},
  "BD": {"name": "Bangladesh", "flag": "🇧🇩"},
  "BY": {"name": "Belarus", "flag": "🇧🇾"},
  "BE": {"name": "Belgium", "flag": "🇧🇪"},
  "BO": {"name": "Bolivia", "flag": "🇧🇴"},
  "BA": {"name": "Bosnia and Herzegovina", "flag": "🇧🇦"},
  "BR": {"name": "Brazil", "flag": "🇧🇷"},
  "BG": {"name": "Bulgaria", "flag": "🇧🇬"},
  "KH": {"name": "Cambodia", "flag": "🇰🇭"},
  "CA": {"name": "Canada", "flag": "🇨🇦"},
  "CL": {"name": "Chile", "flag": "🇨🇱"},
  "CO": {"name": "Colombia", "flag": "🇨🇴"},
  "CR": {"name": "Costa Rica", "flag": "🇨🇷"},
  "HR": {"name": "Croatia", "flag": "🇭🇷"},
  "CY": {"name": "Cyprus", "flag": "🇨🇾"},
  "CZ": {"name": "Czechia", "flag": "🇨🇿"},
  "DK": {"name": "Denmark", "flag": "🇩🇰"},
  "DO": {"name": "Dominican Republic", "flag": "🇩🇴"},
  "EC": {"name": "Ecuador", "flag": "🇪🇨"},
  "EG": {"name": "Egypt", "flag": "🇪🇬"},
  "SV": {"name": "El Salvador", "flag": "🇸🇻"},
  "EE": {"name": "Estonia", "flag": "🇪🇪"},
  "FI": {"name": "Finland", "flag": "🇫🇮"},
  "FR": {"name": "France", "flag": "🇫🇷"},
  "GE": {"name": "Georgia", "flag": "🇬🇪"},
  "DE": {"name": "Germany", "flag": "🇩🇪"},
  "DE": {"name": "Germany", "flag": "🇩🇪"},
  "GH": {"name": "Ghana", "flag": "🇬🇭"},
  "GR": {"name": "Greece", "flag": "🇬🇷"},
  "GT": {"name": "Guatemala", "flag": "🇬🇹"},
  "HN": {"name": "Honduras", "flag": "🇭🇳"},
  "HK": {"name": "Hong Kong", "flag": "🇭🇰"},
  "HU": {"name": "Hungary", "flag": "🇭🇺"},
  "IS": {"name": "Iceland", "flag": "🇮🇸"},
  "IN": {"name": "India", "flag": "🇮🇳"},
  "ID": {"name": "Indonesia", "flag": "🇮🇩"},
  "IQ": {"name": "Iraq", "flag": "🇮🇶"},
  "IE": {"name": "Ireland", "flag": "🇮🇪"},
  "IL": {"name": "Israel", "flag": "🇮🇱"},
  "IT": {"name": "Italy", "flag": "🇮🇹"},
  "JM": {"name": "Jamaica", "flag": "🇯🇲"},
  "JP": {"name": "Japan", "flag": "🇯🇵"},
  "JO": {"name": "Jordan", "flag": "🇯🇴"},
  "KZ": {"name": "Kazakhstan", "flag": "🇰🇿"},
  "KE": {"name": "Kenya", "flag": "🇰🇪"},
  "XK": {"name": "Kosovo", "flag": "🇽🇰"},
  "KW": {"name": "Kuwait", "flag": "🇰🇼"},
  "KG": {"name": "Kyrgyzstan", "flag": "🇰🇬"},
  "LA": {"name": "Laos", "flag": "🇱🇦"},
  "LV": {"name": "Latvia", "flag": "🇱🇻"},
  "LB": {"name": "Lebanon", "flag": "🇱🇧"},
  "LY": {"name": "Libya", "flag": "🇱🇾"},
  "LI": {"name": "Liechtenstein", "flag": "🇱🇮"},
  "LT": {"name": "Lithuania", "flag": "🇱🇹"},
  "LU": {"name": "Luxembourg", "flag": "🇱🇺"},
  "MO": {"name": "Macao", "flag": "🇲🇴"},
  "MK": {"name": "North Macedonia", "flag": "🇲🇰"},
  "MG": {"name": "Madagascar", "flag": "🇲🇬"},
  "MY": {"name": "Malaysia", "flag": "🇲🇾"},
    "MT": {"name": "Malta", "flag": "🇲🇹"},
  "MX": {"name": "Mexico", "flag": "🇲🇽"},
  "ME": {"name": "Montenegro", "flag": "🇲🇪"},
  "MA": {"name": "Morocco", "flag": "🇲🇦"},
  "NP": {"name": "Nepal", "flag": "🇳🇵"},
  "NL": {"name": "Netherlands", "flag": "🇳🇱"},
  "NZ": {"name": "New Zealand", "flag": "🇳🇿"},
  "NI": {"name": "Nicaragua", "flag": "🇳🇮"},
  "NG": {"name": "Nigeria", "flag": "🇳🇬"},
  "MK": {"name": "North Macedonia", "flag": "🇲🇰"},
  "NO": {"name": "Norway", "flag": "🇳🇴"},
  "OM": {"name": "Oman", "flag": "🇴🇲"},
  "PK": {"name": "Pakistan", "flag": "🇵🇰"},
  "PA": {"name": "Panama", "flag": "🇵🇦"},
  "PG": {"name": "Papua New Guinea", "flag": "🇵🇬"},
  "PY": {"name": "Paraguay", "flag": "🇵🇾"},
  "PE": {"name": "Peru", "flag": "🇵🇪"},
  "PH": {"name": "Philippines", "flag": "🇵🇭"},
  "PL": {"name": "Poland", "flag": "🇵🇱"},
  "PT": {"name": "Portugal", "flag": "🇵🇹"},
  "PR": {"name": "Puerto Rico", "flag": "🇵🇷"},
  "QA": {"name": "Qatar", "flag": "🇶🇦"},
  "RO": {"name": "Romania", "flag": "🇷🇴"},
  "RU": {"name": "Russia", "flag": "🇷🇺"},
  "SA": {"name": "Saudi Arabia", "flag": "🇸🇦"},
  "SN": {"name": "Senegal", "flag": "🇸🇳"},
  "RS": {"name": "Serbia", "flag": "🇷🇸"},
  "SG": {"name": "Singapore", "flag": "🇸🇬"},
  "SK": {"name": "Slovakia", "flag": "🇸🇰"},
  "SI": {"name": "Slovenia", "flag": "🇸🇮"},
  "ZA": {"name": "South Africa", "flag": "🇿🇦"},
  "KR": {"name": "South Korea", "flag": "🇰🇷"},
  "ES": {"name": "Spain", "flag": "🇪🇸"},
  "LK": {"name": "Sri Lanka", "flag": "🇱🇰"},
  "SE": {"name": "Sweden", "flag": "🇸🇪"},
  "CH": {"name": "Switzerland", "flag": "🇨🇭"},
  "TW": {"name": "Taiwan", "flag": "🇹🇼"},
  "TZ": {"name": "Tanzania", "flag": "🇹🇿"},
  "TH": {"name": "Thailand", "flag": "🇹🇭"},
  "TN": {"name": "Tunisia", "flag": "🇹🇳"},
  "TR": {"name": "Turkey", "flag": "🇹🇷"},
  "UG": {"name": "Uganda", "flag": "🇺🇬"},
  "UA": {"name": "Ukraine", "flag": "🇺🇦"},
  "AE": {"name": "United Arab Emirates", "flag": "🇦🇪"},
  "GB": {"name": "United Kingdom", "flag": "🇬🇧"},
  "US": {"name": "United States", "flag": "🇺🇸"},
  "UY": {"name": "Uruguay", "flag": "🇺🇾"},
  "VE": {"name": "Venezuela", "flag": "🇻🇪"},
  "VN": {"name": "Vietnam", "flag": "🇻🇳"},
  "YE": {"name": "Yemen", "flag": "🇾🇪"},
  "ZW": {"name": "Zimbabwe", "flag": "🇿🇼"}
}

country_element = document["country"]
country_code = country_element.text

country_data = countries.get(country_code)

if country_data:
  country_name = country_data["name"]
  country_flag = country_data["flag"]
  document.getElementById("country").textContent = country_name
  document.getElementById("flag").innerHTML = country_flag