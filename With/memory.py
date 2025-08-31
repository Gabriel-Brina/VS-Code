import json

class Memory:
    def __init__(self):
        self.states = {}

    def get_state(self, user_id):
        return self.states.get(user_id, {})

    def set_state(self, user_id, state):
        self.states[user_id] = state
    
    def update_conversation_history(self, user_id, message):
        state = self.get_state(user_id)
        if "history" not in state:
            state["history"] = []
        state["history"].append(message)
        self.set_state(user_id, state)

    def get_conversation_history(self, user_id):
        state = self.get_state(user_id)
        return state.get("history", [])

    def clear_conversation_history(self, user_id):
        state = self.get_state(user_id)
        state["history"] = []
        self.set_state(user_id, state)

    def get_client_detail(self, user_id, detail_key):
        return self.get_state(user_id).get(detail_key, None)

    def set_client_detail(self, user_id, detail_key, detail_value):
        state = self.get_state(user_id)
        state[detail_key] = detail_value
        self.set_state(user_id, state)

    def clear_client_details(self, user_id):
        state = self.get_state(user_id)
        for key in list(state.keys()):
            if key != "history":
                del state[key]
        self.set_state(user_id, state)

    def clear_all_data(self, user_id):
        self.set_state(user_id, {})
    
 
