"""Property editor panel for editing node properties"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional, Callable
from ..models.dialogue import DialogueTopic


class PropertyEditor(ttk.Frame):
    """Panel for editing selected node properties"""
    
    def __init__(self, parent, graph_manager, on_change: Optional[Callable] = None, on_node_select: Optional[Callable] = None):
        super().__init__(parent)
        self.graph_manager = graph_manager
        self.on_change = on_change
        self.on_node_select = on_node_select
        self.current_topic_id = None
        self.current_responses = []  # Store current responses for middle-click navigation
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        # Title
        title_label = ttk.Label(self, text="Node Properties", font=("Arial", 12, "bold"))
        title_label.pack(pady=5)
        
        # Topic ID and Type
        id_frame = ttk.Frame(self)
        id_frame.pack(fill="x", padx=5, pady=2)
        ttk.Label(id_frame, text="Topic ID:").pack(anchor="w")
        self.id_var = tk.StringVar()
        self.id_entry = ttk.Entry(id_frame, textvariable=self.id_var, state="readonly")
        self.id_entry.pack(fill="x", pady=(2, 0))
        
        # Show topic type if it's not the default
        self.type_label = ttk.Label(id_frame, text="", font=("Arial", 8), foreground="gray")
        self.type_label.pack(anchor="w", pady=(2, 0))
        
        # Dynamic Line section
        ttk.Label(self, text="Dynamic Line:", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 2))
        
        # Dynamic line display (single-entry listbox like responses)
        dyn_frame = ttk.Frame(self)
        dyn_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.dynamic_line_listbox = tk.Listbox(dyn_frame, height=3)
        dyn_v_scrollbar = ttk.Scrollbar(dyn_frame, orient="vertical", command=self.dynamic_line_listbox.yview)
        dyn_h_scrollbar = ttk.Scrollbar(dyn_frame, orient="horizontal", command=self.dynamic_line_listbox.xview)
        self.dynamic_line_listbox.configure(yscrollcommand=dyn_v_scrollbar.set, xscrollcommand=dyn_h_scrollbar.set)
        
        self.dynamic_line_listbox.grid(row=0, column=0, sticky="nsew")
        dyn_v_scrollbar.grid(row=0, column=1, sticky="ns")
        dyn_h_scrollbar.grid(row=1, column=0, sticky="ew")
        dyn_frame.grid_rowconfigure(0, weight=1)
        dyn_frame.grid_columnconfigure(0, weight=1)
        
        # Dynamic line button
        dyn_btn_frame = ttk.Frame(self)
        dyn_btn_frame.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(dyn_btn_frame, text="Edit", command=self.edit_dynamic_line).pack(side="left", padx=2)
        ttk.Button(dyn_btn_frame, text="Remove", command=self.clear_dynamic_line).pack(side="left", padx=2)
        
        # Responses section
        ttk.Label(self, text="Responses:", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 2))
        
        # Responses listbox with scrollbars
        resp_frame = ttk.Frame(self)
        resp_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.responses_listbox = tk.Listbox(resp_frame, height=6)
        resp_v_scrollbar = ttk.Scrollbar(resp_frame, orient="vertical", command=self.responses_listbox.yview)
        resp_h_scrollbar = ttk.Scrollbar(resp_frame, orient="horizontal", command=self.responses_listbox.xview)
        self.responses_listbox.configure(yscrollcommand=resp_v_scrollbar.set, xscrollcommand=resp_h_scrollbar.set)
        
        # Bind middle-click for navigation
        self.responses_listbox.bind("<Button-2>", self.on_response_middle_click)  # Middle-click (Linux/Windows)
        
        self.responses_listbox.grid(row=0, column=0, sticky="nsew")
        resp_v_scrollbar.grid(row=0, column=1, sticky="ns")
        resp_h_scrollbar.grid(row=1, column=0, sticky="ew")
        resp_frame.grid_rowconfigure(0, weight=1)
        resp_frame.grid_columnconfigure(0, weight=1)
        
        # Response buttons
        resp_btn_frame = ttk.Frame(self)
        resp_btn_frame.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(resp_btn_frame, text="Add", command=self.add_response).pack(side="left", padx=2)
        ttk.Button(resp_btn_frame, text="Edit", command=self.edit_response).pack(side="left", padx=2)
        ttk.Button(resp_btn_frame, text="Remove", command=self.remove_response).pack(side="left", padx=2)
        
        # Speaker Effect section
        ttk.Label(self, text="Speaker Effect:", font=("Arial", 10, "bold")).pack(anchor="w", padx=5, pady=(10, 2))
        
        # Speaker effect display (single-entry listbox like dynamic line)
        effect_frame = ttk.Frame(self)
        effect_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.effect_listbox = tk.Listbox(effect_frame, height=3)
        effect_v_scrollbar = ttk.Scrollbar(effect_frame, orient="vertical", command=self.effect_listbox.yview)
        effect_h_scrollbar = ttk.Scrollbar(effect_frame, orient="horizontal", command=self.effect_listbox.xview)
        self.effect_listbox.configure(yscrollcommand=effect_v_scrollbar.set, xscrollcommand=effect_h_scrollbar.set)
        
        self.effect_listbox.grid(row=0, column=0, sticky="nsew")
        effect_v_scrollbar.grid(row=0, column=1, sticky="ns")
        effect_h_scrollbar.grid(row=1, column=0, sticky="ew")
        effect_frame.grid_rowconfigure(0, weight=1)
        effect_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons for speaker effect
        effect_btn_frame = ttk.Frame(self)
        effect_btn_frame.pack(fill="x", padx=5, pady=2)
        ttk.Button(effect_btn_frame, text="Edit", command=self.edit_speaker_effect).pack(side="left", padx=2)
        ttk.Button(effect_btn_frame, text="Remove", command=self.clear_speaker_effect).pack(side="left", padx=2)
        
        # Update button
        self.update_btn = ttk.Button(self, text="Update Node", command=self.update_node, state="disabled")
        self.update_btn.pack(padx=5, pady=10)
    
    def load_topic(self, topic_id: Optional[str]):
        """Load topic into editor"""
        self.current_topic_id = topic_id
        
        if not topic_id:
            self.id_var.set("")
            self.type_label.config(text="")
            self.dynamic_line_listbox.delete(0, tk.END)
            self.responses_listbox.delete(0, tk.END)
            self.effect_listbox.delete(0, tk.END)
            self.update_btn.config(state="disabled")
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(topic_id)
        if not topic:
            return
        
        self.id_var.set(topic.id)
        # Show topic type if it's not the default
        if topic.type and topic.type != "talk_topic":
            self.type_label.config(text=f"Type: {topic.type}")
        else:
            self.type_label.config(text="")
        # Load dynamic line (single value)
        self.load_dynamic_line(topic.dynamic_line)
        self.load_responses(topic.responses)
        
        # Load speaker effect
        self.load_speaker_effect(topic.speaker_effect)
        
        self.update_btn.config(state="normal")
    
    def load_dynamic_line(self, dynamic_line):
        """Load single dynamic line into listbox with formatted display"""
        self.dynamic_line_listbox.delete(0, tk.END)
        
        if dynamic_line is None:
            self.dynamic_line_listbox.insert(tk.END, "(No dynamic line)")
            return
        
        # Format display similar to responses - no truncation
        if isinstance(dynamic_line, str):
            # Simple string - show full text
            display = dynamic_line
        elif isinstance(dynamic_line, dict):
            # Conditional dynamic line - show with icon like responses
            condition_keys = [k for k in dynamic_line.keys() if k not in ["yes", "no"]]
            if condition_keys:
                main_condition = condition_keys[0]
                if main_condition in ["npc_has_var", "u_has_var", "has_var"]:
                    condition_display = f"{main_condition}:{dynamic_line.get(main_condition, '?')}"
                elif main_condition in ["and", "or", "not"]:
                    condition_display = f"{main_condition}(...)"
                elif main_condition in ["npc_female", "npc_male", "u_female", "u_male"]:
                    condition_display = main_condition
                elif main_condition in ["npc_has_effect", "u_has_effect"]:
                    condition_display = f"{main_condition}:{dynamic_line.get(main_condition, '?')}"
                else:
                    condition_display = f"{main_condition}"
            else:
                condition_display = "condition"
            
            yes_text = dynamic_line.get("yes", "")
            no_text = dynamic_line.get("no", "")
            display = f"⚙ {condition_display} → ✓{yes_text} ✗{no_text}"
        elif isinstance(dynamic_line, list):
            # Array for random selection - show as list
            if len(dynamic_line) > 0:
                first_item = str(dynamic_line[0])
                display = f"📝 [{len(dynamic_line)} items] {first_item}"
            else:
                display = "(Empty array)"
        else:
            # Fallback - show full text
            display = str(dynamic_line)
        
        self.dynamic_line_listbox.insert(tk.END, display)
    
    def edit_dynamic_line(self):
        """Edit the dynamic line"""
        if not self.current_topic_id:
            messagebox.showwarning("No Topic", "Please select a topic first")
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if not topic:
            return
        
        dialog = DynamicLineDialog(self, topic.dynamic_line)
        if dialog.result is not None:
            topic.dynamic_line = dialog.result
            self.load_dynamic_line(topic.dynamic_line)
            if self.on_change:
                self.on_change()
    
    def clear_dynamic_line(self):
        """Clear the dynamic line"""
        if not self.current_topic_id:
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if topic:
            topic.dynamic_line = None
            self.load_dynamic_line(None)
            if self.on_change:
                self.on_change()
    
    def load_speaker_effect(self, speaker_effect):
        """Load speaker effect into listbox with formatted display"""
        self.effect_listbox.delete(0, tk.END)
        
        if speaker_effect is None:
            self.effect_listbox.insert(tk.END, "(No speaker effect)")
            return
        
        # Format display similar to dynamic line and responses
        if isinstance(speaker_effect, dict):
            # Check for common effect structures
            if "effect" in speaker_effect:
                effect_data = speaker_effect["effect"]
                if isinstance(effect_data, dict):
                    # Find the effect type
                    effect_keys = [k for k in effect_data.keys() if k not in ["type", "value", "context", "duration"]]
                    if effect_keys:
                        effect_type = effect_keys[0]
                        effect_value = effect_data.get(effect_type, "")
                        display = f"✨ effect.{effect_type}: {effect_value}"
                    else:
                        display = "✨ effect"
                else:
                    display = f"✨ effect: {effect_data}"
            elif "npc_add_var" in speaker_effect:
                var_name = speaker_effect.get("npc_add_var", "")
                display = f"✨ npc_add_var: {var_name}"
            elif "u_adjust_var" in speaker_effect:
                var_name = speaker_effect.get("u_adjust_var", "")
                display = f"✨ u_adjust_var: {var_name}"
            elif "npc_add_effect" in speaker_effect:
                effect_id = speaker_effect.get("npc_add_effect", "")
                display = f"✨ npc_add_effect: {effect_id}"
            elif "u_add_effect" in speaker_effect:
                effect_id = speaker_effect.get("u_add_effect", "")
                display = f"✨ u_add_effect: {effect_id}"
            elif "mapgen_update" in speaker_effect:
                display = "✨ mapgen_update"
            else:
                # Generic dict - show first key
                first_key = list(speaker_effect.keys())[0] if speaker_effect else ""
                display = f"✨ {first_key}"
        elif isinstance(speaker_effect, list):
            # Array of effects
            if len(speaker_effect) > 0:
                first_item = speaker_effect[0]
                if isinstance(first_item, dict):
                    first_key = list(first_item.keys())[0] if first_item else ""
                    display = f"✨ [{len(speaker_effect)} effects] {first_key}"
                else:
                    display = f"✨ [{len(speaker_effect)} effects]"
            else:
                display = "(Empty effect array)"
        else:
            display = f"✨ {str(speaker_effect)}"
        
        self.effect_listbox.insert(tk.END, display)
    
    def edit_speaker_effect(self):
        """Edit the speaker effect"""
        if not self.current_topic_id:
            messagebox.showwarning("No Topic", "Please select a topic first")
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if not topic:
            return
        
        dialog = SpeakerEffectDialog(self, topic.speaker_effect)
        if dialog.result is not None:
            topic.speaker_effect = dialog.result
            self.load_speaker_effect(topic.speaker_effect)
            if self.on_change:
                self.on_change()
    
    def clear_speaker_effect(self):
        """Clear the speaker effect"""
        if not self.current_topic_id:
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if topic:
            topic.speaker_effect = None
            self.load_speaker_effect(None)
            if self.on_change:
                self.on_change()
    
    def load_responses(self, responses: list):
        """Load responses into listbox - no truncation"""
        self.responses_listbox.delete(0, tk.END)
        self.current_responses = responses  # Store for middle-click navigation
        for resp in responses:
            # Handle truefalsetext - show the true/false structure
            if "truefalsetext" in resp:
                tf_text = resp.get("truefalsetext", {})
                if isinstance(tf_text, dict):
                    true_text = tf_text.get("true", "")
                    false_text = tf_text.get("false", "")
                    text = f"[TF] true:{true_text} false:{false_text}"
                else:
                    text = "[TF]"
            else:
                text = resp.get("text", "")
            
            # No truncation - show full text
            
            # Build display string
            topic = resp.get("topic", "")
            if topic:
                display = f"{text} → {topic}"
            elif "trial" in resp:
                # Trial response - show success and failure
                trial_info = resp.get("trial", {})
                trial_type = trial_info.get("type", "TRIAL") if isinstance(trial_info, dict) else "TRIAL"
                
                success = resp.get("success", {})
                failure = resp.get("failure", {})
                success_topic = success.get("topic", "") if isinstance(success, dict) else ""
                failure_topic = failure.get("topic", "") if isinstance(failure, dict) else ""
                
                display = f"{text} [{trial_type}] → ✓{success_topic} ✗{failure_topic}"
            else:
                display = text
            
            # Add indicators for special fields
            indicators = []
            if "condition" in resp:
                indicators.append("⚙")
            if resp.get("switch") is True:
                indicators.append("🔄")
            if "mission_opinion" in resp:
                indicators.append("🎯")
            if "opinion" in resp:
                indicators.append("💭")
            if "effect" in resp:
                indicators.append("✨")
            if "truefalsetext" in resp:
                indicators.append("📝")
            
            if indicators:
                display = f"{' '.join(indicators)} {display}"
            
            self.responses_listbox.insert(tk.END, display)
    
    def add_response(self):
        """Add a new response"""
        if not self.current_topic_id:
            return
        
        dialog = ResponseDialog(self, self.graph_manager.dialogue_graph)
        if dialog.result:
            topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
            if topic:
                topic.responses.append(dialog.result)
                self.load_responses(topic.responses)
                if self.on_change:
                    self.on_change()
    
    def edit_response(self):
        """Edit selected response"""
        selection = self.responses_listbox.curselection()
        if not selection or not self.current_topic_id:
            messagebox.showwarning("No Selection", "Please select a response to edit")
            return
        
        idx = selection[0]
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if not topic or idx >= len(topic.responses):
            return
        
        old_resp = topic.responses[idx]
        dialog = ResponseDialog(self, self.graph_manager.dialogue_graph, old_resp)
        if dialog.result:
            topic.responses[idx] = dialog.result
            self.load_responses(topic.responses)
            if self.on_change:
                self.on_change()
    
    def on_response_middle_click(self, event):
        """Handle middle-click on response to navigate to target topic"""
        if not self.on_node_select:
            return
        
        # Get clicked item index
        selection = self.responses_listbox.nearest(event.y)
        if selection < 0 or selection >= len(self.current_responses):
            return
        
        resp = self.current_responses[selection]
        
        # Extract topic ID from response
        topic_id = None
        
        # Check for direct topic
        if "topic" in resp:
            topic_id = resp["topic"]
        # Check for trial response (success/failure topics)
        elif "trial" in resp:
            # Try success topic first, then failure
            success = resp.get("success", {})
            failure = resp.get("failure", {})
            if isinstance(success, dict) and "topic" in success:
                topic_id = success["topic"]
            elif isinstance(failure, dict) and "topic" in failure:
                topic_id = failure["topic"]
        
        # Navigate to the topic if found and valid
        if topic_id and topic_id in self.graph_manager.dialogue_graph.topics:
            self.on_node_select(topic_id)
    
    def remove_response(self):
        """Remove selected response"""
        selection = self.responses_listbox.curselection()
        if not selection or not self.current_topic_id:
            messagebox.showwarning("No Selection", "Please select a response to remove")
            return
        
        idx = selection[0]
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if topic and idx < len(topic.responses):
            topic.responses.pop(idx)
            self.load_responses(topic.responses)
            if self.on_change:
                self.on_change()
    
    def update_node(self):
        """Update node with edited properties"""
        if not self.current_topic_id:
            return
        
        topic = self.graph_manager.dialogue_graph.get_topic(self.current_topic_id)
        if not topic:
            return
        
        # Update dynamic lines
        # Dynamic line is already stored in topic object, no need to get from widgets
        
        # Speaker effect is already stored in topic object when edited via dialog
        
        if self.on_change:
            self.on_change()
        
        messagebox.showinfo("Updated", "Node updated successfully")


class SubConditionDialog:
    """Dialog for editing a single sub-condition using the simple editor"""
    
    def __init__(self, parent, current_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Sub-Condition")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry("500x500")
        
        # Notebook for Simple and Raw JSON tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Simple tab
        simple_frame = ttk.Frame(notebook)
        notebook.add(simple_frame, text="Simple")
        self.create_simple_tab(simple_frame, current_data)
        
        # Raw JSON tab
        raw_frame = ttk.Frame(notebook)
        notebook.add(raw_frame, text="Raw JSON")
        self.create_raw_tab(raw_frame, current_data)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_clicked).pack(side="left", padx=5)
        
        self.dialog.wait_window()
    
    def create_simple_tab(self, parent, current_data):
        """Create simple condition editor tab"""
        # Use the same simple condition editor pattern
        # We need to create a parent frame for the condition editor
        cond_parent = ttk.Frame(parent)
        cond_parent.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Get the class that contains the simple condition editor methods
        # We'll need to find which dialog we're called from and use its methods
        # For now, let's duplicate the simple condition editor code here
        self.create_simple_condition_editor(cond_parent, current_data)
    
    def create_raw_tab(self, parent, current_data):
        """Create raw JSON editor tab"""
        ttk.Label(parent, text="Raw JSON:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.raw_text = tk.Text(text_frame, wrap="word", font=("Courier", 9))
        raw_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.raw_text.yview)
        self.raw_text.configure(yscrollcommand=raw_scrollbar.set)
        self.raw_text.pack(side="left", fill="both", expand=True)
        raw_scrollbar.pack(side="right", fill="y")
        
        if current_data:
            import json
            self.raw_text.insert("1.0", json.dumps(current_data, indent=2))
    
    def create_simple_condition_editor(self, parent, current_data):
        """Create simple condition editor for common condition types"""
        # Same implementation as in ResponseDialog/DynamicLineDialog
        condition_dict = current_data if isinstance(current_data, dict) else {}
        
        # Condition type selector
        ttk.Label(parent, text="Condition Type:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.cond_type_var = tk.StringVar(value="simple")
        self.cond_type_var.trace("w", lambda *args: self.update_simple_condition_ui(parent))
        
        cond_type_frame = ttk.Frame(parent)
        cond_type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(cond_type_frame, text="Variable Check", variable=self.cond_type_var, value="var").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Effect Check", variable=self.cond_type_var, value="effect").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Gender Check", variable=self.cond_type_var, value="gender").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Environment", variable=self.cond_type_var, value="env").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Mission Check", variable=self.cond_type_var, value="mission").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Boolean Logic", variable=self.cond_type_var, value="logic").pack(side="left", padx=5)
        
        # Variable check fields
        self.var_frame = ttk.LabelFrame(parent, text="Variable Check")
        
        self.var_target_var = tk.StringVar(value="npc")
        ttk.Label(self.var_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        var_target_frame = ttk.Frame(self.var_frame)
        var_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(var_target_frame, text="NPC", variable=self.var_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(var_target_frame, text="Player", variable=self.var_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.var_frame, text="Variable Name:").pack(anchor="w", padx=5, pady=2)
        self.var_name_entry = ttk.Entry(self.var_frame, width=40)
        self.var_name_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Context:").pack(anchor="w", padx=5, pady=2)
        self.var_context_entry = ttk.Entry(self.var_frame, width=40)
        self.var_context_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.var_value_entry = ttk.Entry(self.var_frame, width=40)
        self.var_value_entry.pack(fill="x", padx=5, pady=2)
        
        # Effect check fields
        self.effect_frame = ttk.LabelFrame(parent, text="Effect Check")
        
        self.effect_target_var = tk.StringVar(value="npc")
        ttk.Label(self.effect_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        effect_target_frame = ttk.Frame(self.effect_frame)
        effect_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(effect_target_frame, text="NPC", variable=self.effect_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(effect_target_frame, text="Player", variable=self.effect_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.effect_frame, text="Effect ID:").pack(anchor="w", padx=5, pady=2)
        self.effect_id_entry = ttk.Entry(self.effect_frame, width=40)
        self.effect_id_entry.pack(fill="x", padx=5, pady=2)
        
        # Gender check fields
        self.gender_frame = ttk.LabelFrame(parent, text="Gender Check")
        
        ttk.Label(self.gender_frame, text="Check:").pack(anchor="w", padx=5, pady=2)
        self.gender_check_var = tk.StringVar(value="npc_female")
        gender_check_frame = ttk.Frame(self.gender_frame)
        gender_check_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(gender_check_frame, text="NPC Female", variable=self.gender_check_var, value="npc_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="NPC Male", variable=self.gender_check_var, value="npc_male").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Female", variable=self.gender_check_var, value="u_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Male", variable=self.gender_check_var, value="u_male").pack(side="left", padx=5)
        
        # Environment fields
        self.env_frame = ttk.LabelFrame(parent, text="Environment Check")
        
        ttk.Label(self.env_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.env_type_var = tk.StringVar(value="days_since_cataclysm")
        env_type_combo = ttk.Combobox(self.env_frame, textvariable=self.env_type_var, 
                                     values=["days_since_cataclysm", "is_season", "is_day", "is_outside"], width=37)
        env_type_combo.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.env_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.env_value_entry = ttk.Entry(self.env_frame, width=40)
        self.env_value_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.env_frame, text="(For days: number, for season: spring/summer/autumn/winter)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        
        # Mission check fields
        self.mission_frame = ttk.LabelFrame(parent, text="Mission Check")
        
        ttk.Label(self.mission_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.mission_type_var = tk.StringVar(value="u_has_mission")
        mission_type_frame = ttk.Frame(self.mission_frame)
        mission_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(mission_type_frame, text="Player Has Mission", variable=self.mission_type_var, value="u_has_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has Assigned Mission", variable=self.mission_type_var, value="has_assigned_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Available Mission", variable=self.mission_type_var, value="has_no_available_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Assigned Mission", variable=self.mission_type_var, value="has_no_assigned_mission").pack(side="left", padx=5)
        
        # Mission ID entry (only shown for u_has_mission)
        self.mission_id_frame = ttk.Frame(self.mission_frame)
        ttk.Label(self.mission_id_frame, text="Mission ID:").pack(anchor="w", padx=5, pady=2)
        self.mission_id_entry = ttk.Entry(self.mission_id_frame, width=40)
        self.mission_id_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.mission_id_frame, text="(e.g., MISSION_BEGGAR_2_PERMISSION)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        # Don't pack initially - update_mission_ui will handle it when mission type is selected
        
        # Update mission UI when type changes
        self.mission_type_var.trace("w", lambda *args: self.update_mission_ui())
        
        # Boolean logic fields (nested support)
        self.logic_frame = ttk.LabelFrame(parent, text="Boolean Logic")
        
        ttk.Label(self.logic_frame, text="Logic Type:").pack(anchor="w", padx=5, pady=2)
        self.logic_type_var = tk.StringVar(value="and")
        logic_type_frame = ttk.Frame(self.logic_frame)
        logic_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(logic_type_frame, text="AND (all true)", variable=self.logic_type_var, value="and").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="OR (any true)", variable=self.logic_type_var, value="or").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="NOT (negate)", variable=self.logic_type_var, value="not").pack(side="left", padx=5)
        
        ttk.Label(self.logic_frame, text="Sub-conditions:").pack(anchor="w", padx=5, pady=2)
        
        # Listbox for sub-conditions
        list_frame = ttk.Frame(self.logic_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.sub_conditions_listbox = tk.Listbox(list_frame, height=4)
        sub_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.sub_conditions_listbox.yview)
        self.sub_conditions_listbox.configure(yscrollcommand=sub_scrollbar.set)
        self.sub_conditions_listbox.pack(side="left", fill="both", expand=True)
        sub_scrollbar.pack(side="right", fill="y")
        
        # Buttons for sub-conditions
        sub_btn_frame = ttk.Frame(self.logic_frame)
        sub_btn_frame.pack(fill="x", padx=5, pady=2)
        ttk.Button(sub_btn_frame, text="Add", command=lambda: self.edit_sub_condition()).pack(side="left", padx=2)
        ttk.Button(sub_btn_frame, text="Edit", command=lambda: self.edit_sub_condition()).pack(side="left", padx=2)
        ttk.Button(sub_btn_frame, text="Remove", command=self.remove_sub_condition).pack(side="left", padx=2)
        
        self.sub_conditions = []  # Store sub-conditions as dicts
        
        # Load current condition if present
        self.load_simple_condition(condition_dict)
        
        # Initial UI update
        self.update_simple_condition_ui(parent)
    
    def update_simple_condition_ui(self, parent):
        """Update which condition frame is visible"""
        self.var_frame.pack_forget()
        self.effect_frame.pack_forget()
        self.gender_frame.pack_forget()
        self.env_frame.pack_forget()
        self.mission_frame.pack_forget()
        self.logic_frame.pack_forget()
        
        cond_type = self.cond_type_var.get()
        if cond_type == "var":
            self.var_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "effect":
            self.effect_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "gender":
            self.gender_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "env":
            self.env_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "mission":
            self.mission_frame.pack(fill="x", padx=10, pady=5)
            self.update_mission_ui()
        elif cond_type == "logic":
            self.logic_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    def update_mission_ui(self):
        """Update mission UI to show/hide mission ID field based on check type"""
        if hasattr(self, 'mission_type_var'):
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                self.mission_id_frame.pack(fill="x", padx=5, pady=2)
            else:
                self.mission_id_frame.pack_forget()
    
    def load_simple_condition(self, condition_dict):
        """Load condition into simple editor"""
        if not condition_dict:
            return
        
        # Handle string conditions (e.g., "has_assigned_mission")
        if isinstance(condition_dict, str):
            if condition_dict in ["has_assigned_mission", "has_no_available_mission", "has_no_assigned_mission"]:
                self.cond_type_var.set("mission")
                self.mission_type_var.set(condition_dict)
                return
            else:
                # Unknown string condition, treat as dict format
                return
        
        # Check for variable checks
        if "npc_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("npc")
            var_info = condition_dict["npc_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
            else:
                self.var_name_entry.insert(0, str(var_info))
        elif "u_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("player")
            var_info = condition_dict["u_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
        # Check for effect checks
        elif "npc_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("npc")
            self.effect_id_entry.insert(0, str(condition_dict["npc_has_effect"]))
        elif "u_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("player")
            self.effect_id_entry.insert(0, str(condition_dict["u_has_effect"]))
        # Check for gender
        elif any(k in condition_dict for k in ["npc_female", "npc_male", "u_female", "u_male"]):
            self.cond_type_var.set("gender")
            for key in ["npc_female", "npc_male", "u_female", "u_male"]:
                if key in condition_dict:
                    self.gender_check_var.set(key)
                    break
        # Check for environment
        elif "days_since_cataclysm" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("days_since_cataclysm")
            self.env_value_entry.insert(0, str(condition_dict["days_since_cataclysm"]))
        elif "is_season" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("is_season")
            self.env_value_entry.insert(0, str(condition_dict["is_season"]))
        elif "is_day" in condition_dict or "is_outside" in condition_dict:
            self.cond_type_var.set("env")
            if "is_day" in condition_dict:
                self.env_type_var.set("is_day")
            else:
                self.env_type_var.set("is_outside")
        # Check for mission conditions
        elif "u_has_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("u_has_mission")
            mission_id = condition_dict["u_has_mission"]
            if isinstance(mission_id, dict):
                # If it's a dict, try to get the mission ID from it
                self.mission_id_entry.insert(0, str(mission_id.get("mission", mission_id.get("id", ""))))
            else:
                self.mission_id_entry.insert(0, str(mission_id))
        elif "has_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_assigned_mission")
        elif "has_no_available_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_available_mission")
        elif "has_no_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_assigned_mission")
        # Check for boolean logic
        elif "and" in condition_dict or "or" in condition_dict or "not" in condition_dict:
            self.cond_type_var.set("logic")
            if "and" in condition_dict:
                self.logic_type_var.set("and")
                self.sub_conditions = condition_dict["and"] if isinstance(condition_dict["and"], list) else [condition_dict["and"]]
            elif "or" in condition_dict:
                self.logic_type_var.set("or")
                self.sub_conditions = condition_dict["or"] if isinstance(condition_dict["or"], list) else [condition_dict["or"]]
            elif "not" in condition_dict:
                self.logic_type_var.set("not")
                self.sub_conditions = [condition_dict["not"]]
            self.refresh_sub_conditions_list()
    
    def refresh_sub_conditions_list(self):
        """Refresh the listbox showing sub-conditions"""
        self.sub_conditions_listbox.delete(0, tk.END)
        for i, cond in enumerate(self.sub_conditions):
            # Create a preview string
            preview = self.condition_preview(cond)
            self.sub_conditions_listbox.insert(tk.END, preview)
    
    def condition_preview(self, cond):
        """Create a preview string for a condition"""
        if isinstance(cond, dict):
            if "npc_has_var" in cond:
                var_info = cond["npc_has_var"]
                if isinstance(var_info, dict):
                    return f"NPC var: {var_info.get('var', var_info.get('name', ''))}"
                return f"NPC var: {var_info}"
            elif "u_has_var" in cond:
                var_info = cond["u_has_var"]
                if isinstance(var_info, dict):
                    return f"Player var: {var_info.get('var', var_info.get('name', ''))}"
                return f"Player var: {var_info}"
            elif "npc_has_effect" in cond:
                return f"NPC effect: {cond['npc_has_effect']}"
            elif "u_has_effect" in cond:
                return f"Player effect: {cond['u_has_effect']}"
            elif "and" in cond or "or" in cond or "not" in cond:
                logic_type = "and" if "and" in cond else ("or" if "or" in cond else "not")
                count = len(cond[logic_type]) if isinstance(cond[logic_type], list) else 1
                return f"{logic_type.upper()} ({count} conditions)"
            else:
                import json
                return json.dumps(cond, separators=(',', ':'))
        return str(cond)
    
    def edit_sub_condition(self, index=None):
        """Edit a sub-condition"""
        if index is None:
            selection = self.sub_conditions_listbox.curselection()
            if selection:
                index = selection[0]
                cond_data = self.sub_conditions[index]
            else:
                cond_data = None
        else:
            cond_data = self.sub_conditions[index] if 0 <= index < len(self.sub_conditions) else None
        
        # Open nested dialog
        dialog = SubConditionDialog(self.dialog, cond_data)
        if dialog.result:
            if index is not None:
                self.sub_conditions[index] = dialog.result
            else:
                self.sub_conditions.append(dialog.result)
            self.refresh_sub_conditions_list()
    
    def remove_sub_condition(self):
        """Remove selected sub-condition"""
        selection = self.sub_conditions_listbox.curselection()
        if selection:
            index = selection[0]
            del self.sub_conditions[index]
            self.refresh_sub_conditions_list()
    
    def get_simple_condition(self):
        """Build condition dict from simple editor"""
        cond_type = self.cond_type_var.get()
        
        if cond_type == "var":
            target = self.var_target_var.get()
            var_name = self.var_name_entry.get().strip()
            if not var_name:
                return None
            
            var_context = self.var_context_entry.get().strip()
            var_value = self.var_value_entry.get().strip()
            
            if var_context or var_value:
                # Full variable check (type is always "dialogue")
                var_dict = {"var": var_name} if "var" not in var_name else {"name": var_name}
                var_dict["type"] = "dialogue"
                if var_context:
                    var_dict["context"] = var_context
                if var_value:
                    var_dict["value"] = var_value
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_dict}
            else:
                # Simple variable check
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_name}
        
        elif cond_type == "effect":
            target = self.effect_target_var.get()
            effect_id = self.effect_id_entry.get().strip()
            if not effect_id:
                return None
            key = "npc_has_effect" if target == "npc" else "u_has_effect"
            return {key: effect_id}
        
        elif cond_type == "gender":
            gender_check = self.gender_check_var.get()
            return {gender_check: True}
        
        elif cond_type == "env":
            env_type = self.env_type_var.get()
            env_value = self.env_value_entry.get().strip()
            if env_type in ["is_day", "is_outside"]:
                return {env_type: True} if env_value.lower() in ["true", "1", "yes"] else {env_type: False}
            elif env_type == "days_since_cataclysm":
                try:
                    return {env_type: int(env_value)}
                except ValueError:
                    return {env_type: 0}
            elif env_type == "is_season":
                return {env_type: env_value}
        
        elif cond_type == "mission":
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                mission_id = self.mission_id_entry.get().strip()
                if not mission_id:
                    return None
                return {"u_has_mission": mission_id}
            else:
                # Boolean flags: has_assigned_mission, has_no_available_mission, has_no_assigned_mission
                return {mission_type: True}
        
        elif cond_type == "logic":
            logic_type = self.logic_type_var.get()
            if not self.sub_conditions:
                return None
            return {logic_type: self.sub_conditions}
        
        return None
    
    def ok_clicked(self):
        """Handle OK button"""
        # Check which tab is active
        notebook = self.dialog.nametowidget(self.dialog.winfo_children()[0])
        current_tab = notebook.index(notebook.select())
        
        if current_tab == 0:  # Simple tab
            self.result = self.get_simple_condition()
        else:  # Raw JSON tab
            raw_text = self.raw_text.get("1.0", tk.END).strip()
            if raw_text:
                try:
                    import json
                    self.result = json.loads(raw_text)
                except json.JSONDecodeError:
                    messagebox.showerror("Invalid JSON", "The JSON is invalid. Please fix it.")
                    return
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button"""
        self.dialog.destroy()


class DynamicLineDialog:
    """Dialog for editing a dynamic line (supports text and conditional logic)"""
    
    def __init__(self, parent, current_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Dynamic Line")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry("550x550")
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Simple Text tab
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="Simple Text")
        self.create_text_tab(text_frame, current_data)
        
        # Conditional tab
        conditional_frame = ttk.Frame(notebook)
        notebook.add(conditional_frame, text="Conditional")
        self.create_conditional_tab(conditional_frame, current_data)
        
        # Advanced tab (raw JSON)
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        self.create_advanced_dynamic_tab(advanced_frame, current_data)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_clicked).pack(side="left", padx=5)
        
        self.dialog.wait_window()
    
    def create_text_tab(self, parent, current_data):
        """Create simple text tab"""
        ttk.Label(parent, text="Dynamic Line Text:").pack(anchor="w", padx=10, pady=5)
        
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.text_widget = tk.Text(text_frame, width=50, height=8, wrap="word")
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        self.text_widget.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        # Load current data
        if current_data:
            if isinstance(current_data, str):
                self.text_widget.insert("1.0", current_data)
            elif isinstance(current_data, dict):
                # Show yes value if available
                self.text_widget.insert("1.0", current_data.get("yes", ""))
    
    def create_conditional_tab(self, parent, current_data):
        """Create conditional logic tab - supports any condition type"""
        # Notebook for Simple vs Advanced
        self.condition_notebook = ttk.Notebook(parent)
        self.condition_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Simple condition editor
        simple_cond_frame = ttk.Frame(self.condition_notebook)
        self.condition_notebook.add(simple_cond_frame, text="Simple")
        self.create_simple_condition_editor(simple_cond_frame, current_data)
        
        # Raw JSON editor
        raw_cond_frame = ttk.Frame(self.condition_notebook)
        self.condition_notebook.add(raw_cond_frame, text="Raw JSON")
        self.create_raw_condition_editor(raw_cond_frame, current_data)
        
        # Yes branch
        ttk.Label(parent, text="Yes Branch (when condition is true):", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        yes_frame = ttk.Frame(parent)
        yes_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.yes_text = tk.Text(yes_frame, width=40, height=3, wrap="word")
        yes_scrollbar = ttk.Scrollbar(yes_frame, orient="vertical", command=self.yes_text.yview)
        self.yes_text.configure(yscrollcommand=yes_scrollbar.set)
        
        self.yes_text.pack(side="left", fill="both", expand=True)
        yes_scrollbar.pack(side="right", fill="y")
        
        # No branch
        ttk.Label(parent, text="No Branch (when condition is false):", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(10, 5))
        no_frame = ttk.Frame(parent)
        no_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.no_text = tk.Text(no_frame, width=40, height=3, wrap="word")
        no_scrollbar = ttk.Scrollbar(no_frame, orient="vertical", command=self.no_text.yview)
        self.no_text.configure(yscrollcommand=no_scrollbar.set)
        
        self.no_text.pack(side="left", fill="both", expand=True)
        no_scrollbar.pack(side="right", fill="y")
        
        # Load current data if it's a dict
        if current_data and isinstance(current_data, dict):
            self.yes_text.insert("1.0", current_data.get("yes", ""))
            self.no_text.insert("1.0", current_data.get("no", ""))
    
    def create_simple_condition_editor(self, parent, current_data):
        """Create simple condition editor for common condition types"""
        # Extract condition from current_data if present
        condition_dict = {}
        if current_data:
            if isinstance(current_data, dict):
                # For dynamic lines, extract condition (everything except yes/no)
                # For responses, current_data IS the condition
                if "yes" in current_data or "no" in current_data:
                    condition_dict = {k: v for k, v in current_data.items() if k not in ["yes", "no"]}
                else:
                    condition_dict = current_data
            else:
                condition_dict = current_data
        
        # Condition type selector
        ttk.Label(parent, text="Condition Type:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.cond_type_var = tk.StringVar(value="simple")
        self.cond_type_var.trace("w", lambda *args: self.update_simple_condition_ui(parent))
        
        cond_type_frame = ttk.Frame(parent)
        cond_type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(cond_type_frame, text="Variable Check", variable=self.cond_type_var, value="var").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Effect Check", variable=self.cond_type_var, value="effect").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Gender Check", variable=self.cond_type_var, value="gender").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Environment", variable=self.cond_type_var, value="env").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Mission Check", variable=self.cond_type_var, value="mission").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Boolean Logic", variable=self.cond_type_var, value="logic").pack(side="left", padx=5)
        
        # Variable check fields
        self.var_frame = ttk.LabelFrame(parent, text="Variable Check")
        self.var_frame.pack(fill="x", padx=10, pady=5)
        
        self.var_target_var = tk.StringVar(value="npc")
        ttk.Label(self.var_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        var_target_frame = ttk.Frame(self.var_frame)
        var_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(var_target_frame, text="NPC", variable=self.var_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(var_target_frame, text="Player", variable=self.var_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.var_frame, text="Variable Name:").pack(anchor="w", padx=5, pady=2)
        self.var_name_entry = ttk.Entry(self.var_frame, width=40)
        self.var_name_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Context:").pack(anchor="w", padx=5, pady=2)
        self.var_context_entry = ttk.Entry(self.var_frame, width=40)
        self.var_context_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.var_value_entry = ttk.Entry(self.var_frame, width=40)
        self.var_value_entry.pack(fill="x", padx=5, pady=2)
        
        # Effect check fields
        self.effect_frame = ttk.LabelFrame(parent, text="Effect Check")
        
        self.effect_target_var = tk.StringVar(value="npc")
        ttk.Label(self.effect_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        effect_target_frame = ttk.Frame(self.effect_frame)
        effect_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(effect_target_frame, text="NPC", variable=self.effect_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(effect_target_frame, text="Player", variable=self.effect_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.effect_frame, text="Effect ID:").pack(anchor="w", padx=5, pady=2)
        self.effect_id_entry = ttk.Entry(self.effect_frame, width=40)
        self.effect_id_entry.pack(fill="x", padx=5, pady=2)
        
        # Gender check fields
        self.gender_frame = ttk.LabelFrame(parent, text="Gender Check")
        
        ttk.Label(self.gender_frame, text="Check:").pack(anchor="w", padx=5, pady=2)
        self.gender_check_var = tk.StringVar(value="npc_female")
        gender_check_frame = ttk.Frame(self.gender_frame)
        gender_check_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(gender_check_frame, text="NPC Female", variable=self.gender_check_var, value="npc_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="NPC Male", variable=self.gender_check_var, value="npc_male").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Female", variable=self.gender_check_var, value="u_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Male", variable=self.gender_check_var, value="u_male").pack(side="left", padx=5)
        
        # Environment fields
        self.env_frame = ttk.LabelFrame(parent, text="Environment Check")
        
        ttk.Label(self.env_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.env_type_var = tk.StringVar(value="days_since_cataclysm")
        env_type_combo = ttk.Combobox(self.env_frame, textvariable=self.env_type_var, 
                                     values=["days_since_cataclysm", "is_season", "is_day", "is_outside"], width=37)
        env_type_combo.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.env_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.env_value_entry = ttk.Entry(self.env_frame, width=40)
        self.env_value_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.env_frame, text="(For days: number, for season: spring/summer/autumn/winter)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        
        # Mission check fields
        self.mission_frame = ttk.LabelFrame(parent, text="Mission Check")
        
        ttk.Label(self.mission_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.mission_type_var = tk.StringVar(value="u_has_mission")
        mission_type_frame = ttk.Frame(self.mission_frame)
        mission_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(mission_type_frame, text="Player Has Mission", variable=self.mission_type_var, value="u_has_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has Assigned Mission", variable=self.mission_type_var, value="has_assigned_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Available Mission", variable=self.mission_type_var, value="has_no_available_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Assigned Mission", variable=self.mission_type_var, value="has_no_assigned_mission").pack(side="left", padx=5)
        
        # Mission ID entry (only shown for u_has_mission)
        self.mission_id_frame = ttk.Frame(self.mission_frame)
        ttk.Label(self.mission_id_frame, text="Mission ID:").pack(anchor="w", padx=5, pady=2)
        self.mission_id_entry = ttk.Entry(self.mission_id_frame, width=40)
        self.mission_id_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.mission_id_frame, text="(e.g., MISSION_BEGGAR_2_PERMISSION)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        # Don't pack initially - update_mission_ui will handle it when mission type is selected
        
        # Update mission UI when type changes
        self.mission_type_var.trace("w", lambda *args: self.update_mission_ui())
        
        # Boolean logic fields
        self.logic_frame = ttk.LabelFrame(parent, text="Boolean Logic")
        
        ttk.Label(self.logic_frame, text="Logic Type:").pack(anchor="w", padx=5, pady=2)
        self.logic_type_var = tk.StringVar(value="and")
        logic_type_frame = ttk.Frame(self.logic_frame)
        logic_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(logic_type_frame, text="AND (all true)", variable=self.logic_type_var, value="and").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="OR (any true)", variable=self.logic_type_var, value="or").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="NOT (negate)", variable=self.logic_type_var, value="not").pack(side="left", padx=5)
        
        ttk.Label(self.logic_frame, text="Sub-conditions:").pack(anchor="w", padx=5, pady=2)
        
        # Listbox for sub-conditions
        list_frame = ttk.Frame(self.logic_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.logic_conditions_listbox = tk.Listbox(list_frame, height=4)
        logic_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.logic_conditions_listbox.yview)
        self.logic_conditions_listbox.configure(yscrollcommand=logic_scrollbar.set)
        self.logic_conditions_listbox.pack(side="left", fill="both", expand=True)
        logic_scrollbar.pack(side="right", fill="y")
        
        # Buttons for sub-conditions
        logic_btn_frame = ttk.Frame(self.logic_frame)
        logic_btn_frame.pack(fill="x", padx=5, pady=2)
        ttk.Button(logic_btn_frame, text="Add", command=self.add_logic_sub_condition).pack(side="left", padx=2)
        ttk.Button(logic_btn_frame, text="Edit", command=self.edit_logic_sub_condition).pack(side="left", padx=2)
        ttk.Button(logic_btn_frame, text="Remove", command=self.remove_logic_sub_condition).pack(side="left", padx=2)
        
        self.logic_sub_conditions = []  # Store sub-conditions as dicts
        
        # Load current condition if present
        self.load_simple_condition(condition_dict)
        
        # Initial UI update
        self.update_simple_condition_ui(parent)
    
    def update_simple_condition_ui(self, parent):
        """Update which condition frame is visible"""
        self.var_frame.pack_forget()
        self.effect_frame.pack_forget()
        self.gender_frame.pack_forget()
        self.env_frame.pack_forget()
        self.mission_frame.pack_forget()
        self.logic_frame.pack_forget()
        
        cond_type = self.cond_type_var.get()
        if cond_type == "var":
            self.var_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "effect":
            self.effect_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "gender":
            self.gender_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "env":
            self.env_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "mission":
            self.mission_frame.pack(fill="x", padx=10, pady=5)
            self.update_mission_ui()
        elif cond_type == "logic":
            self.logic_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    def update_mission_ui(self):
        """Update mission UI to show/hide mission ID field based on check type"""
        if hasattr(self, 'mission_type_var'):
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                self.mission_id_frame.pack(fill="x", padx=5, pady=2)
            else:
                self.mission_id_frame.pack_forget()
    
    def load_simple_condition(self, condition_dict):
        """Load condition into simple editor"""
        if not condition_dict:
            return
        
        # Handle string conditions (e.g., "has_assigned_mission")
        if isinstance(condition_dict, str):
            if condition_dict in ["has_assigned_mission", "has_no_available_mission", "has_no_assigned_mission"]:
                self.cond_type_var.set("mission")
                self.mission_type_var.set(condition_dict)
                return
            else:
                # Unknown string condition, treat as dict format
                return
        
        # Check for variable checks
        if "npc_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("npc")
            var_info = condition_dict["npc_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
            else:
                # Handle flattened structure where type/context/value are at same level
                self.var_name_entry.insert(0, str(var_info))
                # Check if type/context/value are at the same level as npc_has_var
                # Note: type is always "dialogue" so we don't load it
                if "context" in condition_dict:
                    self.var_context_entry.insert(0, str(condition_dict.get("context", "")))
                if "value" in condition_dict:
                    self.var_value_entry.insert(0, str(condition_dict.get("value", "")))
        elif "u_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("player")
            var_info = condition_dict["u_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
            else:
                # Handle flattened structure where type/context/value are at same level
                self.var_name_entry.insert(0, str(var_info))
                # Check if type/context/value are at the same level as u_has_var
                if "type" in condition_dict:
                    self.var_type_entry.insert(0, str(condition_dict.get("type", "")))
                if "context" in condition_dict:
                    self.var_context_entry.insert(0, str(condition_dict.get("context", "")))
                if "value" in condition_dict:
                    self.var_value_entry.insert(0, str(condition_dict.get("value", "")))
        # Check for effect checks
        elif "npc_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("npc")
            self.effect_id_entry.insert(0, str(condition_dict["npc_has_effect"]))
        elif "u_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("player")
            self.effect_id_entry.insert(0, str(condition_dict["u_has_effect"]))
        # Check for gender
        elif any(k in condition_dict for k in ["npc_female", "npc_male", "u_female", "u_male"]):
            self.cond_type_var.set("gender")
            for key in ["npc_female", "npc_male", "u_female", "u_male"]:
                if key in condition_dict:
                    self.gender_check_var.set(key)
                    break
        # Check for environment
        elif "days_since_cataclysm" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("days_since_cataclysm")
            self.env_value_entry.insert(0, str(condition_dict["days_since_cataclysm"]))
        elif "is_season" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("is_season")
            self.env_value_entry.insert(0, str(condition_dict["is_season"]))
        elif "is_day" in condition_dict or "is_outside" in condition_dict:
            self.cond_type_var.set("env")
            if "is_day" in condition_dict:
                self.env_type_var.set("is_day")
            else:
                self.env_type_var.set("is_outside")
        # Check for mission conditions
        elif "u_has_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("u_has_mission")
            mission_id = condition_dict["u_has_mission"]
            if isinstance(mission_id, dict):
                # If it's a dict, try to get the mission ID from it
                self.mission_id_entry.insert(0, str(mission_id.get("mission", mission_id.get("id", ""))))
            else:
                self.mission_id_entry.insert(0, str(mission_id))
        elif "has_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_assigned_mission")
        elif "has_no_available_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_available_mission")
        elif "has_no_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_assigned_mission")
        # Check for boolean logic
        elif "and" in condition_dict or "or" in condition_dict or "not" in condition_dict:
            self.cond_type_var.set("logic")
            if "and" in condition_dict:
                self.logic_type_var.set("and")
                self.logic_sub_conditions = condition_dict["and"] if isinstance(condition_dict["and"], list) else [condition_dict["and"]]
            elif "or" in condition_dict:
                self.logic_type_var.set("or")
                self.logic_sub_conditions = condition_dict["or"] if isinstance(condition_dict["or"], list) else [condition_dict["or"]]
            elif "not" in condition_dict:
                self.logic_type_var.set("not")
                self.logic_sub_conditions = [condition_dict["not"]]
            self.refresh_logic_sub_conditions_list()
    
    def get_simple_condition(self):
        """Build condition dict from simple editor"""
        cond_type = self.cond_type_var.get()
        
        if cond_type == "var":
            target = self.var_target_var.get()
            var_name = self.var_name_entry.get().strip()
            if not var_name:
                return None
            
            var_context = self.var_context_entry.get().strip()
            var_value = self.var_value_entry.get().strip()
            
            if var_context or var_value:
                # Full variable check (type is always "dialogue")
                var_dict = {"var": var_name} if "var" not in var_name else {"name": var_name}
                var_dict["type"] = "dialogue"
                if var_context:
                    var_dict["context"] = var_context
                if var_value:
                    var_dict["value"] = var_value
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_dict}
            else:
                # Simple variable check
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_name}
        
        elif cond_type == "effect":
            target = self.effect_target_var.get()
            effect_id = self.effect_id_entry.get().strip()
            if not effect_id:
                return None
            key = "npc_has_effect" if target == "npc" else "u_has_effect"
            return {key: effect_id}
        
        elif cond_type == "gender":
            gender_check = self.gender_check_var.get()
            return {gender_check: True}
        
        elif cond_type == "env":
            env_type = self.env_type_var.get()
            env_value = self.env_value_entry.get().strip()
            if env_type in ["is_day", "is_outside"]:
                return {env_type: True} if env_value.lower() in ["true", "1", "yes"] else {env_type: False}
            elif env_type == "days_since_cataclysm":
                try:
                    return {env_type: int(env_value)}
                except ValueError:
                    return {env_type: 0}
            elif env_type == "is_season":
                return {env_type: env_value}
        
        elif cond_type == "mission":
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                mission_id = self.mission_id_entry.get().strip()
                if not mission_id:
                    return None
                return {"u_has_mission": mission_id}
            else:
                # Boolean flags: has_assigned_mission, has_no_available_mission, has_no_assigned_mission
                return {mission_type: True}
        
        elif cond_type == "logic":
            logic_type = self.logic_type_var.get()
            if not self.logic_sub_conditions:
                return None
            return {logic_type: self.logic_sub_conditions}
        
        return None
    
    def refresh_logic_sub_conditions_list(self):
        """Refresh the listbox showing logic sub-conditions"""
        if not hasattr(self, 'logic_conditions_listbox'):
            return
        self.logic_conditions_listbox.delete(0, tk.END)
        for cond in self.logic_sub_conditions:
            preview = self.condition_preview(cond)
            self.logic_conditions_listbox.insert(tk.END, preview)
    
    def condition_preview(self, cond):
        """Create a preview string for a condition"""
        if isinstance(cond, dict):
            if "npc_has_var" in cond:
                var_info = cond["npc_has_var"]
                if isinstance(var_info, dict):
                    return f"NPC var: {var_info.get('var', var_info.get('name', ''))}"
                return f"NPC var: {var_info}"
            elif "u_has_var" in cond:
                var_info = cond["u_has_var"]
                if isinstance(var_info, dict):
                    return f"Player var: {var_info.get('var', var_info.get('name', ''))}"
                return f"Player var: {var_info}"
            elif "npc_has_effect" in cond:
                return f"NPC effect: {cond['npc_has_effect']}"
            elif "u_has_effect" in cond:
                return f"Player effect: {cond['u_has_effect']}"
            elif "npc_female" in cond or "npc_male" in cond or "u_female" in cond or "u_male" in cond:
                for key in ["npc_female", "npc_male", "u_female", "u_male"]:
                    if key in cond:
                        return key.replace("_", " ").title()
            elif "days_since_cataclysm" in cond:
                return f"Days since cataclysm: {cond['days_since_cataclysm']}"
            elif "is_season" in cond:
                return f"Season: {cond['is_season']}"
            elif "is_day" in cond:
                return "Is day: True" if cond.get("is_day") else "Is day: False"
            elif "is_outside" in cond:
                return "Is outside: True" if cond.get("is_outside") else "Is outside: False"
            elif "u_has_mission" in cond:
                mission_id = cond["u_has_mission"]
                if isinstance(mission_id, dict):
                    mission_id = mission_id.get("mission", mission_id.get("id", ""))
                return f"Player has mission: {mission_id}"
            elif "has_assigned_mission" in cond:
                return "Has assigned mission"
            elif "has_no_available_mission" in cond:
                return "Has no available mission"
            elif "has_no_assigned_mission" in cond:
                return "Has no assigned mission"
            elif "and" in cond or "or" in cond or "not" in cond:
                logic_type = "and" if "and" in cond else ("or" if "or" in cond else "not")
                count = len(cond[logic_type]) if isinstance(cond[logic_type], list) else 1
                return f"{logic_type.upper()} ({count} conditions)"
            else:
                import json
                return json.dumps(cond, separators=(',', ':'))
        return str(cond)
    
    def add_logic_sub_condition(self):
        """Add a new sub-condition"""
        dialog = SubConditionDialog(self.dialog, None)
        if dialog.result:
            self.logic_sub_conditions.append(dialog.result)
            self.refresh_logic_sub_conditions_list()
    
    def edit_logic_sub_condition(self):
        """Edit selected sub-condition"""
        selection = self.logic_conditions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a sub-condition to edit.")
            return
        index = selection[0]
        cond_data = self.logic_sub_conditions[index]
        
        dialog = SubConditionDialog(self.dialog, cond_data)
        if dialog.result:
            self.logic_sub_conditions[index] = dialog.result
            self.refresh_logic_sub_conditions_list()
    
    def remove_logic_sub_condition(self):
        """Remove selected sub-condition"""
        selection = self.logic_conditions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a sub-condition to remove.")
            return
        index = selection[0]
        del self.logic_sub_conditions[index]
        self.refresh_logic_sub_conditions_list()
    
    def create_raw_condition_editor(self, parent, current_data):
        """Create raw JSON condition editor"""
        ttk.Label(parent, text="Condition (Raw JSON):", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        condition_frame = ttk.Frame(parent)
        condition_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.condition_text = tk.Text(condition_frame, width=50, height=8, wrap="word", font=("Courier", 9))
        condition_scrollbar = ttk.Scrollbar(condition_frame, orient="vertical", command=self.condition_text.yview)
        self.condition_text.configure(yscrollcommand=condition_scrollbar.set)
        
        self.condition_text.pack(side="left", fill="both", expand=True)
        condition_scrollbar.pack(side="right", fill="y")
        
        # Load current condition if it's a dict
        if current_data and isinstance(current_data, dict):
            # Extract condition from dict (everything except yes/no)
            condition_dict = {k: v for k, v in current_data.items() if k not in ["yes", "no"]}
            if condition_dict:
                import json
                self.condition_text.insert("1.0", json.dumps(condition_dict, indent=2))
    
    def create_advanced_dynamic_tab(self, parent, current_data):
        """Create advanced tab for raw JSON editing"""
        ttk.Label(parent, text="Raw JSON (for complex conditional logic):").pack(anchor="w", padx=10, pady=5)
        
        json_frame = ttk.Frame(parent)
        json_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.advanced_json_text = tk.Text(json_frame, width=50, height=12, wrap="none", font=("Courier", 9))
        json_scrollbar_v = ttk.Scrollbar(json_frame, orient="vertical", command=self.advanced_json_text.yview)
        json_scrollbar_h = ttk.Scrollbar(json_frame, orient="horizontal", command=self.advanced_json_text.xview)
        self.advanced_json_text.configure(yscrollcommand=json_scrollbar_v.set, xscrollcommand=json_scrollbar_h.set)
        
        self.advanced_json_text.grid(row=0, column=0, sticky="nsew")
        json_scrollbar_v.grid(row=0, column=1, sticky="ns")
        json_scrollbar_h.grid(row=1, column=0, sticky="ew")
        json_frame.grid_rowconfigure(0, weight=1)
        json_frame.grid_columnconfigure(0, weight=1)
        
        if current_data:
            import json
            if isinstance(current_data, dict):
                self.advanced_json_text.insert("1.0", json.dumps(current_data, indent=2))
            elif isinstance(current_data, str):
                # Show as JSON string
                self.advanced_json_text.insert("1.0", json.dumps(current_data))
    
    def ok_clicked(self):
        """Handle OK button"""
        notebook = None
        for widget in self.dialog.winfo_children():
            if isinstance(widget, ttk.Notebook):
                notebook = widget
                break
        
        if not notebook:
            return
        
        current_tab = notebook.index(notebook.select())
        
        if current_tab == 0:
            # Simple text tab
            text = self.text_widget.get("1.0", tk.END).strip()
            if not text:
                tk.messagebox.showwarning("Invalid Input", "Dynamic line text cannot be empty")
                return
            self.result = text
            
        elif current_tab == 1:
            # Conditional tab - check which sub-tab is active (Simple or Raw JSON)
            yes_text = self.yes_text.get("1.0", tk.END).strip()
            no_text = self.no_text.get("1.0", tk.END).strip()
            
            # Yes and no branches are optional - only include if they have content
            # Get condition from either Simple or Raw JSON tab
            condition_dict = None
            if hasattr(self, 'condition_notebook') and self.condition_notebook:
                cond_tab_index = self.condition_notebook.index(self.condition_notebook.select())
                if cond_tab_index == 0:
                    # Simple tab
                    condition_dict = self.get_simple_condition()
                    if condition_dict is None:
                        tk.messagebox.showwarning("Invalid Input", "Please fill in the condition fields")
                        return
                else:
                    # Raw JSON tab
                    condition_json = self.condition_text.get("1.0", tk.END).strip()
                    if not condition_json:
                        tk.messagebox.showwarning("Invalid Input", "Condition is required")
                        return
                    
                    try:
                        import json
                        condition_dict = json.loads(condition_json)
                        if not isinstance(condition_dict, dict):
                            tk.messagebox.showerror("Invalid Format", "Condition must be a JSON object")
                            return
                    except json.JSONDecodeError as e:
                        tk.messagebox.showerror("Invalid JSON", f"Condition JSON error: {str(e)}")
                        return
            else:
                # Fallback to raw JSON
                condition_json = self.condition_text.get("1.0", tk.END).strip()
                if not condition_json:
                    tk.messagebox.showwarning("Invalid Input", "Condition is required")
                    return
                
                try:
                    import json
                    condition_dict = json.loads(condition_json)
                    if not isinstance(condition_dict, dict):
                        tk.messagebox.showerror("Invalid Format", "Condition must be a JSON object")
                        return
                except json.JSONDecodeError as e:
                    tk.messagebox.showerror("Invalid JSON", f"Condition JSON error: {str(e)}")
                    return
            
            # Build result dict with condition + yes/no (optional branches)
            result_dict = condition_dict.copy()
            if yes_text:
                result_dict["yes"] = yes_text
            if no_text:
                result_dict["no"] = no_text
            
            self.result = result_dict
            
        else:
            # Advanced tab - raw JSON
            json_text = self.advanced_json_text.get("1.0", tk.END).strip()
            if not json_text:
                tk.messagebox.showwarning("Invalid Input", "JSON cannot be empty")
                return
            
            try:
                import json
                parsed = json.loads(json_text)
                if isinstance(parsed, str):
                    self.result = parsed
                elif isinstance(parsed, dict):
                    self.result = parsed
                elif isinstance(parsed, list):
                    # List of strings
                    self.result = parsed
                else:
                    tk.messagebox.showerror("Invalid Format", "JSON must be a string, object, or array")
                    return
            except json.JSONDecodeError as e:
                tk.messagebox.showerror("Invalid JSON", f"JSON parsing error: {str(e)}")
                return
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button"""
        self.dialog.destroy()


class SpeakerEffectDialog:
    """Dialog for editing speaker effect"""
    
    def __init__(self, parent, current_data=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Speaker Effect")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry("500x500")
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Simple tab
        simple_frame = ttk.Frame(notebook)
        notebook.add(simple_frame, text="Simple")
        self.create_simple_tab(simple_frame, current_data)
        
        # Advanced tab (raw JSON)
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        self.create_advanced_tab(advanced_frame, current_data)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_clicked).pack(side="left", padx=5)
        
        self.dialog.wait_window()
    
    def create_simple_tab(self, parent, current_data):
        """Create simple speaker effect editor"""
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
        
        # Effect type selector
        ttk.Label(scrollable_frame, text="Effect Type:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.effect_type_var = tk.StringVar(value="npc_add_var")
        effect_type_frame = ttk.Frame(scrollable_frame)
        effect_type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(effect_type_frame, text="NPC Add Var", variable=self.effect_type_var, value="npc_add_var").pack(side="left", padx=5)
        ttk.Radiobutton(effect_type_frame, text="Player Adjust Var", variable=self.effect_type_var, value="u_adjust_var").pack(side="left", padx=5)
        ttk.Radiobutton(effect_type_frame, text="NPC Add Effect", variable=self.effect_type_var, value="npc_add_effect").pack(side="left", padx=5)
        ttk.Radiobutton(effect_type_frame, text="Player Add Effect", variable=self.effect_type_var, value="u_add_effect").pack(side="left", padx=5)
        ttk.Radiobutton(effect_type_frame, text="Mapgen Update", variable=self.effect_type_var, value="mapgen_update").pack(side="left", padx=5)
        
        # NPC Add Var fields
        self.npc_add_var_frame = ttk.LabelFrame(scrollable_frame, text="NPC Add Var")
        self.npc_add_var_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.npc_add_var_frame, text="Variable Name:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_var_name_entry = ttk.Entry(self.npc_add_var_frame, width=40)
        self.npc_add_var_name_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.npc_add_var_frame, text="Type:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_var_type_entry = ttk.Entry(self.npc_add_var_frame, width=40)
        self.npc_add_var_type_entry.insert(0, "dialogue")
        self.npc_add_var_type_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.npc_add_var_frame, text="Context:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_var_context_entry = ttk.Entry(self.npc_add_var_frame, width=40)
        self.npc_add_var_context_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.npc_add_var_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_var_value_entry = ttk.Entry(self.npc_add_var_frame, width=40)
        self.npc_add_var_value_entry.pack(fill="x", padx=5, pady=2)
        
        # Player Adjust Var fields
        self.u_adjust_var_frame = ttk.LabelFrame(scrollable_frame, text="Player Adjust Var")
        self.u_adjust_var_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.u_adjust_var_frame, text="Variable Name:").pack(anchor="w", padx=5, pady=2)
        self.u_adjust_var_name_entry = ttk.Entry(self.u_adjust_var_frame, width=40)
        self.u_adjust_var_name_entry.pack(fill="x", padx=5, pady=2)
        
        # NPC Add Effect fields
        self.npc_add_effect_frame = ttk.LabelFrame(scrollable_frame, text="NPC Add Effect")
        self.npc_add_effect_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.npc_add_effect_frame, text="Effect ID:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_effect_id_entry = ttk.Entry(self.npc_add_effect_frame, width=40)
        self.npc_add_effect_id_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.npc_add_effect_frame, text="Duration:").pack(anchor="w", padx=5, pady=2)
        self.npc_add_effect_duration_entry = ttk.Entry(self.npc_add_effect_frame, width=40)
        self.npc_add_effect_duration_entry.pack(fill="x", padx=5, pady=2)
        
        # Player Add Effect fields
        self.u_add_effect_frame = ttk.LabelFrame(scrollable_frame, text="Player Add Effect")
        self.u_add_effect_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.u_add_effect_frame, text="Effect ID:").pack(anchor="w", padx=5, pady=2)
        self.u_add_effect_id_entry = ttk.Entry(self.u_add_effect_frame, width=40)
        self.u_add_effect_id_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.u_add_effect_frame, text="Duration:").pack(anchor="w", padx=5, pady=2)
        self.u_add_effect_duration_entry = ttk.Entry(self.u_add_effect_frame, width=40)
        self.u_add_effect_duration_entry.pack(fill="x", padx=5, pady=2)
        
        # Mapgen Update fields
        self.mapgen_frame = ttk.LabelFrame(scrollable_frame, text="Mapgen Update")
        self.mapgen_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.mapgen_frame, text="Note: Mapgen updates require complex JSON. Use Advanced tab.").pack(anchor="w", padx=5, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load current data
        self.load_simple_effect(current_data)
        
        # Update UI based on effect type
        self.effect_type_var.trace("w", lambda *args: self.update_simple_ui(scrollable_frame))
        self.update_simple_ui(scrollable_frame)
    
    def update_simple_ui(self, parent):
        """Update which effect frame is visible"""
        self.npc_add_var_frame.pack_forget()
        self.u_adjust_var_frame.pack_forget()
        self.npc_add_effect_frame.pack_forget()
        self.u_add_effect_frame.pack_forget()
        self.mapgen_frame.pack_forget()
        
        effect_type = self.effect_type_var.get()
        if effect_type == "npc_add_var":
            self.npc_add_var_frame.pack(fill="x", padx=10, pady=5)
        elif effect_type == "u_adjust_var":
            self.u_adjust_var_frame.pack(fill="x", padx=10, pady=5)
        elif effect_type == "npc_add_effect":
            self.npc_add_effect_frame.pack(fill="x", padx=10, pady=5)
        elif effect_type == "u_add_effect":
            self.u_add_effect_frame.pack(fill="x", padx=10, pady=5)
        elif effect_type == "mapgen_update":
            self.mapgen_frame.pack(fill="x", padx=10, pady=5)
    
    def load_simple_effect(self, current_data):
        """Load effect into simple editor"""
        if not current_data:
            return
        
        # Handle effect wrapper: { "effect": { ... } }
        if isinstance(current_data, dict) and "effect" in current_data:
            current_data = current_data["effect"]
        
        if isinstance(current_data, dict):
            if "npc_add_var" in current_data:
                self.effect_type_var.set("npc_add_var")
                var_data = current_data.get("npc_add_var")
                if isinstance(var_data, dict):
                    self.npc_add_var_name_entry.insert(0, str(var_data.get("var", var_data.get("name", ""))))
                    self.npc_add_var_type_entry.delete(0, tk.END)
                    self.npc_add_var_type_entry.insert(0, str(var_data.get("type", "dialogue")))
                    self.npc_add_var_context_entry.insert(0, str(var_data.get("context", "")))
                    self.npc_add_var_value_entry.insert(0, str(var_data.get("value", "")))
                else:
                    # Handle flattened structure where type/context/value are at same level
                    self.npc_add_var_name_entry.insert(0, str(var_data))
                    # Check if type/context/value are at the same level as npc_add_var
                    if "type" in current_data:
                        self.npc_add_var_type_entry.delete(0, tk.END)
                        self.npc_add_var_type_entry.insert(0, str(current_data.get("type", "dialogue")))
                    if "context" in current_data:
                        self.npc_add_var_context_entry.insert(0, str(current_data.get("context", "")))
                    if "value" in current_data:
                        self.npc_add_var_value_entry.insert(0, str(current_data.get("value", "")))
            elif "u_adjust_var" in current_data:
                self.effect_type_var.set("u_adjust_var")
                self.u_adjust_var_name_entry.insert(0, str(current_data.get("u_adjust_var", "")))
            elif "npc_add_effect" in current_data:
                self.effect_type_var.set("npc_add_effect")
                effect_info = current_data.get("npc_add_effect")
                if isinstance(effect_info, dict):
                    self.npc_add_effect_id_entry.insert(0, str(effect_info.get("id", effect_info.get("effect_id", ""))))
                    self.npc_add_effect_duration_entry.insert(0, str(effect_info.get("duration", "")))
                else:
                    self.npc_add_effect_id_entry.insert(0, str(effect_info))
                    # Check if duration is at same level
                    if "duration" in current_data:
                        self.npc_add_effect_duration_entry.insert(0, str(current_data.get("duration", "")))
            elif "u_add_effect" in current_data:
                self.effect_type_var.set("u_add_effect")
                effect_info = current_data.get("u_add_effect")
                if isinstance(effect_info, dict):
                    self.u_add_effect_id_entry.insert(0, str(effect_info.get("id", effect_info.get("effect_id", ""))))
                    self.u_add_effect_duration_entry.insert(0, str(effect_info.get("duration", "")))
                else:
                    self.u_add_effect_id_entry.insert(0, str(effect_info))
                    # Check if duration is at same level
                    if "duration" in current_data:
                        self.u_add_effect_duration_entry.insert(0, str(current_data.get("duration", "")))
            elif "mapgen_update" in current_data:
                self.effect_type_var.set("mapgen_update")
    
    def get_simple_effect(self):
        """Build effect dict from simple editor"""
        effect_type = self.effect_type_var.get()
        
        if effect_type == "npc_add_var":
            name = self.npc_add_var_name_entry.get().strip()
            if not name:
                return None
            
            # Build flattened structure (type/context/value as siblings of npc_add_var)
            var_dict = {"npc_add_var": name}
            
            var_type = self.npc_add_var_type_entry.get().strip()
            if var_type:
                var_dict["type"] = var_type
            
            context = self.npc_add_var_context_entry.get().strip()
            if context:
                var_dict["context"] = context
            
            value = self.npc_add_var_value_entry.get().strip()
            if value:
                var_dict["value"] = value
            
            return var_dict
        
        elif effect_type == "u_adjust_var":
            name = self.u_adjust_var_name_entry.get().strip()
            if not name:
                return None
            return {"u_adjust_var": name}
        
        elif effect_type == "npc_add_effect":
            effect_id = self.npc_add_effect_id_entry.get().strip()
            if not effect_id:
                return None
            
            # Build flattened structure (duration as sibling of npc_add_effect)
            effect_dict = {"npc_add_effect": effect_id}
            
            duration = self.npc_add_effect_duration_entry.get().strip()
            if duration:
                try:
                    effect_dict["duration"] = int(duration) if duration.upper() != "PERMANENT" else "PERMANENT"
                except ValueError:
                    effect_dict["duration"] = duration
            
            return effect_dict
        
        elif effect_type == "u_add_effect":
            effect_id = self.u_add_effect_id_entry.get().strip()
            if not effect_id:
                return None
            
            # Build flattened structure (duration as sibling of u_add_effect)
            effect_dict = {"u_add_effect": effect_id}
            
            duration = self.u_add_effect_duration_entry.get().strip()
            if duration:
                try:
                    effect_dict["duration"] = int(duration) if duration.upper() != "PERMANENT" else "PERMANENT"
                except ValueError:
                    effect_dict["duration"] = duration
            
            return effect_dict
        
        elif effect_type == "mapgen_update":
            # Mapgen updates are complex - user should use Advanced tab
            return None
        
        return None
    
    def create_advanced_tab(self, parent, current_data):
        """Create advanced (raw JSON) tab"""
        ttk.Label(parent, text="Speaker Effect (Raw JSON):", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.advanced_text = tk.Text(text_frame, wrap="word", font=("Courier", 9))
        advanced_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.advanced_text.yview)
        self.advanced_text.configure(yscrollcommand=advanced_scrollbar.set)
        self.advanced_text.pack(side="left", fill="both", expand=True)
        advanced_scrollbar.pack(side="right", fill="y")
        
        if current_data:
            import json
            self.advanced_text.insert("1.0", json.dumps(current_data, indent=2))
    
    def ok_clicked(self):
        """Handle OK button"""
        # Check which tab is active
        notebook = self.dialog.nametowidget(self.dialog.winfo_children()[0])
        current_tab = notebook.index(notebook.select())
        
        if current_tab == 0:  # Simple tab
            self.result = self.get_simple_effect()
        else:  # Advanced tab
            raw_text = self.advanced_text.get("1.0", tk.END).strip()
            if raw_text:
                try:
                    import json
                    self.result = json.loads(raw_text)
                except json.JSONDecodeError:
                    messagebox.showerror("Invalid JSON", "The JSON is invalid. Please fix it.")
                    return
            else:
                self.result = None
        
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button"""
        self.dialog.destroy()


class ResponseDialog:
    """Dialog for editing a response"""
    
    def __init__(self, parent, dialogue_graph, response_data=None):
        self.result = None
        self.dialogue_graph = dialogue_graph
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Response")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.geometry("500x600")
        
        # Notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Basic tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Basic")
        self.create_basic_tab(basic_frame, response_data)
        
        # Trial tab
        trial_frame = ttk.Frame(notebook)
        notebook.add(trial_frame, text="Trial")
        self.create_trial_tab(trial_frame, response_data)
        
        # Advanced tab
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        self.create_advanced_tab(advanced_frame, response_data)
        
        # Buttons
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.cancel_clicked).pack(side="left", padx=5)
        
        self.dialog.wait_window()
    
    def create_basic_tab(self, parent, response_data):
        """Create basic response tab"""
        # Response text
        ttk.Label(parent, text="Response Text:").pack(anchor="w", padx=10, pady=5)
        self.text_entry = ttk.Entry(parent, width=50)
        self.text_entry.pack(fill="x", padx=10, pady=5)
        
        if response_data:
            self.text_entry.insert(0, response_data.get("text", ""))
        
        # Response type
        ttk.Label(parent, text="Response Type:").pack(anchor="w", padx=10, pady=(10, 5))
        self.response_type_var = tk.StringVar(value="direct")
        self.response_type_var.trace("w", self.on_response_type_change)
        
        ttk.Radiobutton(parent, text="Direct Topic", variable=self.response_type_var, value="direct").pack(anchor="w", padx=20)
        ttk.Radiobutton(parent, text="Custom Topic", variable=self.response_type_var, value="custom").pack(anchor="w", padx=20)
        ttk.Radiobutton(parent, text="Trial (Skill Check)", variable=self.response_type_var, value="trial").pack(anchor="w", padx=20)
        
        # Direct topic section (dropdown with existing topics)
        self.direct_frame = ttk.LabelFrame(parent, text="Direct Topic")
        self.direct_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(self.direct_frame, text="Target Topic:").pack(anchor="w", padx=5, pady=5)
        
        topic_frame = ttk.Frame(self.direct_frame)
        topic_frame.pack(fill="x", padx=5, pady=5)
        
        self.topic_var = tk.StringVar()
        # Dropdown with existing topics only
        self.topic_combo = ttk.Combobox(topic_frame, textvariable=self.topic_var, width=40, state="readonly")
        
        # Populate with available topics
        topics = list(self.dialogue_graph.topics.keys())
        topics.extend(["TALK_NONE", "TALK_DONE", "TALK_TRAIN"])
        self.topic_combo['values'] = sorted(topics)
        self.topic_combo.pack(side="left", fill="x", expand=True)
        
        # Custom topic section (free text entry)
        self.custom_frame = ttk.LabelFrame(parent, text="Custom Topic")
        
        ttk.Label(self.custom_frame, text="Target Topic ID:").pack(anchor="w", padx=5, pady=5)
        
        self.custom_topic_var = tk.StringVar()
        self.custom_topic_entry = ttk.Entry(self.custom_frame, textvariable=self.custom_topic_var, width=40)
        self.custom_topic_entry.pack(fill="x", padx=5, pady=5)
        ttk.Label(self.custom_frame, text="(Enter any topic ID, e.g., TALK_CUSTOM_TOPIC)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        
        if response_data:
            if response_data.get("topic"):
                topic_value = response_data.get("topic", "")
                # Check if topic exists in graph or is a special topic
                if topic_value in topics:
                    self.topic_var.set(topic_value)
                    self.response_type_var.set("direct")
                else:
                    # Custom topic (not in existing topics)
                    self.custom_topic_var.set(topic_value)
                    self.response_type_var.set("custom")
            elif response_data.get("trial"):
                self.response_type_var.set("trial")
        
        # Update visibility based on initial type
        self.on_response_type_change()
    
    def create_trial_tab(self, parent, response_data):
        """Create trial response tab"""
        # Trial type
        ttk.Label(parent, text="Trial Type:").pack(anchor="w", padx=10, pady=5)
        self.trial_type_var = tk.StringVar(value="PERSUADE")
        trial_types = ["PERSUADE", "INTIMIDATE", "LIE"]
        self.trial_type_combo = ttk.Combobox(parent, textvariable=self.trial_type_var, values=trial_types, width=20)
        self.trial_type_combo.pack(anchor="w", padx=10, pady=5)
        
        if response_data and response_data.get("trial"):
            trial_info = response_data.get("trial", {})
            if isinstance(trial_info, dict):
                self.trial_type_var.set(trial_info.get("type", "PERSUADE"))
        
        # Difficulty
        ttk.Label(parent, text="Difficulty:").pack(anchor="w", padx=10, pady=(10, 5))
        self.difficulty_var = tk.StringVar(value="0")
        difficulty_entry = ttk.Entry(parent, textvariable=self.difficulty_var, width=20)
        difficulty_entry.pack(anchor="w", padx=10, pady=5)
        
        if response_data and response_data.get("trial"):
            trial_info = response_data.get("trial", {})
            if isinstance(trial_info, dict):
                self.difficulty_var.set(str(trial_info.get("difficulty", 0)))
        
        # Mod (optional)
        ttk.Label(parent, text="Mod (JSON array, optional):").pack(anchor="w", padx=10, pady=(10, 5))
        mod_frame = ttk.Frame(parent)
        mod_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.trial_mod_text = tk.Text(mod_frame, height=3, wrap="word", font=("Courier", 9))
        mod_scrollbar = ttk.Scrollbar(mod_frame, orient="vertical", command=self.trial_mod_text.yview)
        self.trial_mod_text.configure(yscrollcommand=mod_scrollbar.set)
        
        self.trial_mod_text.pack(side="left", fill="both", expand=True)
        mod_scrollbar.pack(side="right", fill="y")
        
        if response_data and response_data.get("trial"):
            trial_info = response_data.get("trial", {})
            if isinstance(trial_info, dict) and "mod" in trial_info:
                import json
                self.trial_mod_text.insert("1.0", json.dumps(trial_info.get("mod"), indent=2))
        
        # Success topic
        ttk.Label(parent, text="Success Topic:").pack(anchor="w", padx=10, pady=(10, 5))
        success_frame = ttk.Frame(parent)
        success_frame.pack(fill="x", padx=10, pady=5)
        
        self.success_topic_var = tk.StringVar()
        # Allow custom entry
        self.success_topic_combo = ttk.Combobox(success_frame, textvariable=self.success_topic_var, width=37, state="normal")
        topics = list(self.dialogue_graph.topics.keys())
        topics.extend(["TALK_NONE", "TALK_DONE", "TALK_TRAIN"])
        self.success_topic_combo['values'] = sorted(topics)
        self.success_topic_combo.pack(side="left", fill="x", expand=True)
        
        if response_data and response_data.get("success"):
            success = response_data.get("success", {})
            if isinstance(success, dict):
                self.success_topic_var.set(success.get("topic", ""))
        
        # Failure topic
        ttk.Label(parent, text="Failure Topic:").pack(anchor="w", padx=10, pady=(10, 5))
        failure_frame = ttk.Frame(parent)
        failure_frame.pack(fill="x", padx=10, pady=5)
        
        self.failure_topic_var = tk.StringVar()
        # Allow custom entry
        self.failure_topic_combo = ttk.Combobox(failure_frame, textvariable=self.failure_topic_var, width=37, state="normal")
        self.failure_topic_combo['values'] = sorted(topics)
        self.failure_topic_combo.pack(side="left", fill="x", expand=True)
        
        if response_data and response_data.get("failure"):
            failure = response_data.get("failure", {})
            if isinstance(failure, dict):
                self.failure_topic_var.set(failure.get("topic", ""))
    
    def create_advanced_tab(self, parent, response_data):
        """Create advanced tab for conditions and effects"""
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
        
        # Condition section with Simple/Raw JSON tabs
        ttk.Label(scrollable_frame, text="Condition:").pack(anchor="w", padx=10, pady=5)
        
        condition_notebook = ttk.Notebook(scrollable_frame)
        condition_notebook.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Simple condition editor (reuse same method but for response context)
        simple_cond_frame = ttk.Frame(condition_notebook)
        condition_notebook.add(simple_cond_frame, text="Simple")
        # Extract condition from response_data
        response_condition = response_data.get("condition") if response_data else None
        self.create_simple_condition_editor(simple_cond_frame, response_condition)
        
        # Raw JSON editor
        raw_cond_frame = ttk.Frame(condition_notebook)
        condition_notebook.add(raw_cond_frame, text="Raw JSON")
        
        condition_frame = ttk.Frame(raw_cond_frame)
        condition_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.condition_text = tk.Text(condition_frame, height=6, wrap="word", font=("Courier", 9))
        condition_scrollbar = ttk.Scrollbar(condition_frame, orient="vertical", command=self.condition_text.yview)
        self.condition_text.configure(yscrollcommand=condition_scrollbar.set)
        
        self.condition_text.pack(side="left", fill="both", expand=True)
        condition_scrollbar.pack(side="right", fill="y")
        
        if response_data and response_data.get("condition"):
            import json
            self.condition_text.insert("1.0", json.dumps(response_data.get("condition"), indent=2))
        
        # Store reference
        self.response_condition_notebook = condition_notebook
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def on_response_type_change(self, *args):
        """Handle response type change"""
        # Hide all frames first
        self.direct_frame.pack_forget()
        self.custom_frame.pack_forget()
        
        response_type = self.response_type_var.get()
        if response_type == "direct":
            self.direct_frame.pack(fill="x", padx=10, pady=5)
        elif response_type == "custom":
            self.custom_frame.pack(fill="x", padx=10, pady=5)
    
    def ok_clicked(self):
        """Handle OK button"""
        result = {}
        
        # Text is required
        text = self.text_entry.get().strip()
        if not text:
            tk.messagebox.showwarning("Invalid Input", "Response text is required")
            return
        result["text"] = text
        
        if self.response_type_var.get() == "direct":
            # Direct topic response
            topic = self.topic_var.get().strip()
            if not topic:
                tk.messagebox.showwarning("Invalid Input", "Target topic is required")
                return
            result["topic"] = topic
        elif self.response_type_var.get() == "custom":
            # Custom topic response
            topic = self.custom_topic_var.get().strip()
            if not topic:
                tk.messagebox.showwarning("Invalid Input", "Target topic ID is required")
                return
            result["topic"] = topic
        else:
            # Trial response
            trial_type = self.trial_type_var.get().strip()
            try:
                difficulty = int(self.difficulty_var.get())
            except ValueError:
                difficulty = 0
            
            trial_obj = {"type": trial_type, "difficulty": difficulty}
            
            # Add mod if provided
            mod_text = self.trial_mod_text.get("1.0", tk.END).strip()
            if mod_text:
                try:
                    import json
                    trial_obj["mod"] = json.loads(mod_text)
                except json.JSONDecodeError:
                    tk.messagebox.showerror("Invalid JSON", "Trial mod must be valid JSON")
                    return
            
            result["trial"] = trial_obj
            
            success_topic = self.success_topic_var.get().strip()
            failure_topic = self.failure_topic_var.get().strip()
            
            if not success_topic or not failure_topic:
                tk.messagebox.showwarning("Invalid Input", "Both success and failure topics are required for trials")
                return
            
            result["success"] = {"topic": success_topic}
            result["failure"] = {"topic": failure_topic}
        
        # Add condition if provided - check which tab is active
        condition_dict = None
        if hasattr(self, 'response_condition_notebook') and self.response_condition_notebook:
            cond_tab_index = self.response_condition_notebook.index(self.response_condition_notebook.select())
            if cond_tab_index == 0:
                # Simple tab
                condition_dict = self.get_simple_condition()
                if condition_dict is None:
                    # Condition is optional, so skip if empty
                    pass
                else:
                    result["condition"] = condition_dict
            else:
                # Raw JSON tab
                condition_text = self.condition_text.get("1.0", tk.END).strip()
                if condition_text:
                    try:
                        import json
                        result["condition"] = json.loads(condition_text)
                    except json.JSONDecodeError:
                        tk.messagebox.showerror("Invalid JSON", "Condition must be valid JSON")
                        return
        else:
            # Fallback - try raw JSON
            condition_text = self.condition_text.get("1.0", tk.END).strip()
            if condition_text:
                try:
                    import json
                    result["condition"] = json.loads(condition_text)
                except json.JSONDecodeError:
                    tk.messagebox.showerror("Invalid JSON", "Condition must be valid JSON")
                    return
        
        self.result = result
        self.dialog.destroy()
    
    def cancel_clicked(self):
        """Handle Cancel button"""
        self.dialog.destroy()
    def create_simple_condition_editor(self, parent, current_data):
        """Create simple condition editor for common condition types"""
        # Extract condition from current_data if present
        condition_dict = {}
        if current_data:
            if isinstance(current_data, dict):
                # For dynamic lines, extract condition (everything except yes/no)
                # For responses, current_data IS the condition
                if "yes" in current_data or "no" in current_data:
                    condition_dict = {k: v for k, v in current_data.items() if k not in ["yes", "no"]}
                else:
                    condition_dict = current_data
            else:
                condition_dict = current_data
        
        # Condition type selector
        ttk.Label(parent, text="Condition Type:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.cond_type_var = tk.StringVar(value="simple")
        self.cond_type_var.trace("w", lambda *args: self.update_simple_condition_ui(parent))
        
        cond_type_frame = ttk.Frame(parent)
        cond_type_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Radiobutton(cond_type_frame, text="Variable Check", variable=self.cond_type_var, value="var").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Effect Check", variable=self.cond_type_var, value="effect").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Gender Check", variable=self.cond_type_var, value="gender").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Environment", variable=self.cond_type_var, value="env").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Mission Check", variable=self.cond_type_var, value="mission").pack(side="left", padx=5)
        ttk.Radiobutton(cond_type_frame, text="Boolean Logic", variable=self.cond_type_var, value="logic").pack(side="left", padx=5)
        
        # Variable check fields
        self.var_frame = ttk.LabelFrame(parent, text="Variable Check")
        self.var_frame.pack(fill="x", padx=10, pady=5)
        
        self.var_target_var = tk.StringVar(value="npc")
        ttk.Label(self.var_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        var_target_frame = ttk.Frame(self.var_frame)
        var_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(var_target_frame, text="NPC", variable=self.var_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(var_target_frame, text="Player", variable=self.var_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.var_frame, text="Variable Name:").pack(anchor="w", padx=5, pady=2)
        self.var_name_entry = ttk.Entry(self.var_frame, width=40)
        self.var_name_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Context:").pack(anchor="w", padx=5, pady=2)
        self.var_context_entry = ttk.Entry(self.var_frame, width=40)
        self.var_context_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.var_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.var_value_entry = ttk.Entry(self.var_frame, width=40)
        self.var_value_entry.pack(fill="x", padx=5, pady=2)
        
        # Effect check fields
        self.effect_frame = ttk.LabelFrame(parent, text="Effect Check")
        
        self.effect_target_var = tk.StringVar(value="npc")
        ttk.Label(self.effect_frame, text="Target:").pack(anchor="w", padx=5, pady=2)
        effect_target_frame = ttk.Frame(self.effect_frame)
        effect_target_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(effect_target_frame, text="NPC", variable=self.effect_target_var, value="npc").pack(side="left", padx=5)
        ttk.Radiobutton(effect_target_frame, text="Player", variable=self.effect_target_var, value="player").pack(side="left", padx=5)
        
        ttk.Label(self.effect_frame, text="Effect ID:").pack(anchor="w", padx=5, pady=2)
        self.effect_id_entry = ttk.Entry(self.effect_frame, width=40)
        self.effect_id_entry.pack(fill="x", padx=5, pady=2)
        
        # Gender check fields
        self.gender_frame = ttk.LabelFrame(parent, text="Gender Check")
        
        ttk.Label(self.gender_frame, text="Check:").pack(anchor="w", padx=5, pady=2)
        self.gender_check_var = tk.StringVar(value="npc_female")
        gender_check_frame = ttk.Frame(self.gender_frame)
        gender_check_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(gender_check_frame, text="NPC Female", variable=self.gender_check_var, value="npc_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="NPC Male", variable=self.gender_check_var, value="npc_male").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Female", variable=self.gender_check_var, value="u_female").pack(side="left", padx=5)
        ttk.Radiobutton(gender_check_frame, text="Player Male", variable=self.gender_check_var, value="u_male").pack(side="left", padx=5)
        
        # Environment fields
        self.env_frame = ttk.LabelFrame(parent, text="Environment Check")
        
        ttk.Label(self.env_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.env_type_var = tk.StringVar(value="days_since_cataclysm")
        env_type_combo = ttk.Combobox(self.env_frame, textvariable=self.env_type_var, 
                                     values=["days_since_cataclysm", "is_season", "is_day", "is_outside"], width=37)
        env_type_combo.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(self.env_frame, text="Value:").pack(anchor="w", padx=5, pady=2)
        self.env_value_entry = ttk.Entry(self.env_frame, width=40)
        self.env_value_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.env_frame, text="(For days: number, for season: spring/summer/autumn/winter)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        
        # Mission check fields
        self.mission_frame = ttk.LabelFrame(parent, text="Mission Check")
        
        ttk.Label(self.mission_frame, text="Check Type:").pack(anchor="w", padx=5, pady=2)
        self.mission_type_var = tk.StringVar(value="u_has_mission")
        mission_type_frame = ttk.Frame(self.mission_frame)
        mission_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(mission_type_frame, text="Player Has Mission", variable=self.mission_type_var, value="u_has_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has Assigned Mission", variable=self.mission_type_var, value="has_assigned_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Available Mission", variable=self.mission_type_var, value="has_no_available_mission").pack(side="left", padx=5)
        ttk.Radiobutton(mission_type_frame, text="Has No Assigned Mission", variable=self.mission_type_var, value="has_no_assigned_mission").pack(side="left", padx=5)
        
        # Mission ID entry (only shown for u_has_mission)
        self.mission_id_frame = ttk.Frame(self.mission_frame)
        ttk.Label(self.mission_id_frame, text="Mission ID:").pack(anchor="w", padx=5, pady=2)
        self.mission_id_entry = ttk.Entry(self.mission_id_frame, width=40)
        self.mission_id_entry.pack(fill="x", padx=5, pady=2)
        ttk.Label(self.mission_id_frame, text="(e.g., MISSION_BEGGAR_2_PERMISSION)", 
                 font=("Arial", 8), foreground="gray").pack(anchor="w", padx=5, pady=2)
        # Don't pack initially - update_mission_ui will handle it when mission type is selected
        
        # Update mission UI when type changes
        self.mission_type_var.trace("w", lambda *args: self.update_mission_ui())
        
        # Boolean logic fields
        self.logic_frame = ttk.LabelFrame(parent, text="Boolean Logic")
        
        ttk.Label(self.logic_frame, text="Logic Type:").pack(anchor="w", padx=5, pady=2)
        self.logic_type_var = tk.StringVar(value="and")
        logic_type_frame = ttk.Frame(self.logic_frame)
        logic_type_frame.pack(fill="x", padx=5, pady=2)
        ttk.Radiobutton(logic_type_frame, text="AND (all true)", variable=self.logic_type_var, value="and").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="OR (any true)", variable=self.logic_type_var, value="or").pack(side="left", padx=5)
        ttk.Radiobutton(logic_type_frame, text="NOT (negate)", variable=self.logic_type_var, value="not").pack(side="left", padx=5)
        
        ttk.Label(self.logic_frame, text="Sub-conditions:").pack(anchor="w", padx=5, pady=2)
        
        # Listbox for sub-conditions
        list_frame = ttk.Frame(self.logic_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.logic_conditions_listbox = tk.Listbox(list_frame, height=4)
        logic_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.logic_conditions_listbox.yview)
        self.logic_conditions_listbox.configure(yscrollcommand=logic_scrollbar.set)
        self.logic_conditions_listbox.pack(side="left", fill="both", expand=True)
        logic_scrollbar.pack(side="right", fill="y")
        
        # Buttons for sub-conditions
        logic_btn_frame = ttk.Frame(self.logic_frame)
        logic_btn_frame.pack(fill="x", padx=5, pady=2)
        ttk.Button(logic_btn_frame, text="Add", command=self.add_logic_sub_condition).pack(side="left", padx=2)
        ttk.Button(logic_btn_frame, text="Edit", command=self.edit_logic_sub_condition).pack(side="left", padx=2)
        ttk.Button(logic_btn_frame, text="Remove", command=self.remove_logic_sub_condition).pack(side="left", padx=2)
        
        self.logic_sub_conditions = []  # Store sub-conditions as dicts
        
        # Load current condition if present
        self.load_simple_condition(condition_dict)
        
        # Initial UI update
        self.update_simple_condition_ui(parent)
    
    def update_simple_condition_ui(self, parent):
        """Update which condition frame is visible"""
        self.var_frame.pack_forget()
        self.effect_frame.pack_forget()
        self.gender_frame.pack_forget()
        self.env_frame.pack_forget()
        self.mission_frame.pack_forget()
        self.logic_frame.pack_forget()
        
        cond_type = self.cond_type_var.get()
        if cond_type == "var":
            self.var_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "effect":
            self.effect_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "gender":
            self.gender_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "env":
            self.env_frame.pack(fill="x", padx=10, pady=5)
        elif cond_type == "mission":
            self.mission_frame.pack(fill="x", padx=10, pady=5)
            self.update_mission_ui()
        elif cond_type == "logic":
            self.logic_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    def update_mission_ui(self):
        """Update mission UI to show/hide mission ID field based on check type"""
        if hasattr(self, 'mission_type_var'):
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                self.mission_id_frame.pack(fill="x", padx=5, pady=2)
            else:
                self.mission_id_frame.pack_forget()
    
    def load_simple_condition(self, condition_dict):
        """Load condition into simple editor"""
        if not condition_dict:
            return
        
        # Handle string conditions (e.g., "has_assigned_mission")
        if isinstance(condition_dict, str):
            if condition_dict in ["has_assigned_mission", "has_no_available_mission", "has_no_assigned_mission"]:
                self.cond_type_var.set("mission")
                self.mission_type_var.set(condition_dict)
                return
            else:
                # Unknown string condition, treat as dict format
                return
        
        # Check for variable checks
        if "npc_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("npc")
            var_info = condition_dict["npc_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
            else:
                # Handle flattened structure where type/context/value are at same level
                self.var_name_entry.insert(0, str(var_info))
                # Check if type/context/value are at the same level as npc_has_var
                # Note: type is always "dialogue" so we don't load it
                if "context" in condition_dict:
                    self.var_context_entry.insert(0, str(condition_dict.get("context", "")))
                if "value" in condition_dict:
                    self.var_value_entry.insert(0, str(condition_dict.get("value", "")))
        elif "u_has_var" in condition_dict:
            self.cond_type_var.set("var")
            self.var_target_var.set("player")
            var_info = condition_dict["u_has_var"]
            if isinstance(var_info, dict):
                self.var_name_entry.insert(0, var_info.get("var", var_info.get("name", "")))
                self.var_context_entry.insert(0, var_info.get("context", ""))
                self.var_value_entry.insert(0, str(var_info.get("value", "")))
            else:
                # Handle flattened structure where type/context/value are at same level
                self.var_name_entry.insert(0, str(var_info))
                # Check if type/context/value are at the same level as u_has_var
                if "type" in condition_dict:
                    self.var_type_entry.insert(0, str(condition_dict.get("type", "")))
                if "context" in condition_dict:
                    self.var_context_entry.insert(0, str(condition_dict.get("context", "")))
                if "value" in condition_dict:
                    self.var_value_entry.insert(0, str(condition_dict.get("value", "")))
        # Check for effect checks
        elif "npc_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("npc")
            self.effect_id_entry.insert(0, str(condition_dict["npc_has_effect"]))
        elif "u_has_effect" in condition_dict:
            self.cond_type_var.set("effect")
            self.effect_target_var.set("player")
            self.effect_id_entry.insert(0, str(condition_dict["u_has_effect"]))
        # Check for gender
        elif any(k in condition_dict for k in ["npc_female", "npc_male", "u_female", "u_male"]):
            self.cond_type_var.set("gender")
            for key in ["npc_female", "npc_male", "u_female", "u_male"]:
                if key in condition_dict:
                    self.gender_check_var.set(key)
                    break
        # Check for environment
        elif "days_since_cataclysm" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("days_since_cataclysm")
            self.env_value_entry.insert(0, str(condition_dict["days_since_cataclysm"]))
        elif "is_season" in condition_dict:
            self.cond_type_var.set("env")
            self.env_type_var.set("is_season")
            self.env_value_entry.insert(0, str(condition_dict["is_season"]))
        elif "is_day" in condition_dict or "is_outside" in condition_dict:
            self.cond_type_var.set("env")
            if "is_day" in condition_dict:
                self.env_type_var.set("is_day")
            else:
                self.env_type_var.set("is_outside")
        # Check for mission conditions
        elif "u_has_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("u_has_mission")
            mission_id = condition_dict["u_has_mission"]
            if isinstance(mission_id, dict):
                # If it's a dict, try to get the mission ID from it
                self.mission_id_entry.insert(0, str(mission_id.get("mission", mission_id.get("id", ""))))
            else:
                self.mission_id_entry.insert(0, str(mission_id))
        elif "has_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_assigned_mission")
        elif "has_no_available_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_available_mission")
        elif "has_no_assigned_mission" in condition_dict:
            self.cond_type_var.set("mission")
            self.mission_type_var.set("has_no_assigned_mission")
        # Check for boolean logic
        elif "and" in condition_dict or "or" in condition_dict or "not" in condition_dict:
            self.cond_type_var.set("logic")
            if "and" in condition_dict:
                self.logic_type_var.set("and")
                self.logic_sub_conditions = condition_dict["and"] if isinstance(condition_dict["and"], list) else [condition_dict["and"]]
            elif "or" in condition_dict:
                self.logic_type_var.set("or")
                self.logic_sub_conditions = condition_dict["or"] if isinstance(condition_dict["or"], list) else [condition_dict["or"]]
            elif "not" in condition_dict:
                self.logic_type_var.set("not")
                self.logic_sub_conditions = [condition_dict["not"]]
            self.refresh_logic_sub_conditions_list()
    
    def get_simple_condition(self):
        """Build condition dict from simple editor"""
        cond_type = self.cond_type_var.get()
        
        if cond_type == "var":
            target = self.var_target_var.get()
            var_name = self.var_name_entry.get().strip()
            if not var_name:
                return None
            
            var_context = self.var_context_entry.get().strip()
            var_value = self.var_value_entry.get().strip()
            
            if var_context or var_value:
                # Full variable check (type is always "dialogue")
                var_dict = {"var": var_name} if "var" not in var_name else {"name": var_name}
                var_dict["type"] = "dialogue"
                if var_context:
                    var_dict["context"] = var_context
                if var_value:
                    var_dict["value"] = var_value
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_dict}
            else:
                # Simple variable check
                key = "npc_has_var" if target == "npc" else "u_has_var"
                return {key: var_name}
        
        elif cond_type == "effect":
            target = self.effect_target_var.get()
            effect_id = self.effect_id_entry.get().strip()
            if not effect_id:
                return None
            key = "npc_has_effect" if target == "npc" else "u_has_effect"
            return {key: effect_id}
        
        elif cond_type == "gender":
            gender_check = self.gender_check_var.get()
            return {gender_check: True}
        
        elif cond_type == "env":
            env_type = self.env_type_var.get()
            env_value = self.env_value_entry.get().strip()
            if env_type in ["is_day", "is_outside"]:
                return {env_type: True} if env_value.lower() in ["true", "1", "yes"] else {env_type: False}
            elif env_type == "days_since_cataclysm":
                try:
                    return {env_type: int(env_value)}
                except ValueError:
                    return {env_type: 0}
            elif env_type == "is_season":
                return {env_type: env_value}
        
        elif cond_type == "mission":
            mission_type = self.mission_type_var.get()
            if mission_type == "u_has_mission":
                mission_id = self.mission_id_entry.get().strip()
                if not mission_id:
                    return None
                return {"u_has_mission": mission_id}
            else:
                # Boolean flags: has_assigned_mission, has_no_available_mission, has_no_assigned_mission
                return {mission_type: True}
        
        elif cond_type == "logic":
            logic_type = self.logic_type_var.get()
            if not self.logic_sub_conditions:
                return None
            return {logic_type: self.logic_sub_conditions}
        
        return None
    
    def refresh_logic_sub_conditions_list(self):
        """Refresh the listbox showing logic sub-conditions"""
        if not hasattr(self, 'logic_conditions_listbox'):
            return
        self.logic_conditions_listbox.delete(0, tk.END)
        for cond in self.logic_sub_conditions:
            preview = self.condition_preview(cond)
            self.logic_conditions_listbox.insert(tk.END, preview)
    
    def condition_preview(self, cond):
        """Create a preview string for a condition"""
        if isinstance(cond, dict):
            if "npc_has_var" in cond:
                var_info = cond["npc_has_var"]
                if isinstance(var_info, dict):
                    return f"NPC var: {var_info.get('var', var_info.get('name', ''))}"
                return f"NPC var: {var_info}"
            elif "u_has_var" in cond:
                var_info = cond["u_has_var"]
                if isinstance(var_info, dict):
                    return f"Player var: {var_info.get('var', var_info.get('name', ''))}"
                return f"Player var: {var_info}"
            elif "npc_has_effect" in cond:
                return f"NPC effect: {cond['npc_has_effect']}"
            elif "u_has_effect" in cond:
                return f"Player effect: {cond['u_has_effect']}"
            elif "npc_female" in cond or "npc_male" in cond or "u_female" in cond or "u_male" in cond:
                for key in ["npc_female", "npc_male", "u_female", "u_male"]:
                    if key in cond:
                        return key.replace("_", " ").title()
            elif "days_since_cataclysm" in cond:
                return f"Days since cataclysm: {cond['days_since_cataclysm']}"
            elif "is_season" in cond:
                return f"Season: {cond['is_season']}"
            elif "is_day" in cond:
                return "Is day: True" if cond.get("is_day") else "Is day: False"
            elif "is_outside" in cond:
                return "Is outside: True" if cond.get("is_outside") else "Is outside: False"
            elif "u_has_mission" in cond:
                mission_id = cond["u_has_mission"]
                if isinstance(mission_id, dict):
                    mission_id = mission_id.get("mission", mission_id.get("id", ""))
                return f"Player has mission: {mission_id}"
            elif "has_assigned_mission" in cond:
                return "Has assigned mission"
            elif "has_no_available_mission" in cond:
                return "Has no available mission"
            elif "has_no_assigned_mission" in cond:
                return "Has no assigned mission"
            elif "and" in cond or "or" in cond or "not" in cond:
                logic_type = "and" if "and" in cond else ("or" if "or" in cond else "not")
                count = len(cond[logic_type]) if isinstance(cond[logic_type], list) else 1
                return f"{logic_type.upper()} ({count} conditions)"
            else:
                import json
                return json.dumps(cond, separators=(',', ':'))
        return str(cond)
    
    def add_logic_sub_condition(self):
        """Add a new sub-condition"""
        dialog = SubConditionDialog(self.dialog, None)
        if dialog.result:
            self.logic_sub_conditions.append(dialog.result)
            self.refresh_logic_sub_conditions_list()
    
    def edit_logic_sub_condition(self):
        """Edit selected sub-condition"""
        selection = self.logic_conditions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a sub-condition to edit.")
            return
        index = selection[0]
        cond_data = self.logic_sub_conditions[index]
        
        dialog = SubConditionDialog(self.dialog, cond_data)
        if dialog.result:
            self.logic_sub_conditions[index] = dialog.result
            self.refresh_logic_sub_conditions_list()
    
    def remove_logic_sub_condition(self):
        """Remove selected sub-condition"""
        selection = self.logic_conditions_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a sub-condition to remove.")
            return
        index = selection[0]
        del self.logic_sub_conditions[index]
        self.refresh_logic_sub_conditions_list()


