# Topic Manager Application

A collaborative topic management application with SQLite database backend, built with Python Tkinter.

## Features

- ✅ Create, edit, and delete topics
- ✅ Add images to topics
- ✅ Search and filter topics
- ✅ Track creation and modification timestamps with user names
- ✅ Shared SQLite database for team collaboration
- ✅ Clean, functional interface

## Requirements

- Python 3.8 or higher
- Pillow (for image handling)
- PyInstaller (for creating executable)

## Installation for Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python topic_manager.py
```

## Building Executable with PyInstaller

### Option 1: Simple Build (One File)
Creates a single executable file (slower startup, but easier to distribute):

```bash
pyinstaller --onefile --windowed --name TopicManager topic_manager.py
```

### Option 2: Folder Build (Recommended)
Creates a folder with the executable and dependencies (faster startup):

```bash
pyinstaller --onedir --windowed --name TopicManager topic_manager.py
```

### Option 3: Custom Build with Icon (if you have an .ico file)

```bash
pyinstaller --onedir --windowed --name TopicManager --icon=app_icon.ico topic_manager.py
```

The executable will be created in the `dist` folder.

## Deploying to Shared Drive

### Step 1: Configure Database Path

Before building with PyInstaller, edit `topic_manager.py` and modify the database path:

```python
# Find this line in the main() function (near the bottom):
db_path = os.path.join(os.path.dirname(__file__), "topics.db")

# Replace with your shared drive path, for example:
db_path = r"\\YourServer\SharedDrive\TopicManager\topics.db"
# OR on mapped drive:
db_path = r"Z:\TopicManager\topics.db"
```

### Step 2: Build the Executable

Run one of the PyInstaller commands above.

### Step 3: Deploy

1. Copy the entire `dist/TopicManager` folder to a location accessible by all users
2. Ensure the database path specified in the code is accessible to all users
3. Users can create a shortcut to `TopicManager.exe` on their desktops

### Important Notes for Shared Database:

- **Network permissions**: Ensure all users have read/write access to the database location
- **SQLite limitations**: SQLite works well for small teams (< 10 concurrent users). For larger teams, consider migrating to PostgreSQL/MySQL
- **File locking**: Only one user can write to SQLite at a time. The app handles this gracefully, but be aware of potential brief delays during concurrent edits

## Usage

### Adding a Topic
1. Click "Add Topic" button
2. Enter your name, topic title, and body
3. Click "Create Topic"

### Editing a Topic
1. Select a topic from the list
2. Click "Edit Topic" button
3. Enter your name and modify title/body
4. Click "Save Changes"

### Adding Images
1. Select a topic
2. Click "Add Image" button
3. Choose an image file
4. Click to view full-size, or delete unwanted images

### Searching Topics
- Type in the search bar to filter topics by title or content

## Switching to CustomTkinter (for modern look)

If you want a more modern appearance, you can easily switch to CustomTkinter:

1. Install CustomTkinter:
```bash
pip install customtkinter
```

2. In `topic_manager.py`, replace imports:
```python
# Change:
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# To:
import customtkinter as ctk
ctk.set_appearance_mode("System")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"
```

3. Replace widget names (find and replace):
- `tk.Frame` → `ctk.CTkFrame`
- `tk.Button` → `ctk.CTkButton`
- `tk.Label` → `ctk.CTkLabel`
- `tk.Entry` → `ctk.CTkEntry`
- Keep `tk.Listbox`, `tk.Text`, `tk.Canvas` as-is (CustomTkinter doesn't have direct replacements)

4. Rebuild with PyInstaller

## Troubleshooting

### "Cannot find topics.db"
- Check that the database path in `topic_manager.py` is correct and accessible
- Verify network permissions if using a shared drive

### Images not displaying
- Ensure PIL/Pillow is installed: `pip install Pillow`
- Check that image files are valid formats (jpg, png, gif, bmp)

### PyInstaller build fails
- Try updating PyInstaller: `pip install --upgrade pyinstaller`
- On Windows, you may need to run as administrator
- Check that Python is added to PATH

### App is slow to start
- Use `--onedir` instead of `--onefile` for faster startup
- Consider excluding unnecessary modules with `--exclude-module`

## Support

For issues or questions, contact your IT administrator or the application developer.
