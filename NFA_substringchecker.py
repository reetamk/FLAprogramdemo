import tkinter as tk

class State:
    def __init__(self, name, is_accept=False):
        self.name = name
        self.is_accept = is_accept
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

class NFA:
    def __init__(self):
        self.states = {}
        self.start_state = None

    def add_state(self, name, is_accept=False):
        state = State(name, is_accept)
        self.states[name] = state
        return state

    def set_start(self, name):
        self.start_state = self.states[name]

    def add_transition(self, from_state, symbol, to_state):
        self.states[from_state].add_transition(symbol, self.states[to_state])

    def simulate(self, input_string):
        current_states = {self.start_state}
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if symbol in state.transitions:
                    next_states.update(state.transitions[symbol])
            current_states = next_states
            if not current_states:
                return False  # If no valid transitions, reject the input

        return any(state.is_accept for state in current_states)

class NFAFactory:
    @staticmethod
    def contains_substring(substring, position="anywhere"):
        nfa = NFA()
        states = [nfa.add_state(f"q{i}") for i in range(len(substring) + 1)]
        accept_state = nfa.add_state(f"q{len(substring)}", is_accept=True)
        nfa.set_start("q0")

        # Build NFA based on the selected position
        if position == "front":
            # For "front", we need the substring to match starting at the very first character of the input
            for i, char in enumerate(substring):
                states[i].add_transition(char, states[i+1] if i+1 < len(substring) else accept_state)
            
            # No self-loop or extra transitions are allowed at the start state for "front"
            # Transition sequence must strictly follow the substring

        elif position == "last":
            # Matches substring only at the end
            for char in '01abc':
                nfa.states["q0"].add_transition(char, nfa.states["q0"])
            for i, char in enumerate(substring):
                states[i].add_transition(char, states[i+1] if i+1 < len(substring) else accept_state)
        
        elif position == "anywhere":
            # Matches substring anywhere
            for i, char in enumerate(substring):
                states[i].add_transition(char, states[i+1] if i+1 < len(substring) else accept_state)

            # Adding self-loops to q0 for any character to allow substring match anywhere
            for state in nfa.states.values():
                for char in '01abc':
                    if char not in state.transitions:
                        state.add_transition(char, nfa.start_state if state == nfa.start_state else state)

        return nfa

class NFASimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NFA Language Checker")

        # Input label and field for the string to check
        self.input_label = tk.Label(root, text="Enter a binary string (or 'a', 'b', 'c'):")
        self.input_label.grid(row=0, column=0, columnspan=2, sticky="w")

        self.input_field = tk.Entry(root)
        self.input_field.grid(row=1, column=0, columnspan=2, sticky="we")
        self.input_field.focus_set()

        # Input label and field for the substring to check for
        self.substring_label = tk.Label(root, text="Enter a substring to detect:")
        self.substring_label.grid(row=2, column=0, columnspan=2, sticky="w")

        self.substring_field = tk.Entry(root)
        self.substring_field.grid(row=3, column=0, columnspan=2, sticky="we")

        # Create buttons for each position option
        self.check_button_front = tk.Button(root, text="Check at Front", command=lambda: self.check_custom_substring("front"))
        self.check_button_front.grid(row=4, column=0, sticky="we")

        self.check_button_last = tk.Button(root, text="Check at Last", command=lambda: self.check_custom_substring("last"))
        self.check_button_last.grid(row=4, column=1, sticky="we")

        self.check_button_anywhere = tk.Button(root, text="Check Anywhere", command=lambda: self.check_custom_substring("anywhere"))
        self.check_button_anywhere.grid(row=5, column=0, columnspan=2, sticky="we")

        # Result label
        self.result_label = tk.Label(root, text="Result: ")
        self.result_label.grid(row=6, column=0, columnspan=2, sticky="w")

    def check_custom_substring(self, position):
        input_string = self.input_field.get().strip()
        substring = self.substring_field.get().strip()

        # Input validation for both fields
        if not all(char in '01abc' for char in input_string):
            self.result_label.config(text="Error: Please enter a valid string containing only '0', '1', 'a', 'b', and 'c'.")
            return
        if not all(char in '01abc' for char in substring):
            self.result_label.config(text="Error: Substring can only contain '0', '1', 'a', 'b', and 'c'.")
            return

        # Create an NFA for the specified substring and position, then check the input string
        nfa = NFAFactory.contains_substring(substring, position)
        is_accepted = nfa.simulate(input_string)
        result_text = f"Result: Contains '{substring}' at {position.capitalize()} - {'Accepted!' if is_accepted else 'Rejected!'}"
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = NFASimulatorApp(root)
    root.mainloop()
