from dataclasses import dataclass
@dataclass
class PaseoCommand:
    destination: str
    profile: str = "budget"
    def __str__(self) -> str:
        return f"PaseoCommand(destination={self.destination}, profile={self.profile})"