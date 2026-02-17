"""
Topic Manager Application
A collaborative topic management tool with SQLite database backend.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, font, colorchooser
import sqlite3
import os
import json
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageTk
import io
import pytz

class RichTextEditor(tk.Frame):
    """Rich text editor with formatting toolbar"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        
        # Create toolbar
        toolbar = tk.Frame(self, bg="#f0f0f0", relief=tk.RAISED, bd=1)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)
        
        # Bold button
        self.bold_btn = tk.Button(toolbar, text="B", font=("Arial", 10, "bold"),
                                  width=3, command=self.toggle_bold)
        self.bold_btn.pack(side=tk.LEFT, padx=2)
        
        # Italic button
        self.italic_btn = tk.Button(toolbar, text="I", font=("Arial", 10, "italic"),
                                    width=3, command=self.toggle_italic)
        self.italic_btn.pack(side=tk.LEFT, padx=2)
        
        # Underline button
        self.underline_btn = tk.Button(toolbar, text="U", font=("Arial", 10, "underline"),
                                       width=3, command=self.toggle_underline)
        self.underline_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Font size
        tk.Label(toolbar, text="Size:", bg="#f0f0f0").pack(side=tk.LEFT, padx=2)
        self.size_var = tk.StringVar(value="11")
        size_combo = ttk.Combobox(toolbar, textvariable=self.size_var, 
                                  values=["8", "9", "10", "11", "12", "14", "16", "18", "20", "24"],
                                  width=5, state="readonly")
        size_combo.pack(side=tk.LEFT, padx=2)
        size_combo.bind('<<ComboboxSelected>>', self.change_font_size)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Text color
        self.color_btn = tk.Button(toolbar, text="Color", width=6, command=self.change_color)
        self.color_btn.pack(side=tk.LEFT, padx=2)
        
        # Bullet point
        self.bullet_btn = tk.Button(toolbar, text="• List", width=6, command=self.insert_bullet)
        self.bullet_btn.pack(side=tk.LEFT, padx=2)
        
        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Clear formatting
        self.clear_btn = tk.Button(toolbar, text="Clear Format", width=10, 
                                   command=self.clear_formatting)
        self.clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(self)
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                           font=("Arial", 11), **kwargs)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)
        
        # Configure tags for formatting
        self.text.tag_configure("bold", font=("Arial", 11, "bold"))
        self.text.tag_configure("italic", font=("Arial", 11, "italic"))
        self.text.tag_configure("underline", font=("Arial", 11, "underline"))
        self.text.tag_configure("bold_italic", font=("Arial", 11, "bold italic"))
        self.text.tag_configure("bold_underline", font=("Arial", 11, "bold underline"))
        self.text.tag_configure("italic_underline", font=("Arial", 11, "italic underline"))
        self.text.tag_configure("bold_italic_underline", font=("Arial", 11, "bold italic underline"))
        
        # Bind keyboard shortcuts
        self.text.bind('<Control-b>', lambda e: self.toggle_bold())
        self.text.bind('<Control-i>', lambda e: self.toggle_italic())
        self.text.bind('<Control-u>', lambda e: self.toggle_underline())
        
        # Track current formatting state
        self.current_tags = set()
    
    def toggle_bold(self):
        """Toggle bold formatting"""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def toggle_italic(self):
        """Toggle italic formatting"""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def toggle_underline(self):
        """Toggle underline formatting"""
        try:
            current_tags = self.text.tag_names("sel.first")
            if "underline" in current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def change_font_size(self, event=None):
        """Change font size for selection"""
        try:
            size = int(self.size_var.get())
            tag_name = f"size_{size}"
            
            # Configure the tag if it doesn't exist
            if tag_name not in self.text.tag_names():
                self.text.tag_configure(tag_name, font=("Arial", size))
            
            # Apply to selection
            self.text.tag_add(tag_name, "sel.first", "sel.last")
        except (tk.TclError, ValueError):
            pass
    
    def change_color(self):
        """Change text color for selection"""
        color = colorchooser.askcolor(title="Choose text color")
        if color[1]:  # color[1] is the hex color
            try:
                tag_name = f"color_{color[1]}"
                if tag_name not in self.text.tag_names():
                    self.text.tag_configure(tag_name, foreground=color[1])
                self.text.tag_add(tag_name, "sel.first", "sel.last")
            except tk.TclError:
                pass
    
    def insert_bullet(self):
        """Insert a bullet point"""
        try:
            self.text.insert(tk.INSERT, "• ")
        except tk.TclError:
            pass
    
    def clear_formatting(self):
        """Clear all formatting from selection"""
        try:
            # Get all tags
            for tag in self.text.tag_names():
                if tag not in ("sel",):
                    self.text.tag_remove(tag, "sel.first", "sel.last")
        except tk.TclError:
            pass
    
    def get_text(self):
        """Get text content"""
        return self.text.get(1.0, tk.END)
    
    def get_formatted_content(self):
        """Get text content with formatting information"""
        import json
        
        text = self.text.get(1.0, tk.END)
        formatting = []
        
        # Get all tags and their ranges
        for tag in self.text.tag_names():
            if tag not in ("sel", ""):
                ranges = self.text.tag_ranges(tag)
                for i in range(0, len(ranges), 2):
                    start = str(ranges[i])
                    end = str(ranges[i+1])
                    formatting.append({
                        'tag': tag,
                        'start': start,
                        'end': end
                    })
        
        return text, json.dumps(formatting)
    
    def set_text(self, text):
        """Set text content"""
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, text)
    
    def set_formatted_content(self, text, formatting_json):
        """Set text content with formatting information"""
        import json
        
        self.text.delete(1.0, tk.END)
        self.text.insert(1.0, text)
        
        if formatting_json:
            try:
                formatting = json.loads(formatting_json)
                for fmt in formatting:
                    tag = fmt['tag']
                    start = fmt['start']
                    end = fmt['end']
                    
                    # Recreate tag configuration if needed
                    if tag.startswith('size_'):
                        size = int(tag.split('_')[1])
                        self.text.tag_configure(tag, font=("Arial", size))
                    elif tag.startswith('color_'):
                        color = tag.replace('color_', '')
                        self.text.tag_configure(tag, foreground=color)
                    
                    self.text.tag_add(tag, start, end)
            except (json.JSONDecodeError, KeyError, ValueError):
                pass
    
    def get_text_widget(self):
        """Get the underlying Text widget for advanced operations"""
        return self.text


class TopicManagerApp:
    def __init__(self, root, db_path):
        self.root = root
        self.root.title("Topic Manager")
        self.root.geometry("1000x700")
        
        self.db_path = db_path
        self.current_topic_id = None
        self.image_references = []  # Keep references to prevent garbage collection
        
        # Initialize database
        self.init_database()
        
        # Create UI
        self.create_widgets()
        
        # Load initial data
        self.refresh_topic_list()
    
    def format_timestamp(self, timestamp_str):
        """Convert UTC timestamp to EST and format it"""
        if not timestamp_str:
            return ""
        
        # Parse the timestamp (SQLite stores in UTC)
        dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        
        # Make it timezone aware (UTC)
        utc = pytz.UTC
        dt = utc.localize(dt)
        
        # Convert to EST
        est = pytz.timezone('America/New_York')
        dt_est = dt.astimezone(est)
        
        # Format it nicely
        return dt_est.strftime('%Y-%m-%d %I:%M %p EST')
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Topics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT,
                body_formatting TEXT,
                created_by TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_by TEXT,
                modified_at TIMESTAMP
            )
        ''')
        
        # Check if body_formatting column exists (for existing databases)
        cursor.execute("PRAGMA table_info(topics)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'body_formatting' not in columns:
            cursor.execute('ALTER TABLE topics ADD COLUMN body_formatting TEXT')
        
        # Images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER NOT NULL,
                image_data BLOB NOT NULL,
                filename TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (topic_id) REFERENCES topics (id) ON DELETE CASCADE
            )
        ''')
        
        # Check if sample topics exist
        cursor.execute('SELECT COUNT(*) FROM topics')
        if cursor.fetchone()[0] == 0:
            # Add sample topics
            sample_topics = [
                ("Welcome to Topic Manager", 
                 "This is a sample topic. You can edit or delete it, and add your own topics.\n\nFeatures:\n- Create and manage topics\n- Add images to topics\n- Search and filter topics\n- Track who created/edited each topic\n- Rich text formatting (bold, italic, colors)",
                 "System"),
                ("Getting Started",
                 "To create a new topic, click the 'Add Topic' button.\n\nYou can:\n1. Add a title and description with rich text formatting\n2. Upload images\n3. Edit existing topics\n4. Delete topics you no longer need\n\nAll changes are tracked with timestamps!",
                 "System")
            ]
            
            for title, body, creator in sample_topics:
                cursor.execute(
                    'INSERT INTO topics (title, body, created_by) VALUES (?, ?, ?)',
                    (title, body, creator)
                )
        
        conn.commit()
        conn.close()
    
    def create_widgets(self):
        """Create the main UI layout"""
        # Main container with two panes
        main_paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Topic list
        left_frame = tk.Frame(main_paned, width=300)
        main_paned.add(left_frame)
        
        # Search bar
        search_frame = tk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_topics())
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Topic list
        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.topic_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.topic_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.topic_listbox.bind('<<ListboxSelect>>', self.on_topic_select)
        scrollbar.config(command=self.topic_listbox.yview)
        
        # Add Topic button
        tk.Button(left_frame, text="Add Topic", command=self.add_topic, 
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(
                     fill=tk.X, padx=5, pady=5)
        
        # Right panel - Topic details
        right_frame = tk.Frame(main_paned)
        main_paned.add(right_frame)
        
        # Topic title and controls
        title_frame = tk.Frame(right_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.title_label = tk.Label(title_frame, text="Select a topic", 
                                    font=("Arial", 16, "bold"), anchor=tk.W)
        self.title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Button frame
        btn_frame = tk.Frame(title_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        self.edit_btn = tk.Button(btn_frame, text="Edit Topic", command=self.edit_topic,
                                  state=tk.DISABLED, bg="#2196F3", fg="white")
        self.edit_btn.pack(side=tk.LEFT, padx=2)
        
        self.delete_btn = tk.Button(btn_frame, text="Delete Topic", command=self.delete_topic,
                                    state=tk.DISABLED, bg="#f44336", fg="white")
        self.delete_btn.pack(side=tk.LEFT, padx=2)
        
        # Timestamp label
        self.timestamp_label = tk.Label(right_frame, text="", font=("Arial", 9), 
                                       fg="gray", anchor=tk.W)
        self.timestamp_label.pack(fill=tk.X, padx=10)
        
        # Separator
        ttk.Separator(right_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Topic body
        body_frame = tk.Frame(right_frame)
        body_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        body_scrollbar = tk.Scrollbar(body_frame)
        body_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.body_text = tk.Text(body_frame, wrap=tk.WORD, yscrollcommand=body_scrollbar.set,
                                font=("Arial", 11), state=tk.DISABLED)
        self.body_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        body_scrollbar.config(command=self.body_text.yview)
        
        # Images section
        images_label_frame = tk.Frame(right_frame)
        images_label_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        tk.Label(images_label_frame, text="Images", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        self.add_image_btn = tk.Button(images_label_frame, text="Add Image", 
                                       command=self.add_image, state=tk.DISABLED,
                                       bg="#FF9800", fg="white")
        self.add_image_btn.pack(side=tk.RIGHT)
        
        # Images container with scrollbar
        images_container = tk.Frame(right_frame)
        images_container.pack(fill=tk.BOTH, padx=10, pady=5)
        
        images_scrollbar = tk.Scrollbar(images_container, orient=tk.HORIZONTAL)
        images_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.images_canvas = tk.Canvas(images_container, height=200, 
                                       xscrollcommand=images_scrollbar.set, bg="white")
        self.images_canvas.pack(side=tk.TOP, fill=tk.BOTH)
        images_scrollbar.config(command=self.images_canvas.xview)
        
        self.images_frame = tk.Frame(self.images_canvas)
        self.images_canvas.create_window((0, 0), window=self.images_frame, anchor=tk.NW)
        self.images_frame.bind('<Configure>', 
                              lambda e: self.images_canvas.configure(scrollregion=self.images_canvas.bbox('all')))
    
    def refresh_topic_list(self, search_term=""):
        """Refresh the topic list from database"""
        self.topic_listbox.delete(0, tk.END)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if search_term:
            cursor.execute(
                'SELECT id, title FROM topics WHERE title LIKE ? OR body LIKE ? ORDER BY id DESC',
                (f'%{search_term}%', f'%{search_term}%')
            )
        else:
            cursor.execute('SELECT id, title FROM topics ORDER BY id DESC')
        
        self.topics_data = cursor.fetchall()
        conn.close()
        
        for topic_id, title in self.topics_data:
            self.topic_listbox.insert(tk.END, title)
    
    def filter_topics(self):
        """Filter topics based on search term"""
        search_term = self.search_var.get()
        self.refresh_topic_list(search_term)
    
    def on_topic_select(self, event):
        """Handle topic selection"""
        selection = self.topic_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        self.current_topic_id = self.topics_data[index][0]
        self.load_topic_details(self.current_topic_id)
        
        # Enable buttons
        self.edit_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)
        self.add_image_btn.config(state=tk.NORMAL)
    
    def load_topic_details(self, topic_id):
        """Load and display topic details"""
        import json
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, body, body_formatting, created_by, created_at, modified_by, modified_at 
            FROM topics WHERE id = ?
        ''', (topic_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return
        
        title, body, body_formatting, created_by, created_at, modified_by, modified_at = result
        
        # Update title
        self.title_label.config(text=title)
        
        # Update timestamp
        if modified_at:
            timestamp_text = f"Last edited by {modified_by} on {self.format_timestamp(modified_at)}"
        else:
            timestamp_text = f"Created by {created_by} on {self.format_timestamp(created_at)}"
        self.timestamp_label.config(text=timestamp_text)
        
        # Update body with formatting
        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete(1.0, tk.END)
        self.body_text.insert(1.0, body or "")
        
        # Apply formatting if it exists
        if body_formatting:
            try:
                formatting = json.loads(body_formatting)
                for fmt in formatting:
                    tag = fmt['tag']
                    start = fmt['start']
                    end = fmt['end']
                    
                    # Configure tag if needed
                    if tag not in self.body_text.tag_names():
                        if tag.startswith('size_'):
                            size = int(tag.split('_')[1])
                            self.body_text.tag_configure(tag, font=("Arial", size))
                        elif tag.startswith('color_'):
                            color = tag.replace('color_', '')
                            self.body_text.tag_configure(tag, foreground=color)
                        elif tag == "bold":
                            self.body_text.tag_configure(tag, font=("Arial", 11, "bold"))
                        elif tag == "italic":
                            self.body_text.tag_configure(tag, font=("Arial", 11, "italic"))
                        elif tag == "underline":
                            self.body_text.tag_configure(tag, font=("Arial", 11, "underline"))
                    
                    self.body_text.tag_add(tag, start, end)
            except (json.JSONDecodeError, KeyError, ValueError, IndexError):
                pass
        
        self.body_text.config(state=tk.DISABLED)
        
        # Load images
        self.load_images(topic_id)
        
        conn.close()
    
    def load_images(self, topic_id):
        """Load and display images for the topic"""
        # Clear existing images
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        self.image_references.clear()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, image_data, filename FROM images WHERE topic_id = ?', (topic_id,))
        images = cursor.fetchall()
        conn.close()
        
        for idx, (image_id, image_data, filename) in enumerate(images):
            self.create_image_thumbnail(image_id, image_data, filename, idx)
    
    def create_image_thumbnail(self, image_id, image_data, filename, position):
        """Create an image thumbnail with delete button"""
        frame = tk.Frame(self.images_frame, relief=tk.RAISED, borderwidth=2, padx=3, pady=3)
        frame.grid(row=0, column=position, padx=5, pady=5, sticky=tk.N)
        
        try:
            # Load and resize image
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image)
            
            # Store reference
            self.image_references.append(photo)
            
            # Image label (clickable)
            img_label = tk.Label(frame, image=photo, cursor="hand2")
            img_label.pack(pady=(0, 3))
            img_label.bind('<Button-1>', lambda e, data=image_data: self.view_full_image(data))
            
            # Filename label
            if filename:
                name_label = tk.Label(frame, text=filename[:12] + "..." if len(filename) > 12 else filename,
                                     font=("Arial", 8), wraplength=100)
                name_label.pack(pady=(0, 3))
            
            # Delete button
            delete_btn = tk.Button(frame, text="Delete", command=lambda: self.delete_image(image_id),
                                  bg="#f44336", fg="white", font=("Arial", 8, "bold"))
            delete_btn.pack(fill=tk.X)
            
        except Exception as e:
            tk.Label(frame, text="Error loading image").pack()
    
    def view_full_image(self, image_data):
        """View full-size image in a new window"""
        window = tk.Toplevel(self.root)
        window.title("Image Viewer")
        
        image = Image.open(io.BytesIO(image_data))
        
        # Resize if too large
        max_size = 800
        if image.width > max_size or image.height > max_size:
            image.thumbnail((max_size, max_size))
        
        photo = ImageTk.PhotoImage(image)
        
        label = tk.Label(window, image=photo)
        label.image = photo  # Keep reference
        label.pack()
    
    def add_topic(self):
        """Open dialog to add a new topic"""
        dialog = AddTopicDialog(self.root, self.db_path)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_topic_list(self.search_var.get())
            # Select the newly created topic
            self.topic_listbox.selection_clear(0, tk.END)
            self.topic_listbox.selection_set(0)
            self.topic_listbox.event_generate('<<ListboxSelect>>')
    
    def edit_topic(self):
        """Open dialog to edit current topic"""
        if not self.current_topic_id:
            return
        
        dialog = EditTopicDialog(self.root, self.db_path, self.current_topic_id)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_topic_list(self.search_var.get())
            self.load_topic_details(self.current_topic_id)
    
    def delete_topic(self):
        """Delete the current topic"""
        if not self.current_topic_id:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this topic?"):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM topics WHERE id = ?', (self.current_topic_id,))
            cursor.execute('DELETE FROM images WHERE topic_id = ?', (self.current_topic_id,))
            conn.commit()
            conn.close()
            
            self.current_topic_id = None
            self.refresh_topic_list(self.search_var.get())
            self.clear_topic_details()
    
    def add_image(self):
        """Add an image to the current topic"""
        if not self.current_topic_id:
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    image_data = f.read()
                
                filename = os.path.basename(file_path)
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO images (topic_id, image_data, filename) VALUES (?, ?, ?)',
                    (self.current_topic_id, image_data, filename)
                )
                conn.commit()
                conn.close()
                
                self.load_images(self.current_topic_id)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add image: {str(e)}")
    
    def delete_image(self, image_id):
        """Delete an image"""
        if messagebox.askyesno("Confirm Delete", "Delete this image?"):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM images WHERE id = ?', (image_id,))
            conn.commit()
            conn.close()
            
            if self.current_topic_id:
                self.load_images(self.current_topic_id)
    
    def clear_topic_details(self):
        """Clear topic details display"""
        self.title_label.config(text="Select a topic")
        self.timestamp_label.config(text="")
        self.body_text.config(state=tk.NORMAL)
        self.body_text.delete(1.0, tk.END)
        self.body_text.config(state=tk.DISABLED)
        
        for widget in self.images_frame.winfo_children():
            widget.destroy()
        self.image_references.clear()
        
        self.edit_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)
        self.add_image_btn.config(state=tk.DISABLED)


class AddTopicDialog:
    """Dialog for adding a new topic"""
    def __init__(self, parent, db_path):
        self.db_path = db_path
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add New Topic")
        self.dialog.geometry("600x500")
        self.dialog.minsize(500, 450)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Your name
        tk.Label(self.dialog, text="Your Name:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        self.name_entry = tk.Entry(self.dialog, font=("Arial", 10))
        self.name_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        tk.Label(self.dialog, text="Topic Title:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        self.title_entry = tk.Entry(self.dialog, font=("Arial", 10))
        self.title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Body with Rich Text Editor
        tk.Label(self.dialog, text="Topic Body:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        
        editor_frame = tk.Frame(self.dialog, height=250)
        editor_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        editor_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        self.body_editor = RichTextEditor(editor_frame)
        self.body_editor.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Create Topic", command=self.create_topic,
                 bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy,
                 font=("Arial", 10)).pack(side=tk.RIGHT)
        
        self.name_entry.focus()
    
    def create_topic(self):
        """Create the new topic"""
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        body, body_formatting = self.body_editor.get_formatted_content()
        body = body.strip()
        
        if not name:
            messagebox.showwarning("Missing Information", "Please enter your name.")
            return
        
        if not title:
            messagebox.showwarning("Missing Information", "Please enter a topic title.")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO topics (title, body, body_formatting, created_by) VALUES (?, ?, ?, ?)',
                (title, body, body_formatting, name)
            )
            conn.commit()
            conn.close()
            
            self.result = True
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create topic: {str(e)}")


class EditTopicDialog:
    """Dialog for editing an existing topic"""
    def __init__(self, parent, db_path, topic_id):
        self.db_path = db_path
        self.topic_id = topic_id
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Topic")
        self.dialog.geometry("600x500")
        self.dialog.minsize(500, 450)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Load existing data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT title, body, body_formatting FROM topics WHERE id = ?', (topic_id,))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            self.dialog.destroy()
            return
        
        existing_title, existing_body, existing_formatting = result
        
        # Your name
        tk.Label(self.dialog, text="Your Name:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        self.name_entry = tk.Entry(self.dialog, font=("Arial", 10))
        self.name_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Title
        tk.Label(self.dialog, text="Topic Title:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        self.title_entry = tk.Entry(self.dialog, font=("Arial", 10))
        self.title_entry.insert(0, existing_title)
        self.title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Body with Rich Text Editor
        tk.Label(self.dialog, text="Topic Body:", font=("Arial", 10)).pack(pady=(10, 0), padx=10, anchor=tk.W)
        
        editor_frame = tk.Frame(self.dialog, height=250)
        editor_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        editor_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        self.body_editor = RichTextEditor(editor_frame)
        self.body_editor.set_formatted_content(existing_body or "", existing_formatting)
        self.body_editor.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(btn_frame, text="Save Changes", command=self.save_changes,
                 bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy,
                 font=("Arial", 10)).pack(side=tk.RIGHT)
        
        self.name_entry.focus()
    
    def save_changes(self):
        """Save the edited topic"""
        name = self.name_entry.get().strip()
        title = self.title_entry.get().strip()
        body, body_formatting = self.body_editor.get_formatted_content()
        body = body.strip()
        
        if not name:
            messagebox.showwarning("Missing Information", "Please enter your name.")
            return
        
        if not title:
            messagebox.showwarning("Missing Information", "Please enter a topic title.")
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE topics 
                   SET title = ?, body = ?, body_formatting = ?, modified_by = ?, modified_at = CURRENT_TIMESTAMP 
                   WHERE id = ?''',
                (title, body, body_formatting, name, self.topic_id)
            )
            conn.commit()
            conn.close()
            
            self.result = True
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update topic: {str(e)}")


def main():
    """Main entry point"""
    # Database path - should be on shared drive
    # For testing, use local path. Replace with your shared drive path
    db_path = os.path.join(os.path.dirname(__file__), "topics.db")
    
    # Uncomment and modify this for production on shared drive:
    # db_path = r"\\shared-drive\path\to\topics.db"
    
    root = tk.Tk()
    app = TopicManagerApp(root, db_path)
    root.mainloop()


if __name__ == "__main__":
    main()
