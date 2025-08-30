
import os
import hashlib

def get_file_hash(filepath):
    """Вычисляет SHA-256 хеш файла (по содержимому)."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Читаем файл по частям — чтобы не грузить память
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"⚠️  Ошибка при чтении {filepath}: {e}")
        return None

def main():
    print("🔍 Поиск дубликатов файлов по содержимому")
    print("—" * 50)

    folder = input("📁 Путь к папке для поиска дубликатов: ").strip()
    
    if not os.path.exists(folder):
        print("❌ Папка не найдена.")
        return
    if not os.path.isdir(folder):
        print("❌ Указанный путь — не папка.")
        return

    print("\n🔄 Сканируем файлы...")

    hash_to_files = {}  # словарь: хеш → список путей
    total_files = 0

    for root, _, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if os.path.isfile(filepath):
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hash_to_files.setdefault(file_hash, []).append(filepath)
                    total_files += 1

    # Фильтруем только те хеши, у которых больше одного файла
    duplicates = {h: paths for h, paths in hash_to_files.items() if len(paths) > 1}

    # Результат
    print("—" * 50)
    if duplicates:
        print(f"🚨 Найдено {len(duplicates)} групп дубликатов:")
        print("—" * 50)
        for group_id, (file_hash, paths) in enumerate(duplicates.items(), 1):
           
