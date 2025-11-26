"""
Enhanced Gradio interface for EcoAgent ChatGPT App
Following OpenAI best practices for great ChatGPT apps
"""

import gradio as gr
import asyncio
import os
from typing import List, Dict, Any
from chatgpt_integration import ChatGPTInterface
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EcoAgentChatGPTApp:
    """Gradio interface for EcoAgent following OpenAI ChatGPT app best practices.
    
    Design principles applied:
    - Focused capabilities (not a full product port)
    - KNOW/DO/SHOW value proposition
    - Cold start: show value immediately for vague + specific intents
    - Model-friendly: clear tool descriptions and structured outputs
    - Ecosystem-ready: small, composable actions
    """
    
    def __init__(self):
        self.interface = ChatGPTInterface()
        self.chat_history = []
        self.first_interaction = True
    
    def add_message(self, user_message: str, chat_history: List) -> List:
        """Add user message to chat history."""
        new_history = chat_history + [[user_message, None]]
        return new_history
    
    def get_bot_response(self, chat_history: List) -> List:
        """Get bot response for the last user message using OpenAI API."""
        if not chat_history or not chat_history[-1][0]:  # Check if last message exists
            return chat_history
        
        user_message = chat_history[-1][0]
        
        try:
            # Process message using OpenAI integration
            response = asyncio.run(self.interface.process_message(user_message))
            
            # Update the last message with bot response
            chat_history[-1][1] = response
            return chat_history
        except Exception as e:
            error_message = f"I'm sorry, I encountered an error: {str(e)}"
            chat_history[-1][1] = error_message
            logger.error(f"Error in bot response: {e}")
            return chat_history
    
    def clear_history(self) -> List:
        """Clear the chat history."""
        return []
    
    def get_available_capabilities_info(self) -> str:
        """Get information about available capabilities following OpenAI best practices.
        
        References: https://developers.openai.com/blog/what-makes-a-great-chatgpt-app
        Three ways to add value: KNOW, DO, SHOW
        """
        info = """# 🌱 EcoAgent Capabilities

## 1️⃣ NEW THINGS TO KNOW
Real environmental context your impact assessment can't access:
- **Calculate Carbon Footprint**: Precise CO2 emissions from transport, flights, home energy
- **Environmental Data**: Current news, local resources, sustainability practices
- **Live Metrics**: Up-to-date environmental information beyond training data

## 2️⃣ NEW THINGS TO DO
Actionable sustainability improvements:
- **Personalized Recommendations**: Specific steps for transportation, energy, diet reduction
- **Unit Conversions**: Understand metrics in familiar units with context
- **Environmental Assessment**: Identify your highest-impact areas

## 3️⃣ BETTER WAYS TO SHOW
Structured environmental data for clarity and action:
- **Carbon Breakdowns**: See impact by category (transport/flight/energy)
- **Comparison Context**: "That's equivalent to X miles of driving"
- **Actionable Formats**: Numbers with context, not just text

## 💬 What You Can Ask
- "How much CO2 do I emit driving 100 miles?"
- "What sustainable options for a 5-mile trip?"
- "How can I reduce my home energy footprint?"
- "Find recycling centers near me"
- "Convert 50 lbs CO2 to kg"
"""
        return info
    
    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface following OpenAI best practices.
        
        Design approach:
        - Focus on 3 core capabilities (KNOW/DO/SHOW)
        - Show immediate value (examples, quick starts)
        - Clear information about what EcoAgent can do
        - Prominent call-to-action for conversation
        """
        with gr.Blocks(
            title="EcoAgent - Sustainability Assistant Powered by OpenAI", 
            theme=gr.themes.Soft(),
            css="""
            .header { text-align: center; }
            .value-prop { background: linear-gradient(135deg, #1e7e34, #2d5a3d); padding: 20px; border-radius: 8px; color: white; margin: 10px 0; }
            .contain { display: flex; flex-direction: column; max-width: 1200px; margin: auto; }
            #component-0 { flex-grow: 1; overflow-y: auto; }
            .chatbot-container { height: 550px; overflow-y: auto; border-radius: 8px; }
            """
        ) as demo:
            
            gr.Markdown("# 🌱 EcoAgent", elem_classes="header")
            gr.Markdown("**Your sustainability assistant powered by OpenAI**", elem_classes="header")
            gr.Markdown("_Calculate environmental impact. Get actionable recommendations. Track your progress._", elem_classes="header")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Sustainability Conversation",
                        bubble_full_width=False,
                        height=500,
                        elem_classes="chatbot-container"
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            label="Your sustainability question",
                            placeholder="Ask about carbon footprint, sustainability tips, environmental impact, etc. (e.g., 'How much CO2 do I emit driving 100 miles?')",
                            container=False,
                            elem_id="user_input"
                        )
                        submit_btn = gr.Button("Send", variant="primary")
                    
                    with gr.Row():
                        clear_btn = gr.Button("Clear Chat", variant="secondary")
                        capabilities_btn = gr.Button("Show Capabilities", variant="secondary")
            
                with gr.Column(scale=1):
                    gr.Markdown("### ✨ What Makes EcoAgent Special")
                    gr.Markdown("""
                    Unlike base ChatGPT alone, EcoAgent provides:
                    
                    **KNOW**: Real carbon calculations + environmental data
                    **DO**: Personalized sustainability recommendations
                    **SHOW**: Structured impact metrics with context
                    """)
                    
                    capabilities_info = gr.Markdown(
                        label="Full Capabilities",
                        value=self.get_available_capabilities_info()
                    )
                    
                    gr.Markdown("### Quick Examples")
                    gr.Examples(
                        examples=[
                            "How much CO2 do I emit driving 100 miles in a car that gets 25 MPG?",
                            "What are sustainable alternatives for a 2-mile trip?",
                            "How can I reduce energy usage in my home?",
                            "Find recycling centers in San Francisco",
                            "What dietary changes reduce carbon impact?",
                            "Tell me about composting as a sustainability practice",
                            "Convert 100 pounds to kilograms",
                            "Calculate my total carbon footprint: 50 lbs transport, 30 lbs flight, 20 lbs home"
                        ],
                        inputs=[msg],
                        label="Try these sustainability questions"
                    )
            
            # Event handling
            submit_btn.click(
                self.add_message,
                inputs=[msg, chatbot],
                outputs=[chatbot],
                queue=False
            ).then(
                self.get_bot_response,
                inputs=[chatbot],
                outputs=[chatbot]
            )
            
            msg.submit(
                self.add_message,
                inputs=[msg, chatbot],
                outputs=[chatbot],
                queue=False
            ).then(
                self.get_bot_response,
                inputs=[chatbot],
                outputs=[chatbot]
            )
            
            clear_btn.click(
                self.clear_history,
                outputs=[chatbot],
                queue=False
            )
            
            capabilities_btn.click(
                self.get_available_capabilities_info,
                outputs=[capabilities_info],
                queue=False
            )
        
        return demo

def main():
    """Launch the EcoAgent ChatGPT Gradio interface."""
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not set. Please set it before running the app.")
        print("Example: export OPENAI_API_KEY='your-openai-api-key'")
    
    app = EcoAgentChatGPTApp()
    interface = app.create_interface()
    
    print("🌱 Starting EcoAgent ChatGPT App...")
    print("OpenAI-integrated sustainability assistant ready!")
    print("Following OpenAI best practices for great ChatGPT apps")
    print("Access the interface at: http://localhost:7860")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False  # Set to True if you want a public URL
    )

if __name__ == "__main__":
    main()