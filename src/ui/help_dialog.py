"""Help dialog with examples and instructions"""

import tkinter as tk
from tkinter import ttk
import webbrowser


class HelpDialog:
    """Dialog showing help and examples for dialogue creation"""
    
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Dialogue Editor - Information Atlas")
        self.dialog.transient(parent)
        self.dialog.geometry("800x600")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Quick Start tab
        quickstart_frame = ttk.Frame(notebook)
        notebook.add(quickstart_frame, text="🚀 Quick Start")
        self.create_quickstart_tab(quickstart_frame)
        
        # Examples tab
        examples_frame = ttk.Frame(notebook)
        notebook.add(examples_frame, text="📚 Examples")
        self.create_examples_tab(examples_frame)
        
        # Format Reference tab
        format_frame = ttk.Frame(notebook)
        notebook.add(format_frame, text="📋 Format Reference")
        self.create_format_tab(format_frame)
        
        # Conditions Reference tab
        conditions_frame = ttk.Frame(notebook)
        notebook.add(conditions_frame, text="🔀 Conditions")
        self.create_conditions_tab(conditions_frame)
        
        # Close button
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Close", command=self.dialog.destroy).pack()
    
    def create_quickstart_tab(self, parent):
        """Create quick start instructions"""
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content = """
CATACLYSM: BRIGHT NIGHTS DIALOGUE EDITOR - QUICK START

FEATURES IMPLEMENTED:
✅ Visual node graph with connections
✅ Import/Export JSON dialogue files
✅ Full topic editing (dynamic lines, responses, effects)
✅ Conditional dynamic lines with yes/no branches
✅ Trial responses (skill checks: PERSUADE, INTIMIDATE, LIE)
✅ Response conditions (variable checks, effects, boolean logic)
✅ Speaker effects editor
✅ Auto-layout for node positioning
✅ Validation for errors and broken references
✅ Pan, zoom, and grid navigation

BASIC WORKFLOW:

1. Import or Start New
   • Click "Import" to load an existing dialogue file
   • Or start with an empty graph

2. Create a Topic
   • Click "New Topic" in the toolbar
   • Enter a topic ID (e.g., "TALK_EXAMPLE_HELLO")
   • Topic IDs can be any value (special: TALK_NONE, TALK_DONE, TALK_TRAIN)

3. Edit the Topic
   • Click on a node in the graph to select it
   • Use the property editor on the right:
     - Click "Edit" under Dynamic Line to edit what the NPC says
     - Click "Add" under Responses to add player dialogue options
     - Click "Edit" under Speaker Effect to add effects
   • Click "Update Node" to save changes

4. Dynamic Line Editor
   • Simple Text: Direct text entry
   • Conditional: Form-based condition editor with yes/no branches (optional)
   • Advanced: Raw JSON for complex structures

5. Response Editor
   • Basic Tab: Direct topic links (can type custom topic IDs)
   • Trial Tab: Skill checks with success/failure branches
   • Advanced Tab: Conditions and special options

6. Connect Topics
   • Responses automatically create visual connections
   • Multiple responses = multiple outgoing connections
   • Click connections to see dialogue flow

7. Navigation
   • Click and drag nodes to reposition (snaps to grid)
   • Mouse wheel to zoom in/out
   • Middle mouse button to pan
   • Arrow keys to pan in any direction
   • Use "Auto Layout" to automatically arrange nodes

8. Validate and Export
   • Click "Validate" to check for errors
   • Click "Export" to save your dialogue file
   • Validation runs automatically on export

EDITOR TABS:
All complex editors have "Simple" and "Advanced" tabs:
- Simple: Form-based editing for common patterns
- Advanced: Raw JSON for power users and complex structures

REFERENCE DOCUMENTATION:
For complete documentation on dialogue formatting, conditions, effects, and more,
see the official Cataclysm Bright Nights documentation:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues
"""
        
        text_widget = tk.Text(scrollable_frame, wrap="word", font=("Arial", 10), width=70, height=30)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled")
        
        # Make link clickable
        def open_writing_dialogues(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues")
        
        text_widget.tag_config("link", foreground="blue", underline=True)
        text_widget.tag_bind("link", "<Button-1>", lambda e: open_writing_dialogues())
        text_widget.tag_bind("link", "<Enter>", lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind("link", "<Leave>", lambda e: text_widget.config(cursor=""))
        
        # Find and tag the link
        start_idx = text_widget.search("https://docs.cataclysmbn.org", "1.0", tk.END)
        if start_idx:
            end_idx = f"{start_idx}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues')}c"
            text_widget.tag_add("link", start_idx, end_idx)
        
        text_widget.pack(anchor="w", fill="both", expand=True, padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_examples_tab(self, parent):
        """Create examples tab"""
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Simple greeting example
        ttk.Label(scrollable_frame, text="Example 1: Simple Greeting", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        simple_example = """Topic ID: TALK_GREETING

Dynamic Lines:
  • "Hello there!"
  • "Hey, how are you?"
  • "Good to see you."

Responses:
  • "Hello" → TALK_CHAT
  • "Goodbye" → TALK_DONE"""
        
        example1_text = tk.Text(scrollable_frame, wrap="word", font=("Courier", 9), height=8, width=60)
        example1_text.insert("1.0", simple_example)
        example1_text.config(state="disabled")
        example1_text.pack(anchor="w", padx=20, pady=5)
        
        # Branching dialogue example
        ttk.Label(scrollable_frame, text="Example 2: Branching Dialogue", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        branching_example = """Topic ID: TALK_MISSION_OFFER

Dynamic Lines:
  • "I need someone to help me clear out zombies."
  • "Could you help me with something?"

Responses:
  • "I'll help" → TALK_MISSION_ACCEPT
  • "Maybe later" → TALK_MISSION_REFUSE
  • "What's the reward?" → TALK_MISSION_REWARD"""
        
        example2_text = tk.Text(scrollable_frame, wrap="word", font=("Courier", 9), height=8, width=60)
        example2_text.insert("1.0", branching_example)
        example2_text.config(state="disabled")
        example2_text.pack(anchor="w", padx=20, pady=5)
        
        # JSON format example with trials and conditions
        ttk.Label(scrollable_frame, text="Example 3: JSON Format", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        json_example = """[
  {
    "type": "talk_topic",
    "id": "TALK_EXAMPLE",
    "dynamic_line": [
      "Hello!",
      "Hi there!"
    ],
    "responses": [
      {
        "text": "Hello",
        "topic": "TALK_CHAT"
      },
      {
        "text": "Goodbye",
        "topic": "TALK_DONE"
      }
    ]
  }
]"""
        
        text_widget = tk.Text(scrollable_frame, height=15, width=60, font=("Courier", 9), wrap="none")
        text_widget.insert("1.0", json_example)
        text_widget.config(state="disabled")
        text_widget.pack(anchor="w", padx=20, pady=5)
        
        # Example with trial
        ttk.Label(scrollable_frame, text="Example 4: Trial Response", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        trial_example = """Response with skill check:
{
  "text": "Why don't you come with me?",
  "trial": {
    "type": "PERSUADE",
    "difficulty": -15
  },
  "success": {
    "topic": "TALK_AGREE_FOLLOW",
    "effect": "follow"
  },
  "failure": {
    "topic": "TALK_DENY_FOLLOW",
    "effect": "deny_follow"
  }
}"""
        
        trial_text = tk.Text(scrollable_frame, wrap="word", font=("Courier", 9), height=10, width=60)
        trial_text.insert("1.0", trial_example)
        trial_text.config(state="disabled")
        trial_text.pack(anchor="w", padx=20, pady=5)
        
        # Example with conditional dynamic line
        ttk.Label(scrollable_frame, text="Example 5: Conditional Dynamic Line", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        conditional_example = """Dynamic line with condition (yes/no branches optional):
{
  "npc_has_var": "knows_u",
  "type": "dialogue",
  "context": "first_meeting",
  "value": "yes",
  "yes": "<greet>",
  "no": "Freeze! Who are you?"
}

Note: Both "yes" and "no" branches are optional in the editor.
You can save a conditional dynamic line with just the condition."""
        
        conditional_text = tk.Text(scrollable_frame, wrap="word", font=("Courier", 9), height=10, width=60)
        conditional_text.insert("1.0", conditional_example)
        conditional_text.config(state="disabled")
        conditional_text.pack(anchor="w", padx=20, pady=5)
        
        # Documentation links
        ttk.Label(scrollable_frame, text="Documentation Links:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 5))
        
        doc_frame = ttk.Frame(scrollable_frame)
        doc_frame.pack(anchor="w", fill="x", padx=20, pady=5)
        
        doc_text_widget = tk.Text(doc_frame, wrap="word", font=("Arial", 9), height=3, width=60)
        doc_text_widget.insert("1.0", """Official Cataclysm Bright Nights Dialogue Documentation:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues

Dialogue Effects Reference:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects""")
        doc_text_widget.config(state="disabled")
        
        # Make links clickable
        def open_writing_link(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues")
        
        def open_effects_link(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects")
        
        doc_text_widget.tag_config("link1", foreground="blue", underline=True)
        doc_text_widget.tag_config("link2", foreground="blue", underline=True)
        doc_text_widget.tag_bind("link1", "<Button-1>", lambda e: open_writing_link())
        doc_text_widget.tag_bind("link2", "<Button-1>", lambda e: open_effects_link())
        doc_text_widget.tag_bind("link1", "<Enter>", lambda e: doc_text_widget.config(cursor="hand2"))
        doc_text_widget.tag_bind("link2", "<Enter>", lambda e: doc_text_widget.config(cursor="hand2"))
        doc_text_widget.tag_bind("link1", "<Leave>", lambda e: doc_text_widget.config(cursor=""))
        doc_text_widget.tag_bind("link2", "<Leave>", lambda e: doc_text_widget.config(cursor=""))
        
        # Tag the links
        link1_start = doc_text_widget.search("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues", "1.0", tk.END)
        if link1_start:
            link1_end = f"{link1_start}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues')}c"
            doc_text_widget.tag_add("link1", link1_start, link1_end)
        
        link2_start = doc_text_widget.search("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects", "1.0", tk.END)
        if link2_start:
            link2_end = f"{link2_start}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects')}c"
            doc_text_widget.tag_add("link2", link2_start, link2_end)
        
        doc_text_widget.pack(anchor="w")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_format_tab(self, parent):
        """Create format reference tab"""
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        content = """
DIALOGUE FILE FORMAT REFERENCE

Dialogue files are JSON arrays containing talk_topic objects.

REQUIRED FIELDS:
• type: Always "talk_topic"
• id: Unique identifier (any string, commonly starts with "TALK_")

OPTIONAL FIELDS:
• dynamic_line: What the NPC says
  - Can be: string, array of strings, or conditional dict
  - Game randomly selects from array if multiple strings
  - Conditional format: { condition..., "yes": "...", "no": "..." }
• responses: Array of response objects
• speaker_effect: Object that runs when topic is spoken

DYNAMIC LINE TYPES SUPPORTED:
✅ Simple string: "Hello there!"
✅ Array of strings: ["Hello", "Hi", "Greetings"]
✅ Conditional: { "npc_has_var": "knows_u", "yes": "Hello!", "no": "Who are you?" }
  - Yes/no branches are optional
  - Supports all condition types (variables, effects, gender, environment, boolean logic)

RESPONSE OBJECT FORMATS:

1. Basic Direct Response:
{
  "text": "What the player sees",
  "topic": "TALK_TARGET_TOPIC_ID"
}

2. Response with Condition:
{
  "text": "Response text",
  "topic": "TALK_TARGET",
  "condition": { "npc_has_var": "flag", "type": "dialogue", "context": "first_meeting", "value": "yes" }
}

3. Trial Response (Skill Check):
{
  "text": "Attempt persuasion",
  "trial": { 
    "type": "PERSUADE", 
    "difficulty": 10,
    "mod": [["value", 2]]  // Optional mod array
  },
  "success": { 
    "topic": "TALK_SUCCESS",
    "effect": "effect_id",  // Optional
    "opinion": { "trust": 1, "value": 1 },  // Optional
    "mission_opinion": { "trust": 2 }  // Optional
  },
  "failure": { 
    "topic": "TALK_FAILURE",
    "effect": "effect_id",  // Optional
    "opinion": { "trust": -1 },  // Optional
    "mission_opinion": { "trust": -1 }  // Optional
  }
}

4. True/False Text Response:
{
  "truefalsetext": {
    "true": "I killed him.",
    "false": "I killed it.",
    "condition": { "mission_goal": "ASSASSINATE" }
  },
  "condition": { "and": ["mission_incomplete", ...] },
  "topic": "TALK_MISSION_SUCCESS"
}

5. Response with Switch:
{
  "text": "I killed them all.",
  "topic": "TALK_MISSION_SUCCESS",
  "condition": { "and": [...] },
  "switch": true
}

SPECIAL TOPIC VALUES:
• TALK_NONE: Return to previous topic
• TALK_DONE: End conversation
• TALK_TRAIN: Start training menu
• Custom values: Can type any topic ID (validated on export)

SPEAKER EFFECT FORMATS:

Supported effect types:
• npc_add_var: "var_name" or { "npc_add_var": "var_name", "type": "dialogue", "context": "...", "value": "..." }
• u_adjust_var: "var_name"
• npc_add_effect: "effect_id" or { "npc_add_effect": "effect_id", "duration": 600 }
• u_add_effect: "effect_id" or { "u_add_effect": "effect_id", "duration": "PERMANENT" }
• mapgen_update: Complex object (use Advanced tab)

Can be wrapped in effect key:
{
  "effect": {
    "npc_add_var": "knows_u",
    "type": "dialogue",
    "context": "first_meeting",
    "value": "yes"
  }
}

CONDITION TYPES SUPPORTED:

✅ Variable Checks: npc_has_var, u_has_var (with type, context, value)
✅ Effect Checks: npc_has_effect, u_has_effect
✅ Gender Checks: npc_female, npc_male, u_female, u_male
✅ Environment: days_since_cataclysm, is_season, is_day, is_outside
✅ Boolean Logic: and, or, not (with nested sub-conditions)

EDITOR FEATURES:
• All editors have "Simple" (form-based) and "Advanced" (raw JSON) tabs
• Simple editors auto-fill fields from imported data
• Nested condition editing through SubConditionDialog
• Horizontal scrollbars for long text
• Visual indicators (emojis) for different content types

VALIDATION:
• All topic IDs must be unique
• All response topics must exist (or be special values)
• Structure validation runs on export
• Use "Validate" button to check before exporting

REFERENCE DOCUMENTATION:
For complete documentation on dialogue formatting, conditions, effects, and more,
see the official Cataclysm Bright Nights documentation:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", font=("Arial", 9), width=80, height=40)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled")
        
        # Make link clickable
        def open_writing_dialogues_link(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues")
        
        text_widget.tag_config("link", foreground="blue", underline=True)
        text_widget.tag_bind("link", "<Button-1>", lambda e: open_writing_dialogues_link())
        text_widget.tag_bind("link", "<Enter>", lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind("link", "<Leave>", lambda e: text_widget.config(cursor=""))
        
        # Find and tag the link
        start_idx = text_widget.search("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues", "1.0", tk.END)
        if start_idx:
            end_idx = f"{start_idx}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues')}c"
            text_widget.tag_add("link", start_idx, end_idx)
        
        text_widget.pack(anchor="w", fill="both", expand=True, padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_conditions_tab(self, parent):
        """Create conditions reference tab"""
        # Scrollable frame
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content about conditions
        content = """
DYNAMIC LINE CONDITIONS

Dynamic lines can use conditional logic to show different text based on game state.

BASIC FORMAT:
{
  "condition_key": condition_value,
  "yes": "Text when condition is true",  // Optional
  "no": "Text when condition is false"   // Optional
}

Note: Yes/no branches are optional. You can create conditional dynamic lines
with just the condition, or with only one branch if needed.

COMMON CONDITION TYPES:

NPC/Player Variables:
• npc_has_var: Check if NPC has a variable
• u_has_var: Check if player has a variable

Gender:
• npc_female: true if NPC is female
• npc_male: true if NPC is male
• u_female: true if player is female
• u_male: true if player is male

Effects:
• npc_has_effect: Check if NPC has an effect
• u_has_effect: Check if player has an effect

Environment:
• days_since_cataclysm: Number (days since event)
• is_season: "spring", "summer", "autumn", "winter"
• is_day: true if daytime
• is_outside: true if NPC is outside

Boolean Logic:
• and: Array of conditions (all must be true)
• or: Array of conditions (any can be true)
• not: Single condition (negation)

EXAMPLES:

Simple variable check:
{
  "npc_has_var": "knows_u",
  "type": "dialogue",
  "context": "first_meeting",
  "value": "yes",
  "yes": "<greet>",
  "no": "Freeze! Who are you?"
}

Gender-based:
{
  "npc_female": true,
  "yes": "Hello, I'm a woman.",
  "no": "Hello, I'm a man."
}

Complex condition (and/or/not):
{
  "and": [
    {"npc_has_var": "knows_u", "type": "dialogue", "context": "first_meeting", "value": "yes"},
    {"days_since_cataclysm": 30}
  ],
  "yes": "We've known each other a while now.",
  "no": "I don't know you."
}

See the full documentation at:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects

WRITING DIALOGUES GUIDE:
For a complete guide on writing dialogues, see:
https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues
        """
        
        text_widget = tk.Text(scrollable_frame, wrap="word", font=("Arial", 9), width=80, height=40)
        text_widget.insert("1.0", content.strip())
        text_widget.config(state="disabled")
        
        # Make links clickable
        def open_effects_link(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects")
        
        def open_writing_link(event=None):
            webbrowser.open("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues")
        
        text_widget.tag_config("link1", foreground="blue", underline=True)
        text_widget.tag_config("link2", foreground="blue", underline=True)
        text_widget.tag_bind("link1", "<Button-1>", lambda e: open_effects_link())
        text_widget.tag_bind("link2", "<Button-1>", lambda e: open_writing_link())
        text_widget.tag_bind("link1", "<Enter>", lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind("link2", "<Enter>", lambda e: text_widget.config(cursor="hand2"))
        text_widget.tag_bind("link1", "<Leave>", lambda e: text_widget.config(cursor=""))
        text_widget.tag_bind("link2", "<Leave>", lambda e: text_widget.config(cursor=""))
        
        # Tag the links
        link1_start = text_widget.search("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects", "1.0", tk.END)
        if link1_start:
            link1_end = f"{link1_start}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#dialogue-effects')}c"
            text_widget.tag_add("link1", link1_start, link1_end)
        
        link2_start = text_widget.search("https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues", "1.0", tk.END)
        if link2_start:
            link2_end = f"{link2_start}+{len('https://docs.cataclysmbn.org/mod/json/reference/creatures/npcs/#writing-dialogues')}c"
            text_widget.tag_add("link2", link2_start, link2_end)
        
        text_widget.pack(anchor="w", fill="both", expand=True, padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


