#!/usr/bin/env python3
"""
Demo Scenario: Urban Dweller Sustainability Journey

This demonstrates a complete sustainability journey for an urban apartment dweller
who wants to reduce their environmental impact.

Run with: uv run python demo/scenario_urban_dweller.py
"""

import asyncio
import sys
from datetime import datetime

sys.path.insert(0, '/Users/vinhnguyenxuan/Developer/learn-by-doing/vtgoodagent/ecoagent')

from ecoagent.main import get_app
from ecoagent.database import db as ecoagent_db


class UrbanDwellerScenario:
    """Demonstrates urban dweller sustainability journey."""

    def __init__(self):
        self.app = get_app()
        self.user_id = "urban_dweller_alex"
        self.session_id = f"session_{datetime.now().timestamp()}"

    async def run(self):
        """Run the urban dweller scenario."""
        print("\n" + "=" * 70)
        print("🏙️  Scenario: Urban Dweller's Sustainability Journey")
        print("=" * 70)

        # Initialize
        print("\nInitializing scenario...")
        await self.app.initialize()

        # Step 1: Baseline Assessment
        await self.step_1_baseline_assessment()
        await asyncio.sleep(2)

        # Step 2: Initial Recommendations
        await self.step_2_initial_recommendations()
        await asyncio.sleep(2)

        # Step 3: Set Goals
        await self.step_3_set_goals()
        await asyncio.sleep(2)

        # Step 4: Ask Questions
        await self.step_4_ask_questions()
        await asyncio.sleep(2)

        # Step 5: Progress Tracking
        await self.step_5_progress_tracking()

        print("\n" + "=" * 70)
        print("✅ Urban Dweller Scenario Complete!")
        print("=" * 70)

    async def step_1_baseline_assessment(self):
        """Step 1: Calculate current carbon footprint."""
        print("\n" + "-" * 70)
        print("STEP 1: Baseline Carbon Footprint Assessment")
        print("-" * 70)

        print("\n📍 Profile: Urban Apartment Dweller")
        print("   Name: Alex")
        print("   Location: New York City")
        print("   Housing: Small apartment, 2 people")
        print("   Lifestyle: Mixed diet, uses public transit sometimes")

        print("\n🧮 Current Activities:")
        print("   Daily commute: 3 miles on subway (already calculated as low-impact)")
        print("   Weekly shopping: 1 car trip = ~20 miles (rides with friend)")
        print("   Monthly flights: 1 domestic flight = ~1000 miles")
        print("   Home energy: 500 kWh/month (city apartment, efficient)")
        print("   Food: Meat 3x per week, mostly local restaurants")

        # Calculate baseline
        car_miles = 20
        mpg = 25
        gallons = car_miles / mpg
        car_carbon = gallons * 19.6

        flight_carbon = 1000 * 0.44

        kwh = 500
        energy_carbon = kwh * 0.954

        total_baseline = car_carbon + flight_carbon + energy_carbon

        print(f"\n📊 Baseline Carbon Calculation (Monthly):")
        print(f"   Car trips: {car_carbon:.2f} lbs CO2")
        print(f"   Flights: {flight_carbon:.2f} lbs CO2")
        print(f"   Home energy: {energy_carbon:.2f} lbs CO2")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Total: {total_baseline:.2f} lbs CO2/month")
        print(f"   Annualized: {total_baseline * 12:.2f} lbs CO2/year")

        # Save to database
        ecoagent_db.save_carbon_footprint(
            user_id=self.user_id,
            carbon_type="baseline_assessment",
            value=round(total_baseline, 2),
            context={
                "profile": "urban_apartment_dweller",
                "car_miles": car_miles,
                "flight_miles": 1000,
                "home_kwh": kwh
            }
        )

    async def step_2_initial_recommendations(self):
        """Step 2: Get personalized recommendations."""
        print("\n" + "-" * 70)
        print("STEP 2: Personalized Recommendations")
        print("-" * 70)

        print("\n🌿 AI-Generated Recommendations for Urban Dweller:")

        recommendations = [
            {
                "title": "Reduce Flight Frequency",
                "impact": "High (40% of carbon footprint)",
                "action": "Combine work trips, use video conferencing for business travel",
                "timeline": "6 months"
            },
            {
                "title": "Reduce Meat Consumption",
                "impact": "Medium (15% reduction potential)",
                "action": "Try 'Meatless Mondays' or reduce to 1x per week",
                "timeline": "Immediate"
            },
            {
                "title": "Optimize Home Energy",
                "impact": "Low (already efficient) but still 20% potential",
                "action": "Switch to renewable energy provider (available in NYC)",
                "timeline": "1-2 months"
            },
            {
                "title": "Minimize Car Usage",
                "impact": "Low (already minimal) but eliminate completely",
                "action": "Use bike-sharing or car-sharing instead",
                "timeline": "Immediate"
            },
            {
                "title": "Offset Strategy",
                "impact": "Medium (carbon neutral achievements)",
                "action": "Invest in verified carbon offset projects",
                "timeline": "Ongoing"
            }
        ]

        for i, rec in enumerate(recommendations, 1):
            print(f"\n   {i}. {rec['title']}")
            print(f"      Impact: {rec['impact']}")
            print(f"      Action: {rec['action']}")
            print(f"      Timeline: {rec['timeline']}")

    async def step_3_set_goals(self):
        """Step 3: Set sustainability goals."""
        print("\n" + "-" * 70)
        print("STEP 3: Setting Sustainability Goals")
        print("-" * 70)

        goals = [
            {
                "title": "Reduce Flight Carbon by 50%",
                "description": "Limit flights to 2 per year instead of 12",
                "target": 50.0,
                "months": 6
            },
            {
                "title": "Adopt Vegetarian Diet",
                "description": "Reduce meat consumption from 3x/week to 0-1x/week",
                "target": 80.0,
                "months": 3
            },
            {
                "title": "Switch to Renewable Energy",
                "description": "Sign up for 100% renewable electricity option",
                "target": 100.0,
                "months": 1
            },
            {
                "title": "Eliminate Car Usage",
                "description": "Use only public transit, bike, or car-sharing",
                "target": 100.0,
                "months": 2
            }
        ]

        print("\n🎯 6-Month Sustainability Goals:")
        total_potential_reduction = 0

        for i, goal in enumerate(goals, 1):
            print(f"\n   Goal {i}: {goal['title']}")
            print(f"      Action: {goal['description']}")
            print(f"      Target: {goal['target']:.0f}% reduction")
            print(f"      Timeline: {goal['months']} months")

            # Save goal to database
            from datetime import timedelta
            goal_data = {
                'id': f'goal_{self.user_id}_{i}',
                'user_id': self.user_id,
                'description': goal['title'],
                'target_value': goal['target'],
                'current_value': 0.0,
                'target_date': (datetime.now() + timedelta(days=goal['months']*30)).isoformat(),
                'status': 'in_progress'
            }
            ecoagent_db.save_sustainability_goal(goal_data)

    async def step_4_ask_questions(self):
        """Step 4: Ask EcoAgent questions."""
        print("\n" + "-" * 70)
        print("STEP 4: Chat with EcoAgent for Guidance")
        print("-" * 70)

        questions = [
            "What's the best way to transition to a vegetarian diet while maintaining nutrition?",
            "How much can I actually reduce my carbon footprint by limiting flights?",
            "Are carbon offsets worth it for my situation?"
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n   Question {i}: {question}")
            print("    EcoAgent Processing...")

            try:
                response = await self.app.process_query(
                    user_id=self.user_id,
                    session_id=self.session_id,
                    query=question
                )
                # Just show a snippet to avoid token issues
                response_snippet = response[:200] if len(response) > 200 else response
                print(f"   Response: {response_snippet}...")
            except Exception as e:
                print(f"   ⚠️  Could not get response: {e}")

    async def step_5_progress_tracking(self):
        """Step 5: Track progress after 3 months."""
        print("\n" + "-" * 70)
        print("STEP 5: 3-Month Progress Review")
        print("-" * 70)

        print("\n📈 Progress After 3 Months:")

        results = [
            {
                "goal": "Flight Reduction",
                "original": 440,  # 1000 miles * 0.44
                "current": 220,
                "reduction": 50.0
            },
            {
                "goal": "Meat Consumption",
                "original": 150,  # estimated
                "current": 30,
                "reduction": 80.0
            },
            {
                "goal": "Car Usage",
                "original": 39.2,  # 20 miles
                "current": 0,
                "reduction": 100.0
            },
            {
                "goal": "Home Energy",
                "original": 477,
                "current": 239.5,  # Switched to renewable
                "reduction": 50.0
            }
        ]

        total_original = sum(r["original"] for r in results)
        total_current = sum(r["current"] for r in results)
        total_reduction = ((total_original - total_current) / total_original) * 100

        for result in results:
            print(f"\n   {result['goal']}:")
            print(f"      Original: {result['original']:.0f} lbs CO2/month")
            print(f"      Current: {result['current']:.0f} lbs CO2/month")
            print(f"      Reduction: {result['reduction']:.0f}% ✅")

        print(f"\n   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   Total Monthly Carbon Footprint:")
        print(f"      Original: {total_original:.0f} lbs CO2")
        print(f"      Current: {total_current:.0f} lbs CO2")
        print(f"      Overall Reduction: {total_reduction:.0f}% 🎉")
        print(f"      Saved: {total_original - total_current:.0f} lbs CO2/month")

        print("\n💪 Next Steps:")
        print("   1. Continue vegetarian diet - reach 100% by month 6")
        print("   2. Implement carbon offset program")
        print("   3. Consider renewable energy for 100%")
        print("   4. Maintain sustainable habits long-term")


async def main():
    """Main entry point."""
    scenario = UrbanDwellerScenario()
    await scenario.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nScenario interrupted. Have a sustainable day! 🌱")
        sys.exit(0)
