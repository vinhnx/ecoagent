#!/usr/bin/env python3
"""
Interactive Demo Script for EcoAgent

This script provides an interactive demonstration of EcoAgent capabilities
including carbon calculation, recommendations, goal tracking, and chat.

Run with: uv run python demo/interactive_demo.py
"""

import asyncio
import sys
from typing import Optional
import json
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, '/Users/vinhnguyenxuan/Developer/learn-by-doing/vtgoodagent/ecoagent')

from ecoagent.main import get_app
from ecoagent.database import db as ecoagent_db
from ecoagent.config import config


class EcoAgentDemo:
    """Interactive demonstration of EcoAgent features."""

    def __init__(self):
        self.app = get_app()
        self.current_user = "demo_user"
        self.session_id = f"session_{datetime.now().timestamp()}"

    async def initialize(self) -> bool:
        """Initialize the demo."""
        print("\n" + "=" * 60)
        print("🌱 Welcome to the EcoAgent Interactive Demo! 🌍")
        print("=" * 60)
        print("\nInitializing EcoAgent system...")

        try:
            result = await self.app.initialize()
            if result:
                print("✅ EcoAgent initialized successfully!\n")
                return True
            else:
                print("❌ Failed to initialize EcoAgent")
                return False
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            return False

    def print_menu(self) -> None:
        """Print the main menu."""
        print("\n" + "-" * 60)
        print("📋 EcoAgent Demo Menu")
        print("-" * 60)
        print("1. 🧮 Calculate Carbon Footprint")
        print("2. 🌿 Get Sustainability Recommendations")
        print("3. 📊 Track a Sustainability Goal")
        print("4. Manage Your Profile")
        print("5. 💬 Chat with EcoAgent (Single Message)")
        print("6. 🗣️  Interactive Chat Session")
        print("7. ℹ️  View System Information")
        print("8. 🚀 Run All Demos (Auto)")
        print("9. ❌ Exit")
        print("-" * 60)

    async def demo_carbon_calculation(self) -> None:
        """Demo: Calculate carbon footprint."""
        print("\n" + "=" * 60)
        print("🧮 Demo: Carbon Footprint Calculator")
        print("=" * 60)

        print("\nLet's calculate your carbon footprint from different activities.")
        print("\nExample 1: Daily Commute")
        print("  - Miles driven: 50 miles (25 miles each way)")
        print("  - Vehicle MPG: 25 MPG")

        # Calculate transportation carbon
        miles = 50
        mpg = 25
        gallons = miles / mpg
        trans_carbon = gallons * 19.6  # lbs CO2 per gallon

        print(f"\n  Calculation:")
        print(f"    50 miles ÷ 25 MPG = {gallons} gallons")
        print(f"    {gallons} gallons × 19.6 lbs CO2/gallon = {trans_carbon:.2f} lbs CO2")
        print(f"\n  ✅ Daily commute carbon: {trans_carbon:.2f} lbs CO2")

        # Save to database
        ecoagent_db.save_carbon_footprint(
            user_id=self.current_user,
            carbon_type="transportation_daily_commute",
            value=round(trans_carbon, 2),
            context={"miles_driven": miles, "vehicle_mpg": mpg}
        )

        print("\nExample 2: Monthly Flights")
        print("  - Miles flown: 2000 miles")

        flight_carbon = 2000 * 0.44  # lbs CO2 per passenger-mile
        print(f"\n  Calculation:")
        print(f"    2000 miles × 0.44 lbs CO2/mile = {flight_carbon:.2f} lbs CO2")
        print(f"\n  ✅ Monthly flight carbon: {flight_carbon:.2f} lbs CO2")

        print("\nExample 3: Home Energy Usage")
        print("  - Monthly usage: 1000 kWh")
        print("  - Renewable ratio: 20%")

        kwh = 1000
        renewable = 0.2
        non_renewable_kwh = kwh * (1 - renewable)
        energy_carbon = non_renewable_kwh * 0.954  # lbs CO2 per kWh

        print(f"\n  Calculation:")
        print(f"    1000 kWh × (1 - 0.20) = {non_renewable_kwh} kWh non-renewable")
        print(f"    {non_renewable_kwh} kWh × 0.954 lbs CO2/kWh = {energy_carbon:.2f} lbs CO2")
        print(f"\n  ✅ Monthly energy carbon: {energy_carbon:.2f} lbs CO2")

        total = trans_carbon + flight_carbon + energy_carbon
        print(f"\n📊 Total Monthly Carbon Footprint: {total:.2f} lbs CO2")
        print(f"   Or approximately: {total/2000:.2f} metric tons CO2")

    async def demo_recommendations(self) -> None:
        """Demo: Get sustainability recommendations."""
        print("\n" + "=" * 60)
        print("🌿 Demo: Sustainability Recommendations")
        print("=" * 60)

        print("\nGenerating personalized recommendations...")
        print("Profile: Urban apartment dweller, vegetarian diet, family of 2")

        recommendations = [
            "🚌 Public Transportation: You're in an urban area - maximize use of public transit",
            "♻️  Recycling Program: Join a comprehensive recycling program in your city",
            "💡 Energy Efficiency: Install LED bulbs throughout your apartment",
            "🍽️  Food Waste Reduction: Composting can reduce 30% of household waste",
            "⚡ Renewable Energy: Check if your utility offers green energy options",
            "🧴 Reduce Plastics: Use reusable containers and bags in daily life",
            "🌱 Indoor Plants: Help purify air and create a healthier living space",
            "🚴 Bike Sharing: Use bike-sharing programs for short trips"
        ]

        print("\n🎯 Recommended Actions:")
        for rec in recommendations:
            print(f"   {rec}")

        print("\n💡 Key Insight: As an urban vegetarian, you're already 40-50% below")
        print("   the average carbon footprint. Focus on transportation and energy!")

    async def demo_goal_tracking(self) -> None:
        """Demo: Track sustainability goals."""
        print("\n" + "=" * 60)
        print("📊 Demo: Goal Tracking")
        print("=" * 60)

        print("\nSetting up sustainability goals...")

        goals = [
            {
                "description": "Reduce transportation carbon by 30%",
                "target_value": 30.0,
                "timeline": "6 months"
            },
            {
                "description": "Switch to 100% renewable home energy",
                "target_value": 100.0,
                "timeline": "1 year"
            },
            {
                "description": "Reduce household waste by 50%",
                "target_value": 50.0,
                "timeline": "3 months"
            }
        ]

        print("\n🎯 Your Sustainability Goals:")
        for i, goal in enumerate(goals, 1):
            goal_data = {
                'id': f'goal_{self.current_user}_{i}_{int(datetime.now().timestamp())}',
                'user_id': self.current_user,
                'description': goal['description'],
                'target_value': goal['target_value'],
                'current_value': 0.0,
                'target_date': (datetime.now() + timedelta(days=180)).isoformat(),
                'status': 'in_progress'
            }

            ecoagent_db.save_sustainability_goal(goal_data)

            print(f"\n   {i}. {goal['description']}")
            print(f"      Target: {goal['target_value']:.0f}%")
            print(f"      Timeline: {goal['timeline']}")
            print(f"      Status: In Progress 📈")

        print("\n✅ Goals saved to your profile!")

    async def demo_profile_management(self) -> None:
        """Demo: Profile management."""
        print("\n" + "=" * 60)
        print("Demo: Profile Management")
        print("=" * 60)

        profile = ecoagent_db.get_user_profile(self.current_user)

        if profile:
            print(f"\n📋 Profile for {self.current_user}:")
            for key, value in profile.items():
                if key not in ['created_at', 'updated_at']:
                    print(f"   {key.replace('_', ' ').title()}: {value}")
        else:
            print(f"\n✨ Creating new profile for {self.current_user}...")
            default_profile = {
                'user_id': self.current_user,
                'name': 'Demo User',
                'location': 'San Francisco, CA',
                'housing_type': 'apartment',
                'family_size': 2,
                'diet': 'vegetarian'
            }
            ecoagent_db.save_user_profile(self.current_user, default_profile)
            print("✅ Profile created!")

    async def demo_single_chat(self) -> None:
        """Demo: Single message chat."""
        print("\n" + "=" * 60)
        print("💬 Demo: Single Message Chat")
        print("=" * 60)

        query = "What are the most impactful actions I can take to reduce my carbon footprint?"

        print(f"\nUser: {query}")
        print(" EcoAgent: Processing your query...")

        try:
            response = await self.app.process_query(
                user_id=self.current_user,
                session_id=self.session_id,
                query=query
            )
            print(f"\n EcoAgent Response:\n{response}")
        except Exception as e:
            print(f"Error: {e}")

    async def demo_interactive_chat(self) -> None:
        """Demo: Interactive chat session."""
        print("\n" + "=" * 60)
        print("🗣️  Demo: Interactive Chat Session")
        print("=" * 60)
        print("\nYou can now chat with EcoAgent. Type 'quit' or 'exit' to exit.")
        print("-" * 60)

        while True:
            try:
                user_input = input(f"\n{self.current_user}@ecoagent> ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print(" Thank you for chatting! Have a sustainable day! 🌱")
                    break

                if not user_input:
                    continue

                print(" EcoAgent: Processing...")

                try:
                    response = await self.app.process_query(
                        user_id=self.current_user,
                        session_id=self.session_id,
                        query=user_input
                    )
                    print(f"\n EcoAgent:\n{response}")
                except Exception as e:
                    print(f"EcoAgent: Sorry, I encountered an error: {e}")

            except KeyboardInterrupt:
                print("\n\n Thank you for using EcoAgent. Have a sustainable day! 🌱")
                break

    def show_system_info(self) -> None:
        """Show system information."""
        print("\n" + "=" * 60)
        print("ℹ️  System Information")
        print("=" * 60)
        print(f"\n  Version: 1.0.0")
        print(f"  Model: {config.default_model}")
        print(f"  Environment: {config.environment}")
        print(f"  API Key Configured: {'Yes' if config.google_api_key else 'No'}")
        print(f"  Database: SQLite (Local)")
        print(f"  Current User: {self.current_user}")
        print(f"  Session ID: {self.session_id}")
        print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    async def run_all_demos(self) -> None:
        """Run all demos automatically."""
        print("\n🚀 Running all demos automatically...")

        await self.demo_carbon_calculation()
        await asyncio.sleep(2)

        await self.demo_recommendations()
        await asyncio.sleep(2)

        await self.demo_goal_tracking()
        await asyncio.sleep(2)

        await self.demo_profile_management()
        await asyncio.sleep(2)

        await self.demo_single_chat()
        await asyncio.sleep(2)

        print("\n" + "=" * 60)
        print("✅ All automated demos completed!")
        print("=" * 60)

    async def run(self) -> None:
        """Run the interactive demo."""
        if not await self.initialize():
            print("Failed to initialize demo")
            return

        while True:
            self.print_menu()
            choice = input("\n👉 Enter your choice (1-9): ").strip()

            try:
                if choice == "1":
                    await self.demo_carbon_calculation()
                elif choice == "2":
                    await self.demo_recommendations()
                elif choice == "3":
                    await self.demo_goal_tracking()
                elif choice == "4":
                    await self.demo_profile_management()
                elif choice == "5":
                    await self.demo_single_chat()
                elif choice == "6":
                    await self.demo_interactive_chat()
                elif choice == "7":
                    self.show_system_info()
                elif choice == "8":
                    await self.run_all_demos()
                elif choice == "9":
                    print("\n🌱 Thank you for using EcoAgent Demo!")
                    print("Have a sustainable day! 🌍\n")
                    break
                else:
                    print("❌ Invalid choice. Please enter 1-9.")
            except KeyboardInterrupt:
                print("\n\n🌱 Demo interrupted by user. Have a sustainable day! 🌍\n")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


async def main():
    """Main entry point."""
    demo = EcoAgentDemo()
    await demo.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🌱 Goodbye! Have a sustainable day! 🌍\n")
        sys.exit(0)
