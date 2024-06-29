import os
from dotenv import load_dotenv
import questionary


class UserInterface:
    def _select_from_list(self, prompt_text, options):
        return questionary.select(prompt_text, choices=options).ask()

    def _get_user_input(self, prompt, default=None):
        return questionary.text(f"{prompt} [{default}]:").ask() or default

    def create_order(self):
        category = "spot"  # Default value
        symbol = "BTCUSDT"  # Default value
        side = self._select_from_list("Select side", ["Buy", "Sell"])
        order_type = "Limit"  # Default value
        qty = self._get_user_input("Enter quantity", "0.001")
        price = self._get_user_input("Enter price", "1000")
        time_in_force = "GTC"  # Default value

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
