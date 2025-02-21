from django import forms
from .models import DeceasedEntry, DeceasedCodes, ICDCode


class DateInput(forms.DateInput):

    input_type = 'date'


class DeceasedEntryForm(forms.ModelForm):

    class Meta:
        model = DeceasedEntry

        states = (("-----", "-----"), ("ALABAMA", "ALABAMA"),
    ("ALASKA", "ALASKA"),
    ("ARIZONA", "ARIZONA"),
    ("ARKANSAS", "ARKANSAS"),
    ("CALIFORNIA", "CALIFORNIA"),
    ("COLORADO", "COLORADO"),
    ("CONNECTICUT", "CONNECTICUT"),
    ("DELAWARE", "DELAWARE"),
    ("FLORIDA", "FLORIDA"),
    ("GEORGIA", "GEORGIA"),
    ("HAWAII", "HAWAII"),
    ("IDAHO", "IDAHO"),
    ("ILLINOIS", "ILLINOIS"),
    ("INDIANA", "INDIANA"),
    ("IOWA", "IOWA"),
    ("KANSAS", "KANSAS"),
    ("KENTUCKY", "KENTUCKY"),
    ("LOUISIANA", "LOUISIANA"),
    ("MAINE", "MAINE"),
    ("MARYLAND", "MARYLAND"),
    ("MASSACHUSETTS", "MASSACHUSETTS"),
    ("MICHIGAN", "MICHIGAN"),
    ("MINNESOTA", "MINNESOTA"),
    ("MISSISSIPPI", "MISSISSIPPI"),
    ("MISSOURI", "MISSOURI"),
    ("MONTANA", "MONTANA"),
    ("NEBRASKA", "NEBRASKA"),
    ("NEVADA", "NEVADA"),
    ("NEW HAMPSHIRE", "NEW HAMPSHIRE"),
    ("NEW JERSEY", "NEW JERSEY"),
    ("NEW MEXICO", "NEW MEXICO"),
    ("NEW YORK", "NEW YORK"),
    ("NORTH CAROLINA", "NORTH CAROLINA"),
    ("NORTH DAKOTA", "NORTH DAKOTA"),
    ("OHIO", "OHIO"),
    ("OKLAHOMA", "OKLAHOMA"),
    ("OREGON", "OREGON"),
    ("PENNSYLVANIA", "PENNSYLVANIA"),
    ("RHODE ISLAND", "RHODE ISLAND"),
    ("SOUTH CAROLINA", "SOUTH CAROLINA"),
    ("SOUTH DAKOTA", "SOUTH DAKOTA"),
    ("TENNESSEE", "TENNESSEE"),
    ("TEXAS", "TEXAS"),
    ("UTAH", "UTAH"),
    ("VERMONT", "VERMONT"),
    ("VIRGINIA", "VIRGINIA"),
    ("WASHINGTON", "WASHINGTON"),
    ("WEST VIRGINIA", "WEST VIRGINIA"),
    ("WISCONSIN", "WISCONSIN"),
    ("WYOMING", "WYOMING"))

        races = (("-----", "-----"), ("BLACK, NOT OF HISPANIC ORIGIN", "BLACK, NOT OF HISPANIC ORIGIN"),
    ("BLACK OR AFRICAN AMERICAN", "BLACK OR AFRICAN AMERICAN"),
    ("AFGHANISTANI", "AFGHANISTANI"),
    ("ISRAELI", "ISRAELI"),
    ("ARAB", "ARAB"),
    ("OTHER RACE", "OTHER RACE"),
    ("DECLINED TO ANSWER", "DECLINED TO ANSWER"),
    ("NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER", "NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER"),
    ("UNKNOWN BY PATIENT", "UNKNOWN BY PATIENT"),
    ("WHITE", "WHITE"),
    ("ASIAN INDIAN", "ASIAN INDIAN"),
    ("BANGLADESHI", "BANGLADESHI"),
    ("BHUTANESE", "BHUTANESE"),
    ("BURMESE", "BURMESE"),
    ("CAMBODIAN", "CAMBODIAN"),
    ("AMERICAN INDIAN OR ALASKA NATIVE", "AMERICAN INDIAN OR ALASKA NATIVE"),
    ("CHINESE", "CHINESE"),
    ("TAIWANESE", "TAIWANESE"),
    ("FILIPINO", "FILIPINO"),
    ("HMONG", "HMONG"),
    ("INDONESIAN", "INDONESIAN"),
    ("JAPANESE", "JAPANESE"),
    ("KOREAN", "KOREAN"),
    ("LAOTIAN", "LAOTIAN"),
    ("MALAYSIAN", "MALAYSIAN"),
    ("OKINAWAN", "OKINAWAN"),
    ("WHITE, NOT OF HISPANIC ORIGIN", "WHITE, NOT OF HISPANIC ORIGIN"),
    ("PAKISTANI", "PAKISTANI"),
    ("SRI LANKAN", "SRI LANKAN"),
    ("THAI", "THAI"),
    ("VIETNAMESE", "VIETNAMESE"),
    ("IWO JIMAN", "IWO JIMAN"),
    ("MALDIVIAN", "MALDIVIAN"),
    ("NEPALESE", "NEPALESE"),
    ("SINGAPOREAN", "SINGAPOREAN"),
    ("MADAGASCAR", "MADAGASCAR"),
    ("BLACK", "BLACK"),
    ("HISPANIC, WHITE", "HISPANIC, WHITE"),
    ("AFRICAN AMERICAN", "AFRICAN AMERICAN"),
    ("AFRICAN", "AFRICAN"),
    ("BOTSWANAN", "BOTSWANAN"),
    ("ETHIOPIAN", "ETHIOPIAN"),
    ("LIBERIAN", "LIBERIAN"),
    ("NAMIBIAN", "NAMIBIAN"),
    ("NIGERIAN", "NIGERIAN"),
    ("ZAIREAN", "ZAIREAN"),
    ("BAHAMIAN", "BAHAMIAN"),
    ("BARBADIAN", "BARBADIAN"),
    ("ASIAN OR PACIFIC ISLANDER", "ASIAN OR PACIFIC ISLANDER"),
    ("DOMINICAN", "DOMINICAN"),
    ("DOMINICA ISLANDER", "DOMINICA ISLANDER"),
    ("HAITIAN", "HAITIAN"),
    ("JAMAICAN", "JAMAICAN"),
    ("TOBAGOAN", "TOBAGOAN"),
    ("TRINIDADIAN", "TRINIDADIAN"),
    ("WEST INDIAN", "WEST INDIAN"),
    ("POLYNESIAN", "POLYNESIAN"),
    ("NATIVE HAWAIIAN", "NATIVE HAWAIIAN"),
    ("SAMOAN", "SAMOAN"),
    ("HISPANIC, BLACK", "HISPANIC, BLACK"),
    ("TAHITIAN", "TAHITIAN"),
    ("TONGAN", "TONGAN"),
    ("TOKELAUAN", "TOKELAUAN"),
    ("MICRONESIAN", "MICRONESIAN"),
    ("GUAMANIAN OR CHAMORRO", "GUAMANIAN OR CHAMORRO"),
    ("GUAMANIAN", "GUAMANIAN"),
    ("CHAMORRO", "CHAMORRO"),
    ("MARIANA ISLANDER", "MARIANA ISLANDER"),
    ("MARSHALLESE", "MARSHALLESE"),
    ("PALAUAN", "PALAUAN"),
    ("UNKNOWN", "UNKNOWN"),
    ("CAROLINIAN", "CAROLINIAN"),
    ("KOSRAEAN", "KOSRAEAN"),
    ("POHNPEIAN", "POHNPEIAN"),
    ("SAIPANESE", "SAIPANESE"),
    ("KIRIBATI", "KIRIBATI"),
    ("CHUUKESE", "CHUUKESE"),
    ("YAPESE", "YAPESE"),
    ("MELANESIAN", "MELANESIAN"),
    ("FIJIAN", "FIJIAN"),
    ("PAPUA NEW GUINEAN", "PAPUA NEW GUINEAN"),
    ("AMERICAN INDIAN OR ALASKA NATIVE-OLD", "AMERICAN INDIAN OR ALASKA NATIVE-OLD"),
    ("SOLOMON ISLANDER", "SOLOMON ISLANDER"),
    ("NEW HEBRIDES", "NEW HEBRIDES"),
    ("OTHER PACIFIC ISLANDER", "OTHER PACIFIC ISLANDER"),
    ("EUROPEAN", "EUROPEAN"),
    ("ARMENIAN", "ARMENIAN"),
    ("ENGLISH", "ENGLISH"),
    ("FRENCH", "FRENCH"),
    ("GERMAN", "GERMAN"),
    ("IRISH", "IRISH"),
    ("ITALIAN", "ITALIAN"),
    ("ASIAN", "ASIAN"),
    ("POLISH", "POLISH"),
    ("SCOTTISH", "SCOTTISH"),
    ("MIDDLE EASTERN OR NORTH AFRICAN", "MIDDLE EASTERN OR NORTH AFRICAN"),
    ("ASSYRIAN", "ASSYRIAN"),
    ("EGYPTIAN", "EGYPTIAN"),
    ("IRANIAN", "IRANIAN"),
    ("IRAQI", "IRAQI"),
    ("LEBANESE", "LEBANESE"),
    ("PALESTINIAN", "PALESTINIAN"),
    ("SYRIAN", "SYRIAN"))

        manners_of_death = (("-----", "-----"), ('Natural Causes', 'Natural Causes'), ('Accident', 'Accident'), ('Suicide', 'Suicide'),
                            ('Homicide', 'Homicide'), ('Pending Investigation', 'Pending Investigation'),
                            ('Could not be determined', 'Could not be determined'))

        places_of_death = (("-----", "-----"), ('Inpatient', 'Inpatient'), ('ER/Outpatient', 'ER/Outpatient'),
                           ('Dead on Arrival', 'Dead on Arrival'), ('Nursing Home', 'Nursing Home'),
                           ('Residence', 'Residence'), ('Other', 'Other'))

        methods_of_verification = (("-----", "-----"), ('Family', 'Family'), ('Newspaper Obituary', 'Newspaper Obituary'),
                                   ('Funeral Home', 'Funeral Home'), ('Death Certificate', 'Death Certificate'),
                                   ('Social Security Death Index', 'Social Security Death Index'), ('Other', 'Other'))

        fields = ('name', 'chart_num', 'dob', 'state_where_died', 'death_cert_num', 'dod', 'place_of_death', 'race',
                  'autopsy_performed', 'manner_of_death', 'death_by_work_injury', 'place_of_injury',
                  'method_of_verification')

        labels = {'name': "Name:", 'chart_num': "Chart Number:", 'dob': "Date of Birth:",
                  'state_where_died': "State where died:", 'death_cert_num': "Death Certificate Number:",
                  'dod': "Date of Death:", 'place_of_death': "Place of Death:", 'race': "Race:",
                  'autopsy_performed': "Was Autopsy Performed:", 'manner_of_death': "Manner of Death:",
                  'death_by_work_injury': "Was Death by Work Injury:", 'place_of_injury': "Place of Injury",
                  'method_of_verification': "Method of Verification:"}

        widgets = {
            'state_where_died': forms.Select(choices=states),
            'race': forms.Select(choices=races),
            'dob': DateInput(),
            'dod': DateInput(),
            'autopsy_performed': forms.Select(choices=((True, 'Yes'), (False, 'No'))),
            'death_by_work_injury': forms.Select(choices=((True, 'Yes'), (False, 'No'))),
            'method_of_verification': forms.Select(choices=methods_of_verification),
            'manner_of_death': forms.Select(choices=manners_of_death),
            'place_of_death': forms.Select(choices=places_of_death),
        }


class NewCodeForm(forms.ModelForm):
    class Meta:
        model = DeceasedCodes

        fields = ('code_id', 'is_primary')
        labels = {'code_id': 'ICD Code:', 'is_primary': 'Is Primary Cause of Death?'}


class NewICDCodeForm(forms.ModelForm):
    class Meta:
        model = ICDCode

        fields = ('code', 'description')
        labels = {'code': 'ICD Code', 'description': 'Code Description'}
