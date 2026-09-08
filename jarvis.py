import openai
from config import OPENAI_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS
from trading_analyzer import TradingAnalyzer
from geopolitical_monitor import GeopoliticalMonitor
from pc_controller import PCController
import json

openai.api_key = OPENAI_API_KEY

class JarvisAI:
    """Main AI Assistant - Like JARVIS from Iron Man"""
    
    def __init__(self):
        self.trading_analyzer = TradingAnalyzer()
        self.geopolitical_monitor = GeopoliticalMonitor()
        self.pc_controller = PCController()
        self.conversation_history = []
        
        self.system_prompt = """You are JARVIS, an advanced AI trading assistant inspired by Iron Man's JARVIS.
        
Your capabilities:
1. Forex Trading Analysis - Analyze charts, provide trading signals, manage risk
2. Geopolitical Monitoring - Track global events affecting forex markets
3. PC Control - Execute system commands and control computer operations
4. Market Intelligence - Provide real-time insights and recommendations

You are sophisticated, professional, witty, and always put the user's interests first.
When analyzing trades, always prioritize risk management.
Provide clear reasoning for all recommendations.
Use technical indicators and geopolitical data to support decisions.

Available functions:
- analyze_forex_pair(pair): Analyze a specific forex pair
- analyze_all_pairs(): Get signals for all configured pairs
- get_geopolitical_summary(): Get latest geopolitical news and impact
- execute_pc_command(command_type, params): Control PC operations
"""
    
    def chat(self, user_message):
        """Process user message and generate response"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        
        # Call OpenAI API with function calling
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            functions=self._get_functions(),
            function_call="auto"
        )
        
        # Process response
        return self._process_response(response)
    
    def _get_functions(self):
        """Define available functions for AI"""
        return [
            {
                "name": "analyze_forex_pair",
                "description": "Analyze a specific forex pair and provide trading signal",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pair": {
                            "type": "string",
                            "description": "Forex pair (e.g., EUR_USD, GBP_USD)"
                        }
                    },
                    "required": ["pair"]
                }
            },
            {
                "name": "analyze_all_pairs",
                "description": "Analyze all configured forex pairs",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_geopolitical_summary",
                "description": "Get latest geopolitical news and market impact analysis",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "execute_pc_command",
                "description": "Execute PC control commands",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command_type": {
                            "type": "string",
                            "description": "Type of command (open, launch, get_system_info, etc.)"
                        },
                        "params": {
                            "type": "object",
                            "description": "Command parameters"
                        }
                    },
                    "required": ["command_type"]
                }
            }
        ]
    
    def _process_response(self, response):
        """Process API response and execute functions if needed"""
        assistant_message = response.choices[0].message
        
        # Check if function calling is needed
        if assistant_message.get("function_call"):
            function_name = assistant_message["function_call"]["name"]
            function_args = json.loads(assistant_message["function_call"]["arguments"])
            
            # Execute function
            function_result = self._execute_function(function_name, function_args)
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.get("content", ""),
                "function_call": assistant_message["function_call"]
            })
            
            # Add function result to history
            self.conversation_history.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_result)
            })
            
            # Get follow-up response from AI
            messages = [{"role": "system", "content": self.system_prompt}]
            messages.extend(self.conversation_history)
            
            follow_up_response = openai.ChatCompletion.create(
                model=MODEL,
                messages=messages,
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS
            )
            
            final_response = follow_up_response.choices[0].message.content
            
            # Add final response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": final_response
            })
            
            return final_response
        
        else:
            # Direct response without function call
            final_response = assistant_message.get("content", "")
            
            self.conversation_history.append({
                "role": "assistant",
                "content": final_response
            })
            
            return final_response
    
    def _execute_function(self, function_name, function_args):
        """Execute requested function"""
        try:
            if function_name == "analyze_forex_pair":
                pair = function_args.get("pair")
                return self.trading_analyzer.analyze_pair(pair)
            
            elif function_name == "analyze_all_pairs":
                return self.trading_analyzer.analyze_all_pairs()
            
            elif function_name == "get_geopolitical_summary":
                return self.geopolitical_monitor.get_geopolitical_summary()
            
            elif function_name == "execute_pc_command":
                command_type = function_args.get("command_type")
                params = function_args.get("params", {})
                return self.pc_controller.execute_command(command_type, params)
            
            else:
                return {"error": f"Unknown function: {function_name}"}
        
        except Exception as e:
            return {"error": str(e)}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history