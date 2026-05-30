# Paseo

Paseo is a conversational travel itinerary engine.

Users issue commands such as:

"Paseo Andorra"

The system generates a FAST itinerary:

F = Flights
A = Activities
S = Stays
T = Transportation

The system uses:

* travel datasets
* strategy modules
* ranking systems
* itinerary composition

The application should be modular and strategy-driven.

Each itinerary category should support independent strategy evolution:

* FlightStrategy
* ActivityStrategy
* StayStrategy
* TransportStrategy

The application evolves in 5 milestones:

1. Mock itinerary generation
2. Real data connectors
3. Strategy engine
4. LLM orchestration
5. Autonomous adaptive planning

Primary stack:

* Python
* FastAPI
* SQLite
* JSON datasets

Goal:
Create a minimal AI-native travel planning system.
