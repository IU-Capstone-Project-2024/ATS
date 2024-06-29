from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import input_dialog


class UserInterface:
    def _select_from_list(self, prompt_text, options):
        completer = WordCompleter(options, ignore_case=True)
        return prompt(f"{prompt_text}: ", completer=completer)

    def _get_user_input(self, prompt, default=None):
        response = input(f"{prompt} [{default}]: ")
        return response if response else default

    def create_order(self):
        category = "spot"  # Default value
        symbol = "BTCUSDT"  # Default value
        side = self._select_from_list("Select side", ["Buy", "Sell"])
        order_type = "Limit"
        qty = self._get_user_input("Enter quantity", "0.001")
        price = self._get_user_input("Enter price", "1000")
        time_in_force = "GTC"

        order_params = {
            "category": category,
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "qty": qty,
            "price": price,
            "time_in_force": time_in_force
        }

        return order_params
