"""
EcoAgent CLI - Command Line Interface for the EcoAgent Sustainability Assistant

This CLI provides a command-line interface to interact with the EcoAgent system
which helps users understand and reduce their environmental impact.
"""

import argparse
import asyncio
import json
import sys
import os
import logging
from typing import Dict, Any, Optional
import datetime
from ecoagent.main import get_app
from ecoagent.agent import root_agent
from ecoagent.config import config
from ecoagent.database import db as ecoagent_db
from ecoagent.models import CalculationRequest


class EcoAgentCLI:
    """Command Line Interface for the EcoAgent system."""

    def __init__(self):
        self.app = get_app()
        self.args = None

    def setup_parser(self) -> argparse.ArgumentParser:
        """Set up the argument parser."""
        parser = argparse.ArgumentParser(
            description="EcoAgent: AI-Powered Sustainability Assistant",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  ecoagent carbon --transportation.miles_driven 500 --transportation.vehicle_mpg 25
  ecoagent recommend --profile.diet vegetarian --profile.location urban
  ecoagent track --goal "Reduce carbon by 20%" --target_value 200.0
  ecoagent --help
            """
        )

        parser.add_argument(
            '--version',
            action='version',
            version='EcoAgent CLI 1.0.0'
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Carbon footprint command
        carbon_parser = subparsers.add_parser('carbon', help='Calculate carbon footprint')
        carbon_parser.add_argument('--transportation.miles_driven', type=float, dest='trans_miles',
                                  help='Miles driven in transportation')
        carbon_parser.add_argument('--transportation.vehicle_mpg', type=float, dest='trans_mpg',
                                  help='Vehicle fuel efficiency in miles per gallon')
        carbon_parser.add_argument('--flight.miles_flown', type=float, dest='flight_miles',
                                  help='Miles flown')
        carbon_parser.add_argument('--energy.kwh_used', type=float, dest='energy_kwh',
                                  help='Kilowatt-hours of energy used')
        carbon_parser.add_argument('--energy.renewable_ratio', type=float, dest='energy_renewable',
                                  default=0.0, help='Fraction of energy from renewable sources (0.0 to 1.0)')
        carbon_parser.add_argument('--user_id', type=str, default='cli_user', help='User identifier')

        # Recommendation command
        rec_parser = subparsers.add_parser('recommend', help='Get sustainability recommendations')
        rec_parser.add_argument('--profile.name', type=str, dest='user_name', help='Your name')
        rec_parser.add_argument('--profile.location', type=str, dest='user_location', help='Your location')
        rec_parser.add_argument('--profile.housing_type', type=str, dest='housing_type',
                               choices=['apartment', 'house', 'condo'], help='Type of housing')
        rec_parser.add_argument('--profile.family_size', type=int, dest='family_size', default=1,
                               help='Number of people in household')
        rec_parser.add_argument('--profile.diet', type=str, dest='diet',
                               choices=['omnivore', 'vegetarian', 'vegan', 'pescatarian'],
                               help='Dietary preference')
        rec_parser.add_argument('--goal', type=str, help='Sustainability goal to focus on')
        rec_parser.add_argument('--user_id', type=str, default='cli_user', help='User identifier')

        # Tracking command
        track_parser = subparsers.add_parser('track', help='Track sustainability goals')
        track_parser.add_argument('--goal', type=str, required=True, help='Goal description')
        track_parser.add_argument('--target_value', type=float, required=True, help='Target value')
        track_parser.add_argument('--current_value', type=float, default=0.0, help='Current progress value')
        track_parser.add_argument('--user_id', type=str, default='cli_user', help='User identifier')

        # Profile command
        profile_parser = subparsers.add_parser('profile', help='Manage user profile')
        profile_parser.add_argument('--action', type=str, choices=['get', 'update'],
                                   default='get', help='Action to perform')
        profile_parser.add_argument('--user_id', type=str, default='cli_user', help='User identifier')

        # Chat command for direct conversation
        chat_parser = subparsers.add_parser('chat', help='Chat with the EcoAgent')
        chat_parser.add_argument('--user_id', type=str, default='cli_user', help='User identifier')
        chat_parser.add_argument('--message', type=str, help='Message to send (interactive if not provided)')

        # Server command to run API service
        server_parser = subparsers.add_parser('serve', help='Run the EcoAgent API service')
        server_parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to bind to')
        server_parser.add_argument('--port', type=int, default=8000, help='Port to run on')
        server_parser.add_argument('--reload', action='store_true', help='Enable auto-reload (development)')

        # Info command
        subparsers.add_parser('info', help='Show system information')

        return parser

    async def run_carbon_command(self, args: argparse.Namespace) -> None:
        """Execute the carbon footprint calculation command."""
        # Prepare carbon calculation data
        calc_data = {}
        if args.trans_miles is not None or args.trans_mpg is not None:
            calc_data['transportation'] = {
                'miles_driven': args.trans_miles or 0,
                'vehicle_mpg': args.trans_mpg or 25.0
            }
        if args.flight_miles is not None:
            calc_data['flight'] = {'miles_flown': args.flight_miles}
        if args.energy_kwh is not None:
            calc_data['energy'] = {
                'kwh_used': args.energy_kwh,
                'renewable_ratio': args.energy_renewable
            }

        if not calc_data:
            print("Error: At least one carbon source must be specified")
            print("Use --transportation.miles_driven, --flight.miles_flown, or --energy.kwh_used")
            return

        calc_data['user_id'] = args.user_id

        try:
            # Simulate carbon calculation using internal functions
            total_carbon = 0
            breakdown = {}

            # Calculate transportation carbon
            if 'transportation' in calc_data:
                trans_data = calc_data['transportation']
                miles = trans_data['miles_driven']
                mpg = trans_data['vehicle_mpg']
                # Estimate: 19.6 lbs CO2 per gallon for gas, average car is ~24 MPG
                gallons = miles / mpg
                trans_carbon = gallons * 19.6
                total_carbon += trans_carbon
                breakdown['transportation'] = round(trans_carbon, 2)

            # Calculate flight carbon
            if 'flight' in calc_data:
                flight_data = calc_data['flight']
                miles = flight_data['miles_flown']
                # Estimate: ~0.44 lbs CO2 per passenger-mile for flights
                flight_carbon = miles * 0.44
                total_carbon += flight_carbon
                breakdown['flight'] = round(flight_carbon, 2)

            # Calculate energy carbon
            if 'energy' in calc_data:
                energy_data = calc_data['energy']
                kwh = energy_data['kwh_used']
                renewable_ratio = energy_data.get('renewable_ratio', 0.0)
                non_renewable_kwh = kwh * (1 - renewable_ratio)
                # Estimate: ~0.954 lbs CO2 per kWh from grid
                energy_carbon = non_renewable_kwh * 0.954
                total_carbon += energy_carbon
                breakdown['energy'] = round(energy_carbon, 2)

            print(f"\n🌱 Carbon Footprint Calculation Results:")
            print(f"Total Carbon: {round(total_carbon, 2)} lbs CO2")
            print(f"Breakdown: {json.dumps(breakdown, indent=2)}")

            # Save to database
            success = ecoagent_db.save_carbon_footprint(
                user_id=args.user_id,
                carbon_type='total_calculated',
                value=round(total_carbon, 2),
                context=calc_data
            )

            if success:
                print(f"✅ Result saved to your profile")
            else:
                print("⚠️  Note: Could not save result to profile")

        except Exception as e:
            print(f"❌ Error calculating carbon footprint: {e}")
            import traceback
            traceback.print_exc()

    async def run_recommend_command(self, args: argparse.Namespace) -> None:
        """Execute the recommendation command."""
        print(f"🔍 Generating sustainability recommendations for user: {args.user_id}")

        try:
            # Build profile description for the agent
            profile_desc = f"name: {args.user_name or 'User'}, "
            profile_desc += f"location: {args.user_location or 'unknown'}, "
            profile_desc += f"family_size: {args.family_size}, "
            profile_desc += f"diet: {args.diet or 'omnivore'}, "
            profile_desc += f"housing: {args.housing_type or 'unknown'}"

            goal_text = f" with a focus on {args.goal}" if args.goal else ""

            query = f"Provide personalized sustainability recommendations for: {profile_desc}{goal_text}"

            # Initialize the app
            init_result = await self.app.initialize()
            print(f"✅ App initialized: {init_result}")

            # For now, we'll provide simulated recommendations based on profile
            print(f"\n💬 Query: {query}")
            print("\n🌿 EcoAgent Recommendations:")
            print("- Consider reducing meat consumption to lower carbon footprint")
            print("- Switch to renewable energy sources if possible")
            print("- Use public transportation or cycling for short trips")
            print("- Minimize food waste by meal planning")
            print("- Choose locally-sourced products when possible")
            print("- Reduce water heating temperature")
            print("- Improve home insulation")
            print("- Plant trees or support reforestation initiatives")

            print("\n💡 Tip: Small changes can make a big difference - start with one practice and gradually adopt more!")

        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            import traceback
            traceback.print_exc()

    async def run_track_command(self, args: argparse.Namespace) -> None:
        """Execute the tracking command."""
        try:
            # Create goal data
            goal_data = {
                'id': f'goal_{args.user_id}_{int(datetime.datetime.now().timestamp())}',
                'user_id': args.user_id,
                'description': args.goal,
                'target_value': args.target_value,
                'current_value': args.current_value,
                'target_date': (datetime.datetime.now() + datetime.timedelta(days=365)).isoformat(),
                'status': 'in_progress'
            }

            # Save goal to database
            success = ecoagent_db.save_sustainability_goal(goal_data)
            if success:
                print(f"✅ Goal saved successfully:")
                print(f"   Goal: {args.goal}")
                print(f"   Target: {args.target_value}")
                print(f"   User: {args.user_id}")
            else:
                print("❌ Failed to save goal")

        except Exception as e:
            print(f"❌ Error tracking goal: {e}")
            import traceback
            traceback.print_exc()

    async def run_profile_command(self, args: argparse.Namespace) -> None:
        """Execute the profile command."""
        if args.action == 'get':
            profile = ecoagent_db.get_user_profile(args.user_id)
            if profile:
                print(f"\nProfile for {args.user_id}:")
                for key, value in profile.items():
                    if key not in ['created_at', 'updated_at']:  # Skip timestamps for readability
                        print(f"   {key.replace('_', ' ').title()}: {value}")
            else:
                print(f"❌ No profile found for user: {args.user_id}")
        elif args.action == 'update':
            print(f"🔄 Profile update functionality for {args.user_id} would go here")
            print("   (This would require additional parameters to update profile)")

    async def run_chat_command(self, args: argparse.Namespace) -> None:
        """Execute the chat command."""
        # Initialize the app first
        await self.app.initialize()

        if args.message:
            # Process single message
            print(f"User: {args.message}")
            print(" EcoAgent: Processing your query...")

            try:
                # Call the actual agent through the app
                response = await self.app.process_query(
                    user_id=args.user_id,
                    session_id=f"session_{args.user_id}",
                    query=args.message
                )
                print(f"EcoAgent: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            # Interactive chat
            print("🌱 EcoAgent Interactive Chat (type 'quit' or 'exit' to exit)")
            print("Ask about carbon footprint, sustainability tips, or environmental impact.")
            print("-" * 60)

            while True:
                try:
                    user_input = input(f"{args.user_id}@ecoagent> ").strip()
                    if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                        print(" EcoAgent: Thank you for using EcoAgent. Have a sustainable day! 🌱")
                        break

                    if not user_input:
                        continue

                    print(" EcoAgent: Processing...")

                    # Call the actual agent through the app
                    try:
                        response = await self.app.process_query(
                            user_id=args.user_id,
                            session_id=f"session_{args.user_id}",
                            query=user_input
                        )
                        print(f"EcoAgent: {response}")
                    except Exception as e:
                        print(f"EcoAgent: Sorry, I encountered an error: {e}")

                except KeyboardInterrupt:
                    print("\n\n EcoAgent: Thank you for using EcoAgent. Have a sustainable day! 🌱")
                    break
                except Exception as e:
                    print(f" EcoAgent: Error during chat: {e}")
                    break

    def run_serve_command(self, args: argparse.Namespace) -> None:
        """Execute the serve command."""
        import uvicorn
        print(f"🚀 Starting EcoAgent API service on {args.host}:{args.port}")
        if args.reload:
            print("(Auto-reload enabled - development mode)")

        # Import and run the API
        from ecoagent.api import app as api_app
        uvicorn.run(
            api_app,
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )

    def run_info_command(self, args: argparse.Namespace) -> None:
        """Execute the info command."""
        print("\n🌱 EcoAgent System Information:")
        print(f"  Version: 1.0.0")
        print(f"  Model: {config.default_model}")
        print(f"  Environment: {config.environment}")
        print(f"  Database: {'SQLite' if config.db_connection_string else 'In-Memory'}")
        print(f"  API Endpoint: http://localhost:8000")
        print(f"  API Docs: http://localhost:8000/docs")
        print(f"  System initialized: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    async def run_command(self, args: argparse.Namespace) -> None:
        """Run the specified command."""
        if args.command == 'carbon':
            await self.run_carbon_command(args)
        elif args.command == 'recommend':
            await self.run_recommend_command(args)
        elif args.command == 'track':
            await self.run_track_command(args)
        elif args.command == 'profile':
            await self.run_profile_command(args)
        elif args.command == 'chat':
            await self.run_chat_command(args)
        elif args.command == 'serve':
            # Serve command is synchronous
            self.run_serve_command(args)
        elif args.command == 'info':
            self.run_info_command(args)
        else:
            print("❌ Unknown command. Use --help for usage information.")

    async def run(self, args: Optional[argparse.Namespace] = None) -> None:
        """Run the CLI application."""
        parser = self.setup_parser()

        if args is None:
            args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        await self.run_command(args)


def main():
    """Main entry point for the CLI."""
    # Set logging to WARNING by default for CLI (suppress verbose output)
    # Users can override with LOG_LEVEL environment variable
    if 'LOG_LEVEL' not in os.environ:
        os.environ['LOG_LEVEL'] = 'WARNING'

    import logging
    log_level = os.getenv("LOG_LEVEL", "WARNING")
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(message)s'  # Minimal format for CLI
    )

    cli = EcoAgentCLI()
    parser = cli.setup_parser()
    args = parser.parse_args()

    try:
        # Handle serve command synchronously (it creates its own event loop)
        if args.command == 'serve':
            cli.run_serve_command(args)
        elif args.command == 'info':
            cli.run_info_command(args)
        elif args.command:
            # Run other commands asynchronously
            asyncio.run(cli.run(args))
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running EcoAgent CLI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()