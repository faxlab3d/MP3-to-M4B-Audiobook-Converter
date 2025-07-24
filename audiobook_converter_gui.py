#!/usr/bin/env python3
"""
MP3 to M4B Audiobook Converter - GUI Version
User-friendly interface for converting multiple MP3 files to M4B audiobook format.
Requires FFmpeg to be installed on your system.
"""

import os
import subprocess
import sys
import threading
import tempfile
from pathlib import Path
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import queue

class AudiobookConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 to M4B Audiobook Converter")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Variables
        self.input_folder = StringVar()
        self.output_file = StringVar()
        self.book_title = StringVar()
        self.author_name = StringVar(value="Unknown")
        self.bitrate = StringVar(value="64k")
        
        # Progress tracking
        self.progress_queue = queue.Queue()
        self.conversion_thread = None
        
        self.create_widgets()
        self.check_ffmpeg_on_start()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="MP3 to M4B Audiobook Converter", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input folder selection
        ttk.Label(main_frame, text="Input Folder:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=1, column=1, sticky=(W, E), padx=(10, 10), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_folder).grid(row=1, column=2, pady=5)
        
        # Output file selection
        ttk.Label(main_frame, text="Output File:").grid(row=2, column=0, sticky=W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file, width=50).grid(row=2, column=1, sticky=(W, E), padx=(10, 10), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(row=2, column=2, pady=5)
        
        # Book details frame
        details_frame = ttk.LabelFrame(main_frame, text="Audiobook Details", padding="10")
        details_frame.grid(row=3, column=0, columnspan=3, sticky=(W, E), pady=10)
        details_frame.columnconfigure(1, weight=1)
        
        ttk.Label(details_frame, text="Title:").grid(row=0, column=0, sticky=W, pady=5)
        ttk.Entry(details_frame, textvariable=self.book_title, width=50).grid(row=0, column=1, sticky=(W, E), padx=(10, 0), pady=5)
        
        ttk.Label(details_frame, text="Author:").grid(row=1, column=0, sticky=W, pady=5)
        ttk.Entry(details_frame, textvariable=self.author_name, width=50).grid(row=1, column=1, sticky=(W, E), padx=(10, 0), pady=5)
        
        ttk.Label(details_frame, text="Bitrate:").grid(row=2, column=0, sticky=W, pady=5)
        bitrate_combo = ttk.Combobox(details_frame, textvariable=self.bitrate, 
                                   values=["32k", "48k", "64k", "96k", "128k"], 
                                   state="readonly", width=10)
        bitrate_combo.grid(row=2, column=1, sticky=W, padx=(10, 0), pady=5)
        
        # File list frame
        list_frame = ttk.LabelFrame(main_frame, text="MP3 Files Found", padding="10")
        list_frame.grid(row=4, column=0, columnspan=3, sticky=(W, E, N, S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox with scrollbar
        self.file_listbox = Listbox(list_frame, height=8)
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.grid(row=0, column=0, sticky=(W, E, N, S))
        scrollbar.grid(row=0, column=1, sticky=(N, S))
        
        # Progress frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=5, column=0, columnspan=3, sticky=(W, E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=0, column=0, sticky=(W, E), pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready to convert")
        self.status_label.grid(row=1, column=0, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.convert_button = ttk.Button(button_frame, text="Convert to M4B", 
                                       command=self.start_conversion, style="Accent.TButton")
        self.convert_button.pack(side=LEFT, padx=5)
        
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=LEFT, padx=5)
        
        # Configure main_frame row weights
        main_frame.rowconfigure(4, weight=1)
        
    def check_ffmpeg_on_start(self):
        """Check if FFmpeg is available when starting the app."""
        if not self.check_ffmpeg():
            messagebox.showerror("FFmpeg Not Found", 
                               "FFmpeg is required but not found on your system.\n\n" +
                               "Please install FFmpeg:\n" +
                               "• Windows: Download from https://ffmpeg.org/\n" +
                               "• Mac: brew install ffmpeg\n" +
                               "• Linux: sudo apt install ffmpeg")
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def browse_input_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Select folder with MP3 files")
        if folder:
            self.input_folder.set(folder)
            self.load_mp3_files()
            self.auto_set_output_and_title()
    
    def browse_output_file(self):
        """Open file save dialog."""
        file = filedialog.asksaveasfilename(
            title="Save M4B file as",
            defaultextension=".m4b",
            filetypes=[("M4B files", "*.m4b"), ("All files", "*.*")]
        )
        if file:
            self.output_file.set(file)
    
    def load_mp3_files(self):
        """Load and display MP3 files from selected folder."""
        folder = self.input_folder.get()
        if not folder or not os.path.isdir(folder):
            return
        
        # Clear listbox
        self.file_listbox.delete(0, END)
        
        # Find MP3 files
        mp3_files = []
        for file in Path(folder).glob('*.mp3'):
            mp3_files.append(str(file))
        
        # Sort files naturally
        mp3_files.sort(key=lambda x: [int(c) if c.isdigit() else c.lower() 
                                    for c in os.path.basename(x)])
        
        # Add to listbox
        for file in mp3_files:
            self.file_listbox.insert(END, os.path.basename(file))
        
        if mp3_files:
            self.status_label.config(text=f"Found {len(mp3_files)} MP3 files")
        else:
            self.status_label.config(text="No MP3 files found in selected folder")
            messagebox.showwarning("No Files", "No MP3 files found in the selected folder.")
    
    def auto_set_output_and_title(self):
        """Automatically set output file and title based on folder name."""
        folder = self.input_folder.get()
        if folder:
            folder_name = os.path.basename(os.path.abspath(folder))
            
            # Set title if not already set
            if not self.book_title.get():
                self.book_title.set(folder_name)
            
            # Set output file if not already set
            if not self.output_file.get():
                output_path = os.path.join(os.path.dirname(folder), f"{folder_name}.m4b")
                self.output_file.set(output_path)
    
    def clear_all(self):
        """Clear all fields."""
        self.input_folder.set("")
        self.output_file.set("")
        self.book_title.set("")
        self.author_name.set("Unknown")
        self.bitrate.set("64k")
        self.file_listbox.delete(0, END)
        self.status_label.config(text="Ready to convert")
    
    def validate_inputs(self):
        """Validate user inputs before conversion."""
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select an input folder.")
            return False
        
        if not os.path.isdir(self.input_folder.get()):
            messagebox.showerror("Error", "Input folder does not exist.")
            return False
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file.")
            return False
        
        if self.file_listbox.size() == 0:
            messagebox.showerror("Error", "No MP3 files found in the selected folder.")
            return False
        
        return True
    
    def get_mp3_files(self):
        """Get sorted list of MP3 files."""
        folder = self.input_folder.get()
        mp3_files = []
        for file in Path(folder).glob('*.mp3'):
            mp3_files.append(str(file))
        
        mp3_files.sort(key=lambda x: [int(c) if c.isdigit() else c.lower() 
                                    for c in os.path.basename(x)])
        return mp3_files
    
    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        if not self.validate_inputs():
            return
        
        if not self.check_ffmpeg():
            messagebox.showerror("Error", "FFmpeg is not available. Please install FFmpeg first.")
            return
        
        # Disable convert button
        self.convert_button.config(state='disabled')
        
        # Start progress bar
        self.progress_bar.start()
        
        # Start conversion in separate thread
        self.conversion_thread = threading.Thread(target=self.convert_files, daemon=True)
        self.conversion_thread.start()
        
        # Start checking for completion
        self.root.after(100, self.check_conversion_progress)
    
    def convert_files(self):
        """Convert MP3 files to M4B using filter_complex concat (no skipping)."""
        try:
            mp3_files = self.get_mp3_files()
            output_file = self.output_file.get()
            title = self.book_title.get() or "Audiobook"
            author = self.author_name.get() or "Unknown"
            bitrate = self.bitrate.get()

            self.progress_queue.put(("status", f"Converting {len(mp3_files)} files..."))

            with tempfile.TemporaryDirectory() as temp_dir:
                # Create chapter metadata
                self.progress_queue.put(("status", "Creating chapter metadata..."))
                chapters = self.create_chapter_metadata(mp3_files)
                metadata_file = self.create_metadata_file(chapters, title, author, temp_dir)

                # Build ffmpeg input arguments
                input_args = []
                filter_inputs = []
                for idx, mp3_file in enumerate(mp3_files):
                    input_args += ['-i', mp3_file]
                    filter_inputs.append(f"[{idx}:a:0]")

                # Combine inputs into filtergraph
                filtergraph = ''.join(filter_inputs) + f"concat=n={len(mp3_files)}:v=0:a=1[outa]"

                # Final command
                cmd = [
                    'ffmpeg',
                    *input_args,                  # All -i inputs go first
                    '-i', metadata_file,          # metadata input LAST
                    '-filter_complex', filtergraph,
                    '-map', '[outa]',
                    '-map_metadata', f'{len(mp3_files)}',  # metadata is input #N (last)
                    '-vn',
                    '-c:a', 'aac',
                    '-b:a', bitrate,
                    '-ar', '44100',
                    '-ac', '2',
                    '-fflags', '+genpts',
                    '-movflags', '+faststart',
                    '-f', 'mp4',
                    '-y', output_file
                ]

                self.progress_queue.put(("status", "Converting audio... Please wait."))

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    self.progress_queue.put(("success", f"Conversion completed!\nSaved: {output_file}"))
                else:
                    self.progress_queue.put(("error", f"Conversion failed:\n{result.stderr}"))

        except Exception as e:
            self.progress_queue.put(("error", f"Error during conversion:\n{str(e)}"))


    
    def create_chapter_metadata(self, mp3_files):
        """Create chapter metadata for the audiobook."""
        chapters = []
        current_time = 0
        
        for i, mp3_file in enumerate(mp3_files):
            # Get duration
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                   '-of', 'csv=p=0', mp3_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                duration = float(result.stdout.strip())
            except:
                duration = 1800  # Default 30 minutes if can't get duration
            
            chapter_title = f"Chapter {i+1}: {Path(mp3_file).stem}"
            chapters.append({
                'start': current_time,
                'end': current_time + duration,
                'title': chapter_title
            })
            current_time += duration
        
        return chapters
    
    def create_metadata_file(self, chapters, title, author, temp_dir):
        """Create FFmpeg metadata file."""
        metadata_file = os.path.join(temp_dir, 'metadata.txt')
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(";FFMETADATA1\n")
            f.write(f"title={title}\n")
            f.write(f"artist={author}\n")
            f.write("album_artist=Audiobook\n")
            f.write("genre=Audiobook\n\n")
            
            for chapter in chapters:
                f.write("[CHAPTER]\n")
                f.write("TIMEBASE=1/1000\n")
                f.write(f"START={int(chapter['start'] * 1000)}\n")
                f.write(f"END={int(chapter['end'] * 1000)}\n")
                f.write(f"title={chapter['title']}\n\n")
        
        return metadata_file
    
    def show_error_dialog(self, error_message):
        """Show error message in a copyable text dialog."""
        error_window = Toplevel(self.root)
        error_window.title("Conversion Error")
        error_window.geometry("600x400")
        error_window.resizable(True, True)
        
        # Make it modal
        error_window.transient(self.root)
        error_window.grab_set()
        
        # Center the window
        error_window.update_idletasks()
        x = (error_window.winfo_screenwidth() // 2) - (error_window.winfo_width() // 2)
        y = (error_window.winfo_screenheight() // 2) - (error_window.winfo_height() // 2)
        error_window.geometry(f"+{x}+{y}")
        
        # Main frame
        main_frame = ttk.Frame(error_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(W, E, N, S))
        
        error_window.columnconfigure(0, weight=1)
        error_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        ttk.Label(main_frame, text="Conversion Failed", 
                 font=('Arial', 12, 'bold'), foreground='red').grid(row=0, column=0, pady=(0, 10))
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=1, column=0, sticky=(W, E, N, S), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        error_text = Text(text_frame, wrap=WORD, font=('Consolas', 9))
        scrollbar_y = ttk.Scrollbar(text_frame, orient=VERTICAL, command=error_text.yview)
        scrollbar_x = ttk.Scrollbar(text_frame, orient=HORIZONTAL, command=error_text.xview)
        
        error_text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        error_text.grid(row=0, column=0, sticky=(W, E, N, S))
        scrollbar_y.grid(row=0, column=1, sticky=(N, S))
        scrollbar_x.grid(row=1, column=0, sticky=(W, E))
        
        # Insert error message
        error_text.insert('1.0', error_message)
        error_text.config(state='normal')  # Keep it editable for copying
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=(10, 0))
        
        def copy_to_clipboard():
            error_window.clipboard_clear()
            error_window.clipboard_append(error_message)
            copy_btn.config(text="Copied!")
            error_window.after(2000, lambda: copy_btn.config(text="Copy Error"))
        
        copy_btn = ttk.Button(button_frame, text="Copy Error", command=copy_to_clipboard)
        copy_btn.pack(side=LEFT, padx=5)
        
        ttk.Button(button_frame, text="Close", command=error_window.destroy).pack(side=LEFT, padx=5)
        
        # Select all text for easy copying
        error_text.focus_set()
        error_text.tag_add(SEL, "1.0", END)
    
    def check_conversion_progress(self):
        """Check conversion progress and handle completion."""
        try:
            while True:
                msg_type, message = self.progress_queue.get_nowait()
                
                if msg_type == "status":
                    self.status_label.config(text=message)
                elif msg_type == "success":
                    self.progress_bar.stop()
                    self.convert_button.config(state='normal')
                    self.status_label.config(text="Conversion completed successfully!")
                    messagebox.showinfo("Success", message)
                    return
                elif msg_type == "error":
                    self.progress_bar.stop()
                    self.convert_button.config(state='normal')
                    self.status_label.config(text="Conversion failed")
                    self.show_error_dialog(message)
                    return
                    
        except queue.Empty:
            # Continue checking
            self.root.after(100, self.check_conversion_progress)

def main():
    root = Tk()
    
    # Set style
    style = ttk.Style()
    style.theme_use('clam')  # Modern looking theme
    
    app = AudiobookConverterGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()