import os
import json
from datetime import datetime
from typing import Optional, Dict, Any

class BackupManager:
    def __init__(self, backup_dir: str = "backups"):
        self.backup_dir: str = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)
        self.last_backup_date: Optional[datetime] = None

    def perform_backup(self, user_data: Dict[str, Any], filename: Optional[str] = None) -> Optional[str]:
        backup_filename = filename if filename else f"user_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        try:
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            self.last_backup_date = datetime.now()
            print(f"Backup performed successfully to {backup_path}")
            return backup_path
        except IOError as e:
            print(f"Error performing backup to {backup_path}: {e}")
            return None

    def restore_backup(self, backup_path: str) -> Optional[Dict[str, Any]]:
        if not os.path.exists(backup_path):
            print(f"Backup file not found: {backup_path}")
            return None
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                restored_data = json.load(f)
            print(f"Backup restored successfully from {backup_path}")
            return restored_data
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error restoring backup from {backup_path}: {e}")
            return None
