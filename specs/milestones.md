# Paseo Milestones

## Milestone 1

Build a runnable minimal app.

Requirements:

* CLI interface

* Accept commands like:
  "Paseo Andorra"

* Extract destination

* Generate FAST itinerary

* Use mock JSON datasets

* Produce terminal output

Output should include:

* flights
* activities
* stays
* transportation

The app must:

* run locally
* have clean modular code
* include README instructions

Success Criteria:
Running:

python app/main.py "Paseo Andorra"

produces a FAST itinerary successfully.

## Milestone 2

Implement strategy-driven itinerary selection.

Requirements:

* Each FAST category must use a strategy class
* Strategies must rank candidate options
* Strategies should support configurable scoring
* Use weighted linear scoring initially

Example:
score =
price_weight * normalized_price +
rating_weight * normalized_rating

The app should:

* evaluate multiple options
* choose best candidates
* print strategy scores

Goal:
Transform Paseo into a modular decision engine.
