mubasshir = [
    'Mubasshir', 'Mub', 'hackermub', 'Md', 'Chowdhury', 'mub.ch'
]

shafin = [
    'Shafin', 'Shafin Alam', 'ShafinAlam', 'ShafinAlam_', 'ShafinAlam_', '_blaNk'
]

ahnaf = [
    'Ahnaf', 'Ahnaf Shahriar Asif', 'Ahnaf.Shahriar.Asif', 'AhnafShahriarAsif', 'Asif', 'shahriar', 'asep'
]

def ahnaf_exists(text: str) -> bool:
    text = text.lower()
    for name in ahnaf:
        if name.lower() in text:
            return True
    return False

def mubasshir_exists(text: str) -> bool:
    text = text.lower()
    for name in mubasshir:
        if name.lower() in text:
            return True
    return False

def shafin_exists(text: str) -> bool:
    text = text.lower()
    for name in shafin:
        if name.lower() in text:
            return True
    return False