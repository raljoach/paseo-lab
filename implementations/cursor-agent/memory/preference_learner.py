class PreferenceLearner:

    def infer_preferences(
        self,
        raw_text: str,
    ) -> list[str]:

        text = raw_text.lower()

        preferences = []

        if "nightlife" in text:
            preferences.append(
                "User likes nightlife"
            )

        if "relax" in text:
            preferences.append(
                "User prefers relaxing trips"
            )

        if "culture" in text:
            preferences.append(
                "User enjoys local culture"
            )

        if "food" in text:
            preferences.append(
                "User enjoys food experiences"
            )

        if "adventure" in text:
            preferences.append(
                "User likes adventure travel"
            )

        return preferences