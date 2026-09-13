import argostranslate.package

print("Fetching available language packages...")
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

# English <-> Hindi (your core Indian-language pair)
# Plus common traveler languages: Spanish, French, German, Japanese, Chinese,korean
wanted_pairs = [
    ("en", "hi"), ("hi", "en"),
    ("en", "es"), ("es", "en"),
    ("en", "fr"), ("fr", "en"),
    ("en", "de"), ("de", "en"),
    ("en", "ja"), ("ja", "en"),
    ("en", "zh"), ("zh", "en"),
    ("en", "ko"), ("ko", "en"),
]

for pkg in available_packages:
    if (pkg.from_code, pkg.to_code) in wanted_pairs:
        print(f"Installing {pkg.from_code} -> {pkg.to_code}...")
        argostranslate.package.install_from_path(pkg.download())

print("Done installing language packages")