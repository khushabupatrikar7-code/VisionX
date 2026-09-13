import argostranslate.package

print("Fetching available language packages...")
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()

languages = set()
for pkg in available_packages:
    languages.add((pkg.from_code, pkg.from_name))
    languages.add((pkg.to_code, pkg.to_name))

print("\nAvailable languages:")
for code, name in sorted(languages, key=lambda x: x[1]):
    print(f"  {code}: {name}")